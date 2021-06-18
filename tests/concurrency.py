
if __name__ == '__main__':

    import numpy as np
    import timeit
    from pathlib import Path
    import pyart
    import sys
    sys.path.append('C:/Users/Marma/Desktop/pysolo/src/pysolo_package/')
    import solo_functions.solo_despeckle as test

    from pysolo_package.utils import radar_structure, ctypes_helper
    from pysolo_package.utils.function_alias import aliases

    path_to_file = Path.cwd() / Path('tests/data/radar_data_c')

    radar = pyart.io.read(path_to_file)
    print(list(radar.fields.keys()))
    # sys.exit(0)


    reflectivity = radar.fields['reflectivity']['data']

    missing = reflectivity.fill_value

    data_before = reflectivity.tolist(missing)
    mask_before = reflectivity.mask.tolist()

    print(radar.nrays)
    sys.exit(0)
    
    ############ [Despeckle] ##############
    a_speckle = 2

    print("Starting Timer...")
    start = timeit.default_timer()
    despeckled_mask_serial = test.despeckle_masked(reflectivity, a_speckle)
    stop = timeit.default_timer()
    print('Time: ', stop - start)

    print("Starting Timer...")
    start = timeit.default_timer()
    despeckled_mask_parallel = test.despeckle_masked(reflectivity, a_speckle, parallel=True)
    stop = timeit.default_timer()
    print('Time: ', stop - start)


    data_serial = despeckled_mask_serial.tolist(missing)
    mask_serial = despeckled_mask_serial.mask.tolist()

    data_parallel = despeckled_mask_parallel.tolist(missing)
    mask_parallel = despeckled_mask_parallel.mask.tolist()

    for i in range(len(data_serial)):
        for j in range(len(data_serial[i])):
            if (data_serial[i][j] != data_parallel[i][j]):
                print("%d -> %d (%s -> %s)" % (data_serial[i][j], data_parallel[i][j], mask_serial[i][j], mask_parallel[i][j]))


    assert(np.ma.allequal(despeckled_mask_serial, despeckled_mask_parallel))
