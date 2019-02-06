import numpy as np
import matplotlib.pyplot as pyplot
from mpl_toolkits.mplot3d import Axes3D

# 3d, Z2 gauge Ising spin model
# Lattice sites form a square grid and are labelled by 0<=x,y,z<N
# Spins lie on edges connecting adjacent lattice sites and are
# labelled by (x,y,z,a):
#   - 0<=x,y,z<N give the corresponding lattice site.
#   - a=0,1,2 gives the direction of the edge from the lattice
#       site on which the spin lies
# Each plaquette is labelled by its "lowest" lattice site and
# by a,b=0,1,2 where a!=b correspond to the x,y,z-directions.

N = 20  # Size of grid is NxNxN (3*N^3 total spins)
T = 0.1   # Temperature
K = 10   # Number of iterations is K * (3*N^3)

choices = [-1, 1, 1]   # Values to choose from to initialize grid


# Returns randomized grid
def randomGrid():
    return np.random.choice(choices, [N, N, N, 3])


# Returns a random lattice site (not a spin site)
def randomSite():
    return np.random.randint(0, N, 3)


# Returns product of four spins on the plaquette labelled by (x,y,z,a,b)
def plaqProduct(g, x, y, z, a, b):
    if a == b:
        print("Error: a==b")
        return 0
    s1 = g[x % N, y % N, z % N, a]
    s2 = g[x % N, y % N, z % N, b]

    if a == 0:
        s3 = g[(x + 1) % N, y % N, z % N, b]
    elif a == 1:
        s3 = g[x % N, (y + 1) % N, z % N, b]
    else:
        s3 = g[x % N, y % N, (z + 1) % N, b]

    if b == 0:
        s4 = g[(x + 1) % N, y % N, z % N, a]
    elif b == 1:
        s4 = g[x % N, (y + 1) % N, z % N, a]
    else:
        s4 = g[x % N, y % N, (z + 1) % N, a]

    return s1 * s2 * s3 * s4


# Change in energy from flipping spin at (x,y,z,a)
def deltaE(g, x, y, z, a):
    dE = 2
    if a != 0:
        dE *= plaqProduct(g, x, y, z, a, 0)
        dE *= plaqProduct(g, x - 1, y, z, a, 0)
    if a != 1:
        dE *= plaqProduct(g, x, y, z, a, 1)
        dE *= plaqProduct(g, x, y - 1, z, a, 1)
    if a != 2:
        dE *= plaqProduct(g, x, y, z, a, 2)
        dE *= plaqProduct(g, x, y, z - 1, a, 2)
    return dE


# Determine if spin at (x,y,z,a) should flip
def flipSpinB(g, x, y, z, a):
    dE = deltaE(g, x, y, z, a)
    if np.log(np.random.random()) < -dE / T:
        return -1
    else:
        return 1


# Choose 3*N^3 random spins (on average each is chosen once)
# and decide to flip or not
def wash(g):
    gNew = g
    for z in range(3 * N ** 3):
        x, y, z = randomSite()
        a = np.random.choice(3)
        gNew[x, y, z, a] *= flipSpinB(gNew, x, y, z, a)
    return gNew


# Initialize grid of spins
grid = randomGrid()

# Keep track of average magnitization as a diagnostic
# for reaching thermal equilibrium
m = [np.average(grid)]

# Wash the grid K times
for k in range(K):
    print("%4.1f" % (100 * k / K), "%")
    grid = wash(grid)
    m = np.append(m, np.average(grid))


majority = m[-1]
majSpins = np.empty([0, 4])
for x in range(N):
    for y in range(N):
        for z in range(N):
            if grid[x, y, z, 0] * majority > 0:
                toAdd = [x + 0.5, y, z, grid[x, y, z, 0]]
                majSpins = np.append(majSpins, [toAdd], axis=0)
            if grid[x, y, z, 1] * majority > 0:
                toAdd = [x, y + 0.5, z, grid[x, y, z, 1]]
                majSpins = np.append(majSpins, [toAdd], axis=0)
            if grid[x, y, z, 2] * majority > 0:
                toAdd = [x, y, z + 0.5, grid[x, y, z, 2]]
                majSpins = np.append(majSpins, [toAdd], axis=0)


pyplot.plot(m)
fig = pyplot.figure()
ax3d = fig.add_subplot(111, projection='3d')
ax3d.scatter(majSpins[:, 0], majSpins[:, 1], majSpins[:, 2], s=1, c='k')
pyplot.show()
