import numpy as np
from resource.ExternalDB.gearbox_db import load_gear_db
from resource.ExternalDB.motor_db import load_motor_db

structurePara = [
    {
        "nest": "groundbase",
        "displacement": np.array([0, 0, 175])*1e-3,
        'offset': 0
    },
    {
        "nest": "link1",
        "displacement": np.array([230, 0, -55])*1e-3,
        'offset': 0
    },
    {
        "nest": "link2",
        "displacement": np.array([175, 0, -40])*1e-3,
        'offset': 0
    },
    {
        "nest": "link3",
        "displacement": np.array([0, 0, -25])*1e-3,
        'offset': 0
    },
    {
        "nest": "link4",
        "displacement": np.array([0, 0, 70])*1e-3,
        'offset': 0
    }
]

massPara = [
    # groundbase structure
    {
        "nest": "groundbase",
        "cm": np.array([-40, 0, 80])*1e-3, "m": 2.5,
        "iT": np.array([40, 180, 159, 0, 0, 0])*1e-6
    },
    # rotation column structure
    {
        "nest": "link1",
        "cm": np.array([110, 0, -20])*1e-3, "m": 0.9,
        "iT": np.array([558.75, 7680.075, 8221.88, 0, 0, 0])*1e-6
    },
    # linkarm structure
    {
        "nest": "link2",
        "cm": np.array([70, -13.54, -60])*1e-3, "m": 2.2,
        "iT": np.array([1338.33, 12558.33, 14226.66, 0, 0, 0])*1e-6
    },
    # arm structure
    {
        "nest": "link3",
        "cm": np.array([0, 0, -50])*1e-3, "m": 0.65,
        "iT": np.array([5910.9, 5910.9, 146.26, 0, 0, 0])*1e-6
    },
    # wrist structure
    {
        "nest": "link4",
        "cm": np.array([0, 0, -60])*1e-3, "m":0.5,  # sum or not
        "iT": np.array([3197.98, 3064.24, 827.51, 0, 0, 0])*1e-6
    },
]

motor_installation = [
    # A1

    {
        "nest": "groundbase",
        "position": np.array([0, 0, 160]) * 1e-3,
        "orientation": np.array([0, 0, 0]),
        'type': 'TS4607N3378E200'
    },

    # A2
    {
        "nest": "link2",
        "position": np.array([0, 0, -15]) * 1e-3,
        "orientation": np.array([0, 0, 0]),
        'type': 'TS4603N3378E200'
    },

    # A3
    {
        "nest": "link2",
        "position": np.array([50, 30, -45]) * 1e-3,
        "orientation": np.array([0, 0, 0]),
        'type': 'TS4603N3378E200'
    },

    # A4
    {
        "nest": "link2",
        "position": np.array([50, -30, -45]) * 1e-3,
        "orientation": np.array([0, 0, 0]),
        'type': 'TS4603N3378E200'
    },
]

motorPara = list(map(load_motor_db, motor_installation))

frictionPara = [
#    {"nest": "link1", "friction": [7.35, 1.02, 1]},
#    {"nest": "link2", "friction": [8.58, 1.47, 1]},
#    {"nest": "link3", "friction": [2.21, 0.78, 1]},
#    {"nest": "link4", "friction": [0.63, 0.14, 1]},
    {"nest": "link1", "friction": [0.0, 0.0, 1.0]},
    {"nest": "link2", "friction": [0.0, 0.0, 1.0]},
    {"nest": "link3", "friction": [0.0, 0.0, 1.0]},
    {"nest": "link4", "friction": [0.0, 0.0, 1.0]},
]

gear_installation = [
    # A1
    {
        "nest": "groundbase",
        "case": 9,
        'type': 'SHG20-50-741769-46',
        'pre ratio': 1,
        "limit_factor": 1.35,
    },
    # A2
    {
        "nest": "link1",
        "case": 9,
        'type': 'SHG17-50-741477-33',
        'pre ratio': 1,
        "limit_factor": 1.35,
    },
    # A3
    {  # A4-A3 coupling -1
        "nest": "link2",
        "case": 2,
        'type': 'EPSON-LS3-401S-A3',
        'pre ratio': 0.82,
        "limit_factor": 1.35,
    },
    # A4
    {  # A3-A4 no coupling
        "nest": "link2",
        "case": 9,
        'type': 'EPSON-LS3-401S-A4',
        'pre ratio': 0.66,
        "limit_factor": 1.35,
    },
]

gearPara = list(map(load_gear_db, gear_installation))
