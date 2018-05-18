# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 17:02:06 2017
Mathematic utilities
@author: pei.sun
"""

import numpy as np
import numba

ar = np.array

def triangle(l1, l2, l3):
    """ solve triangle, 3 edges => 3 angles """
    a1 = np.arccos((l2**2 + l3**2 - l1**2)/(2*l2*l3))
    a2 = np.arccos((l1**2 + l3**2 - l2**2)/(2*l1*l3))
    a3 = np.arccos((l1**2 + l2**2 - l3**2)/(2*l1*l2))
    return [a1, a2, a3]


@numba.jit
def rotation_matrix_x(alpha):
    c = np.cos(alpha)
    s = np.sin(alpha)
    r = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    return r


@numba.jit
def rotation_matrix_y(alpha):
    c = np.cos(alpha)
    s = np.sin(alpha)
    r = np.array([[c, 0, s],[0, 1, 0],[-s, 0, c]])
    return r


@numba.jit
def rotation_matrix_z(alpha):
    c = np.cos(alpha)
    s = np.sin(alpha)
    r = np.array([[c, -s, 0],[s, c, 0],[0, 0, 1]])
    return r


def rotation3d(ax, alpha):
    """ rotation transformation matrix about ax:axis for alpha:angle """
    if ax is 'x':
        return rotation_matrix_x(alpha)
    if ax is 'y':
        return rotation_matrix_y(alpha)
    if ax is 'z':
        return rotation_matrix_z(alpha)
    # return results4axes[ax]


def rotation(phi, theta, psi, order="zyx"):
    """ roll/order[0] -> pitch/order[1] -> yaw/order[2] """
    # order = order.lower()
    roll = rotation3d(order[0], phi)
    pitch = rotation3d(order[1], theta)
    yaw = rotation3d(order[2], psi)
    return roll @ pitch @ yaw


def h(R, d):
    """ extent a rotation to homogenuous transformation"""
    return np.vstack((np.hstack((R, ar([ar(d)]).T)), ar([[0, 0, 0, 1]])))


def solveZYX(R):
    """ z - y - x """
    R = np.round(R,8)
    phi = np.arctan2(R[1,0], R[0,0])
    theta = np.arctan2(R[2,0], np.sqrt(1 - R[2,0]**2))
    psi = np.arctan2(R[2,1], R[2,2])
    for item in [phi, theta, psi]:
        if item > np.pi:
            item = -2*np.pi + item
        elif item < -np.pi:
            item = 2*np.pi + item
    return phi, theta, psi


def solveEuler(R):
    """ x - y - x """
    R = np.round(R,8)
    theta_a = np.arctan2(np.sqrt(1 - R[0,0]**2), R[0,0])
    phi_a = np.arctan2(R[1,0], -R[2,0])
    psi_a = np.arctan2(R[0,1], R[0,2])

    theta_b = -np.arctan2(np.sqrt(1 - R[0,0]**2), R[0,0])
    phi_b = np.arctan2(-R[1,0], R[2,0])
    psi_b = np.arctan2(-R[0,1], -R[0,2])

    # choose the smaller set
    if abs(phi_b)<=abs(phi_a) and abs(psi_b)<=abs(psi_a):
        theta = theta_b
        phi = phi_b
        psi = psi_b
    else:
        theta = theta_a
        phi = phi_a
        psi = psi_a
    return phi, theta, psi

def solveInterAngle(theta0, theta1):
    """
    find theta01 which gives
    R(theta01) @ R(theta0) @ coordinate_O = R(theta1) @ coordinate_O
    tbd
    """
#    R0 = rotation(*theta0)
#    R1 = rotation(*theta1)
#    R01 = R0.T @ R1
#    theta01 = solveZYX(R01)
#    print('theta01:',theta01)
#    print(R0)
#    print(R1)
#    print(R01)
#    return theta01
    pass


def crossProdMx(x):
    """find A(a) which gives a X b = A @ b"""
    x_hat = np.array([
                      [0, -x[2], x[1]],
                      [x[2], 0, -x[0]],
                      [-x[1], x[0], 0]
                     ])
    return x_hat


def twistCoordinate(omega, ref):
    """ xi_hat = [omega_hat, -omega X q; 0, 0]"""
    omega_hat = crossProdMx(omega)
    v = -np.cross(omega, ref)
    xi = np.hstack((v, omega))
    xi_hat_temp = np.hstack((omega_hat, ar([v]).T))
    xi_hat = np.vstack((xi_hat_temp, ar([[0,0,0,0]])))
    return xi, xi_hat


def adjointTransform(R, p):
    p_hat = crossProdMx(p)
    Ad_g = np.vstack((np.hstack((R, p_hat @ R)), np.hstack((np.zeros((3,3)), R))))
    return Ad_g


def mass_combine(m, m_new, cm, cm_new, iT, iT_new):
    """ combine 2 mass """
    m_all = m + m_new
    if m_all != 0:
        cm_all = (m * cm + m_new * cm_new) / m_all
    else:
        cm_all = cm
    d = ar([cm_new - cm_all])
    iT_all = iT + iT_new + m_new * (np.dot(d, d.T)[0, 0] * np.identity(3) - d.T @ d)
    return m_all, cm_all, iT_all


def tensor(*args):
    if len(args) == 6:
        s = np.array([[args[0], args[5], args[4]],
                      [args[5], args[1], args[3]],
                      [args[4], args[3], args[2]]])
    else:
        s = np.diag(args)
    return s


def tear_tensor(s):
    return np.array([s[0,0], s[1,1], s[2,2], s[0,1], s[1,2], s[0,2]])


@numba.jit(nopython=True)
def calc_friction(Rh, Rv, Rz, v, tau, h):
    """
    friction calculation
    :param Rh: Static friction
    :param Rv: dynamic friction coefficient
    :param Rz: torque related friction coefficient
    :param v: speed
    :param h: speed threshold
    :return: 
    """
    # f = Rh * np.sign(v) + Rv * v + (1 - Rz) * abs(tau) * np.sign(v)
    f = np.tanh(1.5*v/h) * Rh + Rv * v + (1 - Rz) * abs(tau) * np.sign(v)
    return f


def calcFriction_static(Rh, Rv, Rz, v, tau):
    """
    friction calculation for static load analysis
    :param Rh: Static friction
    :param Rv: dynamic friction coefficient
    :param Rz: torque related friction coefficient
    :param v: speed
    :param h: speed threshold
    :return: 
    """
    f = Rh * np.sign(v) + Rv * v + (1 - Rz) * abs(tau) * np.sign(v)
    # f = np.tanh(1.5*v/h) * Rh + Rv * v + (1 - Rz) * abs(tau) * np.sign(v)
    return f


@numba.jit(nopython=True)
def easy_friction(Rh, Rv, v, h=0.005):
    f = np.tanh(1.5 * v / h) * Rh + Rv * v
    return f


def curve_min(curve1, curve2):
    """
    combine two curves into a new one by pick the smaller value
    :param curve1: 2D array, first row for x, and second for y
    :param curve2: the other curve
    :return: new curve in a 2D array
    """
    len1 = np.shape(curve1)
    len2 = np.shape(curve2)
    if len2[1] > len1[1]:
        curve1, curve2 = curve2, curve1
    result = []
    for (x1, y1) in zip(curve1[0, :], curve2[1, :]):
        y2 = np.interp(x1, curve2[0, :], curve1[1, :], right=0)
        result.append(min(y1, y2))
    return result


@numba.jit(nopython=True)
def pure_cross(a, b):
    return np.array([-a[2] * b[1] + a[1] * b[2],
                    a[2] * b[0] - a[0] * b[2],
                    -a[1] * b[0] + a[0] * b[1]])


@numba.jit(nopython=True)
def fast_fwd_ne(z_gl, r_hc, r_ht,
                q_dot, q_ddot, omega_im1, alpha_im1, acc_e_im1):
    omega = omega_im1 + q_dot * z_gl
    alpha = alpha_im1 + z_gl * q_ddot + pure_cross(omega, z_gl) * q_dot
    acc = acc_e_im1 + pure_cross(alpha, - r_hc) +\
          pure_cross(omega, pure_cross(omega, -r_hc))
    acc_e = acc_e_im1 + pure_cross(alpha, -r_ht) + \
            pure_cross(omega, pure_cross(omega, - r_ht))
    return omega, alpha, acc, acc_e


@numba.jit(nopython=True)
def fast_bwd_ne(m, acc, r_hc, r_tc, iT_gl, omega, alpha, f_ip1, tau_ip1, gravity):
    f = f_ip1 + m * acc - m * gravity
    tau = tau_ip1 - pure_cross(r_hc, f) + pure_cross(r_tc, f_ip1) + \
          iT_gl @ alpha + pure_cross(omega, (iT_gl @ omega))
    return f, tau
