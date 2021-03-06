# This file is to test features from the package using PyTest

import numpy as np
import math
import src.pysolo as solo


""" converts masked array to python list of data"""
def masked_to_list_data(masked):
    return list(np.ma.getdata(masked))


""" converts masked array's mask to python list of mask"""
def masked_to_list_mask(masked):
    return list(np.ma.getmask(masked))


class TestDespeckle():

    def test_short(self):
        input_data = [3, -3, -3, 5, 5, 5, -3, 5, 5, -3]
        bad = -3
        a_speckle = 3
        dgi = 8
        input_boundary_mask = [True, True, True, True, True, True, True, True, True, True]
        expected_data = [-3, -3, -3, -3, -3, -3, -3, 5, 5, -3]
        result = solo.despeckle(input_data, bad, a_speckle, dgi_clip_gate=dgi, boundary_mask=input_boundary_mask)
        assert masked_to_list_data(result) == expected_data


class TestRingZap():

    def test_short(self):
        input_data = [-3, 4, 6, -3, 8, -3, 10, 12, 14, -3, -3]
        bad = -3
        from_km = 2
        to_km = 9
        dgi = 10
        input_boundary_mask = [True, True, True, True, False, True, True, True, True, True, True]
        expected_data = [-3, 4, -3, -3, 8, -3, -3, -3, -3, -3, -3]
        result = solo.ring_zap(input_data, bad, from_km, to_km, dgi_clip_gate=dgi, boundary_mask=input_boundary_mask)
        assert masked_to_list_data(result) == expected_data


class TestThreshold:

    def test_short(self):
        input_data = [-3,  4,  6, -3,  8,  -3, 10,  12, 14, -3, -3]
        thr_data = [-5, 30, 40, 60, -5,  70, -5, 110, -5, 10, 140]
        expected_data = [-3, -3, -3, -3, -3, -3, -3, 12, -3, -3, -3]
        bad = -3
        thr_bad = -5
        input_boundary_mask = [True, True, True, True, True, True, True, True, True, True, True]
        result = solo.threshold(input_data, thr_data, bad, solo.Where.BELOW.value, 50, 0, thr_missing=thr_bad, boundary_mask=input_boundary_mask)
        assert masked_to_list_data(result) == expected_data


class TestFlagGlitches:

    def test_short(self):
        input_data = [3, 4, 5, -6, -7, 4, 4, 5]
        input_boundary_mask = [True, True, True, True, True, True, True, True]
        input_bad_flag = [False, False, False, False, True, True, True, True]
        bad = -3
        deglitch_threshold = 3
        deglitch_radius = 1
        deglitch_min_bins = 3
        expected_bad_flag = [False, False, True, False, True, True, True, True]
        result = solo.flag_glitches(input_data, bad, deglitch_threshold, deglitch_radius, deglitch_min_bins, input_bad_flag, boundary_mask=input_boundary_mask)
        assert list(np.ma.getmask(result)) == expected_bad_flag



class TestUnfoldLocalWind:
    
    def test_short_one(self):
        data = [3, 4, 5, 6]
        bad = -3
        ngates_averaged = 3
        max_pos_folds = 5
        max_neg_folds = 5
        nyquist_velocity = 10.0
        dds_radd_eff_unamb_vel = 0.0
        azimuth_angle_degrees = 360.0
        elevation_angle_degrees = 90.0
        ew_horiz_wind = 999
        ns_horiz_wind = 999
        vert_wind = 2.0
        expected_data = [3.0, 4.0, 5.0, 6.0]
        result = solo.unfold_local_wind(data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, azimuth_angle_degrees, elevation_angle_degrees,
                                        ew_horiz_wind, ns_horiz_wind, vert_wind, max_pos_folds, max_neg_folds, ngates_averaged)
        assert masked_to_list_data(result) == expected_data

    def test_short_two(self):
        data = [3, -3, -3, 5, 5, -2, -3, 5, 5, -3]
        boundary = [True, False,  True, True, False, True,  True, True, True, False]
        bad = -3
        dgi = 8
        ngates_averaged = 1
        max_pos_folds = 5
        max_neg_folds = 5
        nyquist_velocity = 10.0
        dds_radd_eff_unamb_vel = 0.0
        azimuth_angle_degrees = 360.0
        elevation_angle_degrees = 90.0
        ew_horiz_wind = 999
        ns_horiz_wind = 999
        vert_wind = 3.0
        expected_data = [3, -3, -3, 5, 5, -2, -3, 5, 5, -3]
        result = solo.unfold_local_wind(data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, azimuth_angle_degrees, elevation_angle_degrees, ew_horiz_wind,
                                        ns_horiz_wind, vert_wind, max_pos_folds, max_neg_folds, ngates_averaged, dgi_clip_gate=dgi, boundary_mask=boundary)
        assert masked_to_list_data(result) == expected_data


class TestUnfoldFirstGoodGate:

    def test_short_one(self):
        data = [3, 4, 5, 6]
        bad = -3
        ngates_averaged = 3
        max_pos_folds = 5
        max_neg_folds = 5
        nyquist_velocity = 10.0
        dds_radd_eff_unamb_vel = 0.0
        expected_data = [3.0, 4.0, 5.0, 6.0]
        last_good_v0 = [bad]
        result = solo.unfold_first_good_gate(data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, max_pos_folds, max_neg_folds, ngates_averaged, last_good_v0)
        assert masked_to_list_data(result) == expected_data

    def test_short_two(self):
        data = [-3, -3, 5, 6]
        bad = -3
        ngates_averaged = 3
        max_pos_folds = 5
        max_neg_folds = 5
        nyquist_velocity = 10.0
        dds_radd_eff_unamb_vel = 0.0
        expected_data = [-3, -3, 5, 6]
        last_good_v0 = [bad]
        result = solo.unfold_first_good_gate(data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, max_pos_folds, max_neg_folds, ngates_averaged, last_good_v0)
        assert masked_to_list_data(result) == expected_data

    def test_short_three(self):
        data = [3, 4, 5, 6]
        bad = -3
        ngates_averaged = 3
        max_pos_folds = 5
        max_neg_folds = 5
        nyquist_velocity = 10.0
        dds_radd_eff_unamb_vel = 0.0
        expected_data = [3, 4, 5, 6]
        last_good_v0 = [9]
        result = solo.unfold_first_good_gate(data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, max_pos_folds, max_neg_folds, ngates_averaged, last_good_v0)
        assert masked_to_list_data(result) == expected_data

    def test_short_four(self):
        data = [3, -3, 5, -16, 7, -3, 6]
        boundary = [False, False, True, True, False, True, True]
        bad = -3
        ngates_averaged = 2
        max_pos_folds = 5
        max_neg_folds = 5
        nyquist_velocity = 3.2
        dds_radd_eff_unamb_vel = 0.0
        expected_data = [3, -3, 5, 2, 7, -3, 6]
        last_good_v0 = [bad]
        result = solo.unfold_first_good_gate(data, bad, nyquist_velocity, dds_radd_eff_unamb_vel, max_pos_folds, max_neg_folds, ngates_averaged, last_good_v0, boundary_mask=boundary)
        assert masked_to_list_data(result) == expected_data


class TestRadialShear:

    def test_short_one(self):
        seds_gate_diff_interval = 4
        data = [-3, 4, 5, 6, 7, 8, 9, 10]
        bad = -3
        expected_data = [-3, 4, 4, 4, 7, 8, 9, 10]
        result = solo.radial_shear(data, bad, seds_gate_diff_interval)
        assert masked_to_list_data(result) == expected_data

    def test_short_two(self):
        seds_gate_diff_interval = 5
        data = [8, -3, -3, -3, 4, 8, 6, 4, 4, -3, 2, 3]
        bad = -3
        dgi = 10
        expected_data = [0, -3, -3, -3, -3, 8, 6, 4, 4, -3, 2, 3]
        result = solo.radial_shear(data, bad, seds_gate_diff_interval, dgi_clip_gate=dgi)
        assert masked_to_list_data(result) == expected_data


class TestRemoveACMotion():

    def test_short_one(self):
        data = [3, 4, 5, 6]
        bad_flag = -3
        vert_velocity = 1
        ew_velocity = 1
        ns_velocity = 1
        ew_gndspd_corr = 1
        elevation = 0.0
        tilt = 0.0
        nyquist_velocity = 10.0
        expected_data = [3, 4, 5, 6]
        dds_radd_eff_unamb_vel = 0.0
        result = solo.remove_ac_motion(data, bad_flag, vert_velocity, ew_velocity, ns_velocity, ew_gndspd_corr, tilt, elevation, dds_radd_eff_unamb_vel, nyquist_velocity)
        assert masked_to_list_data(result) == expected_data

    def test_short_two(self):
        data = [3, 4, -5, 6]
        bad_flag = -3
        vert_velocity = 1
        ew_velocity = 1
        ns_velocity = 1
        ew_gndspd_corr = 1
        elevation = 0.0
        tilt = 0.0
        nyquist_velocity = 3.2
        expected_data = [3, -2, 1, 0]
        dds_radd_eff_unamb_vel = 0.0
        result = solo.remove_ac_motion(data, bad_flag, vert_velocity, ew_velocity, ns_velocity, ew_gndspd_corr, tilt, elevation, dds_radd_eff_unamb_vel, nyquist_velocity)
        assert masked_to_list_data(result) == expected_data

    def test_short_three(self):
        data = [-3, 6, 5, -3]
        bad_flag = -3
        vert_velocity = 3  # goes with sin(elevation)
        ew_velocity = 1   # these three go with sin(tilt)
        ns_velocity = 1
        ew_gndspd_corr = 1
        elevation = math.pi/2.0  # or any multiple of pi help make ac_vel = 0
        tilt = 0.0  # or any multiple of pi help make ac_vel = 0
        # Nyquist stuff ...
        # keep the Nyquist velocity greater than any data value,
        # to avoid any folding/unfolding
        nyquist_velocity = 10.0
        clip_gate = 2
        expected_data = [-3, 9, 5, -3]  # no changed
        dds_radd_eff_unamb_vel = 0.0
        result = solo.remove_ac_motion(data, bad_flag, vert_velocity, ew_velocity, ns_velocity, ew_gndspd_corr, tilt, elevation, dds_radd_eff_unamb_vel, nyquist_velocity, dgi_clip_gate=clip_gate)
        assert masked_to_list_data(result) == expected_data

    def test_short_four(self):
        data = [-3, 6, 5, -3]
        bad_flag = -3
        vert_velocity = 3
        ew_velocity = 1
        ns_velocity = 1
        ew_gndspd_corr = 1
        elevation = math.pi/2.0
        tilt = 0.0
        nyquist_velocity = 5.0
        clip_gate = 2
        expected_data = [-3, -1, 5, -3]
        dds_radd_eff_unamb_vel = 0.0
        result = solo.remove_ac_motion(data, bad_flag, vert_velocity, ew_velocity, ns_velocity, ew_gndspd_corr, tilt, elevation, dds_radd_eff_unamb_vel, nyquist_velocity, dgi_clip_gate=clip_gate)
        assert masked_to_list_data(result) == expected_data

    def test_short_five(self):
        data = [-4, -3, 5, 8]
        bad_flag = -3
        vert_velocity = 3
        ew_velocity = 10.0
        ns_velocity = 0.0
        ew_gndspd_corr = 1
        tilt = math.pi/2.0
        elevation = 0.0
        nyquist_velocity = 6.0
        clip_gate = 3
        expected_data = [-5, -3, 4, 8]
        dds_radd_eff_unamb_vel = 0.0
        result = solo.remove_ac_motion(data, bad_flag, vert_velocity, ew_velocity, ns_velocity, ew_gndspd_corr, tilt, elevation, dds_radd_eff_unamb_vel, nyquist_velocity, dgi_clip_gate=clip_gate)
        assert masked_to_list_data(result) == expected_data


class TestMergeFields():

    def test_short_one(self):
        data1 = [4, -3, 6, 7, -3]
        data2 = [40, 50, 60, 70, 80]
        bad = -3
        result = solo.merge_fields(data1, data2, bad)
        expected_data = [4, 50, 6, 7, 80]
        assert masked_to_list_data(result) == expected_data

    def test_short_two(self):
        data1 = [-3]
        data2 = [99]
        bad = -3
        result = solo.merge_fields(data1, data2, bad)
        expected_data = [99]
        assert masked_to_list_data(result) == expected_data

    def test_short_three(self):
        data1 = [100]
        data2 = [-3]
        bad = -3
        result = solo.merge_fields(data1, data2, bad)
        expected_data = [100]
        assert masked_to_list_data(result) == expected_data


class TestAssertBadFlags():

    def test_short_one(self):
        data = [3, 4, 5, 6, 7]
        bad = -3
        mask = [True, True, True, True, True]
        result = solo.assert_bad_flags(data, bad, mask)
        expected_data = [-3, -3, -3, -3, -3]
        assert masked_to_list_data(result) == expected_data

    def test_short_two(self):
        data = [3, 4, 5, 6, 7]
        bad = -3
        mask = [False, False, False, False, False]
        result = solo.assert_bad_flags(data, bad, mask)
        expected_data = [3, 4, 5, 6, 7]
        assert masked_to_list_data(result) == expected_data

    def test_short_three(self):
        data = [3, 4, 5, 6, 7]
        bad = -3
        mask = [False, True, False, True, False]
        result = solo.assert_bad_flags(data, bad, mask)
        expected_data = [3, -3, 5, -3, 7]
        assert masked_to_list_data(result) == expected_data


class TestBadFlags():

    def test_short_one(self):
        data = [-3, 60, 70, 80, 90, 100, 110, 120, -3]
        mask = [True, False, False, False, False, False, False, False, True]
        scaled_thr1 = 100
        scaled_thr2 = 1000
        where = solo.Where.BELOW
        logical = solo.Logical.AND
        bad = -3
        result = solo.bad_flags_logic(data, bad, where.value, logical.value, scaled_thr1, scaled_thr2, mask)
        expected_bad_flag = [False, False, False, False, False, False, False, False, False]
        assert masked_to_list_mask(result) == expected_bad_flag

    def test_short_two(self):
        data = [-3, 60, 70, 80, 90, 100, 110, 120, -3]
        mask = [True, True, True, True, True, True, True, True, True]
        scaled_thr1 = 100
        scaled_thr2 = 1000
        where = solo.Where.BELOW
        logical = solo.Logical.AND
        bad = -3
        result = solo.bad_flags_logic(data, bad, where.value, logical.value, scaled_thr1, scaled_thr2, mask)
        expected_bad_flag = [False, True, True, True, True, False, False, False, False]
        assert masked_to_list_mask(result) == expected_bad_flag

    def test_short_three(self):
        data = [-3,   60,    70,   80,    90,   100,   110,   120,  -3]
        mask = [True, False, True, False, True, False, True, False, True]
        scaled_thr1 = 70
        scaled_thr2 = 100
        where = solo.Where.BETWEEN
        logical = solo.Logical.OR
        bad = -3
        result = solo.bad_flags_logic(data, bad, where.value, logical.value, scaled_thr1, scaled_thr2, mask)
        expected_bad_flag = [True, False, True, True, True, True, True, False, True]
        assert masked_to_list_mask(result) == expected_bad_flag


class TestCopyBadFlags:

    def test_short_one(self):
        data = [3, -3, 5, -3, 7]
        bad = -3
        result = solo.copy_bad_flags(data, bad)
        expected_bad_flag = [False, True, False, True, False]
        assert masked_to_list_mask(result) == expected_bad_flag

    def test_short_two(self):
        data = [-100, -3, 0, 100, -3, 1000, -3, 3, -2.995]
        bad = -3
        result = solo.copy_bad_flags(data, bad)
        expected_bad_flag = [False, True, False, False, True, False, True, False, False]
        assert masked_to_list_mask(result) == expected_bad_flag

    def test_short_three(self):
        data = [-100, -1e-20, 0, 100, -1e-20, 1000, -1e-20, 3, -2.995]
        bad = -1e-20
        result = solo.copy_bad_flags(data, bad)
        expected_bad_flag = [False, True, False, False, True, False, True, False, False]
        assert masked_to_list_mask(result) == expected_bad_flag


class TestFlaggedAdd:

    def test_short_one(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        mask = [True if x % 2 == 0 else False for x in data]
        f_const = 10
        multiply = True
        bad = -3
        result = solo.flagged_add(data, bad, f_const, multiply, mask)
        expected_data = [1, 20, 3, 40, 5, 60, 7, 80, 9, 100]
        assert masked_to_list_data(result) == expected_data

    def test_short_two(self):
        data = [1, 2, -3, 4, -3, 6, 7, -3, 9, -3]
        mask = [True if x % 2 == 0 else False for x in data]
        f_const = 10
        multiply = True
        bad = -3
        result = solo.flagged_add(data, bad, f_const, multiply, mask)
        expected_data = [1, 20, -3, 40, -3, 60, 7, -3, 9, -3]
        assert masked_to_list_data(result) == expected_data

    def test_short_three(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        mask = [True if x % 2 == 0 else False for x in data]
        f_const = 10
        multiply = False
        bad = -3
        result = solo.flagged_add(data, bad, f_const, multiply, mask)
        expected_data = [1, 12, 3, 14, 5, 16, 7, 18, 9, 20]
        assert masked_to_list_data(result) == expected_data

    def test_short_four(self):
        data = [1, 2, -3, 4, -3, 6, 7, -3, 9, -3]
        mask = [True if x % 2 == 0 else False for x in data]
        f_const = 10
        multiply = False
        bad = -3
        result = solo.flagged_add(data, bad, f_const, multiply, mask)
        expected_data = [1, 12, -3, 14, -3, 16, 7, -3, 9, -3]
        assert masked_to_list_data(result) == expected_data


class TestSetBadFlags:

    def test_short_one(self):
        data = [-3, 60, 70, 80, 90, 100, 110, 120, -3]
        scaled_thr1 = 100
        scaled_thr2 = 1000
        where = solo.Where.BELOW
        bad = -3
        result = solo.set_bad_flags(data, bad, where, scaled_thr1, scaled_thr2)
        expected_bad_flag = [False, True, True, True, True, False, False, False, False]
        assert masked_to_list_mask(result) == expected_bad_flag

    def test_short_two(self):
        data = [-3, 60, 70, 80, -3, 90, 100, 110, 120, -3]
        scaled_thr1 = 70
        scaled_thr2 = 90
        where = solo.Where.BETWEEN
        bad = -3
        result = solo.set_bad_flags(data, bad, where, scaled_thr1, scaled_thr2)
        expected_bad_flag = [False, False, True, True, False, True, False, False, False, False]
        assert masked_to_list_mask(result) == expected_bad_flag


class TestAssignValue:

    def test_short_one(self):
        data = [-3, 60, 70, 80, -3, 90, 100, 110, 120, -3]
        bad = -3
        constant = 800
        mask = [True] * len(data)
        result = solo.assign_value(data, bad, constant, mask)
        expected_data = [800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0, 800.0]
        assert masked_to_list_data(result) == expected_data

    def test_short_two(self):
        data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        bad = -3
        constant = 800
        mask = [True if x % 2 == 0 else False for x in data]
        result = solo.assign_value(data, bad, constant, mask)
        expected_data = [1, 800, 3, 800, 5, 800, 7, 800, 9, 800]
        assert masked_to_list_data(result) == expected_data
