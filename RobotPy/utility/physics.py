import numpy as np
from RobotPy.rMath import curve_min


def calcFriction(Rh, Rv, Rz, v, tau, h):
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


def massCombine(m, m_new, cm, cm_new, iT, iT_new):
    """ combine 2 mass """
    m_all = m + m_new
    if m_all != 0:
        cm_all = (m * cm + m_new * cm_new) / m_all
    else:
        cm_all = cm
    d = np.array([cm_new - cm_all])
    iT_all = iT + iT_new + m_new * (np.linalg.norm(d)*np.identity(3) - d.T @ d)
    return m_all,cm_all,iT_all
