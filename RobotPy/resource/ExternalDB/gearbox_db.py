gear_db = {
    'CSG-17-100-2UH': {
        "ratio": 100,
        "rated_tau": 31,
        "acc_tau": 51,
        "max_tau": 70,
        'emergency_tau': 109,
        "max_omega": 7300,
        'rated_omega': 3500,
        "offset": 0,
        "stator": {
             "inertia_drive": 8e-6,
             "inertia_body": [0, 0, 0],
             "cm": 0,
             "m": 0.79
        },
        "rotor": {
             "inertia_drive": 8e-7,
             "inertia_body": [0, 0, 0],
             "cm": 0,
             "m": 0.08
        },
    },

    'SHG-17-100-2SO': {
        "ratio": 100,
        "rated_tau": 31,
        "acc_tau": 51,
        "max_tau": 70,
        'emergency_tau': 143,
        "max_omega": 7300,
        'rated_omega': 3500,
        "offset": 0,
        "stator": {
             "inertia_drive": 8e-6,
             "inertia_body": [0, 0, 0],
             "cm": 0,
             "m": 0.79
        },
        "rotor": {
             "inertia_drive": 8e-7,
             "inertia_body": [0, 0, 0],
             "cm": 0,
             "m": 0.08
        },
    },

    'SHG-17-120-2SO': {
        "ratio": 120,
        "rated_tau": 31,
        "acc_tau": 51,
        "max_tau": 70,
        'emergency_tau': 143,
        "max_omega": 7300,
        'rated_omega': 3500,
        "offset": 0,
        "stator": {
            "inertia_drive": 8e-6,
            "inertia_body": [0, 0, 0],
            "cm": 0,
            "m": 0.79
        },
        "rotor": {
            "inertia_drive": 8e-7,
            "inertia_body": [0, 0, 0],
            "cm": 0,
            "m": 0.08
        },
    },

    'SHG-14-80-2SO-LW': {
        "ratio": 80,
        "offset": 0,
        "rated_tau": 10,
        "acc_tau": 14,
        "max_tau": 30,
        'emergency_tau': 61,
        "max_omega": 8500,
        'rated_omega': 3500,
        "stator": {
             "inertia_drive": 4.7e-6,
             "inertia_body": [0, 0, 0],
             "cm": 0,
             "m": 0.54
        },
        "rotor": {
             "inertia_drive": 4.7e-7,
             "inertia_body": [0, 0, 0],
             "cm": 0,
             "m": 0.05
        },
    },

    'SHG-14-100-2SO-LW': {
        "ratio":         100,
        "offset":        0,
        "rated_tau":     10,
        "acc_tau":       14,
        "max_tau":       30,
        'emergency_tau': 61,
        "max_omega":     8500,
        'rated_omega':   3500,
        "stator":        {
            "inertia_drive": 4.7e-6,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0.54
        },
        "rotor":         {
            "inertia_drive": 4.7e-7,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0
        },
    },

    'CSF-11-50-2A-R': {
        "ratio":        50,
        "offset":       0,
        "rated_tau":    3.5,
        "acc_tau":      5.5,
        "max_tau":      8.3,
        'emergency_tau': 17,
        "max_omega":    8500,
        'rated_omega': 3500,
        "stator": {
             "inertia_drive": 1.4e-6,
             "inertia_body": [0, 0, 0],
             "cm": 0,
             "m": 0.176
        },
        "rotor": {
             "inertia_drive": 0.14e-6,
             "inertia_body": [0, 0, 0],
             "cm": 0,
             "m": 0.01
        },
    },

    'CSF11-50-2UP': {
        "ratio":        50,
        "offset":       0,
        "rated_tau":    3.5,
        "acc_tau":      5.5,
        "max_tau":      8.3,
        'emergency_tau': 17,
        "max_omega":    8500,
        'rated_omega': 3500,
        "stator":       {
            "inertia_drive": 1.5e-6,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0.33
        },
        "rotor":        {
            "inertia_drive": 1.5e-7,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0.03
        },
    },

    'CSF8-50-2UP': {
        "ratio": 50,
        "offset": 0,
        "rated_tau": 1.8,
        "acc_tau": 2.3,
        "max_tau": 3.3,
        'emergency_tau': 6.6,
        "max_omega": 8500,
        'rated_omega': 3500,
        "stator": {
             "inertia_drive": 0.4e-6,
             "inertia_body": [0, 0, 0],
             "cm": 0,
             "m": 0.2
        },
        "rotor": {
             "inertia_drive": 0.4e-7,
             "inertia_body": [0, 0, 0],
             "cm": 0,
             "m": 0.02
        },
    },

    'CSF5-50-2XH-F': {
        "ratio": 50,
        "offset": 0,
        "rated_tau": 0.4,
        "acc_tau": 0.53,
        "max_tau": 0.9,
        'emergency_tau': 1.8,
        "limit_factor": 1.15,
        "max_omega": 8500,
        'rated_omega': 3500,
        "stator": {
            "inertia_drive": 0.25e-6,
            "inertia_body": [0, 0, 0],
            "cm": 0,
            "m": 0.025
        },
        "rotor": {
            "inertia_drive": 0.25e-6,
            "inertia_body": [0, 0, 0],
            "cm": 0,
            "m": 0
        },
    },

    'CSG32-100': {
        "ratio": 100,
        "offset": 68.5e-3,
        "rated_tau": 178,
        "acc_tau": 279,
        "max_tau": 433,
        'emergency_tau': 841,
        "max_omega": 6000,
        'rated_omega': 2000,
        "stator": {
            "inertia_drive": 172e-6,
            "inertia_body":  [4777e-6, 4777e-6, 3725e-6],
            "cm": -36.5e-3,
            "m": 2.2
        },
        "rotor": {
            "inertia_drive": 172e-6,
            "inertia_body":  [954.5e-6, 954.5e-6, 883e-6],
            "cm": -26e-3,
            "m": 1.07
        },
    },

    'SHG32-120': {
        "ratio": 120,
        "offset": 51.7e-3,
        "rated_tau": 178,
        "acc_tau": 245.58,
        "max_tau": 459,
        'emergency_tau': 892,
        "max_omega": 4500,
        'rated_omega': 2000,
        "stator": {
            "inertia_drive": 169e-6,
            "inertia_body":  [0e-6, 0e-6, 0e-6],
            "cm": -15e-3,
            "m": 0.97
        },
        "rotor": {
            "inertia_drive": 169e-6,
            "inertia_body":  [0e-6, 0e-6, 0e-6],
            "cm": -15e-3,
            "m": 0
        },
    },

    'SHG25-100': {
        "ratio": 100,
        "offset": 41e-3,
        "rated_tau": 87,
        "acc_tau": 125.03,
        "max_tau": 204,
        'emergency_tau': 369,
        "max_omega": 4500,
        'rated_omega': 2000,
        "stator": {
            "inertia_drive": 41.3e-6,
            "inertia_body": [0e-6, 0e-6, 0e-6],
            "cm": -15e-3,
            "m": 0.48
        },
        "rotor": {
            "inertia_drive": 41.3e-6,
            "inertia_body": [0e-6, 0e-6, 0e-6],
            "cm": -15e-3,
            "m": 0.0
        },
    },

    'CSG17-80-2A-R-SP': {
        "ratio": 80,
        "offset": 10e-3,
        "rated_tau": 29,
        "acc_tau": 38,
        "max_tau": 56,
        'emergency_tau': 113,
        "max_omega": 6500,
        'rated_omega': 2000,
        "stator": {
            "inertia_drive": 7.9e-6,
            "inertia_body": [223e-6, 223e-6, 187e-6],
            "cm": -17e-3,
            "m": 0.68
        },
        "rotor": {
            "inertia_drive": 7.9e-6,
            "inertia_body": [530.5e-6, 530.5e-6, 384e-6],
            "cm": -14.5e-3,
            "m": 0.0
        },
    },

    'SHG17-80-2SH-SP': {
        "ratio": 80,
        "offset": 26.5e-3,
        "rated_tau": 29,
        "acc_tau": 39.93,
        "max_tau": 56,
        'emergency_tau': 113,
        "max_omega": 7300,
        'rated_omega': 2000,
        "stator": {
            "inertia_drive": 7.9e-6,
            "inertia_body":  [310.5e-6, 310.5e-6, 224e-6],
            "cm": -16.5e-3,
            "m": 0.18
        },
        "rotor": {
            "inertia_drive": 7.9e-6,
            "inertia_body":  [92e-6, 92e-6, 75e-6],
            "cm": -11e-3,
            "m": 0.0
        },
    },

    'PT_SCARA_A1': {
        "ratio":         50,
        "offset":        0,
        "rated_tau":     3.5,
        "acc_tau":       5.5,
        "max_tau":       8.3,
        'emergency_tau': 17,
        "max_omega":     8500,
        'rated_omega':   3500,
        "stator":        {
            "inertia_drive": 1.5e-6,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0.33
        },
        "rotor":         {
            "inertia_drive": 1.5e-7,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0.03
        },
    },

    'PT_SCARA_A2': {
        "ratio":         50,
        "offset":        0,
        "rated_tau":     3.5,
        "acc_tau":       5.5,
        "max_tau":       8.3,
        'emergency_tau': 17,
        "max_omega":     8500,
        'rated_omega':   3500,
        "stator":        {
            "inertia_drive": 1.5e-6,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0.33
        },
        "rotor":         {
            "inertia_drive": 1.5e-7,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0.03
        },
    },

    'PT_SCARA_A3': {
        "ratio":         390,
        "offset":        0,
        "rated_tau":     1.8,
        "acc_tau":       2.3,
        "max_tau":       3.3,
        'emergency_tau': 6.6,
        "max_omega":     8500,
        'rated_omega':   3500,
        "stator":        {
            "inertia_drive": 0.4e-6,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0.2
        },
        "rotor":         {
            "inertia_drive": 0.4e-7,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0.02
        },
    },

    'PT_SCARA_A4':  {
        "ratio":         10,
        "offset":        0,
        "rated_tau":     1.8,
        "acc_tau":       2.3,
        "max_tau":       3.3,
        'emergency_tau': 6.6,
        "max_omega":     8500,
        'rated_omega':   3500,
        "stator":        {
            "inertia_drive": 0.4e-6,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0.2
        },
        "rotor":         {
            "inertia_drive": 0.4e-7,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0.02
        },
    },

    'SHG20-50-741769-46': {
        "ratio": 50,
        "rated_tau": 33,
        "acc_tau": 44,
        "max_tau": 73,
        'emergency_tau': 127,
        "max_omega": 6500,
        'rated_omega': 3500,
        "offset": 26e-3,
        "stator": {
            "inertia_drive": 19.3e-6,
            "inertia_body": [315e-6, 315e-6, 550e-5],
            "cm": 0,
            "m": 0.79
        },
        "rotor": {
            "inertia_drive": 19.3e-7,
            "inertia_body": [0, 0, 0],
            "cm": 0,
            "m": 0.05
        },
    },

    'SHG17-50-741477-33': {
        "ratio": 50,
        "rated_tau": 21,
        "acc_tau": 34,
        "max_tau": 44,
        'emergency_tau': 127,
        "max_omega": 7300,
        'rated_omega': 3500,
        "offset": 26e-3,
        "stator": {
            "inertia_drive": 7.9e-6,
            "inertia_body": [101e-6, 101e-6, 355e-6],
            "cm": 0,
            "m": 0.6
        },
        "rotor": {
            "inertia_drive": 7.9e-7,
            "inertia_body": [0, 0, 0],
            "cm": 0,
            "m": 0.066
        },
    },

    'EPSON-LS3-401S-A3': {
        "ratio":         410.34,  # rad/mm
        "offset":        0,
        "rated_tau":     50,
        "acc_tau":       70,
        "max_tau":       90,
        'emergency_tau': 100,
        "max_omega":     8500,
        'rated_omega':   3500,
        "stator":        {
            "inertia_drive": 0.4e-6,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0.2
        },
        "rotor":         {
            "inertia_drive": 0.4e-7,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0.02
        },
    },

    'EPSON-LS3-401S-A4': {
        "ratio":         1,
        "offset":        0,
        "rated_tau":     1.8,
        "acc_tau":       2.3,
        "max_tau":       3.3,
        'emergency_tau': 6.6,
        "max_omega":     8500,
        'rated_omega':   3500,
        "stator":        {
            "inertia_drive": 0.4e-6,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0.2
        },
        "rotor":         {
            "inertia_drive": 0.4e-7,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0.02
        },
    },

    "175": {
        "ratio":               -80,
        "rated_tau":           85,
        "limit_torque_factor": 1.18,
        "acc_tau":             185.29999999999998,
        "max_tau":             170,
        "emergency_tau":       425,
        "max_omega":           4500,
        "rated_omega":         21.0526,
        "offset":              0,
        "stator":              {
            "inertia_drive": 0.000012,
            "inertia_body":  [
                0,
                0,
                0
            ],
            "cm":            -0.015,
            "m":             1.3
        },
        "rotor":               {
            "inertia_drive": 0.000012,
            "inertia_body":  [
                0,
                0,
                0
            ],
            "cm":            -0.015,
            "m":             0.8
        },
        "characteristic":      [
            [
                0,
                2128.3527835909454,
                2888.8695880103378,
                3304.6917256784864,
                3441.4753235956468
            ],
            [
                372,
                305.57,
                229.77,
                147.53,
                62
            ]
        ]
    },

    "176": {
        "ratio":               -61,
        "rated_tau":           75,
        "limit_torque_factor": 1.18,
        "acc_tau":             163.49999999999997,
        "max_tau":             150,
        "emergency_tau":       375,
        "max_omega":           6000,
        "rated_omega":         32.7869,
        "offset":              0,
        "stator":              {
            "inertia_drive": 0.000004,
            "inertia_body":  [
                0,
                0,
                0
            ],
            "cm":            -0.015,
            "m":             0.8
        },
        "rotor":               {
            "inertia_drive": 0.0000034,
            "inertia_body":  [
                0,
                0,
                0
            ],
            "cm":            -0.015,
            "m":             0.6
        },
        "characteristic":      [
            [
                0,
                1772.7154290063443,
                2407.3913233419435,
                2752.0859900931782,
                2866.984212343586
            ],
            [
                300,
                246.42,
                185.3,
                118.97,
                50
            ]
        ]
    },

    "177": {
        "ratio":               -87,
        "rated_tau":           34,
        "limit_torque_factor": 1.18,
        "acc_tau":             74.11999999999999,
        "max_tau":             68,
        "emergency_tau":       170,
        "max_omega":           6000,
        "rated_omega":         33.8983,
        "offset":              0,
        "stator":              {
            "inertia_drive": 0.0000019,
            "inertia_body":  [
                0,
                0,
                0
            ],
            "cm":            0,
            "m":             0.5
        },
        "rotor":               {
            "inertia_drive": 0.0000019,
            "inertia_body":  [
                0,
                0,
                0
            ],
            "cm":            0,
            "m":             0.4
        },
        "characteristic":      [
            [
                0,
                2128.3527835909454,
                2888.8695880103378,
                3304.6917256784864,
                3441.4753235956468
            ],
            [
                170.64,
                145.39,
                116.58,
                85.33,
                52.82
            ]
        ]
    },

    "178": {
        "ratio":               -60,
        "rated_tau":           75,
        "limit_torque_factor": 1.18,
        "acc_tau":             163.49999999999997,
        "max_tau":             150,
        "emergency_tau":       375,
        "max_omega":           4500,
        "rated_omega":         24.6914,
        "offset":              0,
        "stator":              {
            "inertia_drive": 0.000004,
            "inertia_body":  [
                0,
                0,
                0
            ],
            "cm":            -0.015,
            "m":             0.555
        },
        "rotor":               {
            "inertia_drive": 0.000004,
            "inertia_body":  [
                0,
                0,
                0
            ],
            "cm":            -0.015,
            "m":             0.555
        },
        "characteristic":      [
            [
                0,
                2254.1936936747293,
                3058.4812494276066,
                3501.6601066791955,
                3643.9150485130335
            ],
            [
                43.59,
                36.4,
                28.2,
                19.31,
                10.06
            ]
        ]
    },

    "179": {
        "ratio":               -57.9382889200561,
        "rated_tau":           21,
        "limit_torque_factor": 1.18,
        "acc_tau":             45.779999999999994,
        "max_tau":             56,
        "emergency_tau":       113,
        "max_omega":           7300,
        "rated_omega":         25,
        "offset":              0,
        "stator":              {
            "inertia_drive": 0,
            "inertia_body":  [
                0,
                0,
                0
            ],
            "cm":            -0.0165,
            "m":             0
        },
        "rotor":               {
            "inertia_drive": 0,
            "inertia_body":  [
                0,
                0,
                0
            ],
            "cm":            -0.011,
            "m":             0
        },
        "characteristic":      [
            [
                0,
                2292.4931010915352,
                3118.6660325111548,
                3561.8448897627432,
                3709.5711755132693
            ],
            [
                43.59,
                36.4,
                28.2,
                19.31,
                10.06
            ]
        ]
    },

    "180": {
        "ratio":               -36.580159532636785,
        "rated_tau":           21,
        "limit_torque_factor": 1.18,
        "acc_tau":             45.779999999999994,
        "max_tau":             56,
        "emergency_tau":       113,
        "max_omega":           7300,
        "rated_omega":         25,
        "offset":              0,
        "stator":              {
            "inertia_drive": 0,
            "inertia_body":  [
                0,
                0,
                0
            ],
            "cm":            -0.022,
            "m":             0
        },
        "rotor":               {
            "inertia_drive": 0,
            "inertia_body":  [
                0,
                0,
                0
            ],
            "cm":            -0.018,
            "m":             0
        },
        "characteristic":      [
            [
                0,
                3632.9723606796674,
                4935.1522128509923,
                5646.4269220202041,
                5876.22336652102
            ],
            [
                23.29,
                19.06,
                14.23,
                8.98,
                3.53
            ]
        ]
    }
}


def load_gear_db(installation):
    if 'type' in installation:
        if installation['type'] is not None:
            data = {**installation, **gear_db[installation['type']]}
            return data
    data = {
        **installation,
        "ratio":         1,
        "offset":        0,
        "rated_tau":     0,
        "acc_tau":       0,
        "max_tau":       0,
        'emergency_tau': 0,
        "max_omega":     8500,
        'rated_omega':   3500,
        "stator":        {
            "inertia_drive": 0,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0
        },
        "rotor":         {
            "inertia_drive": 0,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0
        },
    }
    if 'ratio_override' in installation:
        data['ratio'] = installation['ratio_override']
    return data
