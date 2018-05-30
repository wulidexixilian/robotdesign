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
}


def load_gear_db(installation):
    data = {**installation, **gear_db[installation['type']]}
    return data
