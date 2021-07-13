import numpy as np


def masked_func(func, masked_array, *args, boundary_mask=None, second_masked_array=None, usesBadFlags=False):
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
    try:
        missing = masked_array.fill_value
        mask = masked_array.mask.tolist()
        data_list = masked_array.tolist(missing)

        second_data_list = None
        if (second_masked_array is not None):
            second_missing = second_masked_array.fill_value
            second_data_list = second_masked_array.tolist(second_missing)

    except AttributeError as e:
        print("Expected a numpy masked array.")
        print(e)
    
    output_data = []
    output_mask = []

    argsLength = len(args)
    if (usesBadFlags):
        argsList = list(args)
        argsList.append(None)
        args = tuple(argsList)

    for i in range(len(data_list)):
        input_data = data_list[i]
        input_mask = mask[i]
        if second_data_list != None:
            second_input_data = second_data_list[i]
            func_ma = func(input_data, second_input_data, missing, *args, boundary_mask=boundary_mask)
        else:
            if (usesBadFlags):
                argsList = list(args)
                argsList[argsLength] = input_mask
                args = tuple(argsList)
            func_ma = func(input_data, missing, *args, boundary_mask=boundary_mask)
        output_data.append(np.ma.getdata(func_ma))
        output_mask.append(np.ma.getdata(func_ma.mask))

    output_masked_array = np.ma.masked_array(data=output_data, mask=output_mask, fill_value=missing)
    return output_masked_array