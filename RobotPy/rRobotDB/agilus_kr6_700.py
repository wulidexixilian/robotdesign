import numpy as np
from resource.ExternalDB.gearbox_db import load_gear_db
from resource.ExternalDB.motor_db import load_motor_db


structure_para = [
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
        "displacement": np.array([355, 0, -45.5]) * 1e-3,
    },
    {
        "name": "arm",
        "displacement": np.array([136, -25, -55.5]) * 1e-3,
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

mass_para = [
    # groundbase structure
    {
        "nest": "groundbase",
        "cm": np.array([-24, 0.11, 94.5])*1e-3, "m": 6.5,
        "iT": np.array([59577, 73973, 71691, 91, -4423, -78]) * 1e-6
    },
    # rotation column structure
    {
        "nest": "rotationcolumn",
        "cm": np.array([5.9, -0.9, -97.2]) * 1e-3, "m": 7.8,
        "iT": np.array([103036, 70800, 78664, 5324, -4510, -1080]) * 1e-6
    },
    # linkarm structure
    {
        "nest": "linkarm",
        "cm": np.array([155.2, -6.2, -34.6]) * 1e-3, "m": 5.5,
        "iT": np.array([34999.27, 124514.16, 113887.84, 200.8, 7654.1, 203.6]) * 1e-6
    },
    # linkarm screw
    {
        "nest": "linkarm",
        "cm":   np.array([236, -1.8, 33.1]) * 1e-3, "m": 0.5,
        "iT":   np.array([688.4, 9808.4, 9770.4, -47.5, 891, 159.8]) * 1e-6
    },
    # linkarm other
    {
        "nest": "linkarm",
        "cm":   np.array([149.6, -1.45, -82.3]) * 1e-3, "m": 0.3,
        "iT":   np.array([1517, 8343.9, 7887.7, -1.9, 1242.6, 9.7]) * 1e-6
    },
    # linkarm cover
    {
        "nest": "linkarm",
        "cm":   np.array([263.1, -5.6, -51]) * 1e-3, "m": 0.6,
        "iT":   np.array([9057, 11802, 4236, -0.1, 1.3, 217]) * 1e-6
    },
    # arm structure
    {
        "nest": "arm",
        "cm": np.array([47, -11, -53.5]) * 1e-3, "m": 1.8,
        "iT": np.array([6980, 9847, 10570, 70, -255, -1527]) * 1e-6
    },
    # arm screw
    {
        "nest": "arm",
        "cm":   np.array([23, -10, -62.5]) * 1e-3, "m": 0.33,
        "iT":   np.array([1131, 1399, 821, -36, 106, -122]) * 1e-6
    },
    # arm other screw
    {
        "nest": "arm",
        "cm":   np.array([42, -25, -55.5]) * 1e-3, "m": 0.23,
        "iT":   np.array([175.6, 92.5, 92.5, 0, 0, 0]) * 1e-6
    },
    # arm up cover
    {
        "nest": "arm",
        "cm":   np.array([58, 24, -54]) * 1e-3, "m": 0.035,
        "iT":   np.array([71, 70, 77, 0, 0, -25]) * 1e-6
    },
    # arm other screw short
    {
        "nest": "arm",
        "cm":   np.array([146.7, -25, -55.5]) * 1e-3, "m": 0.03,
        "iT":   np.array([75.8, 40.25, 40.25, 0, 0, 0]) * 1e-6
    },
    # arm cover
    {
        "nest": "arm",
        "cm":   np.array([-51.3, -30.5, -58.6]) * 1e-3, "m": 0.18,
        "iT":   np.array([418, 322, 226, 0, -1.5, -85]) * 1e-6
    },
    # arm cable
    {
        "nest": "arm",
        "cm":   np.array([39, 3, -64]) * 1e-3, "m": 0.45,
        "iT":   np.array([725, 3148, 3684, 156, 297, -213]) * 1e-6
    },
    # handbase spline
    {
        "nest": "handbase",
        "cm": np.array([0, 0, 84.3]) * 1e-3, "m": 0.07,
        "iT": np.array([11.8, 11.8, 13.5, 0, 0, 0]) * 1e-6
    },
    # handbase others
    {
        "nest": "handbase",
        "cm":   np.array([0, 67, -152.45]) * 1e-3, "m": 0.04,
        "iT":   np.array([114, 117, 4, 0, 0, 0]) * 1e-6
    },
    # handbase torque unit
    {
        "nest": "handbase",
        "cm":   np.array([7.3, 0, 32.85]) * 1e-3, "m": 0.5,
        "iT":   np.array([448, 498, 292, 0, -11, 0]) * 1e-6
    },
    # handbase valves
    {
        "nest": "handbase",
        "cm":   np.array([0, 33, -39.45]) * 1e-3, "m": 0.2,
        "iT":   np.array([36, 134, 149, -3, 0, 0]) * 1e-6
    },
    # handbase structure
    {
        "nest": "handbase",
        "cm":   np.array([0, 2.5, -101.45]) * 1e-3, "m": 2.15,
        "iT":   np.array([13348, 12263, 6332, -1195, 3.4, -1]) * 1e-6
    },
    # handbase cover
    {
        "nest": "handbase",
        "cm":   np.array([0, 10, -160.45]) * 1e-3, "m": 0.22,
        "iT":   np.array([1635, 772.6, 1194, -28, 0, 0]) * 1e-6
    },
    # handwrist structure
    {
        "nest": "handwrist",
        "cm": np.array([-1.2, 0.1, 5.8]) * 1e-3, "m": 0.32,
        "iT": np.array([464, 507, 528, 1, 1.42, -1.24]) * 1e-6
    },
    # handwrist adapter
    {
        "nest": "handwrist",
        "cm":   np.array([48.8, 0, 0]) * 1e-3, "m": 0.079,
        "iT":   np.array([87, 43, 45, 0, 0, 0]) * 1e-6
    },
    # handwrist others
    {
        "nest": "handwrist",
        "cm":   np.array([28.3, 0.4, 6]) * 1e-3, "m": 0.079,
        "iT":   np.array([126, 163, 130, 1.1, -15.1, -2.2]) * 1e-6
    },
    # wrist hand cable
    {
        "nest": "handwrist",
        "cm":   np.array([11.5, 12, -6.8]) * 1e-3, "m": 0.166,
        "iT":   np.array([110, 100, 121, 10.6, -6.4, -11.9]) * 1e-6
    },
    # flange screw
    {
        "nest": "handflange",
        "cm": np.array([0, 0, 1]) * 1e-3, "m": 0.022,
        "iT": np.array([7.8, 9, 16, 0, 0, 0.5]) * 1e-6
    },
    # flange
    {
        "nest": "handflange",
        "cm":   np.array([0, 0, -1.4]) * 1e-3, "m": 0.21,
        "iT":   np.array([81, 81, 155, 0, 0, 0]) * 1e-6
    },
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
        "nest": "linkarm",
        "position": np.array([25, -56, -179.5])*1e-3,
        "orientation": np.array([0, 0, np.pi]),
        "type": "TSM3304E200"
    },
    # A3 motor
    {
        "nest": "linkarm",
        "position": np.array([174, -12, 44])*1e-3,
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
        "position": np.array([0, 51.3, -108.75])*1e-3,
        "orientation": np.array([0, 0, np.pi/2]),
        "type": "TSM3104E200"
    },
    # A6 motor
    {
        "nest": "handwrist",
        "position": np.array([41.4, 0, -30])*1e-3,
        "orientation": np.array([0, -np.pi/2, 0]),
        "type": "TSM3102E200"
    }
]

motor_para = list(map(load_motor_db, motor_installation))

friction_para = [
    {"nest": "rotationcolumn", "friction": [46.3, 13, 1]},
    {"nest": "linkarm", "friction": [41.4, 15.5, 1]},
    {"nest": "arm", "friction": [20.1, 4.9, 1]},
    {"nest": "handbase", "friction": [4.5, 0.7, 1]},
    {"nest": "handwrist", "friction": [6.5, 1, 1]},
    {"nest": "handflange", "friction": [6.6, 0.6, 1]}
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
        "pre ratio": 26/25,
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
        "case": 10,
        "type": "SHG17-80-2SH-SP",
        "pre ratio": 22/23,
        "limit_factor": 1.377 * 1.16,
    },
    {
        "nest": "handwrist",
        "case": 10,
        "type": "SHG17-80-2SH-SP",
        "pre ratio": 1,
        "limit_factor": 0.68966 * 1.17,
    }
]

gear_para = list(map(load_gear_db, gear_installation))
