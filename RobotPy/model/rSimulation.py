# -*- coding: utf-8 -*-
"""
simulation system
Created on Fri Mar 24 10:57:49 2017

@author: pei.sun
"""
import struct
import time
import matplotlib.animation as ani
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pyprind
from model.rAnalysis import SimulationAnalysis, get_all_friction_in_array
from model.rMath import rotation, tensor, tear_tensor
from scipy.integrate import odeint
from model.rSymbolic import SymDyRobot
import utility.fwd_dyn as dyn
from model.rManipulator import Dynamics
from utility.characteristic import klobps
from utility.trajectory import TrajectoryGenerator


class Simulation():
    """ Simulation environment of one robot with defined trajectory and load case """
    def __init__(self):
        print('\n\n****** Robot Simulation Alpha1.5 ******')
        ar = np.array
        self.coordinateConfigurationDict = {
                                 "groundbase":(ar([0, 0, 0]),
                                               ar([np.pi, 0, 0])),

                                 "rotationcolumn":(ar([np.pi, 0, 0]),
                                                   ar([np.pi/2, 0, 0])),

                                 "linkarm":(ar([-np.pi/2, 0, 0]),
                                            ar([0, 0, 0])),

                                 "arm":(ar([-np.pi/2, 0, 0]),
                                        ar([0, -np.pi/2, -np.pi/2])),

                                 "handbase":(ar([0, -np.pi/2, 0]),
                                             ar([-np.pi/2, 0, np.pi/2])),

                                 "handwrist":(ar([-np.pi/2, 0, 0]),
                                              ar([0, -np.pi/2, -np.pi/2])),

                                 "handflange":(ar([0, -np.pi/2, 0]),
                                               ar([0, np.pi, 0])),

                                 "tcp":(ar([0, np.pi/2, 0]),
                                        ar([0, 0, 0])),
                                 }
        self.filterLen = 50
        self.gravity = 9.8 * np.array([0,0,-1])
        self.aniRun = False
        self.trajectoryGenerator = None
        self.q_cmd_ser = None
        self.ratioMask = [1, 1, 1, 1, 1, 1]

    def set_filter_length(self, length):
        self.filterLen = length

    def set_gravity(self, gravity):
        self.gravity = gravity

    def handleGear(self, gearPara, base):
        """
        Divide a gear box into 3 parts as
        stator mass, rotor mass and and drive train mass
        Assign these masses to their corresponding body objects
        according their configuration types
        """
        ar = np.array
        partList = [
                     "groundbase", "rotationcolumn", "linkarm", "arm",
                     "handbase", "handwrist", "handflange", "tcp",
                  ]
        ratioSign = {1:1, 2:-1, 3:-1, 4:1, 5:1, 6:-1, 7:-1, 8:1,
                     9:-1, 10:1, 11:1, 12:-1, 13:-1, 14:1, 15:1, 16:-1}
        ratioPlus1 = {1:0, 2:1, 3:0, 4:1, 5:0, 6:1, 7:0, 8:1,
                     9:0, 10:1, 11:0, 12:1, 13:0, 14:1, 15:0, 16:1}
        positiveOrientCases = [1,2,3,4,13,14,15,16]
        statorFirstCases = [1,2,3,4,9,10,11,12]

        iT_sr = gearPara["stator"]["inertia_body"]
        iT_rr = gearPara["rotor"]["inertia_body"]
        iT_s = np.array(iT_sr)[[2,1,0]]
        iT_s = np.hstack((iT_s, np.array([0, 0, 0])))
        iT_r = np.array(iT_rr)[[2,1,0]]
        iT_r = np.hstack((iT_r, np.array([0, 0, 0])))
        massListItemStator = {"m":gearPara["stator"]["m"],
                              "iT":iT_s,
                              'name':'stator'}
        massListItemRotor = {"m":gearPara["rotor"]["m"],
                             "iT":iT_r,
                             'name':'rotor'}

        driveListItem0 = {"friction":[0, 0, 1]}
        driveListItem1 = {"friction":[0, 0, 1]}
        driveListItem0["nest"] = partList[partList.index(gearPara["nest"]) + 1]
        driveListItem1["nest"] = partList[partList.index(gearPara["nest"]) + 1]
        driveListItem0["driveInertia"] = 0
        driveListItem0["ratio"] = 1
        case = gearPara["case"]
        driveListItem1["ratio"] = (gearPara["ratio"] + ratioPlus1[case]) *\
                                  ratioSign[case]
        # align = rotation(*gearPara['orientation'], 'zyx')
        # orientation2Nx = self.coordinateConfigurationDict[gearPara['nest']][1]
        # align2Nx = rotation(*orientation2Nx, 'xyz').T
        orientation2Nx = self.coordinateConfigurationDict[gearPara['nest']][1]
        orientation2Nx[2] = 0
        if case in positiveOrientCases:
            align = rotation(*orientation2Nx, 'xyz')
            align2Nx = 1
        else:
            align = -rotation(*orientation2Nx, 'xyz')
            align2Nx = -1
        if case in statorFirstCases:
            massListItemStator["nest"] = gearPara["nest"]
            massListItemRotor["nest"] = partList[partList.index(gearPara["nest"]) + 1]
            massListItemStator["cm"] = align @\
                              ar([0, 0, gearPara["offset"]+gearPara["stator"]["cm"]]) +\
                              base
            massListItemRotor["cm"] = align2Nx * ar([0, 0, gearPara["rotor"]["cm"]])
            driveListItem1["driveInertia"] = gearPara["rotor"]["inertia_drive"]
        else:
            massListItemRotor["nest"] = gearPara["nest"]
            massListItemStator["nest"] = partList[partList.index(gearPara["nest"]) + 1]
            massListItemRotor["cm"] = align @ ar([0, 0, gearPara["rotor"]["cm"]]) + base
            massListItemStator["cm"] = align2Nx * ar([0, 0, gearPara["offset"]+gearPara["stator"]["cm"]])
            driveListItem1["driveInertia"] = gearPara["stator"]["inertia_drive"]

        return [massListItemRotor, massListItemStator, driveListItem0, driveListItem1]

    def handleMotors(self, motorPara):
        massPara_motor = []
        for motor in motorPara:
            massItem = dict()
            massItem['nest'] = motor['nest']
            massItem['m'] = motor['m']
            align = rotation(*motor['orientation'])
            massItem['cm'] = align @ motor['cm'] + motor['position']
            massItem['iT'] = align @ tensor(*motor['iT']) @ align.T
            massItem['name'] = 'motor'
            massPara_motor.append(massItem)
        return massPara_motor

    def buildRobot(self, structurePara, massPara, motorPara, frictionPara, gearPara,
                   load = {"cm":[0, 0, 0], "m":0, "iT":[0, 0, 0, 0, 0, 0]}):
        """
        a robot is constructed here according to geometry, mass, friction data
        Inputs:
            structurePara: list contains geometry of every link
            massPara: list contains all masses and where they are attached to
            frictionPara: friction of every joint
            gearPara: a gear box object serves as a connection between links, it
                      contains its own data of mass and geometry which will be
                      distributed to connecting links
        """
        print('building robot')
        # handle dimensions -- flange to flange displacement
        dimensionList = structurePara
        # mass parameters + load, with out motors and gears, to be completed later
        load['cm'] = np.array(load['cm'])
        load['iT'] = np.array(load['iT'])
        load['nest'] = 'tcp'
        massPara = list(massPara)
        massPara.append(load)
        massList = massPara
        for item in dimensionList:
            offset = 0
            name = item["name"]
            for gear in gearPara:
                if gear["nest"] == name:
                    offset = gear["offset"]
                    if gear["case"]>8:
                        offset = -offset
                    break
            item["offset"] = offset
        # handle motors -- abstract each motor into a mass item
        # and add it to the mass list
        massList = massList + self.handleMotors(motorPara)
        # handle frictions
        driveList = []
        for item in frictionPara:
            driveItem = dict()
            driveItem["nest"] = item["nest"]
            driveItem["driveInertia"] = 0
            driveItem["ratio"] = 1
            driveItem["friction"] = item["friction"]
            driveList.append(driveItem)
        for i, item in enumerate(motorPara):
            if 'characteristic' in item:
                driveList[i]['characteristic_before_ratio'] = \
                    item['characteristic']
        for i, item in enumerate(gearPara):
            if 'limit_factor' in item:
                f = klobps(item['acc_tau'], item['limit_factor'], item['max_omega'])
                omega_range = np.linspace(0, item['max_omega'], 20)
                tau = np.array([f(w) for w in omega_range])
                char = dict()
                char['max'] = np.vstack((omega_range * 2 * np.pi / 60 / item['ratio'],
                                         np.ones(np.shape(omega_range)) * item['max_tau']))
                char['s1'] = np.vstack((omega_range * 2 * np.pi / 60 / item['ratio'], tau))
                driveList[i]['characteristic_after_ratio'] = char

        # handle gears -- abstract each gears to 2 mass item and 2 drive item
        # and add them to their corresponding lists
        for itemGear in gearPara:
            for i, itemDim in enumerate(dimensionList):
                if itemDim['name'] == itemGear['nest']:
                    gearBase = itemDim['displacement']
                    break

            additives = self.handleGear(itemGear, gearBase)
            massList.append(additives[0])
            massList.append(additives[1])
            driveList.insert(0, additives[2])
            driveList.insert(0, additives[3])

        self.dimensionList = dimensionList
        self.massList = massList
        self.driveList = driveList
        self.robot = Dynamics(dimensionList, massList,
                              driveList, self.coordinateConfigurationDict)

    def runStep(self, q, q_dot=np.zeros(6), q_ddot=np.zeros(6)):
        self.robot.k(q)
        self.robot.ne(q_dot, q_ddot, self.gravity)
        self.robot.solve_drivetrain(q_dot, q_ddot)
        q_cmd_capacitor = []
        q_cmd_capacitor.append(q)
        self.q_cmd_ser = np.array(q_cmd_capacitor)
        self.t_ser = np.array([0])
        self.tcp_ser = np.array([self.robot.joints[-1].origin1])
        self.driveTorque_ser = np.array([np.array([self.robot.drives[i].driveTau\
                                                   for i in range(6)])])

    def readTrace(self, fileName, dataName, k):
        """
        access a trace file and read the specified data field
        Inputs:
            fileName: absolute directory to the trace file
            dataName: ask mada guys for what names are available
        """
        with open('../' + fileName + ".dat", "rb") as f1:
            text = f1.read()
        blocks = text.split(b'#BEGINCHANNELHEADER')
        timeBlock = blocks[1]
        if timeBlock.find(b"Zeit") == -1:
            pass
        Ts = float((timeBlock[timeBlock.find(b'241,') + len("241,"):].splitlines())[0])
        N = len(blocks[2:])
        for block in blocks[2:]:
            lines = block.splitlines()
            if lines[1]!=b'200,' + dataName.encode("ascii"):
                continue
            for line in lines:
                if line.find(b'221,')==-1:
                    continue
                index = line.find(b'221,') + len("221,")
                columnNumber = int(line[index:])
                break
            break
        with open('../' + fileName+".r64", "rb") as f2:
            data_all = f2.read()
        L = int(len(data_all) * (k/100.0))
        result_all = [struct.unpack("d", data_all[i:i+8])[0] for i in range(0, L-8, 8)]
        result = np.array(result_all[columnNumber-1::N])
        return result, Ts

    def loadQ(self, fileNameFraction, percentage, ratioMask=[1, 1, 1, 1, 1, 1], speedOverride=1, trace_type='ipo'):
        """
        Load axis angle trajectories from OPC trace files
        Input:
            fileNameFraction: trace file should corresponds to a certain axis with
                              axis No. in the end of its name, e.g. "xxxx1.dat"
                              fileNameFraction is a string contains the
                              absolute directory to the trace file with out the axis
                              Number. For example, for a trace file "C:/yyy/xxx1.dat",
                              fileNameFraction = "C:/yyy/xxx"
            percentage: how much data will be loaded
            ratioMask: a mask helps to solve the sign problem manually

        """
        print("loading q trace")
        q_cmd_capacitor = []
        q_dot_cmd_capacitor = []
        for i in range(6):
            if 'next' in trace_type.lower():
                value, Ts = self.readTrace(fileNameFraction + '#' + str(i+1),
                                           "Sollposition",
                                           percentage)
                q_cmd_capacitor.append(value * np.pi /
                                       180 * 1e-6 / np.array(ratioMask[i]))
                self.q_cmd_ser = (np.array(q_cmd_capacitor)).T
                self.q_dot_cmd_ser = np.gradient(self.q_cmd_ser, self.Ts)[0]
            elif 'ipo' in trace_type.lower():
                value, Ts = self.readTrace(fileNameFraction,
                                           "AxisPos_CmdIpo{}".format(str(i+1)),
                                           percentage)
                q_cmd_capacitor.append(value / np.array(ratioMask[i]))
                self.q_cmd_ser = (np.array(q_cmd_capacitor)).T
                value, Ts = self.readTrace(fileNameFraction,
                                           "AxisVel_CmdIpo{}".format(str(i+1)),
                                           percentage)
                q_dot_cmd_capacitor.append(value / np.array(ratioMask[i]))
                self.q_dot_cmd_ser = (np.array(q_dot_cmd_capacitor)).T

        self.Ts = Ts / speedOverride
        self.ratioMask = ratioMask
        self.t_ser = np.linspace(0, (len(self.q_cmd_ser)-1) * self.Ts, len(self.q_cmd_ser))
        # q_dot_cmd_capacitor = []
        # for i in range(6):
        #     value, Ts = self.readTrace(fileNameFraction + '#' + str(i+1),
        #                             "Sollposition", percentage)
        #     q_dot_cmd_capacitor.append(value * np.pi /
        #                            180 * 1e-6 / np.array(ratioMask[i]))
        # self.q_dot_cmd_ser = (np.array(q_dot_cmd_capacitor)).T

    def simFromQ(self, q=None, qd=None, qdd=None, t=None, Ts=None, ratio_mask=None):
        """
        Inverse dynamics calculation based on axis angle trajectories
        """
        if q is None:
            self.q_ddot_cmd_ser = np.gradient(self.q_dot_cmd_ser, self.Ts)[0]
        else:
            self.q_cmd_ser = q
            self.q_dot_cmd_ser = qd
            self.q_ddot_cmd_ser = qdd
            self.Ts = Ts
            self.ratioMask = ratio_mask
            self.t_ser = t
        N = len(self.q_ddot_cmd_ser)
        driveTorque_capacitor = []
        drivePure_capacitor = []
        friction_capacitor = []
        joint_f_capacitor = np.zeros([len(self.robot.bodies), 3, N])
        joint_tau_capacitor = np.zeros([len(self.robot.bodies), 3, N])
        tcp_capacitor = []

        bar = pyprind.ProgBar(N, track_time=True,
                              title='computing dynamic...', stream=1)
        for i in range(N):
            self.robot.k(self.q_cmd_ser[i,:])
            self.robot.ne(self.q_dot_cmd_ser[i,:],
                          self.q_ddot_cmd_ser[i,:],
                          self.gravity)

            self.robot.solve_drivetrain(self.q_dot_cmd_ser[i, :],
                                        self.q_ddot_cmd_ser[i,:])

            tcp_capacitor.append(self.robot.joints[-1].origin1)

            driveTorque_capacitor.append(
                        [self.robot.drives[j].driveTau for j in range(6)]
                                         )
            drivePure_capacitor.append(
                        [self.robot.drives[j].effectiveTau for j in range(6)]
                                       )
            friction_capacitor.append(
                        [self.robot.drives[j].friction for j in range(6)]
                                      )
            for j, body in enumerate(self.robot.bodies):
                joint_f_capacitor[j, :, i] = body.f
                joint_tau_capacitor[j, :, i] = body.tau
            bar.update()

        self.driveTorque_ser = np.array(driveTorque_capacitor)
        self.drivePure_ser = np.array(drivePure_capacitor)
        self.friction_ser = np.array(friction_capacitor)
        self.joint_f_ser = np.array(joint_f_capacitor)
        self.joint_tau_ser = np.array(joint_tau_capacitor)
        self.tcp_ser = np.array(tcp_capacitor)

    def generate_trajectory(self, trajectory):
        """
        Initialize a path planning instance. And generate a trajectory defined as 
        q(t) series. Only Adept is supported now.
        :param trajectory: trajectory configuration
        :return: 
        """
        self.trajectoryGenerator = TrajectoryGenerator()
        if trajectory['type'] is 'adept':
            self.trajectoryGenerator.adept(trajectory['v_max'],
                                           trajectory['T'],
                                           trajectory['N'],
                                           trajectory['offset'],
                                           trajectory['rotation'],
                                           trajectory['orientation'])
        self.Ts = trajectory['T'] / trajectory['N']
        self.q_cmd_ser = np.array(list(map(self.robot.ik,
                                           self.trajectoryGenerator.trajectory.T)))
        self.q_dot_cmd_ser = np.gradient(self.q_cmd_ser, self.Ts)[0]
        self.t_ser = np.linspace(0, (len(self.q_cmd_ser) - 1) * self.Ts,
                                 len(self.q_cmd_ser))

    def init_symbolic_model(self):
        dimension_lo = []
        mass_centers_lo = []
        masses = []
        its = []
        for body in self.robot.bodies[1:]:
            dimension_lo.append(body.dimension)
            mass_centers_lo.append(body.cm)
            masses.append(body.m)
            its.append(tear_tensor(body.iT))
        fr = {'Rh': [], 'Rv': [], 'Threshold': self.robot.fr_thresholds}
        for drive in self.robot.drives:
            fr['Rh'].append(drive.Rh)
            fr['Rv'].append(drive.Rv)
        self.sdr = SymDyRobot(dimension_lo, fr, mass_centers_lo, masses, its,
                         abs(self.gravity),
                         if_simplify=True)
        self.sdr.generate_equation()

    def set_symbolic_simulation(self, tr, r, ts, t_end, x0, kpd, ki, i0, i_bound):
        self.sdr.environment(tr, r, ts, t_end, x0)
        self.sdr.design_control(kpd, ki, i0, i_bound)

    def run_symbolic_simulation(self):
        start_time = time.clock()
        self.sdr.run()
        print('computing time: {}sec'.format(round(time.clock() - start_time, 2)))
        self.sdr.show()

    def showMotorGearCM(self, ax):
        ar = np.array
        motors = []
        stators = []
        rotors = []
        for item in self.massList:
            if 'name' in item:
                idx = self.robot.idDict[item['nest']]
                joint = self.robot.joints[idx]
                align = joint.align
                cm_gl = self.robot.local2world(align @ item['cm'], idx)[0:3]
                if item['name'] == 'motor':
                    motors.append(cm_gl)
                    marker = 'r+'
                    markersize = 10
                elif item['name'] == 'stator':
                    stators.append(cm_gl)
                    marker = 'b+'
                    markersize = 8
                elif item['name'] == 'rotor':
                    rotors.append(cm_gl)
                    marker = 'c+'
                    markersize = 8
                ax.plot(ar([cm_gl[0]]), ar([cm_gl[1]]), ar([cm_gl[2]]),
                        marker, markersize=markersize)
        return {'motor':motors, 'stator':stators, 'rotor':rotors}

    def snapShot(self, **kwargs):
        """
        static image of the robot in present pose
        For drawing two robots in one figure, call in this way:
            ax = simulation_a.snapShot()
            ax = simulation_b.snapShot(ax = ax, G = G_a2b)
            where G_a2b is the homogenuous transformation from a to b
        """
        G=np.identity(4)
        if 'ax' in kwargs:
            ax = kwargs['ax']
        else:
            fig = plt.figure(figsize=(18, 16))
            ax = fig.add_subplot(111, projection="3d")
            ax.grid()
            ax.set_xlim3d([-0.2, 1.2])
            ax.set_ylim3d([-0.7, 0.7])
            ax.set_zlim3d([0, 1.4])
        if 'G' in kwargs:
            G = kwargs['G']
        else:
            G = np.identity(4)

        js = self.robot.joints
        N = len(js)
        ar = np.array
        for idx in range(N-1):
            pa = (G @ np.hstack((js[idx].origin1, ar([1]))))[0:3]
            pb = (G @ np.hstack((js[idx+1].origin1, ar([1]))))[0:3]
            line, = ax.plot(np.array([pa[0], pb[0]]), np.array([pa[1], pb[1]]),
                            np.array([pa[2], pb[2]]), "#ff9500", lw=1.5)
        for joint in js:
            pa = (G @ np.hstack((joint.origin1, ar([1]))))[0:3]
            line, = ax.plot(np.array([pa[0]]), np.array([pa[1]]), np.array([pa[2]]),
                            'o',
                            markeredgecolor='b', markerfacecolor='none', ms=8, lw=2)

        arrowColor = ["r", "g", "b"]
        arrowHeads = []
        head1 = (G @ np.hstack((self.robot.tool2world(np.array([0,0,0.1]))[0:3],
                                ar([1]))))[0:3]
        head2 = (G @ np.hstack((self.robot.tool2world(np.array([0,0.1,0]))[0:3],
                                ar([1]))))[0:3]
        head3 = (G @ np.hstack((self.robot.tool2world(np.array([0.1,0,0]))[0:3],
                                ar([1]))))[0:3]
        arrowHeads = [head1, head2, head3]
        tail = ( G @ np.hstack((self.robot.joints[-1].origin1, ar([1]))) )[0:3]
        for idx, head in enumerate(arrowHeads):
            line, = ax.plot(ar([tail[0], head[0]]),
                            ar([tail[1], head[1]]),
                            ar([tail[2], head[2]]),
                            arrowColor[idx],lw=1)
        line, = ax.plot(ar([0]), ar([0]), ar([0]), 'gs', markersize=16)
        line, = ax.plot(ar([G[0][3]]), ar([G[1][3]]), ar([G[2][3]]),
                         'gs', markersize=16)
        return ax

    def get_result(self):
        """
        generate a result object for further analysis
        :return: SimulationResult instance 
        """
        ratio = [item.ratio for item in self.robot.drives]
        sr = SimulationAnalysis(self.robot,
                                self.q_cmd_ser, self.q_dot_cmd_ser,
                                self.driveTorque_ser, self.drivePure_ser,
                                self.joint_f_ser, self.joint_tau_ser,
                                self.tcp_ser,
                                self.t_ser,
                                self.Ts)
        return sr

    def onClick(self, event):
        """
        event callback for the animation window
        """
        if self.aniRun:
            self.sim_objects.event_source.stop()
            self.aniRun = False
        else:
            self.sim_objects.event_source.start()
            self.aniRun = True

    def initAni(self):
        """
        callback for animation, initialization
        """
        ar = np.array
        orange = "#ff9500"

        self.robot.k(self.q_cmd_ser[0,:])
        js = self.robot.joints
        N = len(js)

        self.ani_links = []
        for indx in range(N-1):
            line, = self.ax.plot(
                            ar([js[indx].origin1[0], js[indx+1].origin1[0]]),
                            ar([js[indx].origin1[1], js[indx+1].origin1[1]]),
                            ar([js[indx].origin1[2], js[indx+1].origin1[2]]),
                            orange,
                            lw=1.5)
            self.ani_links.append(line)
        self.ani_joints = []
        for joint in js:
            line, = self.ax.plot(ar([joint.origin1[0]]),
                                 ar([joint.origin1[1]]),
                                 ar([joint.origin1[2]]),
                                 'o',
                                 markeredgecolor="b",
                                 markerfacecolor="none",
                                 ms=8,
                                 lw=2)
            self.ani_joints.append(line)
        self.ani_Trajectory, = self.ax.plot(self.tcp_ser[:1, 0],
                                            self.tcp_ser[:1, 1],
                                            self.tcp_ser[:1, 2],
                                            'm--',
                                            lw=1)
#
        arrowHeads = []
        self.arrow = []
        arrowColor = ["r", "g", "b"]
        arrowHeads.append(self.robot.tool2world(np.array([0.1,0,0]))[0:3])
        arrowHeads.append(self.robot.tool2world(np.array([0,0.1,0]))[0:3])
        arrowHeads.append(self.robot.tool2world(np.array([0,0,0.1]))[0:3])
        tail = self.robot.joints[-1].origin1
        for i, head in enumerate(arrowHeads):
            self.arrow.append(
                         self.ax.plot(
                                      np.array([tail[0], head[0]]),
                                      np.array([tail[1], head[1]]),
                                      np.array([tail[2], head[2]]),
                                      arrowColor[i],
                                      lw = 1
                                     )[0]
                             )
        self.x_text = self.ax.text(-0.45, -0.7, 0.8, "tcp[x]:")
        self.y_text = self.ax.text(-0.45, -0.7, 0.7, "tcp[y]:")
        self.z_text = self.ax.text(-0.45, -0.7, 0.6, "tcp[z]:")
        self.t_text = self.ax.text(-0.45, -0.7, 0.5, "T1:")
        self.tau1_text = self.ax.text(0.45, -0.7, 0.8, "T2:")
        self.tau2_text = self.ax.text(0.45, -0.7, 0.7, "T3:")
        self.tau3_text = self.ax.text(0.45, -0.7, 0.6, "T4:")
        self.tau4_text = self.ax.text(0.45, -0.7, 0.5, "T5:")
        self.tau5_text = self.ax.text(0.45, -0.7, 0.4, "T6:")
        self.tau6_text = self.ax.text(0.45, -0.7, 0.3, "T7:")
#
        self.ax.plot(ar([0]), ar([0]), ar([0]), 'gs', markersize=8)
#
        return self.ani_links, self.ani_joints, self.ani_Trajectory,\
               self.x_text, self.y_text, self.z_text, self.t_text,\
               self.tau1_text, self.tau2_text, self.tau3_text, self.tau4_text,\
               self.tau5_text, self.tau6_text,\
               self.arrow

    def updateAni(self, i):
        """
        callback for animation, updating
        """
        ar = np.array
        js = self.robot.joints
        M = len(self.ani_links)
        N = len(self.ani_joints)
        self.robot.k(self.q_cmd_ser[i,:])

        for indx in range(M):
            self.ani_links[indx].set_data(
                    ar([js[indx].origin1[0], js[indx+1].origin1[0]]),
                    ar([js[indx].origin1[1], js[indx+1].origin1[1]]))
            self.ani_links[indx].set_3d_properties(
                    ar([js[indx].origin1[2], js[indx+1].origin1[2]])
                                                   )
        for indx in range(N):
            self.ani_joints[indx].set_data(
                    ar([js[indx].origin1[0]]), ar([js[indx].origin1[1]])
                                          )
            self.ani_joints[indx].set_3d_properties(ar([js[indx].origin1[2]]))

        if i <= 50000:
            self.ani_Trajectory.set_data(self.tcp_ser[:i, 0], self.tcp_ser[:i, 1])
            self.ani_Trajectory.set_3d_properties(self.tcp_ser[:i, 2])
        else:
            self.ani_Trajectory.set_data(self.tcp_ser[i-2000:i, 0],
                                         self.tcp_ser[i-2000:i, 1])
            self.ani_Trajectory.set_3d_properties(self.tcp_ser[i-2000:i, 2])
#
        arrowHeads = []
        arrowHeads.append(self.robot.tool2world(np.array([0.1,0,0]))[0:3])
        arrowHeads.append(self.robot.tool2world(np.array([0,0.1,0]))[0:3])
        arrowHeads.append(self.robot.tool2world(np.array([0,0,0.1]))[0:3])
        tail = self.robot.joints[-1].origin1
        for idx, head in enumerate(arrowHeads):
            self.arrow[idx].set_data(
                                     ar([tail[0], head[0]]),
                                     ar([tail[1], head[1]])
                                    )
            self.arrow[idx].set_3d_properties(ar([tail[2], head[2]]))
#
#
        self.x_text.set_text("tcp[x]: %3.4f" % js[-1].origin1[0])
        self.y_text.set_text("tcp[y]: %3.4f" % js[-1].origin1[1])
        self.z_text.set_text("tcp[z]: %3.4f" % js[-1].origin1[2])
        self.t_text.set_text("t: %3.4f" % self.t_ser[i])
        self.tau1_text.set_text("T1: %3.4f" % self.driveTorque_ser[i,0])
        self.tau2_text.set_text("T2: %3.4f" % self.driveTorque_ser[i,1])
        self.tau3_text.set_text("T3: %3.4f" % self.driveTorque_ser[i,2])
        self.tau4_text.set_text("T4: %3.4f" % self.driveTorque_ser[i,3])
        self.tau5_text.set_text("T5: %3.4f" % self.driveTorque_ser[i,4])
        self.tau6_text.set_text("T6: %3.4f" % self.driveTorque_ser[i,5])
#
        return self.ani_links, self.ani_joints, self.ani_Trajectory,\
               self.x_text, self.y_text, self.z_text, self.t_text,\
               self.tau1_text, self.tau2_text, self.tau3_text, self.tau4_text,\
               self.tau5_text, self.tau6_text,\
               self.arrow

    def animate(self, space_size=1.2):
        """
        animation
        """
        print("visualizing...")
        figAni = plt.figure()
        self.ax = figAni.add_subplot(111, projection='3d')
        self.ax.grid()
        self.ax.set_xlim3d([-space_size, space_size])
        self.ax.set_ylim3d([-space_size, space_size])
        self.ax.set_zlim3d([-space_size, space_size])
        self.ax.text(space_size * 0.8, 0, 0, "x")
        self.ax.text(0, space_size * 0.8, 0, "y")
        self.ax.view_init(30,45)
        figAni.canvas.mpl_connect('button_release_event', self.onClick)
        self.sim_objects = ani.FuncAnimation(figAni, self.updateAni,
                                             len(self.t_ser), interval=2,
                                             repeat=False, blit=False,
                                             init_func=self.initAni)
        # plt.show()

    def solve_fwd_dynamic(self, trajectory_cmd):
        """
        solve the forward dynamic problem in closed loop positioning case
        :param trajectory_cmd: command trajectory [t; q(t); qd(t)]
        :return: simulation trajectory [q(t)', qd(t)']
        """
        q0 = trajectory_cmd[1:7, 0]
        qd0 = trajectory_cmd[7:, 0]
        y0 = np.hstack((q0, qd0))
        t = trajectory_cmd[0, :]
        print('solving forward dynamic')
        Rh, Rv = get_all_friction_in_array(self.robot)
        kp = [1500, 1250, 1250, 750, 500, 400]
        kd = [1, 1, 0.5, 0.2, 0.1, 0.1]
        threshold = 0.001
        sol = odeint(dyn.dyn, y0, t,
                     args=(self.robot, self.gravity, dyn.control,
                           Rh, Rv, trajectory_cmd, (kp, kd), threshold),
                     rtol=5e-5, atol=1e-5)
        return sol

    def solve_brake(self, q0, qd0, tau_brake, t_end=0.6, N=2500):
        """
        solve the forward dynamic problem in emergency brake case
        :param q0: initial position
        :param qd0: initial speed
        :return: simulation trajectory [q(t)', qd(t)']
        """
        y0 = np.hstack((q0, qd0))
        t = np.linspace(0, t_end, N)
        print('solving forward dynamic')
        Rh, Rv = get_all_friction_in_array(self.robot)
        ratio = np.array([drive.ratio for drive in self.robot.drives])
        tau_brake_joint = tau_brake * ratio
        threshold = 0.0001
        sol = odeint(dyn.dyn, y0, t,
                     args=(self.robot, self.gravity, dyn.brake,
                           Rh, Rv, None, tau_brake_joint, threshold),
                     rtol=5e-5, atol=1e-5)
        return sol