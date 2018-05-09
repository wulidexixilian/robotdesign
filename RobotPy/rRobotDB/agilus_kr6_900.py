import numpy as np
from resource.ExternalDB.gearbox_db import load_gear_db
from resource.ExternalDB.motor_db import load_motor_db


structurePara = [
    {
        "name": "groundbase",
        "displacement": np.array([0, 0, 152]) * 1e-3,
    },
    {
        "name": "rotationcolumn",
        "displacement": np.array([25, -102.7, -179.5]) * 1e-3,
    },
    {
        "name": "linkarm",
        "displacement": np.array([455, 0, 45.5]) * 1e-3,
    },
    {
        "name": "arm",
        "displacement": np.array([191, -25, -55.5]) * 1e-3,
    },
    {
        "name": "handbase",
        "displacement": np.array([0, 58.5, -219]) * 1e-3,
    },
    {
        "name": "handwrist",
        "displacement": np.array([53.5, 0, -32]) * 1e-3,
    },
    {
        "name": "handflange",
        "displacement": np.array([0, 0, -10])*1e-3,
    },
]

massPara = [
    # groundbase structure
    {
        "nest": "groundbase",
        "cm": np.array([-24, 0.11, 94.5])*1e-3, "m": 6.5,
        "iT": np.array([59577, 73973, 71691, 91, -4423, -78]) * 1e-6
    },
    # rotation column structure
    {
        "nest": "rotationcolumn",
        "cm": np.array([5.9, -0.9, -97.2])*1e-3, "m": 7.8,
        "iT": np.array([103036, 70800, 78664, 5324, -4510, -1018]) * 1e-6
    },
    # linkarm structure
    {
        "nest": "linkarm",
        "cm": np.array([202.8, -6.8, -41.7])*1e-3, "m": 6.84,
        "iT": np.array([40365, 235940, 222805, 465, 8747, -750]) * 1e-6
    },
    # linkarm cover
    {
        "nest": "linkarm",
        "cm": np.array([383.2, -5.7, -51]) * 1e-3, "m": 0.6,
        "iT": np.array([9431, 12276, 4386, -0.4, 1.3, 225]) * 1e-6
    },
    # linkarm drivetrain + screws
    {
        "nest": "linkarm",
        "cm": np.array([330.9, -2.9, 33.4]) * 1e-3, "m": 0.5,
        "iT": np.array([646.5, 16535, 16460, -39, 1410, 51.2]) * 1e-6
    },
    # linkarm other
    {
        "nest": "linkarm",
        "cm": np.array([218, 0.5, -79.4]) * 1e-3, "m": 0.3,
        "iT": np.array([1633.2, 14875.2, 14377.7, 52.2, 1910.6, 135]) * 1e-6
    },
    # arm structure
    {
        "nest": "arm",
        "cm": np.array([63.6, -13.5, -50.2]) * 1e-3, "m": 3.5,
        "iT": np.array([12423, 30203, 29545, 235, -317, -207]) * 1e-6
    },
    # arm cabel assembly
    {
        "nest": "arm",
        "cm": np.array([60, -3, -85]) * 1e-3, "m": 0.11,
        "iT": np.array([120, 600, 650, 0, 90, -42]) * 1e-6
    },

    # wrist structure
    {
        "nest": "handbase",
        "cm": np.array([0, 2.5, -101.45]) * 1e-3, "m": 2.15,
        "iT": np.array([13348, 12263, 6332, -1195, 3.4, -1]) * 1e-6
    },
    # wrist cable
    {
        "nest": "handbase",
        "cm": np.array([7, -30, -104]) * 1e-3, "m": 0.082,
        "iT": np.array([36, 304, 104, -85, 0, 0]) * 1e-6
    },
    # wrist hand structure
    {
        "nest": "handwrist",
        "cm": np.array([-1.2, 0.1, 5.8]) * 1e-3, "m": 0.32,
        "iT": np.array([464, 507, 528, 0, -13, -0.1]) * 1e-6
    },
    # wrist hand installation material + cable
    {
        "nest": "handwrist",
        "cm": np.array([11.5, 12, -6.8]) * 1e-3, "m": 0.1,
        "iT": np.array([126, 100, 121, 10, -64, -11.9]) * 1e-6
    },
    # wrist hand adapter
    {
        "nest": "handwrist",
        "cm": np.array([48.8, 0, 0]) * 1e-3, "m": 0.079,
        "iT": np.array([87, 43, 45, 0, 0, 0]) * 1e-6
    },
    # wrist hand other
    {
        "nest": "handwrist",
        "cm": np.array([28.3, 0.4, 6]) * 1e-3, "m": 0.079,
        "iT": np.array([126, 163, 130, 1.1, -15.1, -2.2]) * 1e-6
    },
    # flange structure
    {
        "nest": "handflange",
        "cm": np.array([0, 0, -1.4]) * 1e-3, "m": 0.21,
        "iT": np.array([81, 81, 155, 0, 0, 0]) * 1e-6
    },
    # flange screws
    {
        "nest": "handflange",
        "cm": np.array([0, 0, 1]) * 1e-3, "m": 0.022,
        "iT": np.array([7.8, 9, 16, 0, 0, 0]) * 1e-6
    }
]

motor_installation = [
    # A1 motor
    {
        "nest": "groundbase",
        "position": np.array([0, 0, 152])*1e-3,
        "orientation": np.array([0, 0, np.pi]),
        "type": "TSM3304E200"
    },
    # A2 motor
    {
        "nest": "rotationcolumn",
        "position": np.array([25, -56, -179.5])*1e-3,
        "orientation": np.array([0, 0, -np.pi/2]),
        "type": "TSM3304E200"
    },
    # A3 motor
    {
        "nest": "linkarm",
        "position": np.array([294, -12, 44])*1e-3,
        "orientation": np.array([0, 0, np.pi]),
        "type": "TSM3204E200"
    },
    # A4 motor
    {
        "nest": "arm",
        "position": np.array([33.2, -25, -55.5])*1e-3,
        "orientation": np.array([0, -np.pi/2, 0]),
        "type": "TSM3104E200"
    },
    # A5 motor
    {
        "nest": "handbase",
        "position": np.array([0, 53, -112.75])*1e-3,
        "orientation": np.array([0, 0, np.pi/2]),
        "type": "TSM3104E200"
    },
    # A6 motor
    {
        "nest": "handwrist",
        "position": np.array([48.4, 0, -32])*1e-3,
        "orientation": np.array([0, -np.pi/2, 0]),
        "type": "TSM3102E200"
    }
]

motorPara = list(map(load_motor_db, motor_installation))

frictionPara = [
    {"nest": "rotationcolumn", "friction": [26.5, 7.2, 1]},
    {"nest": "linkarm", "friction": [37.4, 10.5, 1]},
    {"nest": "arm", "friction": [19.5, 4.54, 0.95]},
    {"nest": "handbase", "friction": [3.41, 0.85, 1]},
    {"nest": "handwrist", "friction": [3.19, 1.49, 1]},
    {"nest": "handflange", "friction": [2.42, 0.54, 1]}
]

gear_installation = [
    {
        "nest": "groundbase",
        "case": 9,
        "type": "CSG32-100",
        "pre ratio": 1,
        "limit_factor": 1.5674 * 1.18,
    },
    {
        "nest": "rotationcolumn",
        "case": 15,
        "type": "SHG32-120",
        "pre ratio": 1,
        "limit_factor": 1.3797 * 1.125,
    },
    {
        "nest": "linkarm",
        "case": 13,
        "type": "SHG25-100",
        "pre ratio": 1.04,
        "limit_factor": 1.4371 * 1.125,
    },
    {
        "nest": "arm",
        "case": 9,
        "type": "CSG17-80-2A-R-SP",
        "pre ratio": 1,
        "limit_factor": 1.3103 * 1.16,
    },
    {
        "nest": "handbase",
        "case": 13,
        "type": "SHG17-80-2SH-SP",
        "pre ratio": 22/23,
        "limit_factor": 1.377 * 1.16,
    },
    {
        "nest": "handwrist",
        "case": 13,
        "type": "SHG17-80-2SH-SP",
        "pre ratio": 1,
        "limit_factor": 0.68966 * 1.17,
    }
]

gearPara = list(map(load_gear_db, gear_installation))
