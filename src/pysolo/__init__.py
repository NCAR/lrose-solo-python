"""
Python interface for Solo II
"""

import os
os.environ["PYART_QUIET"] = "1"

# pylint: disable=wrong-import-position
import pyart

from .solo_functions import *
from .boundary import *
from .enums import *
