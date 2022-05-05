import ctypes
import numpy as np
import pyart

from ..c_wrapper.run_solo import run_solo_function
from ..c_wrapper import DataPair, masked_op
from ..c_wrapper.function_alias import aliases

se_rain_rate = aliases['rain_rate']

def rain_rate_ray(input_list_data, bad, d_const, dgi_clip_gate=None, boundary_mask=None):
    """ 
        Calculates rain_rate in m/s from reflectivity.
        
        Args:
            input_list: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            d_const: A constant value used from the rain rate calculation.
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask: Defines region over which operations will be done. (default: all True).

        Returns:
          Numpy masked array: Contains an array of data, mask, and fill_value of results.

        Throws:
          ValueError: if input_list and input_boundary_mask are not equal in size,
    """

    args = {
        "d_const" : DataPair.DataTypeValue(ctypes.c_float, d_const),
        "data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "newData" : DataPair.DataTypeValue(np.ctypeslib.ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"), None),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
    }

    return run_solo_function(se_rain_rate, args)


def rain_rate_masked(masked_array, d_const: float, boundary_masks=None):
    """ 
        Performs a <TODO> operation on a numpy masked array
        
        Args:
            masked_array: A numpy masked array data structure,
            d_const: A constant value used from the rain rate calculation.

        Returns:
            Numpy masked array

        Throws:
            ModuleNotFoundError: if numpy is not installed
            AttributeError: if masked_array arg is not a numpy masked array.
    """


    return masked_op.masked_func(rain_rate_ray, masked_array, d_const, boundary_masks = boundary_masks)


def rain_rate_field(radar: pyart.core.Radar, field: str, new_field: str, d_const: float, boundary_masks=None, sweep=0):

    with masked_op.SweepManager(radar, sweep, field, new_field) as sm:
        sm.new_masked_array = rain_rate_masked(sm.radar_sweep_data, d_const, boundary_masks)
