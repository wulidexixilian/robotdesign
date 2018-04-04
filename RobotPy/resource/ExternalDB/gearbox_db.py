gear_db = {
    'CSG-17-100-2UH': {
        "ratio": 100,
        "rated_tau": 31,
        "acc_tau": 51,
        "max_tau": 70,
        'emergency_tau': 109,
        "limit_factor": 1.15,
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
             "inertia_drive": 8e-6,
             "inertia_body": [0, 0, 0],
             "cm": 0,
             "m": 0
        },
    },

    'SHG-17-100-2SO': {
        "ratio": 100,
        "rated_tau": 31,
        "acc_tau": 51,
        "max_tau": 70,
        'emergency_tau': 143,
        "limit_factor": 1.15,
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
             "inertia_drive": 8e-6,
             "inertia_body": [0, 0, 0],
             "cm": 0,
             "m": 0
        },
    },

    'SHG-17-120-2SO': {
        "ratio": 120,
        "rated_tau": 31,
        "acc_tau": 51,
        "max_tau": 70,
        'emergency_tau': 143,
        "limit_factor": 1.2,
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
            "inertia_drive": 8e-6,
            "inertia_body": [0, 0, 0],
            "cm": 0,
            "m": 0
        },
    },

    'SHG-14-80-2SO-LW': {
        "ratio": 80,
        "offset": 0,
        "rated_tau": 10,
        "acc_tau": 14,
        "max_tau": 30,
        'emergency_tau': 61,
        "limit_factor": 1.35,
        "max_omega": 8500,
        'rated_omega': 3500,
        "stator": {
             "inertia_drive": 4.72e-6,
             "inertia_body": [0, 0, 0],
             "cm": 0,
             "m": 0.54
        },
        "rotor": {
             "inertia_drive": 4.72e-6,
             "inertia_body": [0, 0, 0],
             "cm": 0,
             "m": 0
        },
    },

    'SHG-14-100-2SO-LW': {
        "ratio":         100,
        "offset":        0,
        "rated_tau":     10,
        "acc_tau":       14,
        "max_tau":       30,
        'emergency_tau': 61,
        "limit_factor":  1.15,
        "max_omega":     8500,
        'rated_omega':   3500,
        "stator":        {
            "inertia_drive": 4.72e-6,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0.54
        },
        "rotor":         {
            "inertia_drive": 4.72e-6,
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
        "limit_factor": 1.15,
        "max_omega":    8500,
        'rated_omega': 3500,
        "stator": {
             "inertia_drive": 1.4e-6,
             "inertia_body": [0, 0, 0],
             "cm": 0,
             "m": 0.176
        },
        "rotor": {
             "inertia_drive": 0.01e-6,
             "inertia_body": [0, 0, 0],
             "cm": 0,
             "m": 0
        },
    },

    'CSF11-50-2UP': {
        "ratio":        50,
        "offset":       0,
        "rated_tau":    3.5,
        "acc_tau":      5.5,
        "max_tau":      8.3,
        'emergency_tau': 17,
        "limit_factor": 1.2,
        "max_omega":    8500,
        'rated_omega': 3500,
        "stator":       {
            "inertia_drive": 1.5e-6,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0.33
        },
        "rotor":        {
            "inertia_drive": 0.01e-6,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0
        },
    },

    'CSF8-50-2UP': {
        "ratio": 50,
        "offset": 0,
        "rated_tau": 1.8,
        "acc_tau": 2.3,
        "max_tau": 3.3,
        'emergency_tau': 6.6,
        "limit_factor": 1.2,
        "max_omega": 8500,
        'rated_omega': 3500,
        "stator": {
             "inertia_drive": 0.4e-6,
             "inertia_body": [0, 0, 0],
             "cm": 0,
             "m": 0.2
        },
        "rotor": {
             "inertia_drive": 0.5e-6,
             "inertia_body": [0, 0, 0],
             "cm": 0,
             "m": 0
        },
    },

    'CSF5-50-2XH-F': {
        "ratio":         50,
        "offset":        0,
        "rated_tau":     0.4,
        "acc_tau":       0.53,
        "max_tau":       0.9,
        'emergency_tau': 1.8,
        "limit_factor":  1.15,
        "max_omega":     8500,
        'rated_omega':   3500,
        "stator":        {
            "inertia_drive": 0.25e-6,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0.025
        },
        "rotor":         {
            "inertia_drive": 0.25e-6,
            "inertia_body":  [0, 0, 0],
            "cm":            0,
            "m":             0
        },
    },
}


def load_gear_db(installation):
    data = {**installation, **gear_db[installation['type']]}
    if 'pre ratio' in installation:
        if installation['pre ratio'] is not None:
            data['ratio'] = data['ratio'] * data['pre ratio']
    return data
