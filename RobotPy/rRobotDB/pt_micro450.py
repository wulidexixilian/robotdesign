import numpy as np
from resource.ExternalDB.gearbox_db import load_gear_db
from resource.ExternalDB.motor_db import load_motor_db

structurePara = [
    {
        "nest": "groundbase",
        "displacement": np.array([0, 0, 112.5])*1e-3,
    },
    {
        "nest": "rotationcolumn",
        "displacement": np.array([0, -52, -82.5])*1e-3,
    },
    {
        "nest": "linkarm",
        "displacement": np.array([220, 0, -30])*1e-3,
    },
    {
        "nest": "arm",
        "displacement": np.array([75, -9, -22])*1e-3,
    },
    {
        "nest": "handbase",
        "displacement": np.array([0, -8.5, -120])*1e-3,
    },
    {
        "nest": "handwrist",
        "displacement": np.array([30, 0, 8.5])*1e-3,
     },
    {
        "nest": "handflange",
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
        "cm": np.array([-35, -15.62, -15])*1e-3, "m": 0.7,
        "iT": np.array([1335.47, 1678.4, 1286.26, 0, 0, 0])*1e-6
    },
    # wrist structure
    {
        "nest": "handbase",
        "cm": np.array([-1.43, -4.01, -60])*1e-3, "m":0.7,
        "iT": np.array([3197.98, 3064.24, 579.79, 0, 0, 0])*1e-6
    },
    # wrist hand structure
    {
        "nest": "handwrist",
        "cm": np.array([19.8, 9.09, 0])*1e-3, "m": 0.1,
        "iT": np.array([114.01, 70.72, 79.18, 0, 0, 0])*1e-6
    },
    # flange structure
    {
        "nest": "handflange",
        "cm": np.array([0, 0, -3])*1e-3, "m": 0.04,
        "iT": np.array([10, 10, 10, 0, 0, 0])*1e-6
    },
]

motor_installation = [
    # A1

    {
        "nest": "groundbase",
        "position": np.array([0, 0, 112.5]) * 1e-3,
        "orientation": np.array([0, 0, np.pi]),
        'type': 'TSM3104E040'
    },

    # A2
    {
        "nest": "rotationcolumn",
        "position": np.array([0, -52, -82.5]) * 1e-3,
        "orientation": np.array([0, 0, np.pi / 2]),
        'type': 'TSM3104E040'
    },

    # A3
    {
        "nest": "linkarm",
        "position": np.array([100, 0, -30]) * 1e-3,
        "orientation": np.array([0, 0, 0]),
        'type': 'TSM3102E040'
    },

    # A4
    {
        "nest": "arm",
        "position": np.array([75, -9, -22]) * 1e-3,
        "orientation": np.array([0, np.pi / 2, 0]),
        'type': 'TS4873'
    },

    # A5
    {
        "nest": "handbase",
        "position": np.array([0, -8.5, -40]) * 1e-3,
        "orientation": np.array([0, -np.pi / 2, 0]),
        'type': 'TS4873'
        # 'type': 'TS4632'
    },

    # A6
    {
        "nest": "handwrist",
        "position": np.array([30.7, 0, 8.5]) * 1e-3,
        "orientation": np.array([0, np.pi / 2, 0]),
        'type': 'TS4871'
        # 'type': 'TS4632'
    }
]

motorPara = list(map(load_motor_db, motor_installation))

frictionPara = [
    {"nest": "rotationcolumn", "friction": np.array([7.35, 1.02, 1])},
    {"nest": "linkarm", "friction": np.array([8.58, 1.47, 1])},
    {"nest": "arm", "friction": np.array([2.21, 0.78, 1])},
    {"nest": "handbase", "friction": np.array([0.63, 0.14, 1])},
    {"nest": "handwrist", "friction": np.array([0.63, 0.14, 1])},
    {"nest": "handflange", "friction": np.array([0.29, 0.07, 1])}
]

gear_installation = [
    # A1
    {
        "nest": "groundbase",
        "case": 9,
        'type': 'CSG-17-100-2UH',
        'pre ratio': 1,
        "limit_factor": 1.35,
    },
    # A2
    {
        "nest": "rotationcolumn",
        "case": 9,
        'type': 'SHG-17-120-2SO',
        'pre ratio': 1,
        "limit_factor": 1.35,
    },
    # A3
    {
        "nest": "linkarm",
        "case": 9,
        'type': 'SHG-14-80-2SO-LW',
        'pre ratio': 1,
        "limit_factor": 1.35,
    },
    # A4
    {
        "nest": "arm",
        "case": 9,
        'type': 'CSF11-50-2UP',
        'pre ratio': 1,
        "limit_factor": 1.2,
    },
    # A5
    {
        "nest": "handbase",
        "case": 9,
        'type': 'CSF11-50-2UP',
        'pre ratio': 7/5,
        "limit_factor": 1.2,
    },
    # A6
    {
        "nest": "handwrist",
        "case": 9,
        'type': 'CSF8-50-2UP',
        'pre ratio': 1,
        "limit_factor": 1.2,
    }
]

gearPara = list(map(load_gear_db, gear_installation))
