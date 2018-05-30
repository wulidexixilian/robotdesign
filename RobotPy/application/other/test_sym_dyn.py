# -*- coding: utf-8 -*-
"""
test
Created on Tue May 23 14:17:04 2017

@author: pei.sun
"""
#%%
import time
import numpy as np
import matplotlib.pyplot as plt
from RobotPy import rSimulation as sim
from RobotPy.rRobotLib import rConfig_kr6_900 as cfg
from RobotPy.symdy import SymDyRobot
from RobotPy.rMath import tear_tensor
#from RobotPy.rRobotDB import rConfig_kr6_900_exp as cfg
#from RobotPy.rRobotDB import rConfig_kr6_900_old as cfg
#from RobotPy.rRobotDB import rConfig_1100 as cfg
np.set_printoptions(suppress=True)
np.set_printoptions(precision=4)

gravity = 9.8 * np.array([0,0,-1])
##%%
s = sim.simulation()
s.build_robot(cfg.structurePara,
              cfg.massPara,
              cfg.motorPara,
              cfg.frictionPara,
              cfg.gearPara)
##%%
q = [0, -0, 0, 0, 0, 0]
q_dot_max = np.array([270, 225, 333, 450, 450, 600]) / 360 * 2 * np.pi
q_dot = -q_dot_max * 0
q_ddot = [0, 0, 0, 0, 0, 0]
s.run_one_step(q, q_dot)
# ax = s.snapshot()

percentage = 10 # amount of data to be simulated, 100% for all
fileFraction = "C:/Users/pei.sun/Desktop/trace_example/KR6R900/000xTemperatur_NextGenDrive"
s.load_trajectory(fileFraction, percentage, [1, 1, 1, 1, 1, 1])
s.sim_inv_dynamic()
##%%
dimension_lo = []
mass_centers_lo = []
masses = []
its = []
for body in s.robot.bodies[1:]:
    dimension_lo.append(body.dimension)
    mass_centers_lo.append(body.cm)
    masses.append(body.m)
    its.append(tear_tensor(body.iT))
fr = {'Rh': [], 'Rv': [], 'Threshold': s.robot.fr_thresholds}
for drive in s.robot.drives:
    fr['Rh'].append(drive.Rh)
    fr['Rv'].append(drive.Rv)

sdr = SymDyRobot(dimension_lo, fr, mass_centers_lo, masses, its, abs(s.gravity),
                 if_simplify=True)
sdr.generate_equation()

t_end = 1
ts = 0.01
tr = s.Ts
r = np.concatenate((s.q_cmd_ser.T, s.q_dot_cmd_ser.T),0)
x0 = r[:,0]
# r = np.zeros([6, int(t_end/tr)])
sdr.environment(tr, r, ts, t_end, x0)

kpd = [[6000, 1],
       [6000, 1],
       [5500, 0.5],
       [4500, 0.1],
       [3500, 0.1],
       [2000, 0.1]]
ki = np.array([1200, 500, 400, 400, 300, 150])
i0 = np.array([0, -162.3, -58.5, 2.5, -8.5, 2.5])
i_bound = np.array([200, 400, 350, 100, 80, 20])
sdr.design_control(kpd, ki, i0, i_bound)
##%%
start_time = time.clock()
sdr.run()
print('computing time: {}sec'.format(round(time.clock() - start_time, 2)))
##%%
sdr.show()
##%%