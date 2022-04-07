'''
    This module is a wrapper for run_solo. Allows use of run_solo with 2D masked arrays rather than 1D arrays.
'''

import numpy as np


def masked_func(func, masked_array, *args, boundary_masks=None, second_masked_array=None, usesBadFlags=False):
    """
        Performs a solo function on a 2D masked array.

        Args:
            masked_array: A numpy masked array data structure with input data (usually this contains info on a single field),
            args: A list of args, listed in order, as required by the solo function
            (optional) boundary_masks: A boolean list designating which region to perform the operation. (Default = all True, so entire region is operated on.)
            (optional) second_masked_array: Some solo functions do operations on two fields. If so, assign this parameter to the masked array of that other field.
            (optional) usesBadFlags: Some solo functions do operations on masks rather than data. If so, set to true.

        Returns:
            Numpy masked array

        Throws:
            AttributeError: if masked_array arg is not a numpy masked array.
    """

    missing = masked_array.fill_value
    mask = masked_array.mask.tolist()
    data_list = masked_array.tolist(missing)
    if not mask:
        mask = [False] * len(data_list)
    if not boundary_masks:
        boundary_masks = [[True] * len(data_list[0])] * len(data_list)

    # initialize lists with data/masks. These will become lists of lists
    output_data = []
    output_mask = []

    # iterate through each ray
    for i in range(len(data_list)):
        # if i % 11 == 0:
        #     print(i)
        input_data = data_list[i] # gates
        input_mask = mask[i] # mask for gates

        if second_masked_array is not None: # if using second masked array, obtain gates for that
            second_missing = second_masked_array.fill_value
            second_input_data = second_masked_array.tolist(second_missing)[i]
            # in pysolo, second parameter of functions always designates data list for secondary masked list, for functions that have secondary masked arrays.
            func_ma = func(input_data, second_input_data, missing, *args, boundary_mask=boundary_masks[i])
        elif usesBadFlags:
            func_ma = func(input_data, missing, *args, input_mask, boundary_mask=boundary_masks[i])
        else:
            func_ma = func(input_data, missing, *args, boundary_mask=boundary_masks[i])

        output_data.append(np.ma.getdata(func_ma)) # add data to output list of lists
        output_mask.append(np.ma.getdata(func_ma.mask)) # add mask as well

    # convert the list of lists, to a 2D masked array
    output_masked_array = np.ma.masked_array(data=output_data, mask=output_mask, fill_value=missing)
    return output_masked_array

# iterables: {
#   var_name: list,
#   var_name: list
# }

def print_info(name, pay, weather, time, input_data, input_mask):
    print(f"{name} ({pay} / hr): {weather} @ {time}, magic number is {input_data} ({input_mask})")

def print_food(name, calories, color, isEdible, input_data, input_mask, boundary_mask=None):
    print(f"{color} {name} has {calories} calories. Is it edible? {isEdible} ({input_data} - {input_mask})")

def masked_func_v2(func, masked_array, iterables, statics):

    # initialize lists with data/masks. These will become lists of lists
    output_data = []
    output_mask = []

    params_dict = {}

    missing = masked_array.fill_value
    params_dict['bad'] = missing

    mask = masked_array.mask.tolist()
    data_list = masked_array.tolist(missing)

    # iterate through each ray
    for i in range(len(data_list)):
        params_dict['input_list_data'] = data_list[i]
        # params_dict['input_mask'] = mask[i]
        for key, item in iterables.items():
            params_dict[key] = None if item is None else item[i]
        for key, item in statics.items():
            params_dict[key] = item

        func_ma = func(**params_dict)

        output_data.append(np.ma.getdata(func_ma)) # add data to output list of lists
        output_mask.append(np.ma.getdata(func_ma.mask)) # add mask as well

    # convert the list of lists, to a 2D masked array
    output_masked_array = np.ma.masked_array(data=output_data, mask=output_mask, fill_value=missing)
    return output_masked_array

if __name__ == "__main__":
    masked_func_v2(print_info, np.ma.array([1, 2, 3], mask=[0, 0, 1]), {'name': ['jill', 'janice', 'joseph'], 'pay': [4, 5, 6]}, {'weather': 'sunny', 'time': '2:00 PM'})
    masked_func_v2(print_food, np.ma.array([16, 20, 30], mask=[0, 1, 0], fill_value=-1), 
        {'name': ['carrot', 'pear', 'french fries'], 'calories': [40, 50, 200], 'color': ['orange', 'green', 'yellow'], 'boundary_mask': [False, False, True]}, 
        {'isEdible': True}
    )
