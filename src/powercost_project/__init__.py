"""
Designate this folder as a Python package.  Only main.py - Class PonderosaMonitor
is accessible from outside of the package.  Initializations are not done here.
"""

__version__ = "2.2.0"

import time
import os

# Import the submodules
from .main import PonderosaMonitor

# Define the __all__ variable
__all__ = ["PonderosaMonitor"]

# Optional: Run initialization code when the package is imported
