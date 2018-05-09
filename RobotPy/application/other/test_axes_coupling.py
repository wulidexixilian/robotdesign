from sympy.matrices import Matrix
from sympy import symbols, simplify, solve
import numpy as np
from RobotPy.utility.axcoupling import *

DT4 = [
     {'id': 'a', 'axis': 0, 'shape': 'XH',
      'n': (0, 25), 'axisMotion': '000'},
     {'id': 'b', 'axis': 0, 'shape': 'HH',
      'n': (85, 29), 'axisMotion': '000'},
     {'id': 'c', 'axis': 0, 'shape': 'hX',
      'n': (789, 0), 'axisMotion': '000'}
]
DT5 = [
     {'id': 'a', 'axis': 0, 'shape': 'XH',
      'n': (0, 30), 'axisMotion': '000'},
     {'id': 'b', 'axis': 0, 'shape': 'HV',
      'n': (74, 28), 'axisMotion': '000'},
     {'id': 'c', 'axis': 1, 'shape': 'VH',
      'n': (34, 1), 'axisMotion': '100'},
     {'id': 'd', 'axis': 1, 'shape': 'HX',
      'n': (35, 0), 'axisMotion': '100'}
]
DT6 = [
     {'id': 'a', 'axis': 0, 'shape': 'XA',
      'n': (0, 20), 'axisMotion': '000'},
     {'id': 'b', 'axis': 1, 'shape': 'AH',
      'n': (23, 67), 'axisMotion': '100'},
     {'id': 'c', 'axis': 1, 'shape': 'HA',
      'n': (57, 19), 'axisMotion': '110'},
     {'id': 'd', 'axis': 2, 'shape': 'AH',
      'n': (27, 19), 'axisMotion': '110'},
     {'id': 'e', 'axis': 2, 'shape': 'hX',
      'n': (1299, 0), 'axisMotion': '110'}
]
# ****** Input ******
omega_mA4 = symbols('omega_mA4')
omega_mA5 = symbols('omega_mA5')
omega_mA6 = symbols('omega_mA6')
# ****** Output ******
omega_xA4 = symbols('omega_xA4')
omega_xA5 = symbols('omega_xA5')
omega_xA6 = symbols('omega_xA6')
# ****** Solve ******
result_dt4 = solve_drivetrain(DT4, omega_mA4,
                              [omega_xA4, omega_xA5, omega_xA6])
result_dt5 = solve_drivetrain(DT5, omega_mA5,
                              [omega_xA4, omega_xA5, omega_xA6])
result_dt6 = solve_drivetrain(DT6, omega_mA6,
                              [omega_xA4, omega_xA5, omega_xA6])
# ****** Result ******
RAT_MOT4 = result_dt4['bc']['solution_chain'].coeff(omega_mA4)
RAT_MOT5 = result_dt5['cd']['solution_chain'].coeff(omega_mA5)
RAT_MOT6 = result_dt6['de']['solution_chain'].coeff(omega_mA6)
print('RAT_MOT4 : {}'.format(RAT_MOT4))
print('RAT_MOT5 : {}'.format(RAT_MOT5))
print('RAT_MOT6 : {}'.format(RAT_MOT6))
COUP_COMP_45 = result_dt5['cd']['solution_chain'].coeff(omega_xA4)
COUP_COMP_56 = result_dt6['de']['solution_chain'].coeff(omega_xA5)
COUP_COMP_46 = result_dt6['de']['solution_chain'].\
               subs(omega_xA5, result_dt5['cd']['solution_chain']).\
               coeff(omega_xA4)
print('COUP_COMP_46 (246962/22855905) : {}'.format(COUP_COMP_46))
print('COUP_COMP_45 (-2/85) : {}'.format(COUP_COMP_45))
print('COUP_COMP_56 (-1237/105219) : {}'.format(COUP_COMP_56))