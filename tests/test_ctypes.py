import ctypes
import os
import platform

dirname = os.path.dirname(os.path.abspath(__file__))    

libraryName = os.path.join(dirname, 'libhello.so')
os.path.join(dirname, libraryName)
c_lib = ctypes.CDLL(libraryName)
c_lib.doubleVals.restype = None
c_lib.doubleVals.argtypes = [ctypes.POINTER(ctypes.c_float)]

input_list = [4, 5, 6, 7, 2, 43, 435, 12, 64, 23]

data_length = len(input_list)
# data_length_type = ctypes.c_float * data_length

data_length_type = ctypes.c_float * data_length
input_list = ctypes.cast(data_length_type(*input_list), ctypes.POINTER(ctypes.c_float))

c_lib.doubleVals(input_list, ctypes.c_int(10))

input_list = [input_list[i] for i in range(data_length)]

print(input_list)
