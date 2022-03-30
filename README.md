# lrose-solo-python
Python interface to Solo editing functions

Scientific poster for this project: [Poster PDF](https://raw.githubusercontent.com/NCAR/lrose-solo-python/main/poster/NCAR%20Poster.pdf)

## Install 

```shell
pip install pysolo
```
Tested for Windows 10 and Ubuntu 18.04 and 20.04.

View examples on Colab: https://colab.research.google.com/drive/16tsdAjarCjGDoJIqKFDDODaiUnFoQEFP?usp=sharing

Check out the GitHub: https://github.com/NCAR/lrose-solo-python

View it on PyPI: https://pypi.org/project/pysolo/

## Functions
The functions below take in a single ray of data, along with its bad value and additional parameters. `dgi_clip_gate` will default to the end of the ray (no clipping), and `boundary mask` will default to all true (boundary is everywhere).
All functions will return a [Numpy masked array](https://numpy.org/doc/stable/reference/maskedarray.html), which contains the output's data, mask, and bad value.

Name | Function | Source
------------ | ------------- | -------------
Despeckle | ` despeckle(input_list_data, bad, a_speckle, dgi_clip_gate=None, boundary_mask=None)` | [Despeckle.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/Despeckle.cc)
Ring Zap | `ring_zap(input_list_data, bad, from_km, to_km, km_between_gates=1, dgi_clip_gate=None, boundary_mask=None)` | [RemoveRing.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/RemoveRing.cc)
Threshold | ` threshold(input_list_data, threshold_list_data, bad, where, scaled_thr1, scaled_thr2, dgi_clip_gate=None, thr_missing=None, first_good_gate=0, boundary_mask=None) ` | [ThresholdField.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/ThresholdField.cc)
Flag Freckles | `flag_freckles(input_list_data, bad, freckle_threshold, freckle_avg_count, bad_flag_mask, dgi_clip_gate=None, boundary_mask=None)` | [FlagOps.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/FlagOps.cc)
Flag Glitches | `flag_glitches(input_list_data, bad, deglitch_threshold, deglitch_radius, deglitch_min_gates, bad_flag_mask, dgi_clip_gate=None, boundary_mask=None)` | [FlagOps.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/FlagOps.cc)
Forced Unfolding | `forced_unfolding(input_list_data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, center, dgi_clip_gate=None, boundary_mask=None)` | [ForcedUnfolding.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/ForcedUnfolding.cc)
Merge Fields | `merge_fields(input_list_data_1, input_list_data_2, bad, dgi_clip_gate=None, boundary_mask=None)` | [MergeFields.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/MergeFields.cc)
Radial Shear | `radial_shear(input_list_data, bad, seds_gate_diff_interval, dgi_clip_gate=None, boundary_mask=None)` | [RadialShear.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/RadialShear.cc)
Rain Rate | `rain_rate(input_list_data, bad, d_const, dgi_clip_gate=None, boundary_mask=None)` | [RainRate.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/RainRate.cc) 
Remove AC Motion | `remove_ac_motion(input_list_data, bad, vert_velocity, ew_velocity, ns_velocity, ew_gndspd_corr, tilt, elevation, dds_radd_eff_unamb_vel, seds_nyquist_velocity, dgi_clip_gate=None, boundary_mask=None)` | [RemoveAcMotion.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/RemoveAcMotion.cc)
Remove Storm Motion | `remove_storm_motion(input_list_data, bad, wind, speed, dgi_dd_rotation_angle, dgi_dd_elevation_angle, dgi_clip_gate=None, boundary_mask=None)` |  [RemoveSurface.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/RemoveSurface.cc)
Unfold First Good Gate | `unfold_first_good_gate(input_list_data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, max_pos_folds, max_neg_folds, ngates_averaged, last_good_v0, dgi_clip_gate=None, boundary_mask=None)` | [BBUnfolding.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/BBUnfolding.cc)
Unfold Local Wind | `unfold_local_wind(input_list_data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, azimuth_angle_degrees, elevation_angle_degrees, ew_wind,  ns_wind,  ud_wind, max_pos_folds, max_neg_folds, ngates_averaged, dgi_clip_gate=None, boundary_mask=None)` | [BBUnfolding.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/BBUnfolding.cc)

There are masked versions for all these functions, which take in a 2D numpy masked array along with the function's parameters. For instance, for despeckle masked, the function call is:

``` despeckle_masked(masked_array, a_speckle, boundary_mask=None) ```

## Flag Operations
The functions below will modify 'flags' which are a list of masked boolean values representing True for bad values and False for valid values. Returns numpy masked arrays.


Name | Function | Source
------------ | ------------- | -------------
Assign Bad Flags | `assert_bad_flags(input_list_data, bad, bad_flag_mask, dgi_clip_gate=None, boundary_mask=None)` | [FlagOps.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/FlagOps.cc)
Assign Value | `assign_value(input_list_data, bad, constant, bad_flag_mask, dgi_clip_gate=None, boundary_mask=None)` | [FlagOps.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/FlagOps.cc)
Bad Flags Logic | `bad_flags_logic(input_list_data, bad, where, logical, scaled_thr1, scaled_thr2, bad_flag_mask, dgi_clip_gate=None, boundary_mask=None)` | [FlagOps.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/FlagOps.cc)
Clear Bad Flags | `clear_bad_flags(complement, flag)` | [FlagOps.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/FlagOps.cc)
Copy Bad Flags | `copy_bad_flags(input_list_data, bad, dgi_clip_gate=None, boundary_mask=None)` | [FlagOps.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/FlagOps.cc)
Flagged Add | `flagged_add(input_list_data, bad, f_const, multiply, bad_flag_mask, dgi_clip_gate=None, boundary_mask=None)` | [FlagOps.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/FlagOps.cc)
Set Bad Flags | `set_bad_flags(input_list_data, bad, where, scaled_thr1, scaled_thr2, dgi_clip_gate=None, boundary_mask=None)` | [FlagOps.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/FlagOps.cc)