import pyart
from copy import *
import matplotlib.pyplot as plt
from pathlib import Path

import import_package as solo # pylint: disable=import-error

path_to_file = Path.cwd() / Path('tests/data/radar_data_d.nc')

radar = pyart.io.read(path_to_file)

############# [Rain Rate] ##############
# Marshall Palmer Z-R
# for any good values 'g', sets it to g = (1/300) * 10 ^ (0.1 * g * d_const)
d_const = 2
rain_rate_mask = solo.rain_rate_masked(radar.fields['ZZ']['data'], d_const)
radar.add_field_like('ZZ', 'ZZ_rain_rate', rain_rate_mask, replace_existing=True)


display = pyart.graph.RadarMapDisplay(radar)


def graphPlot(plot_field, ref):
    fig, ax = plt.subplots(ncols=2, figsize=(15,7))
    display.plot_ppi(field=ref, vmin=-40, vmax=50, title=ref, cmap='pyart_NWSRef', ax=ax[0])
    display.plot_ppi(field=plot_field, vmin=-40, vmax=1000, title=plot_field + " (RHI)", cmap='pyart_NWSRef', ax=ax[1])
    plt.suptitle(plot_field, fontsize=16)
    plt.show()


graphPlot('ZZ_rain_rate', 'ZZ')
