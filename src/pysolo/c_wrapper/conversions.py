import ctypes

def array_to_list(input_array, size):
    """ converts ctypes array to Python list """
    return [input_array[i] for i in range(size)]


def list_to_array(floats, type):
    """ convert Python list to ctypes array """
    if floats is None:
        return None
    data_length_type = type * len(floats)
    return ctypes.cast(data_length_type(*floats), ctypes.POINTER(type))
