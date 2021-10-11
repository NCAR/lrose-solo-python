# this module handles mapping of C-function names
# also handles which library to import based on platform

import platform
from pathlib import Path
import ctypes


def list_to_array(longs, type):
    """ convert Python list to ctypes array """
    if longs is None:
        return None
    data_length_type = type * len(longs)
    return ctypes.cast(data_length_type(*longs), ctypes.POINTER(type))


shared_lib_path = "/home/ammar/code/python/lrose-solo-python/src/pysolo/libs/libTest.so"

# initialize c_types object for shared library
c_lib = ctypes.CDLL(str(shared_lib_path))

c_lib['se_get_boundary_mask'].restype = None

c_lib['se_get_boundary_mask'].argtypes = (
    ctypes.POINTER(ctypes.c_long),
    ctypes.POINTER(ctypes.c_long),
    ctypes.c_int,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_int,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_float,
    ctypes.c_float,
    ctypes.POINTER(ctypes.c_bool),
)


c_lib['se_get_boundary_mask'](
    list_to_array([1, 2, 3], ctypes.c_long),
    list_to_array([4, 5, 6], ctypes.c_long),
    3,
    ctypes.c_float(5.0),
    ctypes.c_float(6.0),
    ctypes.c_float(7.0),
    ctypes.c_float(8.0),
    ctypes.c_float(9.0),
    ctypes.c_float(10.0),
    11,
    ctypes.c_float(12.0),
    ctypes.c_float(13.0),
    ctypes.c_float(14.0),
    15,
    16,
    ctypes.c_float(17.0),
    ctypes.c_float(18.0),
    list_to_array([True, True, True], ctypes.c_bool),
)
