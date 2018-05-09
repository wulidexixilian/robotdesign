# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 14:51:47 2017
Kinematics
@author: pei.sun
"""
import numpy as np
from model.m_math import rotation, h, solveZYX, solveEuler, triangle
from model.m_component import Body, Joint, Drive

ar = np.array

class Kinematics():

    idDict = {
                 "groundbase":0, "rotationcolumn":1, "linkarm":2, "arm":3,
                 "handbase":4, "handwrist":5, "handflange":6, "tcp":7,
              }

    def __init__(self, dimensions, coordinateConfigurationDict):
        accumulationDisp = ar([0,0,0])
        self.bodies = []
        self.joints = []
        for i, component in enumerate(dimensions):
            axOrientation = coordinateConfigurationDict[component["name"]][0]
            nxOrientation = coordinateConfigurationDict[component["name"]][1]

            #a matrix to transfer everything in Kuka body coordinate into
            #unified natrual body coordinate
            # z
            # ^
            # |
            # y --> x
            # which aligns with the world coordinate when q=0

            align2Base = rotation(axOrientation[0],
                                  axOrientation[1],
                                  axOrientation[2],
                                  order="xyz")
            base2Nxt = rotation(nxOrientation[0],
                                nxOrientation[1],
                                nxOrientation[2],
                                order="xyz")
            # align 2 axes accordingly
            ax = align2Base @ ar([0, 0, 1])
            nx = align2Base @ base2Nxt @ ar([0, 0, 1])
            gearOffset = nx*component["offset"]
            displacement2nx = align2Base @ ar(component["displacement"])
            body = Body(displacement2nx, component["name"], i)
            self.bodies.append(body)
            joint = Joint(accumulationDisp, ax, align2Base, i)
            self.joints.append(joint)
            accumulationDisp = accumulationDisp + displacement2nx + gearOffset

        tcpOrientation = coordinateConfigurationDict["tcp"][0]
        align2Tcp = rotation(tcpOrientation[0],
                                  tcpOrientation[1],
                                  tcpOrientation[2],
                                  order="zyx")
        tcpAx = align2Tcp @ ar([0, 0, 1])
        tcp = Joint(accumulationDisp, tcpAx, align2Tcp, i+1)
        self.joints.append(tcp)
        self.num_axes = len(self.bodies) - 1

    def k(self, q):
        """forward kinematics"""
        self.q = q
        q_ext = np.hstack((ar([0]), ar(q), ar([0])))
        G_gl = np.identity(4)
        for i, joint in enumerate(self.joints):
            joint.twist(q_ext[i])
            G_gl = G_gl @ joint.G_indv
            joint.setGlobalG(G_gl)
            if i == 0:
                k = 0
            else:
                k = i-1
            newPosition = self.joints[k].G_gl @\
                          np.hstack((joint.origin0, ar([1])))
            joint.setPose(newPosition[0:3])

    def ik(self, tcp):
        """
        inverse kinematics, not a universal method. Only for configuration with:
        1) 6 rotation joints
        2) z1 ^; z2 x; z3 x; z4 <; z5 x; z6 <
        3) a common intersection point of A4, A5, A6 axes.
        4) offset only on arm link (flange 2 is not on the axis of flange 1)

                 ___l22____A5
            l21 |A3
               /
              /
         l1  /
            /
         A2/
         Input:
             tcp = {"origin":np.array([x, y, z]), "orientation":np.array([A, B, C])}

        """
        if type(tcp) is dict:
            x, y, z = tcp["tcp"]
            A, B, C = tcp["orientation"]
        elif len(tcp) == 3:
            x, y, z = tcp[0:3]
            A, B, C = 0, 0, 0
        elif len(tcp) == 6:
            x, y, z, A, B, C = tcp
        d = np.linalg.norm(self.joints[5].origin0[[0,2]] -\
                           self.joints[7].origin0[[0,2]])
        R06 = rotation(A,B,C,"zyx")
        G_gl_tcp = h(R06, [x, y, z])
        hand = (G_gl_tcp @ ar([-d, 0, 0, 1]))[0:3]

        theta1 = np.arctan2(hand[1],hand[0])
        A5 = self.joints[5].origin0[[0,2]]
        A3 = self.joints[3].origin0[[0,2]]
        A2 = self.joints[2].origin0[[0,2]]

        l21 = A5[1] - A3[1]
        l22 = A5[0] - A3[0]
        theta31 = np.arctan2(l21, l22)
        l23 = np.linalg.norm(A5 - A3)

        l1 = np.linalg.norm(A3 - A2)
        l2 = l23

        joint1 = self.joints[1]
        joint2 = self.joints[2]
        origin2 = joint2.origin0
        origin2[1] = 0
        joint1.twist(-theta1)
        joint2_newO = (joint1.G_indv @ np.hstack((origin2, ar([1]))))[0:3]
        l3 = np.linalg.norm(hand - joint2_newO)
        delta_big = triangle(l1, l2, l3)

        theta21 = np.arctan2(hand[2] - joint2_newO[2],
                             np.linalg.norm(hand[[0,1]] - joint2_newO[[0,1]]))
        theta22 = delta_big[1]
        theta2 = -(theta21 + theta22)
        theta32 = delta_big[2]
        theta3 = np.pi + theta31 - theta32

        R03 = rotation(theta1, theta2, theta3, "zyy")

        R36 = R03.T @ R06
        theta4, theta5, theta6 = solveEuler(R36)
        return ar([-theta1, theta2, theta3, -theta4, theta5, -theta6])

    def local2world(self, pose_local, ref, target="cs"):
        """
        natrual local cs to world cs
        """
        if isinstance(ref, str):
            idx = self.idDict[ref]
        else:
            idx = ref

        if target=="cs":
            if len(pose_local)==6:
                [x, y, z, A, B, C] = pose_local
            else:
                [x, y, z, A, B, C] = np.hstack((pose_local, ar([0, 0, 0])))

            coord_local = h(rotation(A, B, C, order="zyx"),
                                 ar([x,y,z]) + self.joints[idx].origin0)
            coord_world = self.joints[idx].G_gl @ coord_local
            A_gl, B_gl, C_gl = solveZYX(coord_world[0:3, 0:3])
            [x_gl, y_gl, z_gl] = coord_world[0:3, 3]
            return ar([x_gl, y_gl, z_gl, A_gl, B_gl, C_gl])
        elif target=="vector":
            v_gl = self.joints[idx].G_gl[0:3,0:3] @ pose_local
            return v_gl
        else:
            print("invalid input")
            return

    def kuka2local(self, pose_kukaLocal, ref, target="cs"):
        """
        kuka local cs to natrual local cs
        """
        if isinstance(ref, str):
            idx = self.idDict[ref]
        else:
            idx = ref

        if target == "cs":
            if len(pose_kukaLocal)==6:
                [x, y, z, A, B, C] = pose_kukaLocal
            else:
                [x, y, z, A, B, C] = np.hstack((pose_kukaLocal, ar([0, 0, 0])))

            g_kLo = h(self.joints[idx].align, [0, 0, 0])
            coord_kLo = h(rotation(A, B, C, order="zyx"), [x,y,z])
            coord_local = g_kLo @ coord_kLo
            A_lo, B_lo, C_lo = solveZYX(coord_local[0:3, 0:3])
            [x_lo, y_lo, z_lo] = coord_local[0:3, 3]
            return ar([x_lo, y_lo, z_lo, A_lo, B_lo, C_lo])
        elif target == "vector":
            v_lo = self.joints[idx].align @ pose_kukaLocal
            return v_lo
        else:
            print("invalid input")
            return

    def tool2world(self, p):
        """
        p = (x, y, z, A:z, B:y, C:x) given in tool cs, convert p to world cs
        """
        temp = self.kuka2local(p, 7)
        tcp = self.local2world(temp, 7)
        return tcp

    def jacobian(self):
        """
        generate the Jacobian Matrix based on current kinematics
        """
        p_e = self.joints[-1].origin1
        JT = np.array([]).reshape(0,6)
        for joint in self.joints[1:-1]:
            p_i = joint.origin1
            z_i = joint.axis1
            xi_i_tilt = np.hstack((np.cross(z_i, p_e - p_i), z_i))
            JT = np.vstack((JT, xi_i_tilt))
        return JT.T

    def force2tau_static(self, endForce):
        J = self.jacobian()
        tau = J.T @ np.array(endForce)
        return tau

    def tau2force_static(self, tau):
        J = self.jacobian()
        invJT = np.linalg.inv(J.T)
        force = invJT @ np.array(tau)
        return force

    def get_ik(self):
        """
        ik function
        :return: a function
        """
        return self.ik


class Dynamics(Kinematics):
    """
    Dynamic model with iterative Newton-Euler inverse method.
    Extended from Kinematics
    """
    def __init__(self, componentList, massList,
                 driveTrainList, coordinateConfigurationDict):
        """
        Construct kinematic model and assign mass and moment
        of inertia to every body object
        """
        # kinematics model
        super(Dynamics, self).__init__(componentList, coordinateConfigurationDict)
        # distribute mass to each body
        for mass in massList:
            idx = self.idDict[mass["nest"]]
            if idx == 7:
                body = self.bodies[idx-1]
                isLoad = True
            else:
                body = self.bodies[idx]
                isLoad = False
            # rotation aligns a kuka local cs to natrual body cs
            align = self.joints[idx].align
            body.add_mass(mass["cm"], mass["m"], mass["iT"], align, isLoad)
        # generate drive object to each driving joint
        # (joints[0] and joints[-1] are not included, [0] is the base surface,
        # and [-1] is flange surface)
        self.drives = []
        for joint in self.joints[1:-1]:
            drive = Drive(joint.id)
            self.drives.append(drive)
        # distribute drive train inertia and frictions
        for dPara in driveTrainList:
            if isinstance(dPara["nest"], str):
                dPara["nest"] = self.idDict[dPara["nest"]]
            drive = self.drives[dPara["nest"] - 1]
            drive.update(dPara["friction"], dPara["driveInertia"], dPara["ratio"])
            if 'characteristic_before_ratio' in dPara:
                drive.load_characteristic(dPara['characteristic_before_ratio'])
            if 'characteristic_after_ratio' in dPara:
                drive.load_characteristic(dPara['characteristic_after_ratio'],
                                          'after_ratio')

    def add_load(self, load):
        body = self.bodies[-1]
        align = self.joints[self.idDict['tcp']].align
        body.remove_mass(load["cm"], load["m"], load["iT"], align)

    def k(self, q):
        """
        extended from the father class version
        update kinematics info of each body and drive obj
        used for NE dynamic calculation.
        """
        # solve kinematics
        super(Dynamics, self).k(q)
        # update kinematics info for each body (like their new poses, coordinates...)
        for body in self.bodies:
            idx = body.id
            G_i = self.joints[idx].G_gl
            R_i = G_i[0:3, 0:3]
            z_gl = self.joints[idx].axis1
            cm_gl = self.local2world(body.cm, idx, "cs")[0:3]
            head_gl = self.joints[idx].origin1
            tail_gl = self.joints[idx + 1].origin1
            iT_gl = R_i @ body.iT @ R_i.T
            body.updateKinematics(z_gl, head_gl, tail_gl, cm_gl, iT_gl)
        # update kinematics infor for each drive (their axis orientation)
        for drive in self.drives:
            drive.setAxis(self.joints[drive.id].axis1)

    def ne(self, q_dot, q_ddot, gravity):
        """
        Inverse Dynamics calculation: (q, q_dot, q_ddot) -> (f,tau)
        Iterative Newton_Euler Method in WCS
        """
        zeros = np.array([0, 0, 0])
        # expand calculation to the ground base, which has always zero motion
        q_dot = np.hstack((ar([0]), q_dot))
        q_ddot = np.hstack((ar([0]), q_ddot))
        # initialize forward iterations
        omega_im1 = zeros
        alpha_im1 = zeros
        acc_e_im1 = zeros
        # forward iterations for omega, alpha, acc
        for i, body in enumerate(self.bodies):
            body.ne_fwd_iter(q_dot[i], q_ddot[i],
                             omega_im1, alpha_im1, acc_e_im1)
            # prepare for next iter
            omega_im1 = body.omega
            alpha_im1 = body.alpha
            acc_e_im1 = body.acc_e
        # initialize inversed iterations
        f_ip1 = zeros
        tau_ip1 = zeros
        # inversed iterations for f, tau
        # term_r = []
        tau_ar_axes = []
        for body in reversed(self.bodies):
            body.ne_bwd_iter(f_ip1, tau_ip1, gravity)
            # prepare for next iter
            f_ip1 = body.f
            tau_ip1 = body.tau
            tau_ar_axes.insert(0, np.dot(body.z_gl, body.tau))
        return np.array(tau_ar_axes[1:])

    def solve_drivetrain(self, q_dot, q_ddot):
        """
        solve drive torque (with friction and torque to accelerate drivetrain inertia)
        """
        self.fr_thresholds = np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
        for i, drive in enumerate(self.drives):
            idx = drive.id
            tau = self.bodies[idx].tau
            # idx - 1 since drive id starts from 1, but q_ddot index starts from 0
            # it starts from 1 because there is no drive to the ground base.
            drive.getDriveTau(q_dot[idx-1], q_ddot[idx-1], tau,
                              self.fr_thresholds[i])

    def get_inertia_matrix(self):
        """
        calculate inertia matrix M by M * [1;0;0;0;0;0] + B*qd_0 + K*q_0 = T
        then M[:, 1] = T
        Therefore, calculate T by NE based on pseudo acc and zero speed
        in zero gravity
        do this for each column        
        :return: M inertia matrix in joint space
        """
        n = self.num_axes
        M = np.zeros([n, n])
        # calculate inertia matrix M by M * [1;0;0;0;0;0] + B*qd_0 + K*q_0 = T
        # then M[:, 1] = T
        # Therefore, calculate T by NE based on pseudo acc and zero speed
        # in zero gravity
        # do this for each column
        for idx in range(n):
            qdd_pseudo = np.zeros(n)
            qdd_pseudo[idx] = 1
            tau_pseudo = self.ne(np.zeros(6), qdd_pseudo, np.zeros(3))
            M_col = tau_pseudo
            M[:, idx] = M_col
        return M