"""
test
Created on Fri Mar 24 14:17:04 2017

@author: pei.sun
"""
import numpy as np
import matplotlib.pyplot as plt
from model import rSimulation as sim
from rRobotDB import pt_micro450 as cfg
plt.close("all")
np.set_printoptions(suppress=True)
np.set_printoptions(precision=4)
# *** build robot ***
s = sim.Simulation()
s.set_gravity(9.8 * np.array([0, 0, -1]))
load_dauer3 = {
    "cm": np.array([35, 35, 75])*1e-3, "m": 1.5,
    "iT": np.array([1200, 1200, 1200, 0, 0, 0])*1e-6
}
s.buildRobot(
    cfg.structurePara,
    cfg.massPara,
    cfg.motorPara,
    cfg.frictionPara,
    cfg.gearPara,
    load_dauer3
)
# *** kinematics ***
q = [0, 0, 0, 0, 0, 0]
q_dot_max = np.array([300, 300, 450, 500, 500, 700]) / 180 * np.pi
q_dot = q_dot_max * 0.01
q_ddot = [0, 0, 0, 0, 0, 0]
s.runStep(q, q_dot)
ax = s.snapShot()
s.showMotorGearCM(ax)
# *** inverse dynamic ***
percentage = 100  # amount of data to be simulated, 100% for all
trace_file = 'resource/trace/KR1_IPO/Test1_KRCIpo'
# load q(t) from trace file
s.loadQ(trace_file, percentage)
# inverse dynamic simulation
s.simFromQ()
# animation
s.animate()
# *** result ***
rs = s.get_result()
# stall torque
motor_velocity_max = [q_dot_max[i] * s.robot.drives[i].ratio / np.pi / 2 * 60
                      for i in range(6)]
print('Achievable max motor velocity:\n', np.array(motor_velocity_max))
stall_tau = rs.get_stall_torque(q_dot_max, load_dauer3)
print('Zero position tcp: {}mm'.format(stall_tau['tcp']))
tau_stall_motor = stall_tau['tau_motor']
motor_percent = stall_tau['motor_percent']
print('Motor stall torque:\n {}Nm\n {}%'.format(tau_stall_motor, motor_percent))
print('Gear stall torque: {}Nm'.format(stall_tau['tau_joint']))
# simulation trajectory
rs.show_performance()
# motor characteristic
rs.drive_characteristic(30, 15, tau_stall_motor)
# gearbox characteristic
rs.joint_characteristic(cfg.gearPara)
plt.show()
