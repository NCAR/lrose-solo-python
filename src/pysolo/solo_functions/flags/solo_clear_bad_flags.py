import ctypes

from . import list_to_array, array_to_list
from . import aliases

se_clear_bad_flags = aliases['clear_bad_flags']

# this function is different just enough, so that the regular pattern of implementing functions won't work well.
def clear_bad_flags(complement, flag):
    """ 
        Sets all flags to False. If complement is True, then takes inverse of all flags.
        
        Args:
            complement = Whether to complement masks or not
            flag = Input masks that are to be set to all False or complemented.

        Returns:
          Numpy masked array: Contains an array of data, mask, and fill_value of results.

        Throws:
          ValueError: if input_list and input_boundary_mask are not equal in size,
    """


    # set return type and arg types
    se_clear_bad_flags.restype = None
    se_clear_bad_flags.argtypes = [ctypes.c_bool, ctypes.POINTER(ctypes.c_bool), ctypes.POINTER(ctypes.c_bool), ctypes.c_size_t]

    data_length = len(flag)

    complement_bool = ctypes.c_bool(complement)
    flagArray = list_to_array(flag, ctypes.c_bool)
    complementArray = list_to_array([False]*data_length, ctypes.c_bool)
    nGates_int = ctypes.c_size_t(data_length)

    # run C function, output_array is updated with despeckle results
    se_clear_bad_flags(
        complement_bool,
        flagArray,
        complementArray,
        nGates_int
    )

    # convert ctypes array to python list
    output_list = array_to_list(complementArray, data_length)

    # returns the new data and masks packaged in an object
    return output_list

def main():
    complement = False
    flag = [True, True, True, True]
    clear_bad_flags(complement, flag)


if __name__ == "__main__":
    main()
