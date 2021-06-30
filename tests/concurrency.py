if __name__ == '__main__':

    import numpy as np
    import timeit
    from pathlib import Path
    import pyart
    import sys
    from pathlib import Path
    directory = Path.cwd() / Path('src/pysolo_package/')
    sys.path.append(str(directory))
    import solo_functions.solo_flag_freckles as test

    from pysolo_package.utils import radar_structure, DataPair
    from pysolo_package.utils.function_alias import aliases

    path_to_file = Path.cwd() / Path('tests/data/radar_data_c')

    radar = pyart.io.read(path_to_file)

    print(radar.fields.keys)


    # data_before = reflectivity.tolist(missing)
    # mask_before = reflectivity.mask.tolist()

    # print('{:,}'.format(radar.nrays * radar.ngates))

    # freckle_threshold = 12
    # freckle_avg_count = 2
    # flag_freckles_mask = test.flag_freckles_masked(radar.fields['VV']['data'], freckle_threshold, freckle_avg_count)
    # radar.add_field_like('VV', 'VV_flag_freckles', flag_freckles_mask, replace_existing=True)
    
    # ############ [Despeckle] ############## 
    # a_speckle = 2

    # print("Starting Timer...")
    # start = timeit.default_timer()
    # despeckled_mask_serial = test.despeckle_masked(reflectivity, a_speckle)
    # stop = timeit.default_timer()
    # print('Time: ', stop - start)

    # print("Starting Timer...")
    # start = timeit.default_timer()
    # despeckled_mask_parallel = test.despeckle_masked(reflectivity, a_speckle, parallel=True)
    # stop = timeit.default_timer()
    # print('Time: ', stop - start)


    # data_serial = despeckled_mask_serial.tolist(missing)
    # mask_serial = despeckled_mask_serial.mask.tolist()

    # data_parallel = despeckled_mask_parallel.tolist(missing)
    # mask_parallel = despeckled_mask_parallel.mask.tolist()

    # for i in range(len(data_serial)):
    #     for j in range(len(data_serial[i])):
    #         if (data_serial[i][j] != data_parallel[i][j]):
    #             print("%d -> %d (%s -> %s)" % (data_serial[i][j], data_parallel[i][j], mask_serial[i][j], mask_parallel[i][j]))


    # assert(np.ma.allequal(despeckled_mask_serial, despeckled_mask_parallel))
