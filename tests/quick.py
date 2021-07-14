import ctypes
import numpy as np

data = [4, 5, 6, 7]
missing = 5

masked = np.ma.masked_values(data, missing)

print(np.ma.getdata(masked))
print(list(np.ma.getmask(masked)))
