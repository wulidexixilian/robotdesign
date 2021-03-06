import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from model import m_simulation_scara as sim
from rRobotDB import pt_scara_LS3401S as cfg

ar = np.array

plt.close("all")
np.set_printoptions(suppress=True)
np.set_printoptions(precision=4)
# *** build robot ***
s = sim.SimulationScara()
s.set_gravity(9.8 * np.array([0, 0, -1]))
load = {
    "cm": np.array([0, 0, 0])*1e-3, "m": 1,
    "iT": np.array([1200, 1200, 1200, 0, 0, 0])*1e-6
}
s.build_robot(
    cfg.structure_para,
    cfg.mass_para,
    cfg.motor_para,
    cfg.friction_para,
    cfg.gear_para,
    load
)
q = [0, 0, 0, 0]
q_dot_max = np.array([300, 300, 450, 550]) / 180 * np.pi
q_dot = q_dot_max * 0.01
q_ddot = np.array([0, 0, 0, 0])
rs = s.get_result()
stall_tau = rs.get_stall_torque(q_dot_max, load)
s.load_gear_characteristic(cfg.gear_para, stall_tau['tau_joint'])
# *** kinematics ***
s.run_one_step(q, q_dot, q_ddot)
ax = s.snapshot()
s.show_cm(ax)

print('Current tcp: {}mm'.format(s.robot.joints[-1].origin1))
print('Zero position tcp: {}mm'.format(stall_tau['tcp']))
tau_stall_motor = stall_tau['tau_motor']
motor_percent = stall_tau['motor_percent']
print('Motor stall torque:\n {}Nm\n {}%'.format(tau_stall_motor, motor_percent))
print('Gear stall torque: {}Nm'.format(stall_tau['tau_joint']))
trajectory_def = {
    'v_max': 2000,
    'T': 0.2,
    'N': 1000,
    'offset': ar([-150, -220, 15]),
    'rotation': ar([np.pi/2, 0, 0]),
    'orientation': ar([0, 0, 0]),
    'type': 'adept'
}
s.generate_trajectory(trajectory_def)
s.sim_inv_dynamic()
s.animate()
rs = s.get_result()
rs.show_performance()
rs.drive_characteristic(30, 15, tau_stall_motor)
rs.joint_characteristic(cfg.gear_para, draw_lifetime=False)
plt.show(block=False)


