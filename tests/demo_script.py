from numpy.ma.core import masked_equal
import pyart
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

import src.pysolo as solo 

# https://github.com/Alex-DesRosiers/radarqc_scans/blob/main/cfrad.20161006_190650.891_to_20161006_191339.679_KAMX_SUR.nc
path_to_file = Path.cwd() / Path('tests/data/script_data.nc')

radar = pyart.io.read(path_to_file)

BB_max_pos_folds = 1
BB_max_neg_folds = 1
ew_wind = 7.5
ns_wind = 13.0
ud_wind = 0 # unused
a_speckle = 1
BB_gates_averaged = 20

radar.add_field_like('VEL', 'VU', radar.fields['VEL']['data'])


print("threshold 1")
solo.threshold_fields(radar, 'VU', 'RHO', 'VU', solo.Where.ABOVE, 1.1, 0)
print("threshold 2")
solo.threshold_fields(radar, 'VU', 'RHO', 'VU', solo.Where.BELOW, 0.8, 0)
print("threshold 3")
solo.threshold_fields(radar, 'VU', 'SW', 'VU', solo.Where.ABOVE, 8.0, 0)

print("despeckle")
solo.despeckle_field(radar, 'VU', 'VU', a_speckle)

print("unfold local wind")
solo.unfold_local_wind_fields(radar, 'VU', 'VU', ew_wind, ns_wind, ud_wind, BB_max_pos_folds, BB_max_neg_folds, BB_gates_averaged)

print(radar.scan_type)
