import numpy as np
import matplotlib.pyplot as plt
from model import m_simulation as sim
from rRobotDB import pt_micro450 as cfg
# from utility.compare_with_OPC import compare

plt.close("all")
np.set_printoptions(suppress=True)
np.set_printoptions(precision=4)
# *** build robot ***
s = sim.Simulation()
s.set_gravity(9.8 * np.array([0, 0, -1]))
load_dauer3 = {
    "cm": np.array([35, 0, 70])*1e-3, "m": 1.5,
    "iT": np.array([1200, 1200, 1200, 0, 0, 0])*1e-6
}
s.build_robot(
    cfg.structure_para,
    cfg.mass_para,
    cfg.motor_para,
    cfg.friction_para,
    cfg.gear_para,
    load_dauer3
)
q = [0, 0, 0, 0, 0, 0]
q_dot_max = np.array([300, 300, 450, 550, 550, 700]) / 180 * np.pi
q_dot = q_dot_max * 0.01
q_ddot = np.array([0, 0, 0, 0, 0, 0])
rs = s.get_result()
stall_tau = rs.get_stall_torque(q_dot_max, load_dauer3)
s.load_gear_characteristic(cfg.gear_para, stall_tau['tau_joint'])
# *** kinematics ***
s.run_one_step(q, q_dot, q_ddot)
ax = s.snapshot()
s.show_cm(ax)
# *** inverse dynamic ***
percentage = 100  # amount of data to be simulated, 100% for all
trace_file = 'resource/trace/KR1_IPO/Test1_KRCIpo'
# *** load q(t) from trace file ***
s.load_trajectory(trace_file, percentage)
# *** inverse dynamic simulation ***
s.sim_inv_dynamic()
# *** animation ***
s.animate()
# *** result ***
rs = s.get_result()
motor_velocity_max = [
    q_dot_max[i] * s.robot.drives[i].ratio / np.pi / 2 * 60 for i in range(6)
]
print('Achievable max motor velocity:\n', np.array(motor_velocity_max))
print('Zero position tcp: {}mm'.format(stall_tau['tcp']))
tau_stall_motor = stall_tau['tau_motor']
motor_percent = stall_tau['motor_percent']
print('Motor stall torque:\n {}Nm\n {}%'.format(tau_stall_motor, motor_percent))
print('Gear stall torque: {}Nm'.format(stall_tau['tau_joint']))
# rs.show_performance()
rs.drive_characteristic(30, 15, tau_stall_motor)
rs.get_max_drive_tau()
rs.joint_characteristic(cfg.gear_para)
rs.get_max_joint_tau()
gear_av_tau_percent = rs.gear_average_tau() /\
    np.array([item['acc_tau'] for item in cfg.gear_para])
print('Gear average torque ratio: {}%'.format(gear_av_tau_percent * 100))
# compare(s, trace_file, percentage)
plt.show(block=False)
