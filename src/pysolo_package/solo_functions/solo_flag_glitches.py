import ctypes
from copy import deepcopy

from pysolo_package.utils import radar_structure, ctypes_helper
from pysolo_package.utils.function_alias import aliases

se_flag_glitches = aliases['flag_glitches']

def flag_glitches(deglitch_threshold, deglitch_radius, deglitch_min_gates, input_list, bad, input_boundary_mask, bad_flag_mask, dgi_clip_gate=None, boundary_mask_all_true=False):
    """
        Performs a flag glitches operation on a list of data (a single ray)

        Args:
            deglitch_threshold: <todo>
            deglitch_radius: <todo>
            deglitch_min_gates: <todo>
            input_list: A list containing float data.
            bad_value: A float that represents a missing/invalid data point.
            input_boundary_mask: A list of bools for masking valid/invalid values for input_list
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask_all_true: setting this to True may yield more results in despeckle (default: False)

        Returns:
            RadarData: object containing resultant 'data' and 'masks' lists.

        Throws:
            ValueError: if input_list and input_boundary_mask are not equal in size
    """

    if (len(input_list) != len(input_boundary_mask)):
        raise ValueError(("data size (%d) and mask size (%d) must be of equal size.") % (len(input_list), len(input_boundary_mask)))

    # set return type and arg types
    se_flag_glitches.restype = None
    se_flag_glitches.argtypes = [
        ctypes.c_float,                     # deglitch_threshold
        ctypes.c_int,                       # deglitch_radius
        ctypes.c_int,                       # deglitch_min_bins
        ctypes.POINTER(ctypes.c_float),     # data
        ctypes.c_float,                     # bad
        ctypes.c_size_t,                    # dgi_clip_gate
        ctypes.POINTER(ctypes.c_bool),      # boundary_mask
        ctypes.POINTER(ctypes.c_bool)       # bad_flag_mask
        ]

    boundary_mask_output = deepcopy(input_boundary_mask)

    # retrieve size of input/output/mask array
    data_length = len(input_list)

    # initialize a float array from input_list parameter
    input_array = ctypes_helper.initialize_float_array(data_length, input_list)

    # initialize an empty float array of length
    flag_array = ctypes_helper.initialize_bool_array(data_length, bad_flag_mask)

    # initialize a boolean array from input_boundary_mask
    boundary_array = ctypes_helper.initialize_bool_array(data_length, input_boundary_mask)

    # if optional, last parameter set to True, then create a list of bools set to True of length from above
    if boundary_mask_all_true:
        input_boundary_mask = [True] * data_length
    if dgi_clip_gate == None:
        dgi_clip_gate = data_length

    # run C function, output_array is updated with despeckle results
    se_flag_glitches(
        ctypes.c_float(deglitch_threshold),
        ctypes.c_int(deglitch_radius),
        ctypes.c_int(deglitch_min_gates),
        input_array,
        ctypes.c_size_t(data_length),
        ctypes.c_float(bad),
        ctypes.c_size_t(dgi_clip_gate),
        boundary_array,
        flag_array
    )

    # convert ctypes array to python list
    output_list = ctypes_helper.array_to_list(flag_array, data_length)

    boundary_mask_output, changes = ctypes_helper.update_boundary_mask(input_list, output_list, boundary_mask_output)

    # returns the new data and masks packaged in an object
    return radar_structure.RadarData(output_list, boundary_mask_output, changes)

def flag_glitches_masked():
    return