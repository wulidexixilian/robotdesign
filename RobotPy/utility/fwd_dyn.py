import numpy as np
from numba import jit
from model.m_math import easy_friction


def dyn(y, t, robot, gravity, torque_func, Rh, Rv, ref,
        control_parameter, friction_threshold):
    """
    calculate acceleration in the form of forward dynamic acc = f(q, qd, tau)
    :param y: state [q;qd]
    :param t: current time
    :param gravity: [0, 0, -9.8]
    :param torque_func: function to generate drive torque
    :param ref: target trajectory
    :return: qdd: joint acc
    """
    n = robot.num_axes
    q = y[0:n]
    qd = y[n:]
    robot.k(q)
    M = robot.get_inertia_matrix()
    # coriolis and gravity torque
    # T = M * qdd_0 + B * qd + K * q
    # calculate T by NE
    tau_cor_grav = robot.ne(qd, np.zeros(n), gravity)
    # calculate qdd based on M*qdd + B*qd + K*q = T
    # qdd = inv(M) * (T - T_coriolis_gravity)
    tau_u = torque_func(y, t, ref, control_parameter, friction_threshold)
    tau_friction = easy_friction(Rh, Rv, qd, friction_threshold)
    # qdd = np.linalg.inv(M) @ (tau_u - tau_cor_grav_fric)
    qdd = get_acc(M, tau_u, tau_cor_grav + tau_friction)
    return np.hstack((qd, qdd))


def control(x, t, ref, control_para, para):
    r = [np.interp(t, ref[0, :], ref[idx+1, :]) for idx in range(np.shape(ref)[0]-1)]
    r = np.array(r)
    kp, kd = control_para
    # kp = [1500, 1250, 1250, 750, 500, 400]
    # kd = [1, 1, 0.5, 0.2, 0.1, 0.1]
    kpd = np.hstack((np.diag(kp), np.diag(kd)))
    u = kpd @ (r - x)
    return u


def brake(x, t, ref, tau_brake, threshold):
    v = x[6:]
    u = easy_friction(tau_brake, np.zeros(6), v, threshold)
    # print('t:{}, control: {}'.format(t, u))
    return u


@jit(nopython=True)
def get_acc(M, tau_u, tau_rest):
    acc = np.linalg.inv(M) @ (tau_u - tau_rest)
    return acc