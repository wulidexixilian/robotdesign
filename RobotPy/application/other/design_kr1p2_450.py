# -*- coding: utf-8 -*-
"""
test
Created on Fri Mar 24 14:17:04 2017

@author: pei.sun
"""
import matplotlib.pyplot as plt
import numpy as np
from model import m_simulation as sim
from rRobotDB.not_used import pt_micro_1p2kg450 as cfg

plt.close("all")
np.set_printoptions(suppress=True)
np.set_printoptions(precision=4)
#%%
# setup an identical robot for dauer3 simulation
s_dauer3 = sim.Simulation()
s_dauer3.set_gravity(9.8 * np.array([0,0,-1]))
load_dauer3 = {"cm":np.array([0, 40, 70])*1e-3, "m": 1.2,
               "iT":np.array([1500, 1500, 1500, 0, 0, 0])*1e-6}
s_dauer3.buildRobot(cfg.structurePara,
                    cfg.massPara,
                    cfg.motorPara,
                    cfg.frictionPara,
                    cfg.gearPara,
                    load_dauer3)
# static
q = [0, 0, 0, 0, 0, 0]
q_dot_max = np.array([315, 350, 450, 600, 600, 700]) / 180 * np.pi
q_dot = -q_dot_max * 0.01
q_ddot = [0, 0, 0, 0, 0, 0]
s_dauer3.runStep(q, q_dot)
ax = s_dauer3.snapShot()
s_dauer3.showMotorGearCM(ax)
# brake analysis
# TBD

# ***********************************************************************************
# Dauer3 trajectory inverse dynamic
percentage = 100 # amount of data to be simulated, 100% for all
# trace_file = 'C:/Users/pei.sun/Desktop/mada/trace_example/Dauer_KR6_KR10_R900_2/' \
#              'Dauer_KR6_Tracefile/dauer3_kr6_NextGenDrive'
# trace_file = 'C:/Users/pei.sun/Desktop/mada/trace_example/KRCIPO_Vel_Pos_Dauer3_KR6/dauer3_kr6_KRCIpo'
trace_file = 'resource/trace/KR1_IPO/Test1_KRCIpo'
# load q(t) from trace file
# s_dauer3.loadQ(trace_file, percentage, [100, 160, 3636/25, 100, 2222/23, 101], 1)
s_dauer3.loadQ(trace_file, percentage, np.ones(6), 0.8, trace_type='ipo')
# inverse dynamic simulation
s_dauer3.simFromQ()
# animation
# s_dauer3.animate()

# result
rs_dauer3 = s_dauer3.get_result()
motor_velocity_max = [q_dot_max[i] * s_dauer3.robot.drives[i].ratio / np.pi / 2 * 60 for i in range(6)]
print('Achievable max motor velocity:\n', motor_velocity_max)
# stall torque analysis
stall_tau = rs_dauer3.get_stall_torque(q_dot_max, load_dauer3)
print('Zero position tcp: {}mm'.format(stall_tau['tcp']))
tau_stall_motor = stall_tau['tau_motor']
print('Motor stall torque: {}mm'.format(tau_stall_motor))
print('Gear stall torque: {}mm'.format(stall_tau['tau_joint']))
# rs_dauer3.show_performance()
rs_dauer3.drive_characteristic(30, 15, tau_stall_motor)
# get gearbox side
rs_dauer3.joint_characteristic()
t_av_dauer3 = rs_dauer3.gear_average_tau()
# # load diagram
# print('Gearbox average torque: {}'.format(t_av_dauer3))
# rs_dauer3.load_diagram_show(q_dot_max * 0.01, [0.8, 1, 1.2])

# # brake analysis
# q0 = np.zeros(6)
# qd0 = np.array([315, 350, 350, 500, 500, 700]) / 180 * np.pi
# brake_torque = np.array([0.35, 0.35, 0.17, 0.06, 0.06, 0.04])
# t_end = 0.5
# N = 2500
# sol = s_dauer3.solve_brake(q0, qd0, brake_torque, t_end, N)
# t = np.linspace(0, t_end, N)
#
# plt.figure()
# p1 = [plt.subplot(321+i) for i in range(6)]
# for idx, subfig in enumerate(p1):
#     subfig.plot(t, sol[:, idx], 'b-')
#     subfig.grid(True)
# plt.tight_layout()
# plt.show()
# plt.figure()
#
# p2 = [plt.subplot(321+i) for i in range(6)]
# for idx, subfig in enumerate(p2):
#     subfig.plot(t, sol[:, 6 + idx], 'r-')
#     subfig.grid(True)
# plt.tight_layout()
# plt.show()
figTorqueTrace = plt.figure()
pm = [plt.subplot(321+i) for i in range(6)]
for i in range(6):
   moment_trace = s_dauer3.readTrace(trace_file,
                                     'DriveMotorTorq_CmdIpo{}'.format(i+1),
                                     percentage)[0]
   pm[i].plot(s_dauer3.t_ser[0:len(moment_trace)],
              -moment_trace, 'r-', label="trace T")
   pm[i].plot(s_dauer3.t_ser, s_dauer3.driveTorque_ser[:,i],
              'b-', label="sim T")
   # pm[i].plot(s_dauer3.t_ser,
   #            s_dauer3.friction_ser[:,i]/s_dauer3.robot.drives[i].ratio,
   #            'g--', label="fr")
   # pm[i].plot(s_dauer3.t_ser,
   #            s_dauer3.drivePure_ser[:,i]/s_dauer3.robot.drives[i].ratio,
   #            'y--', label="sim pure T")
   pm[i].grid(True)
   pm[i].legend()
plt.show()




