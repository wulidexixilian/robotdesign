import numpy
import numba
import time


def Z0(a, b):
    c = numpy.cross(a, b)
    return c


def Z1(a, b):
    a_hat = numpy.array([
        [0, -a[2], a[1]],
        [a[2], 0, -a[0]],
        [-a[1], a[0], 0]
    ])
    c = a_hat @ b
    return c


@numba.jit
def Z2(a, b):
    # c = a_hat @ b
    c = [-a[2] * b[1] + a[1] * b[2], a[2] * b[0] - a[0] * b[2], -a[1] * b[0] + a[0] * b[1]]
    return c

a = numpy.array([1., 2., 3.])
b = numpy.array([1.2, 2.3, 3.4])
start0 = time.time()
for i in range(1000):
    c0 = Z0(a, b)
end0 = time.time()
print('numpy cross {}'.format(end0 - start0))

start1 = time.time()
for i in range(1000):
    c1 = Z1(a, b)
end1 = time.time()
print('raw cross matrix {}'.format(end1 - start1))

start2 = time.time()
for i in range(1000):
    c2 = Z2(a, b)
end2 = time.time()
print('jit cross matrix {}'.format(end2 - start2))

np = numpy
# @numba.jit
def rotation3d(ax, alpha):
    """ rotation transformation matrix about ax:axis for alpha:angle """
    c = np.cos(alpha)
    s = np.sin(alpha)
    # results4axes = {
    #         "x":np.array([[1, 0, 0],[0, c, -s],[0, s, c]]),
    #         "y":np.array([[c, 0, s],[0, 1, 0],[-s, 0, c]]),
    #         "z":np.array([[c, -s, 0],[s, c, 0],[0, 0, 1]]),
    #         }
    if ax is 'x':
        return np.array([[1, 0, 0],[0, c, -s],[0, s, c]])
    if ax is 'y':
        return np.array([[c, 0, s],[0, 1, 0],[-s, 0, c]])
    if ax is 'z':
        return np.array([[c, -s, 0],[s, c, 0],[0, 0, 1]])
# @numba.jit
def rotation(phi, theta, psi, order="zyx"):
    """ roll/order[0] -> pitch/order[1] -> yaw/order[2] """
    order = order.lower()
    roll = rotation3d(order[0], phi)
    pitch = rotation3d(order[1], theta)
    yaw = rotation3d(order[2], psi)
    return roll @ pitch @ yaw

start3 = time.time()
for i in range(1000):
    rotation(np.pi/3, np.pi/3, np.pi/3)
end3 = time.time()
print('rotation {}'.format(end3 - start3))

@numba.jit
def inv(M):
    return np.linalg.inv(M)

start4 = time.time()
for i in range(1000):
    inv(np.array([[1.,2.,3.],[4.,5.,6.],[7.,8.,9.]]))
end4 = time.time()
print('inv {}'.format(end4 - start4))