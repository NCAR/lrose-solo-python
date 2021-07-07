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

if (platform.system() == "Windows"):
    path_to_file = Path.cwd() / Path('src/pysolo_package/libs/solo.dll')
    c_lib = ctypes.CDLL(str(path_to_file))
    for function in functions:
        aliases[function] = c_lib["se_" + function]

else:
    import os
    import re
    import shelve

    if not os.path.exists("temp/readelf.txt"):
        os.system("mkdir temp")
        os.system("readelf -Ws src/pysolo_package/libs/libSolo_18.04.so > temp/readelf.txt")

    shelfFile = shelve.open('temp/unmangled_functions')

    if "mangled" not in shelfFile:
        content = open("temp/readelf.txt").read()
        matches = re.findall(r'(_Z\w+se_\w+)', content, re.M)
        shelfFile["mangled"] = matches
        print("Added 'mangled' to shelf.")
    else:
        matches = shelfFile["mangled"]

    path_to_file = Path.cwd() / Path('src/pysolo_package/libs/libSolo_18.04.so')
    c_lib = ctypes.CDLL(str(path_to_file))
    
    for match in matches:
        for func in functions:
            if func in match:
                aliases[func] = c_lib[match]
