# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 17:26:10 2017

@author: pei.sun
"""
from sympy.matrices import Matrix
from sympy import symbols, simplify, solve
import numpy as np


def solve_drivetrain(dt, init, omega_axis):
    omega_last = init
    result = dict()
    for first, second in zip(dt[0:-1], dt[1:]):
        # symbols for velocities of each element
        omega_1st = symbols('omega_{}'.format(first['id']))
        omega_2nd = symbols('omega_{}'.format(second['id']))
        # define vectors for velocities in 3D
        omega_vec_1st = Matrix([0, 0, 0])
        omega_vec_2nd = Matrix([0, 0, 0])
        omega_vec_1st[first['axis']] = omega_1st
        omega_vec_2nd[second['axis']] = omega_2nd
        # define ratio as a 3*3 matrix
        r_1st = Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        r_2nd = Matrix([[0, 0, 0], [0, 0, 0], [0, 0, 0]])
        # The sign of ratio of the first element is toggled based on shapes of two
        # meshing elements. If they have the same shape,
        # then a negative is multiplied
        r_1st[second['axis'], first['axis']] = \
                (1 if first['shape'][1] is second['shape'][0] else -1) * first['n'][1]
        r_2nd[second['axis'], second['axis']] = second['n'][0]
        # Define the orbiting motion
        orbit_vec_1st = Matrix([0 if first['axisMotion'][0] is '0' else omega_axis[0],
                                0 if first['axisMotion'][1] is '0' else omega_axis[1],
                                0])
        orbit_vec_2nd = Matrix([0 if second['axisMotion'][0] is '0' else omega_axis[0],
                                0 if second['axisMotion'][1] is '0' else omega_axis[1],
                                0])
        # symbolic expression of planetary gears
        expr = r_1st * (omega_vec_1st + orbit_vec_1st) + \
               r_2nd * (omega_vec_2nd + orbit_vec_2nd) - \
               (r_1st + r_2nd) * orbit_vec_2nd
        # solve expression
        omega_res_2nd = solve(expr[second['axis']], omega_2nd)[0]
        # substitute omega solved in previous step
        omega_chain = omega_res_2nd.subs(omega_1st, omega_last)
        # prepare to be substituted into the next step
        omega_last = omega_chain
        # result
        mesh_id = first['id'] + second['id']
        result[mesh_id] = {'expression':     expr,
                           'solution_alone': omega_res_2nd,
                           'solution_chain': omega_chain}
    # print('{} : {}'.format(omega_2nd, result[mesh_id]['solution_chain']))
    return result
