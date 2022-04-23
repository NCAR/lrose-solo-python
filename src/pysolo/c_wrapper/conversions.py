import ctypes

def array_to_list(input_array, size):
    """ converts ctypes array to Python list """
    return [input_array[i] for i in range(size)]


def list_to_array(py_list, type):
    """ convert Python list to ctypes array """

    a = (type * len(py_list))()
    a[:] = py_list

    return a
