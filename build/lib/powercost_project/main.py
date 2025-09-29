"""
This Python code handles the setup of the configuration (in config.py),and
database (in database.py) classes.  Most of the work is done in the run()
method.
"""

import sys
import os
import time
import signal
import decimal
import logging
import logging.config

from emu_power import Emu
from .config import PonderosaConfig
from .database import PonderosaDB

class PonderosaMonitor:
    """
    This class encapulates most of the script's logic to isolate responsibilities,
    improve code testability and enable future extensions.
    """
    MAX_RETRIES = 40
    DEMAND_RETRIES = 15

    def __init__(self, ini_path):
        self.ini_path = ini_path
        self.start_ts = time.strftime('%Y%m%d-%H%M')
        self.config = PonderosaConfig(self.ini_path, self.start_ts)
        self.log_path = os.path.join(self.config.log_dir, self.config.log_file)
        self.log_level = self.config.log_level
        self.running_file = self.config.running_file
        self.stop_file = self.config.stop_file
        self.setup_logging()
        self.setup_signal_handler()
        self.pid = os.getpid()
        self.db = None
        self.emu = None

    def setup_logging(self):
        '''
        Set up Python logging based on settings in INI file.
        '''
        logging_config  = {
            'version': 1,
            'disable_existing_loggers': False,
            'formatters': {
                'default': {
                    'format': '%(asctime)s | %(funcName)s:%(lineno)s | %(levelname)s | %(message)s',
                },
            },
            'handlers': {
                'file_handler': {
                    'level': self.log_level,
                    'formatter': 'default',
                    'class': 'logging.FileHandler',
                    'filename': self.log_path,
                },
            },
            'loggers': {
                '': {  # root logger
                    'handlers': ['file_handler'],
                    'level': self.log_level,
                    'propagate': True
                },
            }
        }
        logging.config.dictConfig(logging_config)

    def setup_signal_handler(self):
        '''
        Since this app runs indefinitely, setup signal handling to
        report being killed from the OS.  These signals are not usually
        sent in Windows.  The presence of a "stop file" triggers a
        graceful shutdown.  In Windows, I have also had to use
        Task Manager + Details + End Task which does not send a
        "signal".  This method would be useful in Linux.
        '''
        def handler(sig):
            logging.warning("PEU: Signal %s received. Cleaning up and exiting.", sig)
            if os.path.exists(self.running_file):
                os.remove(self.running_file)
            if os.path.exists(self.stop_file):
                os.remove(self.stop_file)
            logging.shutdown()
            sys.exit(0)
        signal.signal(signal.SIGINT, handler)
        signal.signal(signal.SIGTERM, handler)

    def check_stop_file(self):
        '''
        This method checks for the existence of a file that indicates that
        this daemon-like program should stop gracefully.
        '''
        if os.path.exists(self.stop_file):
            logging.warning("PEU: Stop file %s detected.", self.stop_file)
            os.remove(self.stop_file)
            if os.path.exists(self.running_file):
                os.remove(self.running_file)
            logging.shutdown()
            os.kill(self.pid, signal.SIGTERM)
            sys.exit(1)  #

    def check_already_running(self):
        '''
        This method checks for the existence of a file that indicates that
        this daemon-like program is already running.  It cannot run more than
        one instance at a time.  The Force option was intended to be
        used when the program is started by Windows Scheduled Task.  The original
        intention was that Windows would start the task every Midnight and
        if the application was already running, nothing would happen.
        Starting of the application was changed to System Startup.  Now, I
        just manually start feom a script.  Almost daemon.
        '''
        if os.path.exists(self.running_file):
            logging.warning("PEU: Script already running. Exiting.")
            logging.shutdown()
            os.remove(self.running_file)
            sys.exit(0)

        with open(self.running_file, 'w', encoding="utf-8") as f:
            write_str = f"taskkill /f /pid {str(self.pid)}"
            f.write(write_str)
        logging.info("PEU: check_already_running(): Created running file")

    def wait_until_top_of_hour(self):
        '''
        The application will only make hourly recordsing that contain
        full 60 separate minute readings.  The application will wait how many seconds
        until the top of the next hour or xx:00 AM/PM before starting.
        '''
        now = time.localtime()
        imin = int(time.strftime('%M', now))
        isec = int(time.strftime('%S', now))
        sleep_time = 60 * (60 - imin - 1) + (60 - isec)

        self.check_stop_file()

        time.sleep(sleep_time)

        self.check_stop_file()

    def start_serial(self):
        '''
        Starting a serial connection (via USB on Windows) to the EMU-2.  This
        startup may not work the first time so there is retry logic.
        '''
        for attempt in range(1, self.MAX_RETRIES + 1):
            #if self.log_level == 'INFO':
            #    self.emu = Emu(debug=False, fresh_only=True, timeout=5, synchronous=True)
            #else:
            self.emu = Emu(debug=True, fresh_only=True, timeout=5, synchronous=True)
            self.emu.start_serial(self.config.the_port)
            time.sleep(5)
            self.emu.get_network_info()
            print(self.emu.NetworkInfo)
            return
            #if self.emu.start_serial(self.config.the_port):
            #    return
            #logging.warning("PEU: Serial connection attempt %i failed.", attempt)
            #time.sleep(5)
        logging.error("PEU: Serial connection attempts have failed! Exiting ...")
        self.emu.stop_serial()
        os.remove(self.running_file)
        raise RuntimeError("Failed to start serial connection.")

    def read_demand(self):
        '''
        Reading from the EMU-2 may not work the first time so there is retry logic.
        '''
        for attempt in range(1, self.DEMAND_RETRIES + 1):
            response = self.emu.get_instantaneous_demand()
            if response:
                return response
            logging.warning("PEU: read_demand(): Demand read attempt %i failed.", attempt)
            time.sleep(10)
        logging.error("PEU: read_demand(): Demand read attempts have failed! Exiting ...")
        self.emu.stop_serial()
        os.remove(self.running_file)
        raise RuntimeError("Failed to read demand after multiple attempts.")

    def run(self, now_str, pid):
        '''
        Almost all of the logic is in this method.  Only the acquisition of the
        parameters is done in main.py.
        '''
        logging.info("PEU: main.py - PonderosaMonitor.run(): Time is %s, PID = %s", now_str, pid)

        self.check_already_running()
        self.check_stop_file()

        decimal.getcontext().prec = 3
        self.start_serial()
        self.wait_until_top_of_hour()

        the_date_prev = None
        the_hour_last = -1
        kwh_day = 0
        minute_sum = 0
        minute_count = 0

        with PonderosaDB(self.config.db_config) as self.db:
            while True:
                self.check_stop_file()

                now = time.localtime()
                date_str = time.strftime('%Y-%m-%d', now)
                ##hour_str = time.strftime('%H:00:00', now)
                current_hour = int(time.strftime('%H', now))

                response = self.read_demand()
                demand = decimal.Decimal(response.demand)
                divisor = decimal.Decimal(response.divisor)
                multiplier = decimal.Decimal(response.multiplier)
                kw = multiplier * (demand / divisor)

                if the_hour_last == current_hour:
                    minute_sum += kw
                    minute_count += 1
                else:
                    the_hour_last_str = f"{the_hour_last:02d}:00:00"
                    if minute_count > 0:
                        avg_kwh = minute_sum / minute_count
                        self.db.insert_usage(date_str, the_hour_last_str, avg_kwh)
                        kwh_day += avg_kwh
                    minute_sum = kw
                    minute_count = 1
                    the_hour_last = current_hour

                    self.emu.stop_serial()
                    time.sleep(5)
                    self.start_serial()

                if the_date_prev != date_str:
                    if the_date_prev is not None:
                        logging.info("PEU: New day: %s, Total kWh yesterday: %.3f}",
                                     date_str, kwh_day)
                    the_date_prev = date_str
                    kwh_day = 0

                sleep_secs = 60 - int(time.strftime('%S', time.localtime()))
                time.sleep(sleep_secs)
                self.check_stop_file()
