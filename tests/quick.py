n_gates = 10
n_rays = 10
rays = []

for _ in range(n_rays):
    rays.append([0]  * n_gates)

for i in range(n_rays):
    for j in range(n_gates):
        rays[i][j] = str(i) + str(j)

for ray in rays:
    print(*ray)
