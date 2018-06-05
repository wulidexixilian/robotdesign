import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from model import m_simulation_scara as sim
from rRobotDB import pt_scara as cfg

ar = np.array

plt.close("all")
np.set_printoptions(suppress=True)
np.set_printoptions(precision=4)
# *** build robot ***
s = sim.SimulationScara()
s.set_gravity(9.8 * np.array([0, 0, -1]))
load_dauer3 = {
    "cm": np.array([35, 0, 70])*1e-3, "m": 3,
    "iT": np.array([1200, 1200, 1200, 0, 0, 0])*1e-6
}
s.build_robot(
    cfg.structurePara,
    cfg.massPara,
    cfg.motorPara,
    cfg.frictionPara,
    cfg.gearPara,
    load_dauer3
)
q = [0, 0, 0, 0]
q_dot_max = np.array([300, 300, 450, 550]) / 180 * np.pi
q_dot = q_dot_max * 0.01
q_ddot = np.array([0, 0, 0, 0])
rs = s.get_result()
stall_tau = rs.get_stall_torque(q_dot_max, load_dauer3)
s.load_gear_characteristic(cfg.gearPara, stall_tau['tau_joint'])
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
    'v_max': 1200,
    'T': 0.35,
    'N': 1000,
    'offset': ar([-150, -200, 15]),
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
rs.joint_characteristic(cfg.gearPara)
plt.show(block=False)


