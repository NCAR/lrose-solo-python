# this module handles mapping of C-function names
# also handles which library to import based on platform

import platform
from pathlib import Path
import ctypes

aliases = {}

if (platform.system() == "Windows"):
    path_to_file = Path.cwd() / Path('src/pysolo_package/libs/solo.dll')
    c_lib = ctypes.CDLL(str(path_to_file))
    despeckle = c_lib.se_despeckle
    ring_zap = c_lib.se_ring_zap
    threshold = c_lib.se_threshold_field
    flag_glitches = c_lib.se_flag_glitches
    flag_freckles = c_lib.se_flag_freckles
    forced_unfolding = c_lib.se_funfold
else:
    path_to_file = Path.cwd() / Path('src/pysolo_package/libs/libSolo_18.04.so')
    c_lib = ctypes.CDLL(str(path_to_file))
    despeckle = c_lib._Z12se_despecklePKfPfmfimPb
    ring_zap = c_lib._Z11se_ring_zapmmPKfPfmfmPb
    threshold = c_lib._Z18se_threshold_field5WhereffiPKfS1_mPfffmPbPKb
    flag_glitches = c_lib._Z16se_flag_glitchesfiiPKfmfmPbS1_
    flag_freckles = c_lib._Z16se_flag_frecklesfmPKfmfmPbS1_
    forced_unfolding = c_lib._Z10se_funfoldPKfPfmffffmPb

aliases['despeckle'] = despeckle
aliases['ring_zap'] = ring_zap
aliases['threshold'] = threshold
aliases['flag_glitches'] = flag_glitches
aliases['flag_freckles'] = flag_freckles
aliases['forced_unfolding'] = forced_unfolding
