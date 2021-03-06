"""
    This module is a wrapper for C-types that runs the C-function based on c-type function object and parameter map.
"""

import ctypes
import re
import numpy as np
from .conversions import list_to_array, array_to_list
# Regex pattern to determine if c-type is a primative or array
isArray = re.compile(r"<class '.*\.LP_(c_.*)'>")


def update_boundary_mask(input_list, bad):
    """ update boundary mask for new invalid entries that were replaced """
    mask = []
    for i in range(len(input_list)):
        if input_list[i] == np.float32(bad):
            mask.append(True)
        else:
            mask.append(False)
    return mask


def run_solo_function(c_func, args):
    """ 
        Runs a solo library function from python
        
        Args:
            c_func: a reference to the solo function, from c_types
            args: a dictionary of {String : DataTypeValue}
                String is the name of the parameter as it's called from the function
                DataTypeValue contains c-types type and corresponding value.

        Returns:
          Numpy masked array: Contains an array of data, mask, and fill_value of results.

    """

    # data list either comes from "data" or "data1" parameters.
    # data is 1 ray with n gates.
    if "data" not in args:
        if "data1" in args:
            input_list_data = args["data1"].value
        else:
            # All solo functions have data or data1. If not in parametrs, raise error.
            raise ValueError(
                "Expected either Data or Data1 as a parameter for solo functions."
            )
    else:
        input_list_data = args["data"].value

    if "bad" in args:
        bad = args["bad"].value
    else:
        bad = 0
        
    # Obtain clipping and boundary mask, if it's none, then change it to defaults.
    dgi_clip_gate = args["dgi_clip_gate"].value
    boundary_mask = args["boundary_mask"].value

    # retrieve size of input/output/mask array
    data_length = len(input_list_data)

    # nGates will always be the size of data_length, so update its value in args dict.
    args["nGates"].value = data_length

    # optional parameters, if None, then set to default values.
    if boundary_mask is None:
        args["boundary_mask"].value = [True] * data_length # setting boundary mask to all true here will mean C-function does operation on entire dataset. 
    if dgi_clip_gate is None:
        args["dgi_clip_gate"].value = data_length # clip to the end of the data

    # newData is an array expected from solo functions that eventually gets filled with values. 
    # newData must be equal in size as input_data. Initialize it with copying input_data to ensure they are
    # the same size. Not all solo functions have newData parameter.
    if "newData" in args:
        args["newData"].value = input_list_data.copy()

    # parallel lists below
    argtypes = [] # becomes a list of c types expected from C-function call, in order that they are called
    parameters = [] # becomes a list of values, these values correspond to the types in argtypes.

    for i, j in args.items(): # i = key (string of parameter), j = value (DataTypeValue structure with 'type' and 'value')
        argtypes.append(j.type) # extract c-type & append
        result = isArray.search(str(j.type)) # check if this type is an array
        if result: # if so...
            array_type = result.group(1) # extract what type of array... either a float or bool array.
            if (array_type == 'c_float'):
                array = list_to_array(j.value, ctypes.c_float) # convert list to array by specifying the list's values and designated type.
            elif (array_type == 'c_bool'):
                array = list_to_array(j.value, ctypes.c_bool)
            else: # solo functions don't have any other array tile than floats/bools.
                raise Exception("Unexpected type for array.")
            args[i].value = array # finally, update this list to array conversion onto dictionary
            parameters.append(j.value) # and add this array to the parameter list
        else:
            parameters.append(j.type(j.value)) # if not array, simply add to parameter list

    # none of the solo functions have return types
    c_func.restype = None
    # obtained from iteration above
    c_func.argtypes = argtypes
    # run the actual function here. 
    c_func(*parameters)

    # running c_func either:
    # updated "newData" with... new data
    # or
    # updated "bad_flag_mask" with new masks
    if "newData" in args: # if newData was updated...
        # convert resultant ctypes array back to python list
        output_list = array_to_list(args['newData'].value, data_length)
        # create and return masked array
        output_mask = update_boundary_mask(output_list, bad)
        return np.ma.masked_array(data=output_list, mask=output_mask, fill_value=bad)
    elif "bad_flag_mask" in args:
        output_flag_list = array_to_list(args['bad_flag_mask'].value, data_length)
        return np.ma.masked_array(data=input_list_data, mask=output_flag_list, fill_value=bad)
    raise Exception("Unexpected control flow.")
    