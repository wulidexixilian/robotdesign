# -*- coding: utf-8 -*-
"""
test
Created on Fri Mar 24 14:17:04 2017

@author: pei.sun
"""
import numpy as np
import matplotlib.pyplot as plt
from RobotPy import rSimulation as sim
from RobotPy.rRobotLib import rConfig_kr6_700 as cfg
# from RobotPy.rRobotDB import rConfig_kr6_900_exp as cfg
# from RobotPy.rRobotDB import rConfig_kr6_900_old as cfg
#from RobotPy.rRobotDB import rConfig_1100 as cfg
np.set_printoptions(suppress=True)
np.set_printoptions(precision=4)

gravity = 9.8 * np.array([0,0,-1])
##%%
s = sim.Simulation()
s.buildRobot(cfg.structurePara,
             cfg.massPara,
             cfg.motorPara,
             cfg.frictionPara,
             cfg.gearPara)
##%%
q = [0.5792, 0.6252, 0.6909, 0.3623, 0.275, 0.31]
q_dot_max = np.array([270, 225, 333, 450, 450, 600]) / 180 * np.pi
q_dot = -q_dot_max * 0.0
q_ddot = [0, 0, 0, 0, 0, 0]
s.runStep(q, q_dot)
ax = s.snapShot()
s.showMotorGearCM(ax)

print("tcp:\n", s.robot.joints[-1].origin1)
mTorques = np.array([item.driveTau for item in s.robot.drives])
print('motor tau:\n', mTorques)
eTorques = np.array([item.effectiveTau for item in s.robot.drives])
print('tau:\n', eTorques)
##%%
# static force analysis
# force = np.array([0, 0, 6*9.8, 0, 0, 0])
# torque_static = s.robot.force2tau_static(force)
# print('static torque:', torque_static)
# force_again = s.robot.tau2force_static(torque_static)
# print('static force:', force_again)

plt.show()