"""
Entry point for project.  _init__.py does not do much.  For now, this code: handles
arguments passed to the package; there is only one argument: the location of the
INI file.  This code instantiates the primary controller class PonderosaMonitor
where control is passed to the run() method to do most of the work.
"""

import os
import time
import argparse
import logging


from  powercost_project import PonderosaMonitor

def main(ini_path: str):
    """
    Entry Point.  This is the only method and it instantiates the PonderosaMonitor
    class and control passes to the run() method.
    """
    pid = os.getpid()

    now = time.localtime()
    now_str = time.strftime("%Y-%m-%d %H:%M:%S", now)

    monitor = PonderosaMonitor(ini_path=ini_path)
    logging.info("__main__.py: Time is %s, PID = %s", now_str, pid)
    monitor.run(now_str=now_str, pid=pid)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ini', required=True, help='Path to the INI configuration file')
    args = parser.parse_args()
    args_ini: str = args.ini

    main(ini_path=args_ini)
