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
from mpl_toolkits.mplot3d import axes3d, Axes3D
import numpy as np
import pyprind
from model.m_analysis import StaticAnalysis, SimulationAnalysis, get_all_friction_in_array
from utility.u_math import rotation, tensor, tear_tensor
from scipy.integrate import odeint
from model.m_symbolic import SymDyRobot
import utility.fwd_dyn as dyn
from model.m_manipulator import Dynamics
from utility.trajectory import TrajectoryGenerator
from utility.characteristic import klobps
from utility.inverse_kinematic import ik_industry
import os

ar = np.array


class Simulation:
    """
        Simulation environment of one robot
        Methods to establish robot, load trace,
        calculate static properties, solve kinematic problems,
        dynamic simulation.
    """
    ratioSign = {1: 1, 2: -1, 3: -1, 4: 1, 5: 1, 6: -1, 7: -1, 8: 1,
                 9: -1, 10: 1, 11: 1, 12: -1, 13: -1, 14: 1, 15: 1, 16: -1}
    ratioPlus1 = {1: 0, 2: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1,
                  9: 0, 10: 1, 11: 0, 12: 1, 13: 1, 14: 1, 15: 0, 16: 1}
    positive_orient_cases = [1, 2, 3, 4, 13, 14, 15, 16]
    stator_first_cases = [1, 2, 3, 4, 9, 10, 11, 12]
    frame_config = {
        "groundbase": {
            'frame0': ar([0, 0, 0]),
            'frame1': ar([np.pi, 0, 0]),
        },
        "rotationcolumn": {
            'frame0': ar([np.pi, 0, 0]),
            'frame1': ar([np.pi / 2, 0, 0])
        },
        "linkarm": {
            'frame0': ar([-np.pi / 2, 0, 0]),
            'frame1': ar([0, 0, 0])
        },
        "arm": {
            'frame0': ar([-np.pi / 2, 0, 0]),
            'frame1': ar([0, -np.pi / 2, -np.pi / 2])
        },
        "handbase": {
            'frame0': ar([0, -np.pi / 2, 0]),
            'frame1': ar([-np.pi / 2, 0, np.pi / 2])
        },
        "handwrist": {
            'frame0': ar([-np.pi / 2, 0, 0]),
            'frame1': ar([0, -np.pi / 2, -np.pi / 2])
        },
        "handflange": {
            'frame0': ar([0, -np.pi / 2, 0]),
            'frame1': ar([0, np.pi, 0])
        },
        "tcp": {
            'frame0': ar([0, np.pi / 2, 0]),
            'frame1': ar([0, 0, 0])
        },
    }

    def __init__(self):
        print('\n\n****** Robot Simulation *******')
        self.robot = None
        self.filterLen = 50
        self.gravity = 9.8 * np.array([0, 0, -1])
        self.aniRun = False
        self.trajectory_generator = None
        self.t_ser = None
        self.ts = None
        self.ratioMask = None
        self.dimension_list = None
        self.mass_list = None
        self.drive_list = None
        self.q_cmd_ser = None
        self.q_dot_cmd_ser = None
        self.q_ddot_cmd_ser = None
        self.tau_motor_ser = None
        self.tau_motor_ser = None
        self.tau_joint_ser = None
        self.friction_ser = None
        self.f_joint_ser = None
        self.tau_joint_3d_ser = None
        self.tcp_ser = None

    def set_filter_length(self, length):
        self.filterLen = length

    def set_gravity(self, gravity):
        self.gravity = gravity

    def handle_gear(self, gear_para, base):
        """
        Divide a gear box into 3 parts as
        stator mass, rotor mass and and drive train mass
        Assign these masses to their corresponding body objects
        according their configuration types
        """
        link_name = list(self.frame_config.keys())
        # ratioSign = {1:1, 2:-1, 3:-1, 4:1, 5:1, 6:-1, 7:-1, 8:1,
        #              9:-1, 10:1, 11:1, 12:-1, 13:-1, 14:1, 15:1, 16:-1}
        # ratioPlus1 = {1:0, 2:1, 3:0, 4:1, 5:0, 6:1, 7:0, 8:1,
        #              9:0, 10:1, 11:0, 12:1, 13:0, 14:1, 15:0, 16:1}
        # positive_orient_cases = [1,2,3,4,13,14,15,16]
        # stator_first_cases = [1,2,3,4,9,10,11,12]

        inertia_stator_raw = gear_para["stator"]["inertia_body"]
        inertia_rotor_raw = gear_para["rotor"]["inertia_body"]
        inertia_stator = np.hstack(
            (np.array(inertia_stator_raw)[[2, 1, 0]], np.array([0, 0, 0]))
        )
        inertia_rotor = np.hstack(
            (np.array(inertia_rotor_raw)[[2, 1, 0]], np.array([0, 0, 0]))
        )
        mass_list_item_stator = {
            "m": gear_para["stator"]["m"], "iT": inertia_stator, 'name': 'stator'
        }
        mass_list_item_rotor = {
            "m": gear_para["rotor"]["m"], "iT": inertia_rotor, 'name': 'rotor'
        }
        drivetrain_item_0 = dict()
        drivetrain_item_1 = dict()
        drivetrain_item_0['friction'] = [0, 0, 1]
        drivetrain_item_1['friction'] = [0, 0, 1]
        drivetrain_item_0["nest"] = link_name[link_name.index(gear_para["nest"]) + 1]
        drivetrain_item_1["nest"] = link_name[link_name.index(gear_para["nest"]) + 1]
        drivetrain_item_0["driveInertia"] = 0
        drivetrain_item_0["ratio"] = 1
        drivetrain_item_1["ratio"] = gear_para['ratio']
        case = gear_para["case"]
        orientation2nx = self.frame_config[gear_para['nest']]['frame1']
        orientation2nx[2] = 0
        if case in self.positive_orient_cases:
            align = rotation(*orientation2nx, 'xyz')
            align2nx = 1
        else:
            align = -rotation(*orientation2nx, 'xyz')
            align2nx = -1
        if case in self.stator_first_cases:
            mass_list_item_stator["nest"] = gear_para["nest"]
            mass_list_item_rotor["nest"] = link_name[
                link_name.index(gear_para["nest"]) + 1
            ]
            mass_list_item_stator["cm"] = align @ ar(
                [0, 0, gear_para["offset"] + gear_para["stator"]["cm"]]
                ) + base
            mass_list_item_rotor["cm"] = align2nx * ar(
                [0, 0, gear_para["rotor"]["cm"]]
            )
            drivetrain_item_1["driveInertia"] = gear_para["rotor"]["inertia_drive"]
        else:
            mass_list_item_rotor["nest"] = gear_para["nest"]
            mass_list_item_stator["nest"] = link_name[
                link_name.index(gear_para["nest"]) + 1
            ]
            mass_list_item_rotor["cm"] = align @ ar(
                [0, 0, gear_para["rotor"]["cm"]]
            ) + base
            mass_list_item_stator["cm"] = align2nx * ar(
                [0, 0, gear_para["offset"] + gear_para["stator"]["cm"]]
            )
            drivetrain_item_1["driveInertia"] = gear_para["stator"]["inertia_drive"]

        return mass_list_item_rotor, mass_list_item_stator, drivetrain_item_0, \
            drivetrain_item_1

    @staticmethod
    def handle_motor(motor_para):
        mass_para_motor = []
        for motor in motor_para:
            mass_item = dict()
            mass_item['nest'] = motor['nest']
            mass_item['m'] = motor['m']
            align = rotation(*motor['orientation'])
            mass_item['cm'] = align @ motor['cm'] + motor['position']
            mass_item['iT'] = align @ tensor(*motor['iT']) @ align.T
            mass_item['name'] = 'motor'
            mass_para_motor.append(mass_item)
        return mass_para_motor

    def build_robot(
        self, structure_para, mass_para, motor_para,
        friction_para, gear_para, load=None
    ):
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
        dimension_list = structure_para
        # mass parameters + load, with out motors and gears, to be completed later
        if load is None:
            load = {"cm": [0, 0, 0], "m": 0, "iT": [0, 0, 0, 0, 0, 0]}
        load['cm'] = np.array(load['cm'])
        load['iT'] = np.array(load['iT'])
        load['nest'] = 'tcp'
        mass_para = list(mass_para)
        mass_para.append(load)
        mass_list = mass_para
        for item in dimension_list:
            if 'offset' in item:
                continue
            else:
                offset = 0
                name = item["nest"]
                for gear in gear_para:
                    if gear["nest"] == name:
                        offset = gear["offset"]
                        if gear["case"] > 8:
                            offset = -offset
                        break
                item["offset"] = offset
        # handle motors -- abstract each motor into a mass item
        # and add it to the mass list
        mass_list = mass_list + self.handle_motor(motor_para)
        # handle frictions
        drive_list = []
        for idx, item in enumerate(friction_para):
            drive_item = dict()
            drive_item["nest"] = item["nest"]
            drive_item['joint'] = idx + 1
            drive_item["driveInertia"] = 0
            drive_item["ratio"] = 1
            drive_item["friction"] = item["friction"]
            drive_list.append(drive_item)
        for i, item in enumerate(motor_para):
            if 'characteristic' in item:
                drive_list[i]['characteristic_before_ratio'] = item['characteristic']
        # ratioSign = {1:1, 2:-1, 3:-1, 4:1, 5:1, 6:-1, 7:-1, 8:1,
        #              9:-1, 10:1, 11:1, 12:-1, 13:-1, 14:1, 15:1, 16:-1}
        # ratioPlus1 = {1:0, 2:1, 3:0, 4:1, 5:0, 6:1, 7:0, 8:1,
        #              9:0, 10:1, 11:0, 12:1, 13:0, 14:1, 15:0, 16:1}
        for i, item in enumerate(gear_para):
            case = item['case']
            item["ratio"] = (item["ratio"] + self.ratioPlus1[case]) \
                * self.ratioSign[case] * item['pre ratio']
            # if 'limit_factor' in item:
            #     f = klobps(
            #         item['rated_tau'], item['limit_factor'], item['max_omega']
            #     )
            #     omega_range = np.linspace(0, item['max_omega'], 20)
            #     tau = np.array([f(w) for w in omega_range])
            #     char = dict()
            #     r = np.abs(item['ratio'])
            #     char['max'] = np.vstack((omega_range * 2 * np.pi / 60 / r,
            #                   np.ones(np.shape(omega_range)) * item['max_tau']))
            #     char['s1'] = np.vstack((omega_range * 2 * np.pi / 60 / r, tau))
            #     driveList[i]['characteristic_after_ratio'] = char
        # handle gears -- abstract each gears to 2 mass item and 2 drive item
        # and add them to their corresponding lists
        for idx_joint, item_gear in enumerate(gear_para):
            gear_base = None
            for item_dim in dimension_list:
                if item_dim['nest'] == item_gear['nest']:
                    gear_base = item_dim['displacement']
                    break
            if gear_base is None:
                print('nest info does not match, building robot terminated')
                return
            additives = self.handle_gear(item_gear, gear_base)
            mass_list.append(additives[0])
            mass_list.append(additives[1])
            additives[2]['joint'] = idx_joint + 1
            additives[3]['joint'] = idx_joint + 1
            drive_list.insert(0, additives[2])
            drive_list.insert(0, additives[3])
        self.dimension_list = dimension_list
        self.mass_list = mass_list
        self.drive_list = drive_list
        self.robot = Dynamics(
            dimension_list,
            mass_list,
            drive_list,
            self.frame_config
        )
        self.set_ik()

    def set_ik(self):
        self.robot.inverse_dynamic = ik_industry

    def load_gear_characteristic(
        self, gear_data, stall_torque, max_omega_override=None
    ):
        for idx, item in enumerate(gear_data):
            if 'limit_factor' in item:
                if max_omega_override is not None:
                    max_omega = max_omega_override[idx]
                else:
                    max_omega = item['max_omega']
                f = klobps(
                    item['rated_tau'], item['limit_factor'],
                    max_omega, abs(stall_torque[idx])
                )
                omega_range = np.linspace(0, max_omega, 20)
                tau = np.array([f(w) for w in omega_range])
                char = dict()
                r = np.abs(item['ratio'])
                char['max'] = np.vstack(
                    (
                        omega_range * 2 * np.pi / 60 / r,
                        np.ones(np.shape(omega_range)) * item['max_tau']
                    )
                )
                char['s1'] = np.vstack((omega_range * 2 * np.pi / 60 / r, tau))
                self.robot.drives[idx].load_characteristic(char, 'after_ratio')

    def run_one_step(self, q, q_dot, q_ddot):
        self.robot.k(q)
        self.robot.ne(q_dot, q_ddot, self.gravity)
        self.robot.solve_drivetrain(q_dot, q_ddot)
        q_cmd_capacitor = list()
        q_cmd_capacitor.append(q)
        self.q_cmd_ser = np.array(q_cmd_capacitor)
        self.t_ser = np.array([0])
        self.tcp_ser = np.array([self.robot.joints[-1].origin1])
        self.tau_motor_ser = np.array(
            [np.array([d.tau_drive for d in self.robot.drives])]
        )

    @staticmethod
    def read_trace(filename, dataname, k=100):
        """
        access a trace file and read the specified data field
        Inputs:
            fileName: absolute directory to the trace file
            dataName: ask mada guys for what names are available
        """
        tracedef_path = os.path.abspath(filename + '.dat')
        with open(tracedef_path, "rb") as f1:
            text = f1.read()
        blocks = text.split(b'#BEGINCHANNELHEADER')
        time_block = blocks[1]
        if time_block.find(b"Zeit") == -1:
            pass
        ts = float(
            (time_block[time_block.find(b'241,') + len("241,"):].splitlines())[0]
        )
        n = len(blocks[2:])
        column_index = None
        for block in blocks[2:]:
            lines = block.splitlines()
            if lines[1] != b'200,' + dataname.encode("ascii"):
                continue
            for line in lines:
                if line.find(b'221,') == -1:
                    continue
                index = line.find(b'221,') + len("221,")
                column_index = int(line[index:])
                break
            break
        if column_index is None:
            print('target signal is not found')
            result = None
            ts = None
            return result, ts
        tracedata_path = os.path.abspath(filename + ".r64")
        with open(tracedata_path, "rb") as f2:
            data_all = f2.read()
        data_length = int(len(data_all) * (k/100.0))
        result_all = [
            struct.unpack("d", data_all[i:i+8])[0]
            for i in range(0, data_length-8, 8)
        ]
        result = np.array(result_all[column_index-1::n])
        return result, ts

    def load_trajectory(
        self, filename_fraction, percentage, ratio_mask=None,
        speed_override=1, trace_chnl='ipo', trace_type='cmd'
    ):
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
        ts = None
        n = self.robot.num_axes
        if ratio_mask is None:
            ratio_mask = np.ones(n)
        # for i in range(6):
        if 'next' in trace_chnl.lower():
            for i in range(n):
                value, ts = self.read_trace(
                    filename_fraction + '#' + str(i + 1),
                    "Sollposition",
                    percentage
                )
                pos_value = value * np.pi / 180 * 1e-6 / np.array(ratio_mask[i])
                q_cmd_capacitor.append(pos_value)
                speed_value = np.gradient(pos_value, ts)
                q_dot_cmd_capacitor.append(speed_value)
        elif 'ipo' in trace_chnl.lower():
            for i in range(n):
                if 'cmd' in trace_type.lower():
                    value, ts = self.read_trace(
                        filename_fraction,
                        "AxisPos_CmdIpo{}".format(str(i+1)),
                        percentage
                    )
                    q_cmd_capacitor.append(value / np.array(ratio_mask[i]))
                    value, ts = self.read_trace(
                        filename_fraction,
                        "AxisVel_CmdIpo{}".format(str(i+1)),
                        percentage
                    )
                    q_dot_cmd_capacitor.append(value / np.array(ratio_mask[i]))
                elif 'act' in trace_type.lower():
                    value, ts = self.read_trace(
                        filename_fraction,
                        "AxisPos_Act{}".format(str(i + 1)),
                        percentage
                    )
                    q_cmd_capacitor.append(value / np.array(ratio_mask[i]))
                    value, ts = self.read_trace(
                        filename_fraction,
                        "AxisVel_Act{}".format(str(i + 1)),
                        percentage
                    )
                    q_dot_cmd_capacitor.append(value / np.array(ratio_mask[i]))
                else:
                    print('incorrect trace type')
        else:
            print('incorrect trace chnl')
            return
        self.q_cmd_ser = (np.array(q_cmd_capacitor)).T
        if len(q_dot_cmd_capacitor[-1]) < len(q_dot_cmd_capacitor[-2]):
            q_dot_cmd_capacitor[-1] = np.hstack(
                (q_dot_cmd_capacitor[-1], q_dot_cmd_capacitor[-1][-1])
            )
        self.q_dot_cmd_ser = (np.array(q_dot_cmd_capacitor)).T
        self.ts = ts / speed_override
        self.ratioMask = ratio_mask
        self.t_ser = np.linspace(
            0, (len(self.q_cmd_ser)-1) * self.ts, len(self.q_cmd_ser)
        )

    def sim_inv_dynamic(
        self, q=None, qd=None, qdd=None, t=None, ts=None, ratio_mask=None
    ):
        """
        Inverse dynamics calculation based on axis angle trajectories
        """
        if q is None:
            self.q_ddot_cmd_ser = np.gradient(self.q_dot_cmd_ser, self.ts)[0]
        else:
            self.q_cmd_ser = q
            self.q_dot_cmd_ser = qd
            self.q_ddot_cmd_ser = qdd
            self.ts = ts
            if ratio_mask is None:
                ratio_mask = np.ones(self.robot.num_axes)
            self.ratioMask = ratio_mask
            self.t_ser = t
        data_len = len(self.q_ddot_cmd_ser)
        num_axes = self.robot.num_axes
        tau_motor_capacitor = []
        tau_joint_capacitor = []
        friction_capacitor = []
        f_joint_capacitor = np.zeros([len(self.robot.bodies), 3, data_len])
        tau_joint_3d_capacitor = np.zeros([len(self.robot.bodies), 3, data_len])
        tcp_capacitor = []

        bar = pyprind.ProgBar(data_len, track_time=True,
                              title='computing dynamic...', stream=1)
        for i in range(data_len):
            self.robot.k(self.q_cmd_ser[i, :])
            self.robot.ne(
                self.q_dot_cmd_ser[i, :],
                self.q_ddot_cmd_ser[i, :],
                self.gravity
            )
            self.robot.solve_drivetrain(
                self.q_dot_cmd_ser[i, :],
                self.q_ddot_cmd_ser[i, :]
            )
            tcp_capacitor.append(self.robot.joints[-1].origin1)
            tau_motor_capacitor.append(
                [self.robot.drives[j].tau_drive for j in range(num_axes)]
            )
            tau_joint_capacitor.append(
                [self.robot.drives[j].tau_joint for j in range(num_axes)]
            )
            friction_capacitor.append(
                [self.robot.drives[j].tau_friction for j in range(num_axes)]
            )
            for j, body in enumerate(self.robot.bodies):
                f_joint_capacitor[j, :, i] = body.f
                tau_joint_3d_capacitor[j, :, i] = body.tau
            bar.update()

        self.tau_motor_ser = np.array(tau_motor_capacitor)
        self.tau_joint_ser = np.array(tau_joint_capacitor)
        self.friction_ser = np.array(friction_capacitor)
        self.f_joint_ser = np.array(f_joint_capacitor)
        self.tau_joint_3d_ser = np.array(tau_joint_3d_capacitor)
        self.tcp_ser = np.array(tcp_capacitor)

    def generate_trajectory(self, trajectory):
        """
        Initialize a path planning instance. And generate a trajectory defined as 
        q(t) series. Only Adept is supported now.
        :param trajectory: trajectory configuration
        :return: 
        """
        self.trajectory_generator = TrajectoryGenerator()
        if trajectory['type'] is 'adept':
            self.trajectory_generator.adept(trajectory['v_max'],
                                            trajectory['T'],
                                            trajectory['N'],
                                            trajectory['offset'],
                                            trajectory['rotation'],
                                            trajectory['orientation'])
        self.ts = trajectory['T'] / trajectory['N']
        self.t_ser = np.linspace(0, (trajectory['N'] - 1) * self.ts, trajectory['N'])
        # plt.figure()
        # plt.plot(self.t_ser, self.trajectory_generator.trajectory[0, :])
        # plt.figure()
        # plt.plot(self.t_ser, self.trajectory_generator.trajectory[1, :])
        # plt.figure()
        # plt.plot(self.t_ser, self.trajectory_generator.trajectory[2, :])
        # plt.show(block=False)
        self.q_cmd_ser = np.array(
            list(
                map(self.robot.ik, self.trajectory_generator.trajectory.T)
            )
        )
        self.q_dot_cmd_ser = np.gradient(self.q_cmd_ser, self.ts)[0]


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
        self.sdr = SymDyRobot(
            dimension_lo, fr, mass_centers_lo, masses, its,
            abs(self.gravity),
            if_simplify=True
        )
        self.sdr.generate_equation()

    def set_symbolic_simulation(self, tr, r, ts, t_end, x0, kpd, ki, i0, i_bound):
        self.sdr.environment(tr, r, ts, t_end, x0)
        self.sdr.design_control(kpd, ki, i0, i_bound)

    def run_symbolic_simulation(self):
        start_time = time.clock()
        self.sdr.run()
        print('computing time: {}sec'.format(round(time.clock() - start_time, 2)))
        self.sdr.show()

    def show_cm(self, ax):
        motors = []
        stators = []
        rotors = []
        for item in self.mass_list:
            if 'name' in item:
                idx = list(self.frame_config.keys()).index(item['nest'])
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
                else:
                    print('Only motor and gear components have key "name"')
                    return
                ax.plot(ar([cm_gl[0]]), ar([cm_gl[1]]), ar([cm_gl[2]]),
                        marker, markersize=markersize)
        return {'motor': motors, 'stator': stators, 'rotor': rotors}

    def snapshot(self, **kwargs):
        """
        static image of the robot in present pose
        For drawing two robots in one figure, call in this way:
            ax = simulation_a.snapshot()
            ax = simulation_b.snapshot(ax = ax, G = G_a2b)
            where G_a2b is the homogenuous transformation from a to b
        """
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

        arrow_color = ["r", "g", "b"]
        head1 = (G @ np.hstack((self.robot.tool2world(np.array([0,0,0.1]))[0:3],
                                ar([1]))))[0:3]
        head2 = (G @ np.hstack((self.robot.tool2world(np.array([0,0.1,0]))[0:3],
                                ar([1]))))[0:3]
        head3 = (G @ np.hstack((self.robot.tool2world(np.array([0.1,0,0]))[0:3],
                                ar([1]))))[0:3]
        arrow_heads = [head1, head2, head3]
        tail = (G @ np.hstack((self.robot.joints[-1].origin1, ar([1]))))[0:3]
        for idx, head in enumerate(arrow_heads):
            line, = ax.plot(ar([tail[0], head[0]]),
                            ar([tail[1], head[1]]),
                            ar([tail[2], head[2]]),
                            arrow_color[idx],lw=1)
        line, = ax.plot(ar([0]), ar([0]), ar([0]), 'gs', markersize=16)
        line, = ax.plot(
            ar([G[0][3]]), ar([G[1][3]]), ar([G[2][3]]), 'gs', markersize=16
        )
        return ax

    def get_result(self):
        """
        generate a result object for further analysis
        :return: SimulationResult instance 
        """
        if self.q_cmd_ser is None:
            sr = StaticAnalysis(self.robot)
        else:
            sr = SimulationAnalysis(
                self.robot,
                self.q_cmd_ser, self.q_dot_cmd_ser,
                self.tau_motor_ser, self.tau_joint_ser,
                self.f_joint_ser, self.tau_joint_3d_ser,
                self.tcp_ser,
                self.t_ser,
                self.ts
            )
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
                orange, lw=1.5
            )
            self.ani_links.append(line)
        self.ani_joints = []
        for joint in js:
            line, = self.ax.plot(
                ar([joint.origin1[0]]),
                ar([joint.origin1[1]]),
                ar([joint.origin1[2]]),
                'o', markeredgecolor="b", markerfacecolor="none", ms=8, lw=2
            )
            self.ani_joints.append(line)
        self.ani_Trajectory, = self.ax.plot(
            self.tcp_ser[:1, 0],
            self.tcp_ser[:1, 1],
            self.tcp_ser[:1, 2],
            'm--', lw=1
        )
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
        # self.tau1_text = self.ax.text(0.45, -0.7, 0.8, "T2:")
        # self.tau2_text = self.ax.text(0.45, -0.7, 0.7, "T3:")
        # self.tau3_text = self.ax.text(0.45, -0.7, 0.6, "T4:")
        # self.tau4_text = self.ax.text(0.45, -0.7, 0.5, "T5:")
        # self.tau5_text = self.ax.text(0.45, -0.7, 0.4, "T6:")
        # self.tau6_text = self.ax.text(0.45, -0.7, 0.3, "T7:")
#
        self.ax.plot(ar([0]), ar([0]), ar([0]), 'gs', markersize=8)
#
        return self.ani_links, self.ani_joints, self.ani_Trajectory,\
               self.x_text, self.y_text, self.z_text, self.t_text, self.arrow\
               # self.tau1_text, self.tau2_text, self.tau3_text, self.tau4_text,\
               # self.tau5_text, self.tau6_text,\
               # self.arrow

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
        # self.tau1_text.set_text("T1: %3.4f" % self.tau_motor_ser[i, 0])
        # self.tau2_text.set_text("T2: %3.4f" % self.tau_motor_ser[i, 1])
        # self.tau3_text.set_text("T3: %3.4f" % self.tau_motor_ser[i, 2])
        # self.tau4_text.set_text("T4: %3.4f" % self.tau_motor_ser[i, 3])
        # self.tau5_text.set_text("T5: %3.4f" % self.tau_motor_ser[i, 4])
        # self.tau6_text.set_text("T6: %3.4f" % self.tau_motor_ser[i, 5])
#
        return self.ani_links, self.ani_joints, self.ani_Trajectory,\
               self.x_text, self.y_text, self.z_text, self.t_text, self.arrow\
               # self.tau1_text, self.tau2_text, self.tau3_text, self.tau4_text,\
               # self.tau5_text, self.tau6_text,\
               # self.arrow

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
        sol = odeint(
            dyn.dyn, y0, t,
            args=(
                self.robot, self.gravity, dyn.control,
                Rh, Rv, trajectory_cmd, (kp, kd), threshold
            ),
            rtol=5e-5, atol=1e-5
        )
        return sol

    def solve_brake(self, q0, qd0, tau_brake, t_end=0.6, num_sample=2500):
        """
        solve the forward dynamic problem in emergency brake case
        """
        y0 = np.hstack((q0, qd0))
        t = np.linspace(0, t_end, num_sample)
        print('solving forward dynamic')
        Rh, Rv = get_all_friction_in_array(self.robot)
        ratio = np.array([drive.ratio for drive in self.robot.drives])
        tau_brake_joint = tau_brake * ratio
        threshold = 0.0001
        sol = odeint(
            dyn.dyn, y0, t,
            args=(
                self.robot, self.gravity, dyn.brake,
                Rh, Rv, None, tau_brake_joint, threshold),
            rtol=5e-5, atol=1e-5
        )
        return sol
