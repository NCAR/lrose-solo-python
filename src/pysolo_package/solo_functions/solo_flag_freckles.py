import ctypes

from pysolo_package.utils import radar_structure, ctypes_helper, masked_op
from pysolo_package.utils.function_alias import aliases

se_flag_freckles = aliases['flag_freckles']

def flag_freckles(input_list_data, bad, freckle_threshold, freckle_avg_count, input_list_mask=None, dgi_clip_gate=None, boundary_mask=None):
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

    if (input_list_mask != None and len(input_list_data) != len(input_list_mask)):
        raise ValueError(("data size (%d) and mask size (%d) must be of equal size.") % (len(input_list_data), len(input_list_mask)))


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
    data_length = len(input_list_data)

    # if optional, last parameter set to True, then create a list of bools set to True of length from above
    if boundary_mask == None:
        boundary_mask = [True] * data_length
    if dgi_clip_gate == None:
        dgi_clip_gate = data_length
    if input_list_mask == None:
        input_list_mask = [True if x == bad else False for x in input_list_data]                

    # create a ctypes float/bool array from a list of size data_length
    input_array = ctypes_helper.initialize_float_array(data_length, input_list_data)

    boundary_array = ctypes_helper.initialize_bool_array(data_length, boundary_mask)

    # initialize an empty bool array of length
    flag_array = ctypes_helper.initialize_bool_array(data_length, input_list_mask)


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

    # convert resultant ctypes array back to python list
    output_flag_list = ctypes_helper.array_to_list(flag_array, data_length)

    # returns the new data and masks packaged in an object
    return radar_structure.RayData(input_list_data, output_flag_list, 0)

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

    return masked_op.masked_func(flag_freckles, masked_array, freckle_threshold, freckle_avg_count, boundary_mask = boundary_mask)
