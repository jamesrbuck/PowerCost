"""
For powercost package.
"""

__version__ = "1.0.0"

import time
import os

# Import the submodules
from .main import PonderosaMonitor

# Define the __all__ variable
__all__ = ["PonderosaMonitor"]

# Optional: Run initialization code when the package is imported
now = time.localtime()
now_str = time.strftime("%Y-%m-%d %H:%M:%S", now)
pid = os.getpid()
print(f"__init__.py: Package powercost is being initialized. name={__name__}")
print(f"   Time is {now_str}, PID = {pid}", flush=True)
