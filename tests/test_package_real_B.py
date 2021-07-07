import pyart
from copy import *

import pysolo_package as solo
from pysolo_package.utils.radar_structure import RayData
from pysolo_package.utils.enums import Where
import matplotlib.pyplot as plt

from pathlib import Path

path_to_file = Path.cwd() / Path('tests/data/radar_data_b')

radar = pyart.io.read(path_to_file)


############# [Rain Rate] ##############
# for any good values 'g', sets it to g = (1/300) * 10 ^ (0.1 * g * d_const)
d_const = 2
rain_rate_mask = solo.rain_rate_masked(radar.fields['reflectivity']['data'], d_const)
radar.add_field_like('reflectivity', 'reflectivity_rain_rate', rain_rate_mask, replace_existing=True)


display = pyart.graph.RadarMapDisplay(radar)


def graphPlot(plot_field, ref):
    fig, ax = plt.subplots(ncols=2, figsize=(15,7))
    display.plot(field=ref, vmin=-40, vmax=40, title=ref, cmap='pyart_NWSRef', ax=ax[0])
    display.plot(field=plot_field, vmin=-40, vmax=40, title=plot_field + " (RHI)", cmap='pyart_NWSRef', ax=ax[1])
    plt.suptitle(plot_field, fontsize=16)
    plt.show()


graphPlot('reflectivity_rain_rate', 'reflectivity')
graphPlot('reflectivity_radial_shear', 'reflectivity')