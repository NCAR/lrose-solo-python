# this module handles mapping of C-function names
# also handles which library to import based on platform

import platform
import os
import ctypes

aliases = {}

dirname = os.path.dirname(os.path.abspath(__file__))    

if (platform.system() == "Windows"):
	libraryName = os.path.join(dirname, 'libs/solo.dll')
	os.path.join(dirname, libraryName)
	c_lib = ctypes.CDLL(libraryName)
	despeckle = c_lib.se_despeckle
	ring_zap = c_lib.se_ring_zap
else:
	libraryName = os.path.join(dirname, 'libs/libSolo_18.04.so')
	os.path.join(dirname, libraryName)
	c_lib = ctypes.CDLL(libraryName)
	despeckle = c_lib._Z12se_despecklePKfPfmfimPb
	ring_zap = c_lib._Z11se_ring_zapmmPKfPfmfmPb

aliases['despeckle'] = despeckle
aliases['ring_zap'] = ring_zap
