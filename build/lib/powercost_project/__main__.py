"""
Entry point for project
"""
# src/powercostcli.py

import os
import time
import argparse

from  powercost_project import PonderosaMonitor

def main(ini_path: str):
    """
    Entry Point - Only method
    """
    now = time.localtime()
    now_str = time.strftime("%Y-%m-%d %H:%M:%S", now)
    pid = os.getpid()
    print(f"__main__.py: Time is {now_str}, PID = {pid}", flush=True)

    monitor = PonderosaMonitor(ini_path=args.ini)
    monitor.run(now_str=now_str, pid=pid)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ini', required=True, help='Path to the INI configuration file')
    args = parser.parse_args()
    main(ini_path=args.ini)
