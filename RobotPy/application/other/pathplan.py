import matplotlib.pyplot as plt
import numpy as np
from model import m_system
from model import m_simulation as sim
from rRobotDB import pt_micro450 as cfg

plt.close("all")
np.set_printoptions(suppress=True)
np.set_printoptions(precision=4)
#%%
# setup an identical robot for dauer3 simulation
s = sim.Simulation()
s.set_gravity(9.8 * np.array([0,0,-1]))
load_dauer3 = {"cm":np.array([0, 40, 70])*1e-3, "m": 1.2,
               "iT":np.array([1500, 1500, 1500, 0, 0, 0])*1e-6}
s.build_robot(
    cfg.structurePara,
    cfg.massPara,
    cfg.motorPara,
    cfg.frictionPara,
    cfg.gearPara,
    load_dauer3
)
q_dot_max = np.array([350, 350, 350, 500, 500, 700]) * np.pi / 180
rs = s.get_result()
stall_tau = rs.get_stall_torque(q_dot_max, load_dauer3)
s.load_gear_characteristic(cfg.gearPara, stall_tau['tau_joint'])

q_start = np.array([0, -np.pi/2, np.pi/2, 0, 0, 0])
q_end = np.array([np.pi/3, np.pi/3, -np.pi/3, np.pi/3, -np.pi/3, np.pi/3]) + q_start
qd_limit = np.array([350, 350, 350, 500, 500, 700]) * np.pi / 180
qd_override = 50.0
ts = 1e-4
pos, vel, acc = m_system.ptp(q_start, q_end, qd_override, qd_limit, ts)
t_new, pos_new, vel_new, acc_new = m_system.planner(pos, vel, acc, ts, s.robot)
t = np.linspace(0, len(pos[0, :]) * ts, len(pos[0, :]))
plt.figure()
plt.subplot(311)
plt.plot(t, pos[1, :], 'b-')
plt.plot(t_new, pos_new[1, :], 'r-')
plt.subplot(312)
plt.plot(t, vel[1, :], 'b-')
plt.plot(t_new, vel_new[1, :], 'r-')
plt.subplot(313)
plt.plot(t, acc[1, :], 'b-')
plt.plot(t_new, acc_new[1, :], 'r-')
# s.sim_inv_dynamic(pos_new.T, vel_new.T, acc_new.T, t_new, ts, ratio_mask=np.ones(6))
#
# # result
# rs = s.get_result()
# rs.drive_characteristic(30, 15)
# rs.joint_characteristic()

plt.show()