# this module handles mapping of C-function names
# also handles which library to import based on platform

import platform
from pathlib import Path
import ctypes

aliases = {}

functions = [
    "BB_unfold_first_good_gate",
    "BB_unfold_local_wind",
    "despeckle",
    "flag_freckles",
    "flag_glitches",
    "funfold",
    "radial_shear",
    "rain_rate",
    "ring_zap",
    "threshold_field",
    "remove_ac_motion",
    "remove_storm_motion"
]

# TODO: verify correctness of path for Windows
if (platform.system() == "Windows"):
    path_to_file = Path.cwd() / Path('src/pysolo_package/libs/solo.dll')
    c_lib = ctypes.CDLL(str(path_to_file))
    for function in functions:
        aliases[function] = c_lib["se_" + function]

else:
    import os
    import re
    import shelve

    pysolo_package_dir = Path(__file__).parents[1].absolute()
    temp_dir = pysolo_package_dir / Path("temp")
    shared_lib_path = Path(__file__).parents[1].absolute() / Path('libs/libSolo_18.04.so')

    if not os.path.exists(temp_dir):
        os.system("mkdir %s" % temp_dir)
        os.system("readelf -Ws %s > %s" % (shared_lib_path, temp_dir / Path("readelf.txt")))

    shelfFile = shelve.open(str(temp_dir / Path("unmangled_functions")))

    if "mangled" not in shelfFile:
        content = open(temp_dir / Path("readelf.txt")).read()
        matches = re.findall(r'(_Z\w+se_\w+)', content, re.M)
        shelfFile["mangled"] = matches
    else:
        matches = shelfFile["mangled"]

    # from this script file, go up two directories (pysolo_package) then into libs/libSolo...
    c_lib = ctypes.CDLL(str(shared_lib_path))
    for match in matches:
        for func in functions:
            if func in match:
                aliases[func] = c_lib[match]



for func in functions:
    assert func in aliases, func
