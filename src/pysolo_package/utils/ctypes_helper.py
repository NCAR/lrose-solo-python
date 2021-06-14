import ctypes

def array_to_list(input_array, size):
    """ converts ctype array to python list """
    return [input_array[i] for i in range(size)]


def initialize_float_array(size, floats=None):
    """ returns an empty float buffer of size """
    data_length_type = ctypes.c_float * size
    if (floats == None):
        return ctypes.cast(data_length_type(), ctypes.POINTER(ctypes.c_float))
    else:
        return ctypes.cast(data_length_type(*floats), ctypes.POINTER(ctypes.c_float))


def initialize_bool_array(size, bools):
    """ returns an empty float buffer of size """
    data_length_type = ctypes.c_bool * size
    return ctypes.cast(data_length_type(*bools), ctypes.POINTER(ctypes.c_bool))


def update_boundary_mask(input_list, bad, input_mask):
    # update boundary mask for new invalid entries that were replaced 
    removal_count = 0
    for i in range(len(input_list)):
        if input_list[i] == bad:
            input_mask[i] = True
            removal_count += 1
    return input_mask, removal_count
