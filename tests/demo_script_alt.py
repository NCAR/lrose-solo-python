from pathlib import Path
from matplotlib import pyplot as plt
import pyart
import numpy as np
from tqdm import tqdm

import src.pysolo as solo

# https://github.com/Alex-DesRosiers/radarqc_scans/blob/main/cfrad.20161006_190650.891_to_20161006_191339.679_KAMX_SUR.nc
path_to_file = Path.cwd() / Path('tests/data/script_data.nc')

radar: pyart.core.Radar = pyart.io.read(path_to_file)
display = pyart.graph.RadarMapDisplay(radar)


def graphPlot(before_field: str, after_field: str):
    _, ax = plt.subplots(ncols=2, figsize=(14, 7))

    display.plot_ppi(field=after_field, title=after_field, cmap='pyart_NWSVel', sweep=0, ax=ax[0])
    display.set_limits((-350, 350), (-350, 350), ax=ax[0])

    display.plot_ppi(field=before_field, title=before_field, cmap='pyart_NWSVel', sweep=0, ax=ax[1])
    display.set_limits((-350, 350), (-350, 350), ax=ax[1])

    plt.suptitle(after_field, fontsize=16)
    plt.savefig('2.png')


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

VEL_array: np.ma.array = radar.fields['VEL']['data'].copy()

RHO_array = radar.get_field(0, 'RHO')
SW_array = radar.get_field(0, 'SW')
VU_array = radar.get_field(0, 'VU')

first_sweep_slice = radar.get_slice(0)

RHO_missing = RHO_array.fill_value
RHO_ray_mask = RHO_array.mask.tolist()
RHO_data_list = RHO_array.tolist(RHO_missing)

SW_missing = SW_array.fill_value
SW_mask_list = SW_array.mask.tolist()
SW_data_list = SW_array.tolist(SW_missing)

VU_missing = VU_array.fill_value
VU_mask_list = VU_array.mask.tolist()
VU_data_list = VU_array.tolist(VU_missing)

nyquist_velocity = radar.get_nyquist_vel(0)
dds_radd_eff_unamb_vel = 0
azimuth_angle_degrees = list(radar.get_azimuth(0))
elevation_angle_degrees = list(radar.get_elevation(0))

assert RHO_missing == SW_missing == VU_missing

# initialize lists with data/masks. These will become lists of lists
output_data = []
output_mask = []

# iterate through each ray
for i in tqdm(range(first_sweep_slice.start, first_sweep_slice.stop), desc="Loading...", ascii=False, ncols=150):

    RHO_ray_data = RHO_data_list[i]
    SW_ray_data = SW_data_list[i]

    VU_ray_data = VU_data_list[i]

    new_masked_array = solo.threshold(VU_ray_data, RHO_ray_data, VU_missing, solo.Where.ABOVE, 1.1, 0)
    VU_ray_data = new_masked_array.tolist(VU_missing)

    new_masked_array = solo.threshold(VU_ray_data, RHO_ray_data, VU_missing, solo.Where.BELOW, 0.8, 0)
    VU_ray_data = new_masked_array.tolist(VU_missing)

    new_masked_array = solo.threshold(VU_ray_data, SW_ray_data, VU_missing, solo.Where.ABOVE, 8.0, 0)
    VU_ray_data = new_masked_array.tolist(VU_missing)

    new_masked_array = solo.despeckle(VU_ray_data, VU_missing, a_speckle)
    VU_ray_data = new_masked_array.tolist(VU_missing)

    azimuth_ray = azimuth_angle_degrees[i]
    elevation_ray = elevation_angle_degrees[i]

    new_masked_array = solo.unfold_local_wind(VU_ray_data, VU_missing, nyquist_velocity, dds_radd_eff_unamb_vel, azimuth_ray, elevation_ray,
                        ew_wind, ns_wind, ud_wind, BB_max_neg_folds, BB_max_neg_folds, BB_gates_averaged)

    VEL_array[i] = new_masked_array

radar.add_field_like("VU", "VU", VEL_array, replace_existing=True)

graphPlot('VEL', 'VU')
