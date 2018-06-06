import matplotlib.pyplot as plt
import numpy as np

from model import m_analysis
from utility import pp
import matlab.engine


class PathPlan:
    def __init__(self):
        pass


def ptp(start, end, speed_setting, speed_limit, ts):
    meng = matlab.engine.start_matlab()
    q_start = matlab.double(np.array([start]).T.tolist())
    q_end = matlab.double(np.array([end]).T.tolist())
    qd_limit = matlab.double(np.array([speed_limit]).T.tolist())
    q, qd, qdd = meng.PTP2(q_start, q_end, speed_setting, qd_limit, ts,
                           nargout=3)
    pos = np.array(q._data.tolist()).reshape(q.size[1], q.size[0]).transpose()
    vel = np.array(qd._data.tolist()).reshape(qd.size[1], qd.size[0]).transpose()
    acc = np.array(qdd._data.tolist()).reshape(qdd.size[1], qdd.size[0]).transpose()
    meng.quit()
    return pos, vel, acc


def planner(pos, vel, acc, ts, robot):
    Rv = np.array([drive.Rv for drive in robot.drives])
    c_ser = []
    for idx in range(np.shape(pos)[1]):
        q = pos[:, idx]
        qd = vel[:, idx]
        qdd = acc[:, idx]
        robot.k(q)
        robot.ne(qd, qdd, np.array([0, 0, -9.8]))
        tau = robot.get_free_axis_potential()
        rs = m_analysis.StaticAnalysis(robot)
        [ll, ul] = rs.max_joint_tau_output(q, qd)
        tau_limit = np.where(tau < 0, ll, ul)
        c = pp.rescale(tau, tau_limit, qd, Rv)
        c_ser.append(c)
    c_ser = np.array(c_ser)
    pos_new, vel_new, acc_new = pp.resample(c_ser, pos, vel, acc, ts)
    t_new = np.linspace(ts, np.shape(pos_new)[1] * ts, np.shape(pos_new)[1])

    # fig1, ax_arr1 = plt.subplots(3, 2)
    # fig1.suptitle('trajectory planning : position [rad/s - sec]')
    # for idx in range(np.shape(pos)[0]):
    #     ax = ax_arr1[int(idx / 2), (idx % 2)]
    #     ax.plot(t_new, pos_new[idx, :], 'r-')
    #     t_old = np.linspace(ts, np.shape(vel)[1] * ts, np.shape(pos)[1])
    #     ax.plot(t_old, pos[idx, :], 'b--')
    #     ax.grid()
    #
    # fig2, ax_arr2 = plt.subplots(3, 2)
    # fig2.suptitle('trajectory planning : vel [rad - sec]')
    # for idx in range(np.shape(vel)[0]):
    #     ax = ax_arr2[int(idx / 2), (idx % 2)]
    #     ax.plot(t_new, vel_new[idx, :], 'r-')
    #     t_old = np.linspace(ts, np.shape(vel)[1] * ts, np.shape(vel)[1])
    #     ax.plot(t_old, vel[idx, :], 'b--')
    #     ax.grid()
    #
    # fig3, ax_arr3 = plt.subplots(3, 2)
    # fig3.suptitle('trajectory planning : acc [rad - sec]')
    # for idx in range(np.shape(acc)[0]):
    #     ax = ax_arr3[int(idx / 2), (idx % 2)]
    #     ax.plot(t_new, acc_new[idx, :], 'r-')
    #     t_old = np.linspace(ts, np.shape(acc)[1] * ts, np.shape(acc)[1])
    #     ax.plot(t_old, acc[idx, :], 'b--')
    #     ax.grid()
    #
    # plt.show()

    return t_new, pos_new, vel_new, acc_new