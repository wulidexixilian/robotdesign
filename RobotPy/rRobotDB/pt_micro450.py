# -*- coding: utf-8 -*-
"""
robot configurations kr6 900
Created on Fri Mar 24 11:03:07 2017

@author: pei.sun
"""
import numpy as np
from resource.ExternalDB.gearbox_db import load_gear_db
from resource.ExternalDB.motor_db import load_motor_db

structurePara = [
    {
        "name": "groundbase",
        "displacement": np.array([0, 0, 112.5])*1e-3,
    },
    {
        "name": "rotationcolumn",
        "displacement": np.array([0, -52, -82.5])*1e-3,
    },
    {
        "name": "linkarm",
        "displacement": np.array([220, 0, -30])*1e-3,
    },
    {
        "name": "arm",
        "displacement": np.array([75, -9, -22])*1e-3,
    },
    {
        "name": "handbase",
        "displacement": np.array([0, -8.5, -120])*1e-3,
    },
    {
        "name": "handwrist",
        "displacement": np.array([30, 0, 8.5])*1e-3,
     },
    {
        "name": "handflange",
        "displacement": np.array([0, 0, -5])*1e-3,
    }
]

massPara = [
    # groundbase structure
    {
        "nest": "groundbase",
        "cm": np.array([-12.2, 0, 52.59])*1e-3, "m": 1.2,
        "iT": np.array([0, 0, 0, 0, 0, 0])*1e-6
    },
    # rotation column structure
    {
        "nest": "rotationcolumn",
        "cm": np.array([-1.75, -2.16, -28.85])*1e-3, "m": 1.2,
        "iT": np.array([3671.92, 3600.79, 3128.22, 0, 0, 0])*1e-6
    },
    # linkarm structure
    {
        "nest": "linkarm",
        "cm": np.array([100, -13.54, -47.15])*1e-3, "m": 1.4,
        "iT": np.array([8038.03, 19211.05, 14393.16, 0, 0, 0])*1e-6
    },
    # arm structure
    {
        "nest": "arm",
        "cm": np.array([-18.74, -15.62, -38])*1e-3, "m": 0.5,
        "iT": np.array([1335.47, 1678.4, 1286.26, 0, 0, 0])*1e-6
    },
    # wrist structure
    {
        "nest": "handbase",
        "cm": np.array([-1.43, -4.01, -60])*1e-3, "m":0.3,
        "iT": np.array([3197.98, 3064.24, 579.79, 0, 0, 0])*1e-6
    },
    # wrist hand structure
    {
        "nest": "handwrist",
        "cm": np.array([0, 9.09, 19.8])*1e-3, "m": 0.1,
        "iT": np.array([114.01, 70.72, 79.18, 0, 0, 0])*1e-6
    },
    # flange structure
    {
        "nest": "handflange",
        "cm": np.array([0, 0, -3])*1e-3, "m": 0.01,
        "iT": np.array([50, 50, 50, 0, 0, 0])*1e-6
    },
]

motor_installation = [
    # A1

    {
        "nest":           "groundbase",
        "position":       np.array([0, 0, 112.5]) * 1e-3,
        "orientation":    np.array([0, 0, np.pi]),
        'type':           'TSM3104E040'
    },

    # A2
    {
        "nest":           "rotationcolumn",
        "position":       np.array([0, -52, -82.5]) * 1e-3,
        "orientation":    np.array([0, 0, np.pi / 2]),
        'type':           'TSM3104E040'
    },

    # A3
    {
        "nest":           "linkarm",
        "position":       np.array([100, 0, -30]) * 1e-3,
        "orientation":    np.array([0, 0, 0]),
        'type':           'TSM3102E040'
    },

    # A4
    {
        "nest":           "arm",
        "position":       np.array([75, -9, -22]) * 1e-3,
        "orientation":    np.array([0, np.pi / 2, 0]),
        'type':           'TS4873'
    },

    # A5
    {
        "nest":           "handbase",
        "position":       np.array([0, -8.5, -50]) * 1e-3,
        "orientation":    np.array([-np.pi / 2, 0, 0]),
        'type':           'TS4872'
    },

    # A6
    {
        "nest":           "handwrist",
        "position":       np.array([30.7, 0, 8.5]) * 1e-3,
        "orientation":    np.array([0, np.pi / 2, 0]),
        'type':           'TS4871'
    }
]

motorPara = list(map(load_motor_db, motor_installation))

frictionPara = [
    {"nest": "rotationcolumn", "friction": [7.35, 1.02, 1]},
    {"nest": "linkarm", "friction": [8.58, 1.47, 1]},
    {"nest": "arm", "friction": [2.21, 0.78, 1]},
    {"nest": "handbase", "friction": [0.63, 0.14, 1]},
    {"nest": "handwrist", "friction": [0.63, 0.14, 1]},
    {"nest": "handflange", "friction": [0.29, 0.07, 1]}
]

gear_installation = [
    # A1
    {
        "nest": "groundbase",
        "case": 9,
        'type': 'CSG-17-100-2UH',
        'pre ratio': 1
    },
    # A2
    {
        "nest": "rotationcolumn",
        "case": 9,
        'type': 'SHG-17-120-2SO',
        'pre ratio': 1
    },
    # A3
    {
        "nest": "linkarm",
        "case": 9,
        'type': 'SHG-14-80-2SO-LW',
        'pre ratio': 1
    },
    # A4
    {
        "nest": "arm",
        "case": 9,
        'type': 'CSF11-50-2UP',
        'pre ratio': 1
    },
    # A5
    {
        "nest": "handbase",
        "case": 9,
        'type': 'CSF11-50-2UP',
        'pre ratio': 6/5
    },
    # A6
    {
        "nest": "handwrist",
        "case": 9,
        'type': 'CSF8-50-2UP',
        'pre ratio': 1
    }
]

gearPara = list(map(load_gear_db, gear_installation))
