from pathlib import Path
from matplotlib import pyplot as plt
import pyart

import src.pysolo as solo

'''
BB-max-pos-folds is 1
BB-max-neg-folds is 1
BB-use-local-wind
ew-wind is 7.5
ns-wind is 13.0
a-speckle is 1 gates
BB-gates-averaged is 20 gates
! for-each-ray
copy VEL to VU
threshold VU on RHO above 1.1
threshold VU on RHO below 0.8
threshold VU on SW above 8.0
despeckle VU
BB-unfolding of VU
'''

# https://github.com/Alex-DesRosiers/radarqc_scans/blob/main/cfrad.20161006_190650.891_to_20161006_191339.679_KAMX_SUR.nc
path_to_file = Path.cwd() / Path('tests/data/script_data.nc')

radar: pyart.core.Radar = pyart.io.read(path_to_file)
display = pyart.graph.RadarMapDisplay(radar)


def graphPlot(before_field: str, after_field: str, output_file_name=None):
    _, ax = plt.subplots(ncols=2, figsize=(14, 7))

    display.plot_ppi(field=after_field, title=after_field, cmap='pyart_NWSVel', sweep=0, ax=ax[0])
    display.set_limits((-350, 350), (-350, 350), ax=ax[0])

    display.plot_ppi(field=before_field, title=before_field, cmap='pyart_NWSVel', sweep=0, ax=ax[1])
    display.set_limits((-350, 350), (-350, 350), ax=ax[1])

    plt.suptitle(after_field, fontsize=16)
    # plt.show()
    if output_file_name:
        print(f"Saving figure to {output_file_name}...")
        plt.savefig(output_file_name)


print("Stats".center(24, '='))
print("fields", list(radar.fields))
print("ngates", radar.ngates)
print("nrays", radar.nrays)


BB_max_pos_folds = 1    # BB-max-pos-folds is 1
BB_max_neg_folds = 1    # BB-max-neg-folds is 1
ew_wind = 7.5           # ew-wind is 7.5
ns_wind = 13.0          # ns-wind is 13.0
ud_wind = 0             # unused
a_speckle = 1           # a-speckle is 1 gates
BB_gates_averaged = 20  # BB-gates-averaged is 20 gates

radar.add_field_like('VEL', 'VU', radar.fields['VEL']['data'].copy())  # copy VEL to VU


print("threshold 1")
solo.threshold_fields(radar, 'VU', 'RHO', 'VU', solo.Where.ABOVE, 1.1, 0)  # threshold VU on RHO above 1.1

print("threshold 2")
solo.threshold_fields(radar, 'VU', 'RHO', 'VU', solo.Where.BELOW, 0.8, 0)  # threshold VU on RHO below 0.8

print("threshold 3")
solo.threshold_fields(radar, 'VU', 'SW', 'VU', solo.Where.ABOVE, 8.0, 0)  # threshold VU on SW above 8.0

print("despeckle")
solo.despeckle_field(radar, 'VU', 'VU', a_speckle)  # despeckle VU

print("unfold local wind")
solo.unfold_local_wind_fields(radar, 'VU', 'VU', ew_wind, ns_wind, ud_wind, BB_max_pos_folds, BB_max_neg_folds, BB_gates_averaged)  # BB-unfolding of VU

graphPlot("VEL", "VU", "outputs/may5/mine.png")

path_to_file = Path.cwd() / Path('tests/data/alex_output.nc')

alex_radar: pyart.core.Radar = pyart.io.read(path_to_file)
display = pyart.graph.RadarMapDisplay(alex_radar)

graphPlot("VEL", "VU", "outputs/may5/his.png")
