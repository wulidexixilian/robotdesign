import numpy as np

def rescale(tau_ref, tau_max, qd_ref, Rv):
    n_axes = len(Rv)
    c_candidate = np.zeros(n_axes)
    for idx in range(n_axes):
        root = np.roots(
            np.array([tau_max[idx], Rv[idx] * qd_ref[idx], -tau_ref[idx]])
        )
        # if np.size(np.where(root>0.1))>0:
        #     c_candidate[idx] = max(root)
        # else:
        #     c_candidate[idx] = 1
        c_candidate[idx] = max(root)
        c = max(c_candidate)
    return c


def resample(c, q_ref, qd_ref, qdd_ref, ts):
    m, n = np.shape(q_ref)
    t_rescaled = np.cumsum(ts * c * np.ones(n))
    t_resampled = np.linspace(t_rescaled[0], t_rescaled[-1], int(t_rescaled[-1] / ts))
    q_resampled_tuple = ()
    qd_resampled_tuple = ()
    qdd_resampled_tuple = ()
    for idx in range(m):
        q_resampled = np.interp(t_resampled, t_rescaled, q_ref[idx, :])
        qd_resampled = np.interp(t_resampled, t_rescaled, qd_ref[idx, :] / c)
        qdd_resampled = np.interp(t_resampled, t_rescaled, qdd_ref[idx, :] / c**2)
        q_resampled_tuple = q_resampled_tuple + (q_resampled, )
        qd_resampled_tuple = qd_resampled_tuple + (qd_resampled,)
        qdd_resampled_tuple = qdd_resampled_tuple + (qdd_resampled,)
    q_resampled = np.vstack(q_resampled_tuple)
    qd_resampled = np.vstack(qd_resampled_tuple)
    qdd_resampled = np.vstack(qdd_resampled_tuple)
    return q_resampled, qd_resampled, qdd_resampled

