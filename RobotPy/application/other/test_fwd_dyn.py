import numpy as np
import matplotlib.pyplot as plt
from RobotPy import rSimulation as sim
from RobotPy.rRobotLib import pt_micro_1kg380 as cfg
import time

plt.close("all")
np.set_printoptions(suppress=True)
np.set_printoptions(precision=4)

# setup robot
s = sim.Simulation()
s.set_gravity(9.8 * np.array([0, 0, -1]))
load_dauer3 = {"cm":np.array([15, 15, 30])*1e-3, "m": 1,
               "iT":np.array([1500, 1500, 1500, 0, 0, 0])*1e-6}
s.build_robot(cfg.structurePara,
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
percentage = 10 # amount of data to be simulated, 100% for all
trace_file = 'C:/Users/pei.sun/Desktop/mada/trace_example/Dauer_KR6_KR10_R900_2/' \
             'Dauer_KR6_Tracefile/dauer3_kr6_NextGenDrive'
# load q(t) from trace file
s.load_trajectory(trace_file, percentage, [100, 160, 3636 / 25, 100, 2222 / 23, 101], 1)
ref = np.vstack((s.t_ser.T, np.vstack((s.q_cmd_ser.T, s.q_dot_cmd_ser.T))))
start_time = time.time()
sol = s.solve_fwd_dynamic(ref)
end_time = time.time()
print('solving time: {}s'.format(end_time - start_time))

plt.figure()
p = [plt.subplot(321+i) for i in range(6)]
for idx, subfig in enumerate(p):
    subfig.plot(ref[0, :], ref[idx+1, :], 'b-')
    subfig.plot(ref[0, :], sol[:, idx], 'r--')