import ctypes
from copy import deepcopy

from pysolo_package.utils import radar_structure, ctypes_helper
from pysolo_package.utils.function_alias import aliases
from pysolo_package.utils.enums import Where

se_threshold = aliases['threshold']

def threshold(where, scaled_thr1, scaled_thr2, first_good_gate, input_list, thr_list, bad, thr_bad, boundary_mask_input, dgi_clip_gate=0,  boundary_mask_all_true=False):
    """
        Performs a <todo>

        Args:
            where: A 'Where' enum, ABOVE(0), BELOW(1), BETWEEN(2)
            scaled_thr1: <todo>
            scaled_thr2: <todo>
            first_good_gate: <todo>
            input_list: <todo>
            thr_list: <todo>
            bad: A float that represents a missing/invalid data point.
            thr_bad: <todo>
            boundary_mask_input: A list of bools for masking valid/invalid values for input_list
            (optional) dgi_clip_gate: An integer determines the end of the ray (default: length of input_list)
            (optional) boundary_mask_all_true: setting this to True may yield more results in despeckle (default: False)

        Returns:
            RadarData: object containing resultant 'data' and 'masks' lists.

        Throws:
            ValueError: if input_list and boundary_mask_input are not equal in size
    """

    if (len(input_list) != len(thr_list)):
        raise ValueError(("data size (%d) and threshold size (%d) must be of equal size.") % (len(input_list), len(thr_list)))
    elif (len(input_list) != len(boundary_mask_input)):
        raise ValueError(("data size (%d) and mask size (%d) must be of equal size.") % (len(input_list), len(boundary_mask_input)))

    # set return type and arg types
    se_threshold.restype = None
    se_threshold.argtypes = [
        ctypes.c_int,                           # where
        ctypes.c_float,                         # scaled_thr1
        ctypes.c_float,                         # scaled_thr2
        ctypes.c_int,                           # first_good_gate
        ctypes.POINTER(ctypes.c_float),         # data
        ctypes.POINTER(ctypes.c_float),         # thr_data
        ctypes.c_size_t,                        # nGates
        ctypes.POINTER(ctypes.c_float),         # newData
        ctypes.c_float,                         # bad
        ctypes.c_float,                         # thr_bad
        ctypes.c_size_t,                        # dgi_clip_gate
        ctypes.POINTER(ctypes.c_bool),          # boundary_mask
        ctypes.POINTER(ctypes.c_bool)           # bad_flag_mask
        ]

    boundary_mask_output = deepcopy(boundary_mask_input)

    # retrieve size of input/output/mask array
    data_length = len(input_list)
    # create a ctypes type that is an array of floats of length from above
    data_length_type = ctypes.c_float * data_length
    # initialize an empty float array of length
    output_array = ctypes_helper.initialize_float_array(data_length)

    # create a ctypes type that is an array of bools of length from above
    boundary_length_type = ctypes.c_bool * data_length

    # if optional, last parameter set to True, then create a list of bools set to True of length from above
    if boundary_mask_all_true:
        boundary_mask_input = [True] * data_length
    if dgi_clip_gate == 0:
        dgi_clip_gate = data_length

    # run C function, output_array is updated with despeckle results
    se_threshold(
        ctypes.c_int(where),
        ctypes.c_float(scaled_thr1),
        ctypes.c_float(scaled_thr2),
        ctypes.c_int(first_good_gate),
        data_length_type(*input_list),
        data_length_type(*thr_list),
        ctypes.c_size_t(data_length),
        output_array,
        ctypes.c_float(bad),
        ctypes.c_float(thr_bad),
        ctypes.c_size_t(dgi_clip_gate),
        boundary_length_type(*boundary_mask_input),
        boundary_length_type(*boundary_mask_input)
    )

    # convert ctypes array to python list
    output_list = ctypes_helper.array_to_list(output_array, data_length)

    boundary_mask_output = ctypes_helper.update_boundary_mask(input_list, output_list, boundary_mask_output)

    # returns the new data and masks packaged in an object
    return radar_structure.RadarData(output_list, boundary_mask_output)
