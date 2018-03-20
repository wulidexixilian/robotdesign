# -*- coding: utf-8 -*-
"""
test
Created on Fri Mar 24 14:17:04 2017

@author: pei.sun
"""
import numpy as np
import matplotlib.pyplot as plt
from RobotPy import rSimulation as sim
from RobotPy.rRobotLib import pt_micro_1kg380 as cfg
plt.close("all")
np.set_printoptions(suppress=True)
np.set_printoptions(precision=4)
#%%
s_adept = sim.Simulation()
s_adept.set_gravity(9.8 * np.array([0,0,-1]))
load_adept = {"cm":np.array([0, 0, 10])*1e-3, "m":0.32,
              "iT":np.array([1500, 1500, 1500, 0, 0, 0])*1e-6}
s_adept.buildRobot(cfg.structurePara,
                   cfg.massPara,
                   cfg.motorPara,
                   cfg.frictionPara,
                   cfg.gearPara,
                   load_adept)

# setup an identical robot for dauer3 simulation
s_dauer3 = sim.Simulation()
s_dauer3.set_gravity(9.8 * np.array([0,0,-1]))
load_dauer3 = {"cm":np.array([15, 15, 30])*1e-3, "m": 1,
               "iT":np.array([1500, 1500, 1500, 0, 0, 0])*1e-6}
s_dauer3.buildRobot(cfg.structurePara,
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
s_dauer3.runStep(q, q_dot)
ax = s_dauer3.snapShot()
s_dauer3.showMotorGearCM(ax)

print('static analysis')
print("tcp:\n", s_dauer3.robot.joints[-1].origin1)
mTorques = np.array([item.driveTau for item in s_dauer3.robot.drives])
print('motor tau:\n', mTorques)
eTorques = np.array([item.effectiveTau for item in s_dauer3.robot.drives])
print('tau:\n', eTorques)
motor_velocity_max = [q_dot_max[i] * s_dauer3.robot.drives[i].ratio / np.pi / 2 * 60 for i in range(6)]
print('motor velocity:\n', motor_velocity_max)
max_power = [q_dot_max[i] * s_dauer3.robot.drives[i].ratio * mTorques[i] * 1.2 for i in range(6)]
print('max power:\n', max_power)

# brake analysis
print('Worst case kinetic energy (kJ):')
s_dauer3.robot.k(np.array([0, 0, 0, 0, 0, 0]))
for idx in range(6):
    E_k = s_dauer3.robot.get_kinetic(idx+1, q_dot_max)
    print('A{}: {}'.format(idx+1, E_k/1000))

# ***********************************************************************************
# adept trajectory inverse dynamic
percentage = 100 # amount of data to be simulated, 100% for all
# Adept Trajectory generating
trajectoryDef = {'type': 'adept', 'v_max': 1250, 'T': 0.35, 'N': 3000,
                 'offset': [-165, -265, 60], 'rotation': [np.pi/2, 0, 0],
                 'orientation': [0, 2*np.pi/5, 0]}

s_adept.generate_trajectory(trajectoryDef)
# inverse dynamic simulation for Adept
s_adept.simFromQ()
# animation
# s_adept.animate()

# Dauer3 trajectory inverse dynamic
percentage = 100 # amount of data to be simulated, 100% for all
trace_file = 'C:/Users/pei.sun/Desktop/mada/trace_example/Dauer_KR6_KR10_R900_2/' \
             'Dauer_KR6_Tracefile/dauer3_kr6_NextGenDrive'
# load q(t) from trace file
s_dauer3.loadQ(trace_file, percentage, [100, 160, 3636/25, 100, 2222/23, 101], 1)
# inverse dynamic simulation
s_dauer3.simFromQ()
# animation
# s_dauer3.animate()

# result
rs_adept = s_adept.get_result()
# rs_adept.show_performance()
rs_dauer3 = s_dauer3.get_result()
# rs_dauer3.show_performance()
rs_adept.drive_characteristic(30, 15)
rs_dauer3.drive_characteristic(30, 15)
# get gearbox side
rs_adept.joint_characteristic()
rs_dauer3.joint_characteristic()
t_av_adept = rs_adept.gear_average_tau()
t_av_dauer3 = rs_dauer3.gear_average_tau()
print('Gearbox average torque, maximum over two trajectories: ')
print(np.maximum(t_av_adept, t_av_dauer3))

rs_adept.load_diagram_data(q_dot_max * 0.01, 1)