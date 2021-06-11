import ctypes

from pysolo_package.utils import radar_structure, ctypes_helper
from pysolo_package.utils.function_alias import aliases

se_flag_freckles = aliases['flag_freckles']

def flag_freckles(freckle_threshold, freckle_avg_count, input_list, bad, input_boundary_mask, bad_flag_mask, dgi_clip_gate=None, boundary_mask_all_true=False):
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
            RadarData: object containing resultant 'data' and 'masks' lists.

        Throws:
            ValueError: if input_list and input_boundary_mask are not equal in size
    """

    if (len(input_list) != len(input_boundary_mask)):
        raise ValueError(("data size (%d) and mask size (%d) must be of equal size.") % (len(input_list), len(input_boundary_mask)))


    # set return type and arg types
    se_flag_freckles.restype = None
    se_flag_freckles.argtypes = [
        ctypes.c_float,                     # freckle_threshold
        ctypes.c_size_t,                    # freckle_avg_count
        ctypes.POINTER(ctypes.c_float),     # data
        ctypes.c_size_t,                    # ngates
        ctypes.c_float,                     # bad
        ctypes.c_size_t,                    # dgi_clip_gate
        ctypes.POINTER(ctypes.c_bool),      # boundary_mask
        ctypes.POINTER(ctypes.c_bool)       # bad_flag_mask
        ]

    # retrieve size of input/output/mask array
    data_length = len(input_list)

    # if optional, last parameter set to True, then create a list of bools set to True of length from above
    if boundary_mask_all_true:
        input_boundary_mask = [True] * data_length
    if dgi_clip_gate == None:
        dgi_clip_gate = data_length

    # initialize a float array from input_list parameter
    input_array = ctypes_helper.initialize_float_array(data_length, input_list)

    # initialize an empty float array of length
    flag_array = ctypes_helper.initialize_bool_array(data_length, bad_flag_mask)

    # initialize a boolean array from input_boundary_mask
    boundary_array = ctypes_helper.initialize_bool_array(data_length, input_boundary_mask)

    # run C function, output_array is updated with flag freckles results
    se_flag_freckles(
        ctypes.c_float(freckle_threshold),
        ctypes.c_size_t(freckle_avg_count),
        input_array,
        ctypes.c_size_t(data_length),
        ctypes.c_float(bad),
        ctypes.c_size_t(dgi_clip_gate),
        boundary_array,
        flag_array
    )

    # convert ctypes array to python list
    output_flag_list = ctypes_helper.array_to_list(flag_array, data_length)

    # returns the new data and masks packaged in an object
    return radar_structure.RadarData(input_list, output_flag_list, 0)

def flag_freckles_masked(masked_array, bad_flag_mask, freckle_threshold, freckle_avg_count, boundary_mask_all_true=False):
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
    try:
        import numpy as np
        missing = masked_array.fill_value
        mask = masked_array.mask.tolist()
        data_list = masked_array.tolist(missing)
    except ModuleNotFoundError:
        print("You must have Numpy installed.")
    except AttributeError:
        print("Expected a numpy masked array.")
    
    output_data = []
    output_mask = []

    for i in range(len(data_list)):
        input_data = data_list[i]
        boundary_mask = mask[i]
        bad_flag = bad_flag_mask[i]

        # run flag
        flag = flag_freckles(freckle_threshold, freckle_avg_count, input_data, missing, boundary_mask, bad_flag, boundary_mask_all_true=boundary_mask_all_true)
        output_data.append(flag.data)
        output_mask.append(flag.mask)

    assert output_data == data_list
    output_masked_array = np.ma.masked_array(data=output_data, mask=output_mask, fill_value=missing)
    return output_masked_array
