"""
Filename: Ponderosa_Electricity_Usage.py
Author: James Buck
Created: 2025-06-24
Last Modified: 2025-06-24
Description: This script processes electricity usage data and inserts that data into a MySQL table.

Additional Description

This script is something like Version 3 which has had considerable input from ChatGPT for improvements.
My work on this script has been a long-running learning of Python.  Version 3 is like a teaching
class in Python focused on my script.  I continue a separate effort in taking Python classes.

These scripts are also my personal coding project that I can feature on LinkedIn.
"""

import sys
import os
import time
import signal
import decimal
import argparse
import logging
from emu_power import Emu
from PonderosaConfig import PonderosaConfig
from PonderosaDB import PonderosaDB

class PonderosaMonitor:
    MAX_RETRIES = 20
    DEMAND_RETRIES = 15

    def __init__(self, ini_path, force=False):
        self.ini_path = ini_path
        self.force = force
        self.start_ts = time.strftime('%Y%m%d-%H%M')
        self.config = PonderosaConfig(self.ini_path, self.start_ts)
        self.log_path = os.path.join(self.config.log_dir, self.config.log_file)
        self.stop_file = os.path.join(self.config.log_dir, "stop.txt")
        self.running_file = os.path.join(self.config.log_dir, "Ponderosa_Electricity_Usage.running")
        self.setup_logging()
        self.setup_signal_handler()
        self.pid = os.getpid()
        self.db = None
        self.emu = None

    def setup_logging(self):
        logging.basicConfig(
            filename=self.log_path,
            encoding='utf-8',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        logging.info("Logging initialized.")

    def setup_signal_handler(self):
        def handler(sig, frame):
            logging.warning(f"Signal {sig} received. Cleaning up and exiting.")
            if os.path.exists(self.running_file):
                os.remove(self.running_file)
            sys.exit(0)
        signal.signal(signal.SIGINT, handler)

    def check_already_running(self):
        if os.path.exists(self.stop_file):
            sys.exit(0)

        if os.path.exists(self.running_file):
            if not self.force:
                logging.info("Script already running. Exiting.")
                sys.exit(0)
            else:
                os.remove(self.running_file)

        with open(self.running_file, 'w') as f:
            f.write(str(self.pid))

    def wait_until_top_of_hour(self):
        now = time.localtime()
        imin = int(time.strftime('%M', now))
        isec = int(time.strftime('%S', now))
        sleep_time = 60 * (60 - imin - 1) + (60 - isec)
        logging.info("Sleeping %s seconds until top of the hour.", sleep_time)
        time.sleep(sleep_time)

    def start_serial(self):
        for attempt in range(1, self.MAX_RETRIES + 1):
            self.emu = Emu(debug=False, fresh_only=True, timeout=5, synchronous=True)
            if self.emu.start_serial(self.config.the_port):
                logging.info(f"Serial connection established on {self.config.the_port}")
                return
            logging.warning(f"Serial connection attempt {attempt} failed.")
            time.sleep(5)
        raise RuntimeError("Failed to start serial connection.")

    def read_demand(self):
        for attempt in range(1, self.DEMAND_RETRIES + 1):
            response = self.emu.get_instantaneous_demand()
            if response:
                return response
            logging.warning(f"Demand read attempt {attempt} failed.")
            time.sleep(10)
        raise RuntimeError("Failed to read demand after multiple attempts.")

    def run(self):
        self.check_already_running()
        decimal.getcontext().prec = 3
        self.start_serial()
        self.wait_until_top_of_hour()

        the_date_prev = ""
        the_hour_last = -1
        kwh_day = 0
        minute_sum = 0
        minute_count = 0

        with PonderosaDB(self.config.dbConfig) as self.db:
            while True:
                if os.path.exists(self.stop_file):
                    logging.info("Stop file detected. Exiting.")
                    break

                now = time.localtime()
                date_str = time.strftime('%Y-%m-%d', now)
                hour_str = time.strftime('%H:00:00', now)
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
                    if minute_count > 0:
                        avg_kwh = minute_sum / minute_count
                        self.db.insert_usage(date_str, hour_str, avg_kwh)
                        kwh_day += avg_kwh
                    minute_sum = kw
                    minute_count = 1
                    the_hour_last = current_hour

                    self.emu.stop_serial()
                    time.sleep(5)
                    self.start_serial()

                if the_date_prev != date_str:
                    logging.info(f"New day: {date_str}, Total kWh yesterday: {kwh_day:.3f}")
                    the_date_prev = date_str
                    kwh_day = 0

                sleep_secs = 60 - int(time.strftime('%S', time.localtime()))
                time.sleep(sleep_secs)

        if os.path.exists(self.running_file):
            os.remove(self.running_file)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ini', required=True, help='Path to the INI configuration file')
    parser.add_argument('--force', action='store_true', help='Force start even if already running')
    args = parser.parse_args()

    monitor = PonderosaMonitor(ini_path=args.ini, force=args.force)
    monitor.run()


if __name__ == '__main__':
    main()
