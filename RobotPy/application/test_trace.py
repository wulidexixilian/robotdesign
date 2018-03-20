# -*- coding: utf-8 -*-
"""
test
Created on Fri Mar 24 14:17:04 2017

@author: pei.sun
"""
import numpy as np
import matplotlib.pyplot as plt
from RobotPy import rSimulation as sim
# from RobotPy.rRobotDB import rConfig_kr6_900 as cfg
# from RobotPy.rRobotDB import rConfig_kr6_900_exp as cfg
from RobotPy.rRobotLib import rConfig_kr6_900_old as cfg
#from RobotPy.rRobotDB import rConfig_1100 as cfg
np.set_printoptions(suppress=True)
np.set_printoptions(precision=4)
##%%
s = sim.Simulation()
s.set_gravity(9.8 * np.array([0,0,-1]))
s.buildRobot(cfg.structurePara,
             cfg.massPara,
             cfg.motorPara,
             cfg.frictionPara,
             cfg.gearPara)
#%%
percentage = 100 # amount of data to be simulated, 100% for all
# trace source
trace_file = "C:/Users/pei.sun/Desktop/mada/trace_example/KR6R900/000xTemperatur_NextGenDrive"
# load q(t) from trace file
s.loadQ(trace_file, percentage, [1, 1, 1, 1, 1, 1])
# inverse dynamic simulation
s.simFromQ()
# visualization
plt.close("all")
s.animate()
s.show()
# show drive characteristics and v-T diagram
s.drive_characteristic(40,40)
s.fea_inputs()
#%%
#Comparing results with OPC trace
figTorqueTrace = plt.figure()
pm = [plt.subplot(321+i) for i in range(6)]
for i in range(6):
   moment_trace = s.readTrace(trace_file+'#'+str(i+1),"Istmoment", percentage)[0]
   pm[i].plot(s.t_ser[0:len(moment_trace)], moment_trace, 'r-', label="trace T")
   pm[i].plot(s.t_ser, s.driveTorque_ser[:,i], 'b-', label="sim T")
   pm[i].plot(s.t_ser, s.friction_ser[:,i]/s.robot.drives[i].ratio, 'g--', label="fr")
   pm[i].plot(s.t_ser, s.drivePure_ser[:,i]/s.robot.drives[i].ratio, 'y--', label="sim pure T")
   pm[i].grid(True)
   pm[i].legend()

figSTTrace = plt.figure()
pst = [plt.subplot(321+i) for i in range(6)]
for i in range(6):
   moment_trace = s.readTrace(trace_file+'#'+str(i+1),"Istmoment", percentage)[0]
   speed_trace = s.readTrace(trace_file+'#'+str(i+1),"Istgeschwindigkeit", percentage)[0]
   pst[i].plot(speed_trace[0:len(moment_trace)], moment_trace, 'r-', label="trace T")
   pst[i].grid(True)

plt.show()
