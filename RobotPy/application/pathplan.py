import matplotlib.pyplot as plt
import numpy as np
from model import rSystem
from model import rSimulation as sim
from rRobotDB import pt_micro_1p2kg450 as cfg

plt.close("all")
np.set_printoptions(suppress=True)
np.set_printoptions(precision=4)
#%%
# setup an identical robot for dauer3 simulation
s = sim.Simulation()
s.set_gravity(9.8 * np.array([0,0,-1]))
load_dauer3 = {"cm":np.array([0, 40, 70])*1e-3, "m": 1.2,
               "iT":np.array([1500, 1500, 1500, 0, 0, 0])*1e-6}
s.buildRobot(cfg.structurePara,
                    cfg.massPara,
                    cfg.motorPara,
                    cfg.frictionPara,
                    cfg.gearPara,
                    load_dauer3)

q_start = np.array([0, -np.pi/2, np.pi/2, 0, 0, 0])
q_end = np.array([np.pi/3, np.pi/3, -np.pi/3, np.pi/3, -np.pi/3, np.pi/3]) + q_start
qd_limit = np.array([350, 350, 350, 500, 500, 700]) * np.pi / 180
qd_override = 100.0
ts_in = 1e-4
ts_out = 2e-4
pos, vel, acc = rSystem.ptp(q_start, q_end, qd_override, qd_limit, ts_in)
t_new, pos_new, vel_new, acc_new = rSystem.planner(pos, vel, acc, ts_in, ts_out, s.robot)

s.simFromQ(pos_new.T, vel_new.T, acc_new.T, t_new, ts_out, ratio_mask=np.ones(6))

# result
rs = s.get_result()
rs.drive_characteristic(30, 15)
rs.joint_characteristic()

plt.show()