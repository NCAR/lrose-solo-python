import ctypes
import numpy as np


class DataTypeValue:
    def __init__(self, ctype_type, value):
        self.type = ctype_type
        self.value = value