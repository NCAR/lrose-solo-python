import ctypes
import pyart

from ..c_wrapper.run_solo import run_solo_function
from ..c_wrapper import DataPair, masked_op
from ..c_wrapper.function_alias import aliases

se_flag_glitches = aliases['flag_glitches']


def flag_glitches_ray(input_list_data, bad, deglitch_threshold, deglitch_radius, deglitch_min_gates, bad_flag_mask, dgi_clip_gate=None, boundary_mask=None):
    """
        Routine to remove discountinuities (freckles) from the data.

        Args:
            input_list: A list containing float data.
            bad: A float that represents a missing/invalid data point.
            deglitch_threshold: <TODO>
            deglitch_radius: <TODO>
            deglitch_min_gates: <TODO>
            bad_flag_mask: A mask for input_list marking good or bad values.
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask: Defines region over which operations will be done. (default: all True)

        Returns:
            Numpy masked array: Contains an array of data, mask, and fill_value of results.


    """

    args = {
        "deglitch_threshold": DataPair.DataTypeValue(ctypes.c_float, deglitch_threshold),
        "deglitch_radius": DataPair.DataTypeValue(ctypes.c_int, deglitch_radius),
        "deglitch_min_gates": DataPair.DataTypeValue(ctypes.c_int, deglitch_min_gates),
        "data": DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "nGates": DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad": DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate": DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask": DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
        "bad_flag_mask": DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), bad_flag_mask)
    }

    return run_solo_function(se_flag_glitches, args)


def flag_glitches_masked(masked_array, deglitch_threshold: float, deglitch_radius: int, deglitch_min_gates: int, boundary_masks=None):
    """ 
        Routine to remove discountinuities (freckles) from the data.

        Args:
            masked_array: A numpy masked array data structure,
            bad_flag_mask: A list of lists,
            deglitch_threshold: <TODO>,
            deglitch_radius: <TODO>,
            deglitch_min_gates: <TODO>

        Returns:
            Numpy masked array

        Throws:
            ModuleNotFoundError: if numpy is not installed
            AttributeError: if masked_array arg is not a numpy masked array.
    """

    return masked_op.masked_func(flag_glitches_ray, masked_array, deglitch_threshold, deglitch_radius, deglitch_min_gates, boundary_masks=boundary_masks, usesBadFlags=True)


def flag_glitches_field(radar: pyart.core.Radar, field: str, new_field: str, deglitch_threshold: float, deglitch_radius: int, deglitch_min_gates: int, boundary_masks=None, sweep=0):
    with masked_op.SweepManager(radar, sweep, field, new_field) as sm:
        sm.new_masked_array = flag_glitches_masked(sm.radar_sweep_data, deglitch_threshold, deglitch_radius, deglitch_min_gates, boundary_masks)
