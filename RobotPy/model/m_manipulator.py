# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 14:51:47 2017
Kinematics
@author: pei.sun
"""
import numpy as np
from utility.u_math import rotation, h, solveZYX
from model.m_component import Body, Joint, Drive

ar = np.array


class Kinematics:

    def __init__(self, dimensions, frame_config):
        accumulation_displacement = ar([0, 0, 0])
        self.bodies = []
        self.joints = []
        self.q = None
        self.link_names = list(frame_config.keys())
        for i, component in enumerate(dimensions):
            orientation_ax = frame_config[component["nest"]]['frame0']
            orientation_nx = frame_config[component["nest"]]['frame1']
            #a matrix to transfer everything in Kuka body coordinate into
            #unified natrual body coordinate
            # z
            # ^
            # |
            # y --> x
            # which aligns with the world coordinate when q=0
            align2Base = rotation(orientation_ax[0],
                                  orientation_ax[1],
                                  orientation_ax[2],
                                  order="xyz")
            base2Nxt = rotation(orientation_nx[0],
                                orientation_nx[1],
                                orientation_nx[2],
                                order="xyz")
            # align 2 axes accordingly
            ax = align2Base @ ar([0, 0, 1])
            nx = align2Base @ base2Nxt @ ar([0, 0, 1])
            gear_offset = nx * component["offset"]
            displacement2nx = align2Base @ ar(component["displacement"])
            body = Body(displacement2nx, component["nest"], i)
            self.bodies.append(body)
            if 'mode' in frame_config[component["nest"]].keys():
                joint_mode = frame_config[component["nest"]]['mode']
            else:
                joint_mode = 0
            joint = Joint(accumulation_displacement, ax, align2Base, i, joint_mode)
            self.joints.append(joint)
            accumulation_displacement = accumulation_displacement +\
                displacement2nx + gear_offset

        tcp_orientation = frame_config["tcp"]['frame0']
        align2tcp = rotation(
            tcp_orientation[0],
            tcp_orientation[1],
            tcp_orientation[2],
            order="xyz"
        )
        tcpAx = align2tcp @ ar([0, 0, 1])
        tcp = Joint(accumulation_displacement, tcpAx, align2tcp, i + 1)
        self.joints.append(tcp)
        self.num_axes = len(self.bodies) - 1
        self.inverse_dynamic = None

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
            new_position = self.joints[k].G_gl @\
                          np.hstack((joint.origin0, ar([1])))
            joint.setPose(new_position[0:3])

    def ik(self, tcp, st=None):
        if self.inverse_dynamic is None:
            print('set inverse dynamic method before solving')
            return
        geometry = self.joints
        q = self.inverse_dynamic(tcp, geometry, st)
        return q

    def local2world(self, pose_local, ref, target="cs"):
        """
        natrual local cs to world cs
        """
        if isinstance(ref, str):
            idx = self.link_names.index(ref)
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
            idx = self.link_names.index(ref)
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
        temp = self.kuka2local(p, self.num_axes+1)
        tcp = self.local2world(temp, self.num_axes+1)
        return tcp

    def jacobian(self):
        """
        generate the Jacobian Matrix based on current kinematics
        """
        p_e = self.joints[-1].origin1
        JT = np.array([]).reshape(0, 6)
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
    def __init__(
        self,
        component_list, mass_list, drivetrain_list, frame_config
    ):
        """
        Construct kinematic model and assign mass and moment
        of inertia to every body object
        """
        # kinematics model
        super(Dynamics, self).__init__(component_list, frame_config)
        # distribute mass to each body
        for mass in mass_list:
            # body_idx = self.link_dict_industry[mass["nest"]]
            body_idx = self.link_names.index(mass["nest"])
            if mass["nest"] == 'tcp':
                body = self.bodies[body_idx-1]
                is_load = True
            else:
                body = self.bodies[body_idx]
                is_load = False
            # rotation aligns a kuka local cs to natrual body cs
            align = self.joints[body_idx].align
            body.add_mass(mass["cm"], mass["m"], mass["iT"], align, is_load)
        # generate drive object to each driving joint
        # (joints[0] and joints[-1] are not included, [0] is the base surface,
        # and [-1] is flange surface)
        self.drives = []
        for joint in self.joints[1:-1]:
            drive = Drive(joint.id)
            self.drives.append(drive)
        # distribute drive train inertia and frictions
        for dPara in drivetrain_list:
            if isinstance(dPara["nest"], str):
                dPara["nest"] = self.link_names.index(dPara["nest"])
            drive = self.drives[dPara["nest"] - 1]
            drive.update(dPara["friction"], dPara["driveInertia"], dPara["ratio"])
            if 'characteristic_before_ratio' in dPara:
                drive.load_characteristic(dPara['characteristic_before_ratio'])
            if 'characteristic_after_ratio' in dPara:
                drive.load_characteristic(dPara['characteristic_after_ratio'],
                                          'after_ratio')

    def add_load(self, load):
        body = self.bodies[-1]
        align = self.joints[-1].align
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
            body.update_kinematics(z_gl, head_gl, tail_gl, cm_gl, iT_gl)
        # update kinematics infor for each drive (their axis orientation)
        for drive in self.drives:
            drive.set_axis(self.joints[drive.id].axis1)

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
            body.ne_fwd_iter(
                q_dot[i], q_ddot[i],
                omega_im1, alpha_im1, acc_e_im1
            )
            # prepare for next iter
            omega_im1 = body.omega
            alpha_im1 = body.alpha
            acc_e_im1 = body.acc_e
        # initialize inverse iterations
        f_ip1 = zeros
        tau_ip1 = zeros
        # inverse iterations for f, tau
        for body in reversed(self.bodies):
            body.ne_bwd_iter(f_ip1, tau_ip1, gravity)
            # prepare for next iter
            f_ip1 = body.f
            tau_ip1 = body.tau

    def get_free_axis_potential(self):
        return np.where(
            ar([self.joints[d.id].mode for d in self.drives]),
            ar([self.bodies[d.id].f[-1] for d in self.drives]),
            ar([self.bodies[d.id].tau[-1] for d in self.drives])
        )

    def solve_drivetrain(self, q_dot, q_ddot):
        """
        solve drive torque (with friction and torque to accelerate drivetrain inertia
        """
        self.fr_thresholds = np.array([0.01, 0.01, 0.01, 0.01, 0.01, 0.01])
        for idx, drive in enumerate(self.drives):
            idx_axis = drive.id
            if self.joints[idx_axis].mode == 0:
                tau = self.bodies[idx_axis].tau
            else:
                tau = self.bodies[idx_axis].f
            drive.get_drive_tau(
                q_dot[idx], q_ddot[idx],
                tau, self.fr_thresholds[idx]
            )

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
            self.ne(np.zeros(n), qdd_pseudo, np.zeros(3))
            tau_pseudo = self.get_free_axis_potential()
            M_col = tau_pseudo
            M[:, idx] = M_col
        return M