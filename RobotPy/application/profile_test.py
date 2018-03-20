import numpy as np
import matplotlib.pyplot as plt
from RobotPy import rSimulation as sim
from RobotPy.rRobotLib import pt_micro_1kg380 as cfg
import time
from RobotPy.utility import fwd_dyn


def foo():
    plt.close("all")
    np.set_printoptions(suppress=True)
    np.set_printoptions(precision=4)

    # setup robot
    s = sim.Simulation()
    s.set_gravity(9.8 * np.array([0, 0, -1]))
    load_dauer3 = {"cm":np.array([15, 15, 30])*1e-3, "m": 1,
                   "iT":np.array([1500, 1500, 1500, 0, 0, 0])*1e-6}
    s.buildRobot(cfg.structurePara,
                 cfg.massPara,
                 cfg.motorPara,
                 cfg.frictionPara,
                 cfg.gearPara,
                 load_dauer3)

    # static
    q = [0, 0, 0, 0, 0, 0]
    q_dot_max = np.array([315, 400, 400, 600, 600, 600]) / 180 * np.pi
    q_dot = q_dot_max * 0.01
    q_ddot = [0, 0, 0, 0, 0, 0]
    # s.runStep(q, q_dot)
    # ax = s.snapShot()
    # s.showMotorGearCM(ax)

    # load trajectory
    percentage = 30 # amount of data to be simulated, 100% for all
    trace_file = 'C:/Users/pei.sun/Desktop/mada/trace_example/Dauer_KR6_KR10_R900_2/' \
                 'Dauer_KR6_Tracefile/dauer3_kr6_NextGenDrive'
    # load q(t) from trace file
    s.loadQ(trace_file, percentage, [100, 160, 3636/25, 100, 2222/23, 101], 1)
    ref = np.vstack((s.t_ser.T, np.vstack((s.q_cmd_ser.T, s.q_dot_cmd_ser.T))))
    # fwd_dyn.dyn(ref[1:, 0].T, 0, s.robot, np.array([0, 0, -9.8]), fwd_dyn.control, ref)
    t = 0
    gravity = np.array([0, 0, -9.8])
    y = ref[1:, 0].T
    for i in range(100):
        n = s.robot.num_axes
        q = y[0:n]
        qd = y[n:]
        s.robot.k(q)
        M = s.robot.get_inertia_matrix()
        tau_cor_grav_fric = s.robot.ne(qd, np.zeros(n), gravity)
        tau_u = fwd_dyn.control(y, t, ref)
        qdd = fwd_dyn.get_acc(M, tau_u, tau_cor_grav_fric)