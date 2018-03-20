import numpy as np

def rescale(tau_ref, tau_max, qd_ref, Rv):
    n_axes = len(Rv)
    c_candidate = np.zeros(n_axes)
    for idx in range(n_axes):
        root = np.roots(np.array([tau_max[idx],
                                  Rv[idx] * qd_ref[idx],
                                  -tau_ref[idx]]))
        if np.size(np.where(root>0.3))>0:
            c_candidate[idx] = root[np.where(root>0.1)]
            c = max(c_candidate)
        else:
            c = 1
    return c


def resample(c_series, q_ref_series, ts_in, ts_out):
    m, n = np.shape(q_ref_series)
    t_rescaled = np.cumsum(ts_in * c_series * np.ones(n))
    t_resampled = np.linspace(t_rescaled[0], t_rescaled[-1], int(t_rescaled[-1] / ts_out))
    q_resampled_tuple = ()
    qd_resampled_tuple = ()
    qdd_resampled_tuple = ()
    for idx in range(m):
        q_axis_resampled = np.interp(t_resampled, t_rescaled, q_ref_series[idx, :])
        qd_axis_resampled = np.gradient(q_axis_resampled, ts_out)
        qdd_axis_resampled = np.gradient(qd_axis_resampled, ts_out)
        q_resampled_tuple = q_resampled_tuple + (q_axis_resampled, )
        qd_resampled_tuple = qd_resampled_tuple + (qd_axis_resampled,)
        qdd_resampled_tuple = qdd_resampled_tuple + (qdd_axis_resampled,)
    q_resampled = np.vstack(q_resampled_tuple)
    qd_resampled = np.vstack(qd_resampled_tuple)
    qdd_resampled = np.vstack(qdd_resampled_tuple)
    return q_resampled, qd_resampled, qdd_resampled

