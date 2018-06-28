# -*- coding: utf-8 -*-
"""
Created on Wed Mar 15 16:32:46 2017
Compnents to form a robot
@author: pei.sun
"""
import numpy as np
import scipy.linalg as li
from utility.u_math import mass_combine, twist_coordinate, tensor
from utility.u_math import calc_friction, curve_min, pure_cross
from utility.u_math import fast_fwd_ne, fast_bwd_ne
# from numba import jitclass
# from numba import int32, float32

X = pure_cross


class Body:
    """ a rigid body """
    def __init__(self, dimension, name, idx):
        self.dimension = dimension
        self.name = name
        self.id = idx
        self.cm = np.array([0, 0, 0])
        self.m = 0
        self.iT = np.zeros((3, 3))
        self.omega = None # about cm in World
        self.alpha = None # about cm in World
        self.acc = None # about cm in World
        self.z_gl = None
        self.cm_gl = None
        self.r_hc = None
        self.r_ht = None
        self.r_tc = None
        self.iT_gl = None
        self.head_gl = None
        self.tail_gl = None
        self.acc_e = None
        self.f = None
        self.tau = None

    def add_mass(self, cm_new, m_new, iT_new_ar, align, isLoad=False):
        """
        add a new mass to body obj. Overall cm, iT, m are updated
        Local Coordinate Sys
        """
        iT_new = tensor(*iT_new_ar)
        cm = self.cm
        iT = self.iT
        m = self.m
        cm_new_aligned = align @ cm_new
        if isLoad:
            cm_new_aligned = cm_new_aligned + self.dimension
        iT_new_aligned = align @ iT_new @ align.T
        res = mass_combine(m, m_new, cm, cm_new_aligned, iT, iT_new_aligned)
        (self.m, self.cm, self.iT) = res

    def remove_mass(self, cm_target, m_target, iT_target_ar, align):
        """
        add a new mass to body obj. Overall cm, iT, m are updated
        Local Coordinate Sys
        """
        iT_target = tensor(*iT_target_ar)
        cm = self.cm
        iT = self.iT
        m = self.m
        cm_target_aligned = align @ cm_target
        cm_target_aligned = cm_target_aligned + self.dimension
        iT_target_aligned = align @ iT_target @ align.T
        res = mass_combine(-m, m_target, cm, cm_target_aligned, iT, -iT_target_aligned)
        (self.m, self.cm, self.iT) = res

    def resetMass(self):
        """ clear all mass data """
        self.cm = np.array([0, 0, 0])
        self.m = 0
        self.iT = np.identity([3,3])

    def update_kinematics(self, z_gl, head_gl, tail_gl, cm_gl, iT_gl):
        """ update kinematics dependent info for dynamics calculation """
        self.z_gl = z_gl
        self.cm_gl = cm_gl
        self.r_hc = head_gl - cm_gl
        self.r_ht = head_gl - tail_gl
        self.r_tc = tail_gl - cm_gl
        self.iT_gl = iT_gl
        self.head_gl = head_gl
        self.tail_gl = tail_gl

    def ne_fwd_iter(self, q_dot, q_ddot, omega_im1, alpha_im1, acc_e_im1):
        """
        Newton-Euler forward recursive step
        All calculations are in World Coordinate Sys
        :param q_dot: joint speed
        :param q_ddot: joint speed
        :param omega_im1: body angular speed of the previous body
        :param alpha_im1: body angular acc of the previous bocy
        :param acc_e_im1: linear speed of joint (end joint of the last body, 
                                                 first of this body)
        :return: 
        """
        # # Calculate CM angular velocity (WCS)
        # self.omega = omega_im1 + q_dot * self.z_gl
        # # Calculate CM angular acceleration (WCS)
        # self.alpha = alpha_im1 + self.z_gl * q_ddot +\
        #              X(self.omega, self.z_gl) * q_dot
        # # Calculate CM linear acc (WCS)
        # self.acc = acc_e_im1 + X(self.alpha, -self.r_hc) +\
        #            X(self.omega, X(self.omega, -self.r_hc))
        # # Calculate body end (flange2) linear acc (WCS)
        # self.acc_e = acc_e_im1 + X(self.alpha, -self.r_ht) +\
        #              X(self.omega, X(self.omega, -self.r_ht))
        self.omega, self.alpha, self.acc, self.acc_e = fast_fwd_ne(
            self.z_gl, self.r_hc, self.r_ht,
            q_dot, q_ddot, omega_im1, alpha_im1, acc_e_im1
        )

    def ne_bwd_iter(self, f_ip1, tau_ip1, gravity):
        """
        Newton-Euler backward recursive step
        All calculations are in World Coordinate Sys
        :param f_ip1: force about CM of next body in World 
        :param tau_ip1: torque about CM of next body in World
        :param gravity: gravity acc vector in World
        :return: 
        """
        # # Calculate force at CM without gravity included
        # self.f = f_ip1 + self.m * self.acc - self.m * gravity
        # # Calculate torque at CM without gravity torque included
        # self.tau = tau_ip1 - X(self.r_hc, self.f) + X(self.r_tc, f_ip1) +\
        # self.iT_gl @ self.alpha + X(self.omega, (self.iT_gl @ self.omega))
        self.f, self.tau = fast_bwd_ne(
            self.m, self.acc, self.r_hc, self.r_tc,
            self.iT_gl, self.omega, self.alpha,
            f_ip1, tau_ip1, gravity
        )


class Joint:
    """ abstract object defining the twist motion between two bodies """
    def __init__(self, origin0, axis0, align, idx, mode=0):
        self.origin0 = origin0
        self.origin1 = origin0
        self.axis0 = axis0
        self.axis1 = axis0
        self.align = align
        self.id = idx
        self.mode = mode
        #init homogenuous transformation
        if mode == 0:
            self.xi_hat = twist_coordinate(axis0, origin0)
        else:
            self.xi_hat = twist_coordinate(axis0, origin0, 1)
        self.G_gl = np.identity(4)
        self.G_indv = np.identity(4)

    def twist(self, theta):
        """ generate local homogenuous transformation matrix """
        self.G_indv = li.expm(self.xi_hat * theta)

    def setPose(self, newPosition):
        """ new position after motion """
        self.origin1 = newPosition
        self.axis1 = self.G_gl[0:3, 0:3] @ self.axis0

    def setGlobalG(self, G_gl):
        """
        global homogenuous transformation, action of previous joints are included
        """
        self.G_gl = G_gl


class Drive:
    """ drive torque and friction """
    def __init__(self, ref):
        self.id = ref
        self.drivetrain_inertia = 0
        self.ratio = 1
        self.Rh = 0
        self.Rv = 0
        self.Rz = 1
        self.z = None
        self.tau_joint = None
        self.tau_friction = None
        self.tau_drivetrain_inertia = None
        self.tau_drive = None
        self.characteristic_before_ratio = None
        self.characteristic_after_ratio = None
        self.char_group_before_ratio = []
        self.char_group_after_ratio = []

    def update(self, friction, new_inertia, ratio):
        # equivalent inertia over ratio conversion
        # self.driveInertia = (self.driveInertia + driveInertia) * ratio**2
        self.drivetrain_inertia = self.drivetrain_inertia * abs(ratio) + new_inertia
        self.ratio *= ratio
        self.Rh += friction[0]
        self.Rv += friction[1]
        self.Rz *= friction[2]

    def load_characteristic(self, char_dict, pos='before_ratio'):
        if pos is 'before_ratio':
            self.char_group_before_ratio.append(char_dict)
            if self.characteristic_before_ratio is None:
                self.characteristic_before_ratio = char_dict
            else:
                self.characteristic_before_ratio['s1'] = curve_min(
                    self.characteristic_before_ratio['s1'], char_dict['s1']
                )
                self.characteristic_before_ratio['max'] = curve_min(
                    self.characteristic_before_ratio['max'], char_dict['max']
                )
        elif pos is 'after_ratio':
            self.char_group_after_ratio.append(char_dict)
            if self.characteristic_after_ratio is None:
                self.characteristic_after_ratio = char_dict
            else:
                self.characteristic_after_ratio['s1'] = curve_min(
                    self.characteristic_after_ratio['s1'], char_dict['s1']
                )
                self.characteristic_after_ratio['max'] = curve_min(
                    self.characteristic_after_ratio['max'], char_dict['max']
                )

    def set_axis(self, z):
        self.z = z

    def get_drive_tau(self, q_dot, q_ddot, tau, fr_threshold):
        # joint torque along axis, a scalar
        self.tau_joint = np.dot(self.z, tau)
        # self.friction = self.Rh * np.sign(q_dot) + self.Rv * q_dot +\
        #                 (1-self.Rz)*abs(self.effectiveTau)*np.sign(q_dot)
        self.tau_friction = calc_friction(
            self.Rh, self.Rv, self.Rz, q_dot, self.tau_joint, fr_threshold
        )
        # extra torque to accelerate drivetrain
        self.tau_drivetrain_inertia = q_ddot * self.drivetrain_inertia
        # overall torque output of the drive motor
        self.tau_drive = (
            self.tau_joint + self.tau_drivetrain_inertia + self.tau_friction
        ) / self.ratio
