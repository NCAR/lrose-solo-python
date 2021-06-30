import ctypes
from pysolo_package.utils.run_solo import run_solo_function

from pysolo_package.utils import radar_structure, DataPair, masked_op
from pysolo_package.utils.function_alias import aliases

se_flag_freckles = aliases['flag_freckles']

def flag_freckles(input_list_data, bad, freckle_threshold, freckle_avg_count, bad_flag_mask, dgi_clip_gate=None, boundary_mask=None):
    """
        Performs a <TODO>

        Args:
            freckle_threshold: <TODO>
            freckle_avg_count: <TODO>
            input_list: A list containing float data.
            bad: A float that represents a missing/invalid data point.
            input_boundary_mask: A list of bools for masking valid/invalid values for input_list
            bad_flag_mask: <TODO>
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask_all_true: setting this to True may yield more results in despeckle (default: False)

        Returns:
            RayData: object containing resultant 'data' and 'masks' lists.

        Throws:
            ValueError: if input_list and input_boundary_mask are not equal in size
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


def flag_freckles_masked(masked_array, freckle_threshold, freckle_avg_count, boundary_mask=None):
    """ 
        Performs a deglitch on a numpy masked array
        
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

    return masked_op.masked_func(flag_freckles, masked_array, freckle_threshold, freckle_avg_count, boundary_mask = boundary_mask, usesBadFlags=True)
