
from numpy import product


import re
isArray = re.compile(r"<class '.*\.LP_c_.*'>")
test_val = r"<class '__main__.LP_c_float'>"
if isArray.search(test_val):
    print("Matched")
