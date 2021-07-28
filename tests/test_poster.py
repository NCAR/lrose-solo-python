import pyart
import pysolo as solo
import matplotlib
import matplotlib.pyplot as plt
import time

radar = pyart.io.read(
    "C:/Users/Marma_na00b8q/Desktop/GitHub/lrose-solo-python/tests/data/radar_data_b.nc"
)

############ [Ring Zap] ##############
# start_time = time.time()

# from_km = 30
# to_km = 35
# km_between_gates = radar.range["meters_between_gates"] / 1000
# ring_zapped_mask = solo.ring_zap_masked(
#     radar.fields["reflectivity"]["data"], 
#     from_km, 
#     to_km, 
#     km_between_gates
# )
# radar.add_field_like("reflectivity", "reflectivity_ring", ring_zapped_mask)

# print("--- %s seconds ---" % (time.time() - start_time))


########### [Despeckle] ##############
a_speckle = 10
reflectivity_masked_array = radar.fields['reflectivity']['data']
despeckled_mask = solo.despeckle_masked(reflectivity_masked_array, a_speckle)
radar.add_field_like('reflectivity', 'reflectivity_despeckled', despeckled_mask, replace_existing=True)


SMALL_SIZE = 10
MEDIUM_SIZE = 14
BIG_SIZE = 16
BIGGER_SIZE = 20


plt.rc('font', size=SMALL_SIZE)          # controls default text sizes
plt.rc('axes', titlesize=MEDIUM_SIZE)     # fontsize of the axes title
plt.rc('axes', labelsize=MEDIUM_SIZE)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('ytick', labelsize=SMALL_SIZE)    # fontsize of the tick labels
plt.rc('legend', fontsize=SMALL_SIZE)    # legend fontsize
plt.rc('figure', titlesize=BIGGER_SIZE)  # fontsize of the figure title

########### [Plot Results] ############
display = pyart.graph.RadarMapDisplay(radar)
fig, ax = plt.subplots(ncols=2, figsize=(21, 7))
display.plot(field="reflectivity", title="Original", vmin=-20, vmax=40, cmap="pyart_NWSRef", ax=ax[0])
display.set_limits((-200, 200), (-70, 70), ax=ax[0])
# display.plot(field="reflectivity_ring", title="Result", vmin=-20, vmax=40, cmap="pyart_NWSRef", ax=ax[1])
display.plot(field="reflectivity_despeckled", title="Result", vmin=-20, vmax=40, cmap="pyart_NWSRef", ax=ax[1])
display.set_limits((-200, 200), (-70, 70), ax=ax[1])
# plt.suptitle(f"Ring zap from {from_km} to {to_km}")
plt.suptitle(f"Despeckle with a_speckle = {a_speckle}")
plt.savefig("C:/Users/Marma_na00b8q/Pictures/tests/despeckle", bbox_inches="tight")
plt.show()

