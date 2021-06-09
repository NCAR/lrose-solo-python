import numpy as np

data = [4, 5, 6]
mask = [True, False, True]
missing = -3

expected = [-3, 5, -3]

masked = np.ma.masked_array(data=data, mask=mask, fill_value=missing)

print(masked.tolist(missing))
print(masked.mask.tolist())
