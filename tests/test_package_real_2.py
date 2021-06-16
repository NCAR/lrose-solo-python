if __name__ == '__main__':
    import pyart
    import numpy as np
    import cartopy.crs as ccrs
    import matplotlib.pyplot as plt
    from copy import *
    import timeit
    import sys

    import pysolo_package as solo
    from pysolo_package.utils.radar_structure import RayData
    from pysolo_package.utils.enums import Where

    from pathlib import Path

    path_to_file = Path.cwd() / Path('tests/radar_data_c')

    radar = pyart.io.read(path_to_file)

    # print(list(radar.fields.keys()))

    reflectivity = radar.fields['reflectivity']['data']

    missing = reflectivity.fill_value



    ############ [Despeckle] ##############
    print("Starting Timer...")
    start = timeit.default_timer()
    a_speckle = 2
    despeckled_mask_serial = solo.despeckle_masked(reflectivity, a_speckle)
    radar.add_field_like('reflectivity', 'reflectivity_despeckled_serial', despeckled_mask_serial, replace_existing=True)
    stop = timeit.default_timer()
    print('Time: ', stop - start)

    print("Starting Timer...")
    start = timeit.default_timer()
    a_speckle = 2
    despeckled_mask_parallel = solo.despeckle_masked(reflectivity, a_speckle, parallel=True)
    radar.add_field_like('reflectivity', 'reflectivity_despeckled_parallel', despeckled_mask_parallel, replace_existing=True)
    stop = timeit.default_timer()
    print('Time: ', stop - start)


    display = pyart.graph.RadarMapDisplay(radar)

    def graphPlot(display, plot_field):
        fig, ax = plt.subplots(ncols=2, figsize=(15,7))
        display.plot(field='reflectivity', title="Original", cmap='pyart_NWSRef', ax=ax[0])
        #display.set_limits((-50, 50), (-10, 35), ax=ax[0])
        display.plot(field=plot_field, title=plot_field, cmap='pyart_NWSRef', ax=ax[1])
        #display.set_limits((-50, 50), (-10, 35), ax=ax[1])
        plt.suptitle(plot_field, fontsize=16)
        plt.show()

    assert np.ma.allequal(despeckled_mask_serial, despeckled_mask_parallel)

    data_serial = despeckled_mask_serial.tolist(missing)
    mask_serial = despeckled_mask_serial.mask.tolist()

    data_parallel = despeckled_mask_parallel.tolist(missing)
    mask_parallel = despeckled_mask_parallel.mask.tolist()

    for i in range(len(data_serial)):
        for j in range(len(data_serial[i])):
            if (data_serial[i][j] != data_parallel[i][j]):
                print("%d -> %d (%s -> %s)" % (data_serial[i][j], data_parallel[i][j], mask_serial[i][j], mask_parallel[i][j]))

    graphPlot(display, 'reflectivity_despeckled_serial')
    graphPlot(display, 'reflectivity_despeckled_parallel')
