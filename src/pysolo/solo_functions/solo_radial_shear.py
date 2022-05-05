import ctypes
import numpy as np
import pyart

from ..c_wrapper.run_solo import run_solo_function

from ..c_wrapper import DataPair, masked_op
from ..c_wrapper.function_alias import aliases

se_radial_shear = aliases['radial_shear']

def radial_shear_ray(input_list_data, bad, seds_gate_diff_interval, dgi_clip_gate=None, boundary_mask=None):
    """ 
        Performs a radial shear, input_list_data is subtracted by an offset of itself
        
        Args:
            input_list: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            seds_gate_diff_interval: Marks the offset of the data
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask: Defines region over which operations will be done. (default: all True).

        Returns:
          Numpy masked array: Contains an array of data, mask, and fill_value of results.

        Throws:
          ValueError: if input_list and input_boundary_mask are not equal in size,
    """

    args = {
        "seds_gate_diff_interval" : DataPair.DataTypeValue(ctypes.c_size_t, seds_gate_diff_interval),
        "data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "newData" : DataPair.DataTypeValue(np.ctypeslib.ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"), None),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
    }

    return run_solo_function(se_radial_shear, args)


def radial_shear_masked(masked_array, seds_gate_diff_interval: int, boundary_masks=None):
    """ 
        Performs a radial shear, masked_array is subtracted by an offset of itself
        
        Args:
            masked_array: A numpy masked array data structure,
            seds_gate_diff_interval: Marks the offset of the data


        Returns:
            Numpy masked array

        Throws:
            ModuleNotFoundError: if numpy is not installed
            AttributeError: if masked_array arg is not a numpy masked array.
    """

    return masked_op.masked_func(radial_shear_ray, masked_array, seds_gate_diff_interval, boundary_masks = boundary_masks)


def radial_shear_field(radar: pyart.core.Radar, field: str, new_field: str, seds_gate_diff_interval: int, boundary_masks=None, sweep=0):

    with masked_op.SweepManager(radar, sweep, field, new_field) as sm:
        sm.new_masked_array = radial_shear_masked(sm.radar_sweep_data, seds_gate_diff_interval, boundary_masks)
