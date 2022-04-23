BB_max_pos_folds = 1
BB_max_neg_folds = 1
# BB_use_local_wind
ew_wind = 7.5
ns_wind = 13.0
a_speckle = 1 
BB_gates_averaged = 20 
! for-each-ray
copy VEL to VU
threshold VU on RHO above 1.1
threshold VU on RHO below 0.8
threshold VU on SW above 8.0
despeckle VU
BB-unfolding of VU

# ######### [Unfold Local Wind] ##########
nyquist_velocity = 25
dds_radd_eff_unamb_vel = 5
azimuth_angle_degrees = 5
elevation_angle_degrees = 5
ew_wind = 5
ns_wind = 5
ud_wind = 5
max_pos_folds = 10
max_neg_folds = 10
ngates_averaged = 20
