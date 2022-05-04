import ctypes
import numpy as np
from ..c_wrapper.run_solo import run_solo_function

from ..c_wrapper import DataPair, masked_op
from ..c_wrapper.function_alias import aliases

se_remove_storm_motion = aliases['remove_storm_motion']

def remove_storm_motion_ray(input_list_data, bad, wind, speed, dgi_dd_rotation_angle, dgi_dd_elevation_angle, dgi_clip_gate=None, boundary_mask=None):
    """ 
        Performs a <TODO> operation on a list of data.
        
        Args:
            input_list: A list containing float data,
            bad: A float that represents a missing/invalid data point,
            wind: <TODO>
            speed: <TODO>
            dgi_dd_rotation_angle: <TODO>
            dgi_dd_elevation_angle: <TODO>
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask: Defines region over which operations will be done. (default: all True).

        Returns:
          Numpy masked array: Contains an array of data, mask, and fill_value of results.

        Throws:
          ValueError: if input_list and input_boundary_mask are not equal in size,
    """

    args = {
        "wind" : DataPair.DataTypeValue(ctypes.c_float, wind),
        "speed" : DataPair.DataTypeValue(ctypes.c_float, speed),
        "dgi_dd_rotation_angle" : DataPair.DataTypeValue(ctypes.c_float, dgi_dd_rotation_angle),
        "dgi_dd_elevation_angle" : DataPair.DataTypeValue(ctypes.c_float, dgi_dd_elevation_angle),
        "data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "newData" : DataPair.DataTypeValue(np.ctypeslib.ndpointer(ctypes.c_float, flags="C_CONTIGUOUS"), None),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
    }

    return run_solo_function(se_remove_storm_motion, args)


def remove_storm_motion_masked(masked_array, wind, speed, dgi_dd_rotation_angle, dgi_dd_elevation_angle, boundary_masks=None):
    """ 
        Performs a <TODO> operation on a numpy masked array
        
        Args:
            masked_array: A numpy masked array data structure,
            wind: <TODO>
            speed: <TODO>
            dgi_dd_rotation_angle: <TODO>
            dgi_dd_elevation_angle: <TODO>

        Returns:
            Numpy masked array

        Throws:
            ModuleNotFoundError: if numpy is not installed
            AttributeError: if masked_array arg is not a numpy masked array.
    """


    return masked_op.masked_func(remove_storm_motion_ray, masked_array, wind, speed, dgi_dd_rotation_angle, dgi_dd_elevation_angle, boundary_masks = boundary_masks)
