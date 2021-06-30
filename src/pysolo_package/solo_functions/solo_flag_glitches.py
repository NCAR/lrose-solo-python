import ctypes
from pysolo_package.utils.run_solo import run_solo_function

from pysolo_package.utils import radar_structure, DataPair, masked_op
from pysolo_package.utils.function_alias import aliases

se_flag_glitches = aliases['flag_glitches']

def flag_glitches(input_list_data, bad, deglitch_threshold, deglitch_radius, deglitch_min_gates, bad_flag_mask, dgi_clip_gate=None, boundary_mask=None):
    """
        Performs a flag glitches operation on a list of data (a single ray)

        Args:
            input_list: A list containing float data.
            bad: A float that represents a missing/invalid data point.
            deglitch_threshold: <TODO>
            deglitch_radius: <TODO>
            deglitch_min_gates: <TODO>
            input_boundary_mask: A list of bools for masking valid/invalid values for input_list
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask_all_true: setting this to True may yield more results in despeckle (default: False)

        Returns:
            RayData: object containing resultant 'data' and 'masks' lists.

        Throws:
            ValueError: if input_list and input_boundary_mask are not equal in size
    """

    args = {
        "deglitch_threshold" : DataPair.DataTypeValue(ctypes.c_float, deglitch_threshold),
        "deglitch_radius" : DataPair.DataTypeValue(ctypes.c_int, deglitch_radius),
        "deglitch_min_gates" : DataPair.DataTypeValue(ctypes.c_int, deglitch_min_gates),
        "data" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_float), input_list_data),
        "nGates" : DataPair.DataTypeValue(ctypes.c_size_t, None),
        "bad" : DataPair.DataTypeValue(ctypes.c_float, bad),
        "dgi_clip_gate" : DataPair.DataTypeValue(ctypes.c_size_t, dgi_clip_gate),
        "boundary_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), boundary_mask),
        "bad_flag_mask" : DataPair.DataTypeValue(ctypes.POINTER(ctypes.c_bool), bad_flag_mask)
    }

    return run_solo_function(se_flag_glitches, args)


def flag_glitches_masked(masked_array, deglitch_threshold, deglitch_radius, deglitch_min_gates, boundary_mask=None):
    """ 
        Performs a deglitch on a numpy masked array
        
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

    return masked_op.masked_func(flag_glitches, masked_array, deglitch_threshold, deglitch_radius, deglitch_min_gates, boundary_mask = boundary_mask, usesBadFlags=True)
