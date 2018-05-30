import numpy as np
from resource.ExternalDB.gearbox_db import load_gear_db
from resource.ExternalDB.motor_db import load_motor_db

structurePara = [
    {
        "nest": "groundbase",
        "displacement": np.array([0, 0, 100])*1e-3,
        'offset': 0
    },
    {
        "nest": "link1",
        "displacement": np.array([200, 0, -20])*1e-3,
        'offset': 0
    },
    {
        "nest": "link2",
        "displacement": np.array([150, 0, -20])*1e-3,
        'offset': 0
    },
    {
        "nest": "link3",
        "displacement": np.array([0, 0, 50])*1e-3,
        'offset': 0
    },
    {
        "nest": "link4",
        "displacement": np.array([0, 0, 5])*1e-3,
        'offset': 0
    }
]

massPara = [
    # groundbase structure
    {
        "nest": "groundbase",
        "cm": np.array([0, 0, 50])*1e-3, "m": 1.2,
        "iT": np.array([0, 0, 0, 0, 0, 0])*1e-6
    },
    # rotation column structure
    {
        "nest": "link1",
        "cm": np.array([100, 0, -10])*1e-3, "m": 1.2,
        "iT": np.array([500, 2000, 2000, 0, 0, 0])*1e-6
    },
    # linkarm structure
    {
        "nest": "link2",
        "cm": np.array([75, 0, -10])*1e-3, "m": 1.6,
        "iT": np.array([1000, 2000, 2000, 0, 0, 0])*1e-6
    },
    # arm structure
    {
        "nest": "link3",
        "cm": np.array([0, 0, 0])*1e-3, "m": 0.7,
        "iT": np.array([10, 1000, 1000, 0, 0, 0])*1e-6
    },
    # wrist structure
    {
        "nest": "link4",
        "cm": np.array([0, 0, -5])*1e-3, "m": 0.05,
        "iT": np.array([50, 50, 200, 0, 0, 0])*1e-6
    },
]

motor_installation = [
    # A1

    {
        "nest": "groundbase",
        "position": np.array([0, 0, 100]) * 1e-3,
        "orientation": np.array([0, 0, np.pi]),
        'type': 'PT_SCARA_A1'
    },

    # A2
    {
        "nest": "link2",
        "position": np.array([0, 0, 0]) * 1e-3,
        "orientation": np.array([0, 0, 0]),
        'type': 'PT_SCARA_A2'
    },

    # A3
    {
        "nest": "link2",
        "position": np.array([20, 0, 0]) * 1e-3,
        "orientation": np.array([0, 0, 0]),
        'type': 'PT_SCARA_A3'
    },

    # A4
    {
        "nest": "link2",
        "position": np.array([20, 20, 0]) * 1e-3,
        "orientation": np.array([0, 0, 0]),
        'type': 'PT_SCARA_A4'
    },
]

motorPara = list(map(load_motor_db, motor_installation))

frictionPara = [
    {"nest": "link1", "friction": [7.35, 1.02, 1]},
    {"nest": "link2", "friction": [8.58, 1.47, 1]},
    {"nest": "link3", "friction": [2.21, 0.78, 1]},
    {"nest": "link4", "friction": [0.63, 0.14, 1]},
]

gear_installation = [
    # A1
    {
        "nest": "groundbase",
        "case": 9,
        'type': 'PT_SCARA_A1',
        'pre ratio': 1,
        "limit_factor": 1.35,
    },
    # A2
    {
        "nest": "link1",
        "case": 9,
        'type': 'PT_SCARA_A2',
        'pre ratio': 1,
        "limit_factor": 1.35,
    },
    # A3
    {
        "nest": "link2",
        "case": 9,
        'type': 'PT_SCARA_A3',
        'pre ratio': 1,
        "limit_factor": 1.35,
    },
    # A4
    {
        "nest": "link3",
        "case": 9,
        'type': 'PT_SCARA_A4',
        'pre ratio': 1,
        "limit_factor": 1.35,
    },
]

gearPara = list(map(load_gear_db, gear_installation))
