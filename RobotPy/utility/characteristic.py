import numpy as np


def klobps(acc_tau, tau_factor, max_speed):
    max_tau = acc_tau * tau_factor

    def get_klobps_tau(omega):
        omega = np.abs(omega)
        if omega > max_speed:
            tau = 0
        else:
            tau = (1 - np.arcsin(omega/max_speed) / (np.pi/2)) * max_tau
        return tau

    return get_klobps_tau
