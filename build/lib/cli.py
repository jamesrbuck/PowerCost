# src/powercostcli.py

import os
import time
import argparse

from  powercost_project.main import PonderosaMonitor

def main():
    now = time.localtime()
    now_str = time.strftime("%Y-%m-%d %H:%M:%S", now)
    pid = os.getpid()
    print(f"name={__name__}, main(): Time is {now_str}, PID = {pid}", flush=True)

    parser = argparse.ArgumentParser()
    parser.add_argument('--ini', required=True, help='Path to the INI configuration file')
    args = parser.parse_args()

    monitor = main.PonderosaMonitor(ini_path=args.ini)
    monitor.run(now_str=now_str, pid=pid)
