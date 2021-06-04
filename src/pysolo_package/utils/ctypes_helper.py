import ctypes

def array_to_list(input_array, size):
    """ converts ctype array to python list """
    return [input_array[i] for i in range(size)]


def initialize_float_array(size):
    """ returns an empty float buffer of size """
    data_length_type = ctypes.c_float * size
    return ctypes.cast(data_length_type(), ctypes.POINTER(ctypes.c_float))


def update_boundary_mask(input_list, output_list, boundary_mask_output):
    # update boundary mask for new invalid entries that were replaced by despeckle
    changes = 0
    for i in range(len(input_list)):
        if input_list[i] != output_list[i]:
            boundary_mask_output[i] = True
    return boundary_mask_output, changes
