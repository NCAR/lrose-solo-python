from pathlib import Path

fileName = "C:/Users/Marma_na00b8q/Desktop/GitHub/lrose-solo-python/tests/data/fieldDBZ-sweep0-Boundary1"
data = Path(fileName).read_bytes()  # Python 3.5+
print((len(data)-20)/4)
i = int.from_bytes(data[:5], byteorder='little', signed=True)
import struct
ints = struct.unpack('iiffif', data[:24])
print(ints)
for i in range(15):
    start = 20 + i*4
    end = start + 8
    x, y = struct.unpack('ff', data[start:end])
    print(i, start, end, x, y)

# 48.0 95.0
# 95.0 43.0
# 43.0 37.0
# 37.0 88.0
# 88.0 7.0
# 7.0 137.0
# 137.0 27.0
# 27.0 111.0
# 111.0 48.0
# 48.0 77.0
# 77.0 46.0
# 46.0 70.0
# 70.0 82.0
# 82.0 48.0
# 48.0 95.0