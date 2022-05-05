# this module handles mapping of C-function names
# also handles which library to import based on platform

import platform
from pathlib import Path
import ctypes
import os
import re

aliases = {}

# list of functions PySolo uses
functions = [
    "assert_bad_flags",
    "assign_value",
    "bad_flags_logic",
    "BB_unfold_first_good_gate",
    "BB_unfold_local_wind",
    "clear_bad_flags",
    "copy_bad_flags",
    "do_clear_bad_flags_array",
    "despeckle",
    "flagged_add",
    "flag_freckles",
    "flag_glitches",
    "funfold",
    "get_boundary_mask",
    "merge_fields",
    "radial_shear",
    "rain_rate",
    "ring_zap",
    "set_bad_flags",
    "threshold_field",
    "remove_ac_motion",
    "remove_storm_motion",
]

# from this script file, go up two directories (pysolo) then into libs/libSolo...
pysolo_dir = Path(__file__).parents[1].absolute()

# get appropriate library depending on platform
# the DLL from Windows has "extern C" so no name mangling occurs.
if platform.system() == "Windows":
    raise OSError("Windows is not supported for this library")

# Linux, on the other hand, has name manging.
# Algorithm was required to retrieve the functions from the mangled names.
else:

    def get_lib(relative_path):
        temp_dir = pysolo_dir / Path("temp")
        shared_lib_path = Path(__file__).parents[1].absolute() / Path(relative_path)

        # run readelf to get a list of C-functions with their mangled names, save results to file
        os.system(f"mkdir {temp_dir}")
        os.system(f"readelf -Ws {shared_lib_path} > {temp_dir / Path('readelf.txt')}")

        # read all content from the command
        content = open(temp_dir / Path("readelf.txt"), encoding='utf-8').read()

        # use regex pattern to discover all mangled functions, retrieve the unmangled name from group
        matches = re.findall(r'(_Z\w+se_\w+)', content, re.M)

        # initialize c_types object for shared library
        c_lib = ctypes.CDLL(str(shared_lib_path))


        # iterate through matches, check if PySolo uses that function. If so, save to map.
        for match in matches:
            for func in functions:
                if func in match:
                    aliases[func] = c_lib[match]

        # remove command output.
        os.system(f"rm -r {temp_dir}")

    try:
        get_lib('libs/libSolo_20.04.so')
    except OSError:
        get_lib('libs/libSolo_18.04.so')


# make sure all the needed functions are mapped
for func_ in functions:
    assert func_ in aliases, func_
