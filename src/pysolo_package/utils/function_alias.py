# this module handles mapping of C-function names
# also handles which library to import based on platform

import platform
import os
import ctypes

aliases = {}

dirname = os.path.dirname(os.path.abspath(__file__))    
if (platform.system() == "Windows"):
    libraryName = os.path.join(dirname, 'libs/solo.dll')
    c_lib = ctypes.CDLL(libraryName)
    despeckle = c_lib.se_despeckle
    ring_zap = c_lib.se_ring_zap
    threshold = c_lib.se_threshold_field
    flag_glitches = c_lib.se_flag_glitches
    flag_freckles = c_lib.se_flag_freckles
else:
    libraryName = os.path.join(dirname, 'libs/libSolo_18.04.so')
    c_lib = ctypes.CDLL(libraryName)
    despeckle = c_lib._Z12se_despecklePKfPfmfimPb
    ring_zap = c_lib._Z11se_ring_zapmmPKfPfmfmPb
    threshold = c_lib._Z18se_threshold_field5WhereffiPKfS1_mPfffmPbPKb
    flag_glitches = c_lib._Z16se_flag_glitchesfiiPKfmfmPbS1_
    flag_freckles = c_lib._Z16se_flag_frecklesfmPKfmfmPbS1_

aliases['despeckle'] = despeckle
aliases['ring_zap'] = ring_zap
aliases['threshold'] = threshold
aliases['flag_glitches'] = flag_glitches
aliases['flag_freckles'] = flag_freckles
