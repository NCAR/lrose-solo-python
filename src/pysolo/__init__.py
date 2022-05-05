"""
Python interface for Solo II
"""

from .solo_functions.solo_despeckle import *
from .solo_functions.solo_ring_zap import *
from .solo_functions.solo_threshold import *
from .solo_functions.solo_flag_glitches import *
from .solo_functions.solo_flag_freckles import *
from .solo_functions.solo_forced_unfolding import *
from .solo_functions.solo_unfold_first_good_gate import unfold_first_good_gate, unfold_first_good_gate_masked
from .solo_functions.solo_unfold_local_wind import *
from .solo_functions.solo_radial_shear import *
from .solo_functions.solo_rain_rate import *
from .solo_functions.solo_remove_ac_motion import remove_ac_motion_ray, remove_ac_motion_masked
from .solo_functions.solo_remove_storm_motion import remove_storm_motion_ray, remove_storm_motion_masked
# from .solo_functions.solo_fix_vortex_vels import fix_vortex_vels, fix_vortex_vels_masked
from .solo_functions.solo_merge_fields import *
from .solo_functions.flags.solo_assign_value import assign_value, assign_value_masked
from .solo_functions.flags.solo_assert_bad_flags import assert_bad_flags, assert_bad_flags_masked
from .solo_functions.flags.solo_bad_flags_logic import bad_flags_logic, bad_flags_logic_masked
from .solo_functions.flags.solo_copy_bad_flags import copy_bad_flags, copy_bad_flags_masked
from .solo_functions.flags.solo_flagged_add import flagged_add, flagged_add_masked
from .solo_functions.flags.solo_set_bad_flags import set_bad_flags, set_bad_flags_masked
from .solo_functions.flags.solo_clear_bad_flags import clear_bad_flags
from .boundary import *
from .enums import Where, Logical