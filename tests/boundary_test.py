from pathlib import Path

fileName = "/home/ammar/code/python/lrose-solo-python/tests/fieldDBZ_F-sweep1-Boundary1"

data = Path(fileName).read_bytes() 
iterations = int((len(data)-20)/8)

i = int.from_bytes(data[:5], byteorder='little', signed=True)
import struct
ints = struct.unpack('iiffif', data[:24])
print("header", ints)

print("{:<8} {:<8} {:<8} {:<8} {:<8}".format("i", "start", "end", "x", "y"))
for i in range(iterations):
    start = 20 + i*8
    end = start + 8
    x, y = struct.unpack('ff', data[start:end])
    print("{:<8} {:<8} {:<8} {:<8} {:<8}".format(i, start, end, x, y))
