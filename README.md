# lrose-solo-python

Python interface to Solo editing functions

Scientific poster for this project: [Poster PDF](https://raw.githubusercontent.com/NCAR/lrose-solo-python/main/poster/NCAR%20Poster.pdf)

## Install

```shell
pip install pysolo
```

Tested for Ubuntu 18.04 and 20.04.

Check out the GitHub: https://github.com/NCAR/lrose-solo-python

View it on PyPI: https://pypi.org/project/pysolo/

## PyArt Functions

The functions below work with PyArt to do Solo II operations. The functions all require the following:

- `radar`: PyArt radar object.
- `field`: Name of the field containing the data.
- `new_field`: Name of the new field to save the operation on.
- Addtional parameters as needed by the function.
- `boundary_mask`: a 2D list of mask boundaries to do the operation on (default: None).
- `sweep`: the sweep to do the operation on (default: 0).

| Name                         | Function                                                                                                                                                 | Source                                                                                                              |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Despeckle Field              | `despeckle_field(radar, field, new_field, a_speckle, boundary_mask=None, sweep=0)`                                                                       | [Despeckle.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/Despeckle.cc)             |
| Ring Zap Field               | `ring_zap_field(radar, field, new_field, from_km, to_km, boundary_mask=None, sweep=0)`                                                                   | [RemoveRing.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/RemoveRing.cc)           |
| Threshold Field              | `threshold_field(radar, field, field_ref, new_field, where, scaled_thr1, scaled_thr2, thr_missing=None, first_good_gate=0, boundary_mask=None)`          | [ThresholdField.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/ThresholdField.cc)   |
| Flag Freckles Field          | `flag_freckles_field(radar, field, new_field, freckle_threshold, freckle_avg_count, boundary_mask=None, sweep=0)`                                        | [FlagOps.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/FlagOps.cc)                 |
| Flag Glitches Field          | `flag_glitches_field(radar, field, new_field, deglitch_threshold, deglitch_radius, deglitch_min_gates, boundary_mask=None, sweep=0)`                     | [FlagOps.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/FlagOps.cc)                 |
| Forced Unfolding Field       | `forced_unfolding_field(radar, field, new_field, dds_radd_eff_unamb_vel, center, boundary_mask=None, sweep=0)`                                           | [ForcedUnfolding.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/ForcedUnfolding.cc) |
| Merge Fields Field           | `merge_fields_field(radar, field, new_field, boundary_mask=None, sweep=0)`                                                                               | [MergeFields.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/MergeFields.cc)         |
| Radial Shear Field           | `radial_shear_field(radar, field, new_field, seds_gate_diff_interval, boundary_mask=None, sweep=0)`                                                      | [RadialShear.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/RadialShear.cc)         |
| Rain Rate Field              | `rain_rate_field(radar, field, new_field, dconst, boundary_mask=None, sweep=0)`                                                                          | [RainRate.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/RainRate.cc)               |
| Unfold First Good Gate Field | `unfold_first_good_gate_field(radar, field, new_field, max_neg_folds, ngates_averaged, last_good_v0, boundary_mask=None, sweep=0)`                       | [BBUnfolding.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/BBUnfolding.cc)         |
| Unfold Local Wind Field      | `unfold_local_wind_field(radar, field, new_field,ew_wind, ns_wind, ud_wind, max_pos_folds, max_neg_folds, ngates_averaged, boundary_mask=None, sweep=0)` | [BBUnfolding.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/BBUnfolding.cc)         |

In addition to these functions, there are `masked_array` and `ray` variants. The masked array functions intake a numpy masked array and output a resultant masked array, while the ray variants intake a single ray and output a 1D masked array.

## Boundary Masks

Boundaries are enclosed polygons to select which areas to perform Solo II operations on. In code, they are a list of lists of flags. PySolo contains functions to load in boundaries either from file format or two lists. Either function will return a list, which may be passed into any of the functions mentioned above to perform processing on an enclosed region.

### Read Boundary From File

```py
get_boundary_mask_from_file(radar, file_path)
```

### Read Boundary From Lists

```py
get_boundary_mask_from_list(radar, x_points, y_points)
```

The x_points and y_points correspond to cartesian coordinate pairs. For instance, if `x_points = [0, 0, 20, 20]` and `y_points = [40, 80, 80, 40]`, this corresponds to a boundary with edges:
`(0, 40), (0,80), (20,80), (20, 40)`.

## Flag Operations

The functions below will work on individual rays and generate certain masks for them based on the function's behavior.

| Name             | Function                                                                                                                                 | Source                                                                                              |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| Assign Bad Flags | `assert_bad_flags(input_list_data, bad, bad_flag_mask, dgi_clip_gate=None, boundary_mask=None)`                                          | [FlagOps.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/FlagOps.cc) |
| Assign Value     | `assign_value(input_list_data, bad, constant, bad_flag_mask, dgi_clip_gate=None, boundary_mask=None)`                                    | [FlagOps.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/FlagOps.cc) |
| Bad Flags Logic  | `bad_flags_logic(input_list_data, bad, where, logical, scaled_thr1, scaled_thr2, bad_flag_mask, dgi_clip_gate=None, boundary_mask=None)` | [FlagOps.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/FlagOps.cc) |
| Clear Bad Flags  | `clear_bad_flags(complement, flag)`                                                                                                      | [FlagOps.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/FlagOps.cc) |
| Copy Bad Flags   | `copy_bad_flags(input_list_data, bad, dgi_clip_gate=None, boundary_mask=None)`                                                           | [FlagOps.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/FlagOps.cc) |
| Flagged Add      | `flagged_add(input_list_data, bad, f_const, multiply, bad_flag_mask, dgi_clip_gate=None, boundary_mask=None)`                            | [FlagOps.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/FlagOps.cc) |
| Set Bad Flags    | `set_bad_flags(input_list_data, bad, where, scaled_thr1, scaled_thr2, dgi_clip_gate=None, boundary_mask=None)`                           | [FlagOps.cc](https://github.com/NCAR/lrose-core/blob/master/codebase/libs/Solo/src/Solo/FlagOps.cc) |
