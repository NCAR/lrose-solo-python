from ..src.pysolo_package.solo_functions import *

complement = True
flag = [True, True, True, True, False, False]
result = solo.flags.solo_clear_bad_flags.clear_bad_flags(complement, flag)
