# -*- coding: utf-8 -*-
"""
test
Created on Fri Mar 24 14:17:04 2017

@author: pei.sun
"""
import numpy as np
import matplotlib.pyplot as plt
from RobotPy import rSimulation as sim
from RobotPy.rRobotLib import rConfig_kr6_900 as cfg

np.set_printoptions(suppress=True)
np.set_printoptions(precision=4)
#%%
s = sim.Simulation()
s.set_gravity(9.8 * np.array([0,0,-1]))
s.buildRobot(cfg.structurePara,
             cfg.massPara,
             cfg.motorPara,
             cfg.frictionPara,
             cfg.gearPara)
#%%
percentage = 10 # amount of data to be simulated, 100% for all
# Trajectory generating
trajectoryDef = {'type': 'adept', 'v_max': 1200, 'T': 0.32, 'N': 2500,
                 'offset': [-165, -200, 110], 'rotation': [np.pi/2, 0, 0],
                 'orientation': [0, np.pi/3, 0]}
s.generate_trajectory(trajectoryDef)

# inverse dynamic simulation
s.simFromQ()
# animation
plt.close("all")
s.animate()
# get result
result = s.get_result()
result.show_performance()
# show drive characteristics and v-T diagram
characteristic = [drive.characteristic for drive in s.robot.drives]
result.drive_characteristic(40, 40, characteristic)
# 3D force and torque at joint for FEA
result.get_fea_input()
