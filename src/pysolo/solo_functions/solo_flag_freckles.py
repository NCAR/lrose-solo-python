import ctypes
import pyart

from ..c_wrapper.run_solo import run_solo_function
from ..c_wrapper import DataPair, masked_op
from ..c_wrapper.function_alias import aliases

se_flag_freckles = aliases['flag_freckles']

def flag_freckles_ray(input_list_data, bad, freckle_threshold, freckle_avg_count, bad_flag_mask, dgi_clip_gate=None, boundary_mask=None):
    """
        Routine to remove discountinuities (freckles) from the data.

        Args:
            input_list: A list containing float data.
            bad: A float that represents a missing/invalid data point.
            freckle_threshold: <TODO>
            freckle_avg_count: <TODO>
            bad_flag_mask: A mask for input_list marking good or bad values.
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask: Defines region over which operations will be done. (default: all True)

        Returns:
            Numpy masked array: Contains an array of data, mask, and fill_value of results.


    """

    args = {
        "freckle_threshold" : DataPair.DataTypeValue(ctypes.c_float, freckle_threshold),
        "freckle_avg_count" : DataPair.DataTypeValue(ctypes.c_size_t, freckle_avg_count),
        "data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
        "bad_flag_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), bad_flag_mask)
    }

    return run_solo_function(se_flag_freckles, args)


def flag_freckles_masked(masked_array, freckle_threshold: float, freckle_avg_count: int, boundary_masks=None):
    """
        routine to remove discountinuities (freckles) from the data.

        Args:
            masked_array: A numpy masked array data structure,
            bad_flag_mask: A list of lists,
            freckle_threshold: <TODO>,
            freckle_avg_count: <TODO>

        Returns:
            Numpy masked array

        Throws:
            ModuleNotFoundError: if numpy is not installed
            AttributeError: if masked_array arg is not a numpy masked array.
    """

    return masked_op.masked_func(flag_freckles_ray, masked_array, freckle_threshold, freckle_avg_count, boundary_masks = boundary_masks, usesBadFlags=True)


def flag_freckles_field(radar: pyart.core.Radar, field: str, new_field: str, freckle_threshold: float, freckle_avg_count: int, boundary_masks=None, sweep=0):

    with masked_op.SweepManager(radar, sweep, field, new_field) as sm:
        sm.new_masked_array = flag_freckles_masked(sm.radar_sweep_data, freckle_threshold, freckle_avg_count, boundary_masks)
