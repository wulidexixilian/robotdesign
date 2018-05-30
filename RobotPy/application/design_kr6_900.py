import numpy as np
import matplotlib.pyplot as plt
from model import m_simulation as sim
from rRobotDB import agilus_kr6_900 as cfg
plt.close('all')
np.set_printoptions(suppress=True)
np.set_printoptions(precision=4)
# *** build robot ***
s = sim.Simulation()
s.set_gravity(9.8 * np.array([0,0,-1]))
load_rated = {
    "nest": "tcp",
    "cm": np.array([60, 0, 80]) * 1e-3, "m": 6,
    "iT": np.array([45000, 45000, 45000, 0, 0, 0]) * 1e-6
}
s.build_robot(
    cfg.structurePara,
    cfg.massPara,
    cfg.motorPara,
    cfg.frictionPara,
    cfg.gearPara,
    load_rated
)
q = [0, 0, 0, 0, 0, 0]
q_dot_max = np.array([360, 300, 462, 450, 470, 600]) / 180 * np.pi
q_dot = q_dot_max * 0.01
q_ddot = [0, 0, 0, 0, 0, 0]
rs = s.get_result()
stall_tau = rs.get_stall_torque(q_dot_max, load_rated)
s.load_gear_characteristic(cfg.gearPara, stall_tau['tau_joint'])
# *** kinematics ***
s.run_one_step(q, q_dot)
ax = s.snapshot()
s.show_cm(ax)
# *** inverse dynamic ***
percentage = 100 # amount of data to be simulated, 100% for all
# load q(t) from trace file
# trace_file = "resource/trace/KR6R900_NextGen/000xTemperatur_NextGenDrive"
# s.load_trajectory(trace_file, percentage,
#         ratioMask=[100, 120, 105.4, 80, 77.48, 81],
#         trace_type='NextGenDrive')
trace_file = "resource/trace/KR6R900_IPO/dauer3_kr6_KRCIpo"
s.load_trajectory(trace_file, percentage)
# inverse dynamic simulation
s.sim_inv_dynamic()
# *** result ***
rs = s.get_result()
# stall torque
motor_velocity_max = [q_dot_max[i] * s.robot.drives[i].ratio / np.pi / 2 * 60
                      for i in range(6)]
print('Achievable max motor velocity:\n', np.array(motor_velocity_max))
print('Zero position tcp: {}mm'.format(stall_tau['tcp']))
tau_stall_motor = stall_tau['tau_motor']
motor_percent = stall_tau['motor_percent']
print('Motor stall torque:\n {}Nm\n {}%'.format(tau_stall_motor, motor_percent))
print('Gear stall torque: {}Nm'.format(stall_tau['tau_joint']))
# simulation trajectory
# rs.show_performance()
# motor characteristic
rs.drive_characteristic(30, 15, tau_stall_motor)
rs.get_max_drive_tau()
# gearbox characteristic
rs.joint_characteristic(cfg.gearPara)
rs.get_max_joint_tau()
gear_av_tau_percent = rs.gear_average_tau() /\
    np.array([item['acc_tau'] for item in cfg.gearPara])
print('Gear average torque ratio: {}%'.format(gear_av_tau_percent * 100))
plt.show()
