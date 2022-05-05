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

    if second_masked_array is not None:
        second_missing = second_masked_array.fill_value
        second_data_list = second_masked_array.tolist(second_missing)

    if not mask:
        mask = [False] * len(data_list)
    if not boundary_masks:
        boundary_masks = [[True] * len(data_list[0])] * len(data_list)

    # initialize lists with data/masks. These will become lists of lists
    output_data = []
    output_mask = []

    # iterate through each ray
    for i in range(len(data_list)):
        # for i in range(len(data_list)):
        input_data = data_list[i]  # gates
        input_mask = mask[i]  # mask for gates

        if second_masked_array is not None:  # if using second masked array, obtain gates for that
            second_input_data = second_data_list[i]
            # in pysolo, second parameter of functions always designates data list for secondary masked list, for functions that have secondary masked arrays.
            func_ma = func(input_data, second_input_data, missing, *args, boundary_mask=boundary_masks[i])
        elif usesBadFlags:
            func_ma = func(input_data, missing, *args, input_mask, boundary_mask=boundary_masks[i])
        else:
            func_ma = func(input_data, missing, *args, boundary_mask=boundary_masks[i])

        output_data.append(np.ma.getdata(func_ma))  # add data to output list of lists
        output_mask.append(np.ma.getdata(func_ma.mask))  # add mask as well

    # convert the list of lists, to a 2D masked array
    output_masked_array = np.ma.masked_array(data=output_data, mask=output_mask, fill_value=missing)
    return output_masked_array


def masked_func_iterable(func, masked_array, iterables, statics):

    # initialize lists with data/masks. These will become lists of lists
    output_data = []
    output_mask = []

    params_dict = {}

    missing = masked_array.fill_value
    params_dict['bad'] = missing

    for key, value in statics.items():
        params_dict[key] = value

    data_list = masked_array.tolist(missing)

    # iterate through each ray
    for i in range(len(data_list)):
        params_dict['input_list_data'] = data_list[i]
        for key, value in iterables.items():
            params_dict[key] = None if value is None else value[i]

        func_ma = func(**params_dict)

        output_data.append(np.ma.getdata(func_ma))  # add data to output list of lists
        output_mask.append(np.ma.getdata(func_ma.mask))  # add mask as well

    # convert the list of lists, to a 2D masked array
    output_masked_array = np.ma.masked_array(data=output_data, mask=output_mask, fill_value=missing)
    return output_masked_array


class SweepManager:

    def __init__(self, radar, sweep, field, new_field) -> None:
        self.radar = radar
        self.sweep = sweep
        self.field = field
        self.new_field = new_field
        self.new_field_data: np.ma.array = radar.fields[field]['data'].copy()
        self.radar_sweep_data = radar.get_field(sweep, field)
        self.new_masked_array = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):

        a = self.radar.get_slice(self.sweep)

        for ray in range(a.start, a.stop):
            self.new_field_data[ray] = self.new_masked_array[ray]

        self.radar.add_field_like(self.field, self.new_field, self.new_field_data, replace_existing=True)
