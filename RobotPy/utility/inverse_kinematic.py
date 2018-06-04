# -*- coding: utf-8 -*-

import numpy as np
from utility.u_math import rotation, h, triangle, solveEuler

ar = np.array


def ik_industry(tcp, geometry, st=None):
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
    d = np.linalg.norm(geometry[5].origin0[[0, 2]] - \
                       geometry[7].origin0[[0, 2]])
    R06 = rotation(A, B, C, "zyx")
    G_gl_tcp = h(R06, [x, y, z])
    hand = (G_gl_tcp @ ar([-d, 0, 0, 1]))[0:3]
    theta1 = np.arctan2(hand[1], hand[0])
    A5 = geometry[5].origin0[[0, 2]]
    A3 = geometry[3].origin0[[0, 2]]
    A2 = geometry[2].origin0[[0, 2]]
    l21 = A5[1] - A3[1]
    l22 = A5[0] - A3[0]
    theta31 = np.arctan2(l21, l22)
    l23 = np.linalg.norm(A5 - A3)
    l1 = np.linalg.norm(A3 - A2)
    l2 = l23
    joint1 = geometry[1]
    joint2 = geometry[2]
    origin2 = joint2.origin0
    origin2[1] = 0
    joint1.twist(-theta1)
    joint2_newO = (joint1.G_indv @ np.hstack((origin2, ar([1]))))[0:3]
    l3 = np.linalg.norm(hand - joint2_newO)
    delta_big = triangle(l1, l2, l3)
    theta21 = np.arctan2(hand[2] - joint2_newO[2],
                         np.linalg.norm(hand[[0, 1]] - joint2_newO[[0, 1]]))
    theta22 = delta_big[1]
    theta2 = -(theta21 + theta22)
    theta32 = delta_big[2]
    theta3 = np.pi + theta31 - theta32
    R03 = rotation(theta1, theta2, theta3, "zyy")
    R36 = R03.T @ R06
    theta4, theta5, theta6 = solveEuler(R36)
    return ar([-theta1, theta2, theta3, -theta4, theta5, -theta6])


def ik_scara(tcp, geometry, st=None):
    """
    Inverse kinematics for SCARA type robot (4-axis)
        zero position
        XY-plane                              XZ-plane            __
                                                                  ||
                                                        __________||_
        ^                                              |          || |
      y |                                              |          || |
        |    x                                  _______|__________||_|
        O----->------O----------XD          -  (     _____)      -||- ---> TCP orientation 0
     Joint1        Joint2     Joint3&4      |   |z^ |                      q3 position 0
          \         /\          /           H   | | |
              L1          L2                _  _| |_|___>x
                                                origin
    Input:
        1) p_cartesian - {"origin":np.array([x, y, z]), "orientation":theta}
            - world frame is defined as robot root
            - x,y,z : unit mm
            - theta : angle with x positive direction, unit rad, range [-pi,pi]
        2) geometry - np.array([L1, L2, H])
            - L1 : length of link 1
            - L2 : length of link 2
            - H  : length
        3) ST - 2-bit string binary marker for solution selection
                e.g. ST='00' - '[bit1][bit0]'
            - bit 0 :  '0' -> q2>0 (right-elbow)
                       '1' -> q2<=0 (left-elbow)
            - bit 1 :  '0' -> |q1|<pi
                       '1' -> |q1|>=pi
    Output:
        q - np.array([q1, q2, q3, q4])
              ~ q1, q2, q4 unit mm
              ~ q3 unit rad
    """
<<<<<<< HEAD

    x, y, z = tcp["origin"][0], tcp["origin"][1], tcp["origin"][2]
    theta = tcp["orientation"]

    L1 = np.linalg.norm(
             geometry[2].origin0[[0, 1]] - geometry[1].origin0[[0, 1]]
         )
    L2 = np.linalg.norm(
             geometry[3].origin0[[0, 1]] - geometry[2].origin0[[0, 1]]
         )
    H = geometry[5].origin0[2]

=======
    if st is None:
        st = '00'
    if type(tcp) is dict:
        x, y, z = tcp["tcp"]
        A, B, C = tcp["orientation"]
    elif len(tcp) == 3:
        x, y, z = tcp[0:3]
        A, B, theta = 0, 0, 0
    elif len(tcp) == 6:
        x, y, z, A, B, theta = tcp

    L1 = np.linalg.norm(
        geometry[2].origin0[[0, 1]] - geometry[1].origin0[[0, 1]]
    )
    L2 = np.linalg.norm(
        geometry[3].origin0[[0, 1]] - geometry[2].origin0[[0, 1]]
    )
    H = geometry[5].origin0[2]
>>>>>>> 58b65ab95b26b7a4fd909560928b1d3c920ad08f
    # solve q1, q2
    # ax^2 + bx + c = 0
    D = L1 ** 2 - L2 ** 2 + x ** 2 + y ** 2
    a = (y / x) ** 2 + 1
    b = -D * y / (x ** 2)
    c = (D / 2 / x) ** 2 - L1 ** 2
    d = b ** 2 - 4 * a * c
    root_judge = np.sign(d)

    if root_judge == 1:
        y_1 = np.array([(-b + np.sqrt(d)) / 2 / a, (-b - np.sqrt(d)) / 2 / a])
        x_1 = D / 2 / x - y / x * y_1
        q1_temp = np.arctan2(y_1, x_1)
        q2_temp = np.arctan2(y - y_1, x - x_1) - q1_temp
        q1_index = np.abs(q2_temp) >= np.pi
        q2_temp[q1_index] = q2_temp[q1_index] - np.sign(
            q2_temp[q1_index]) * 2 * np.pi
        if st[1] == '0':
            q1 = q1_temp[q2_temp > 0][0]
            q2 = q2_temp[q2_temp > 0][0]
        else:
            q1 = q1_temp[q2_temp < 0][0]
            q2 = q2_temp[q2_temp < 0][0]

    elif root_judge == -1:  #
        print('Position out of range. (X,Y distance not reachable)')
        q = [np.nan, np.nan, np.nan, np.nan]
        return q

    elif root_judge == 0:  # only 1 solution exists
        q1 = np.arctan2(y, x)
        y_1 = -b / (2 * a)
        x_1 = D / (2 * x) - y / x * y_1
        A2 = np.array([x_1, y_1])
        A3 = np.array([x, y])
        if np.linalg.norm(A2 - A3) > L1 + L2:  # axis 2 could never be = 180 degree
            print('Position out of range. (Axis 2 not reachable = 180 deg)')
            q = [np.nan, np.nan, np.nan, np.nan]
            return q
        q2 = 0
    else:
        print('inverse kinematics failure')
        return

    if st[0] == '1':
        q1 = q1 - np.sign(q1) * 2 * np.pi
    # Solve q3
    q3 = H - z
    if q3 < 0:
        q = [np.nan, np.nan, np.nan, np.nan]
        print('Position out of range. (Z distance not reachable)')
        return q

    # Solve q4
    q4 = theta - q1 - q2
    if np.abs(q4) > np.pi:
        q4 = q4 - np.sign(q4) * 2 * np.pi

    q = np.array([q1, q2, q3, q4])
    return q






