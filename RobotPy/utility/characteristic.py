import numpy as np


def klobps(tau_rated, limit_factor, max_speed, tau_stall):
    max_tau = tau_rated * limit_factor

    def get_klobps_tau(omega):
        omega = np.abs(omega)
        if omega > max_speed:
            tau = 0
        else:
            tau = (1 - np.arcsin(omega/max_speed) / (np.pi/2)) *\
                  (max_tau - tau_stall) + tau_stall
        return tau

    return get_klobps_tau
