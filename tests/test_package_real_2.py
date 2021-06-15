
import pyart
import numpy as np
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
from copy import *
import timeit
import sys

import pysolo_package as solo
from pysolo_package.utils.radar_structure import RadarData
from pysolo_package.utils.enums import Where

from pathlib import Path

path_to_file = Path.cwd() / Path('tests/radar_data_b')

radar = pyart.io.read(path_to_file)

# print(list(radar.fields.keys()))

reflectivity = radar.fields['reflectivity']['data']

missing = reflectivity.fill_value

data_before = reflectivity.tolist(missing)
mask_before = reflectivity.mask.tolist()

############ [Despeckle] ##############
start = timeit.default_timer()
a_speckle = 2
despeckled_mask = solo.despeckle_masked(reflectivity, a_speckle)
radar.add_field_like('reflectivity', 'reflectivity_despeckled', despeckled_mask, replace_existing=True)
stop = timeit.default_timer()

print('Time: ', stop - start)

data_after = despeckled_mask.tolist(missing)
mask_after = despeckled_mask.mask.tolist()

# for i in range(len(data_before)):
#     for j in range(len(data_before[i])):
#         if (data_before[i][j] != data_after[i][j] and not mask_before[i][j]):
#             print("%d -> %d (%s -> %s)" % (data_before[i][j], data_after[i][j], mask_before[i][j], mask_after[i][j]))

# sys.exit(0)

display = pyart.graph.RadarMapDisplay(radar)

def graphPlot(display, plot_field):
    fig, ax = plt.subplots(ncols=2, figsize=(15,7))
    display.plot(field='reflectivity', title="Original", cmap='pyart_NWSRef', ax=ax[0])
    #display.set_limits((-50, 50), (-10, 35), ax=ax[0])
    display.plot(field=plot_field, title=plot_field, cmap='pyart_NWSRef', ax=ax[1])
    #display.set_limits((-50, 50), (-10, 35), ax=ax[1])
    plt.suptitle(plot_field, fontsize=16)
    plt.show()

graphPlot(display, 'reflectivity_despeckled')
