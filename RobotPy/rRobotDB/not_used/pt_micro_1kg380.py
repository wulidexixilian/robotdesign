# -*- coding: utf-8 -*-
"""
robot configurations kr6 900
Created on Fri Mar 24 11:03:07 2017

@author: pei.sun
"""
import numpy as np

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
             "displacement": np.array([155.3, 0, -30])*1e-3,
             },
            {
             "name": "arm",
             "displacement": np.array([64, -9, -22])*1e-3,
             },
            {
             "name": "handbase",
             "displacement": np.array([0, -8.5, -100])*1e-3,
             },
            {
             "name": "handwrist",
             "displacement": np.array([40.7, 0, 8.5])*1e-3,
             },
            {
             "name": "handflange",
             "displacement": np.array([0, 0, 0])*1e-3,
             }
            ]

massPara = [
            # groundbase structure
            {
             "nest": "groundbase", "cm": np.array([-12.2, 0, 52.59])*1e-3, "m": 1.21,
             "iT": np.array([0, 0, 0, 0, 0, 0])*1e-6
            },
            # rotation column structure
            {
             "nest": "rotationcolumn", "cm": np.array([-1.75, -2.16, -28.85])*1e-3, "m": 1.39,
             "iT": np.array([3671.92, 3600.79, 3128.22, 0, 0, 0])*1e-6
            },
            # linkarm structure
            {
             "nest": "linkarm", "cm": np.array([66.85, -13.54, -47.15])*1e-3, "m": 1.45,
             "iT": np.array([8038.03, 19211.05, 14393.16, 0, 0, 0])*1e-6
            },
            # arm structure
            {
             "nest": "arm", "cm": np.array([-18.74, -15.62, -34.72])*1e-3, "m": 0.51,
             "iT": np.array([1335.47, 1678.4, 1286.26, 0, 0, 0])*1e-6
            },
            # wrist structure
            {
             "nest": "handbase", "cm":np.array([-1.43, -4.01, -64.16])*1e-3, "m":0.48,
             "iT":np.array([3197.98, 3064.24, 579.79, 0, 0, 0])*1e-6
            },
            # wrist hand structure
            {
             "nest": "handwrist", "cm": np.array([0, 9.09, 19.8])*1e-3, "m": 0.094,
             "iT": np.array([114.01, 70.72, 79.18, 0, 0, 0])*1e-6
            },
            # flange structure
            {
             "nest": "handflange", "cm": np.array([0, 0, -3])*1e-3, "m": 0.04,
             "iT": np.array([50, 50, 50, 0, 0, 0])*1e-6
            },
            # load
            # {
            #  "nest":"tcp", "cm":np.array([0, 10, 30])*1e-3, "m":0.5,
            #  "iT":np.array([500, 500, 500, 0, 0, 0])*1e-6
            # }
           ]

motorPara = [
                # A1 motor TSM4102 AC200V
                {
                    "nest": "groundbase",
                    "position": np.array([0, 0, 75.5])*1e-3,
                    "orientation": np.array([0, 0, np.pi]),
                    "cm": np.array([0, 0, -35])*1e-3,
                    "m": 0.6,
                    "J_rotor": 2.9e-6,
                    "iT": np.array([0, 0, 0, 0, 0, 0])*1e-6,
                    "characteristic": {
                        'max': [[0, 3500, 6000],
                                [0.56, 0.56, 0.56]],
                        's1': [[0, 3000, 6000],
                               [0.159, 0.159, 0.09]]
                    }
                },
                # A2 motor TSM4102 AC200V
                {
                    "nest": "rotationcolumn",
                    "position": np.array([0, -25, -82.5])*1e-3,
                    "orientation": np.array([0, 0, np.pi/2]),
                    "cm": np.array([0, 0, -35])*1e-3,
                    "m": 0.6,
                    "J_rotor": 2.9e-6,
                    "iT": np.array([0, 0, 0, 0, 0, 0])*1e-6,
                    "characteristic": {
                        'max': [[0, 3500, 6000],
                                [0.56, 0.56, 0.56]],
                        's1': [[0, 3000, 6000],
                               [0.159, 0.159, 0.09]]
                    }
                },
                # A3 motor TS4601 DC24V
                {
                    "nest": "linkarm",
                    "position": np.array([75.7, -30, -5])*1e-3,
                    "orientation": np.array([0, 0, 0]),
                    "cm": np.array([0, 0, -25])*1e-3,
                    "m": 0.3,
                    "J_rotor": 0.1e-6,
                    "iT": np.array([0, 0, 0, 0, 0, 0])*1e-6,
                    "characteristic": {
                        'max': [[0, 3000, 6000],
                                [0.29, 0.29, 0.14]],
                        's1': [[0, 3000, 6000],
                               [0.095, 0.095, 0.07]]
                    }
                },
                # A4 motor TS4864DC24V
                # {
                #     "nest":           "arm",
                #     "position":       np.array([30, -14, -33]) * 1e-3,
                #     "orientation":    np.array([0, -np.pi / 2, 0]),
                #     "cm":             np.array([0, 0, -35]) * 1e-3,
                #     "m":              0.09,
                #     "J_rotor":        0.17e-6,
                #     "iT":             np.array([0, 0, 0, 0, 0, 0]) * 1e-6,
                #     "characteristic": {
                #         'max': [[0, 6000],
                #                 [0.096, 0.096]],
                #         's1':  [[0, 3000, 6000],
                #                 [0.032, 0.032, 0.0125]]
                #     }
                # },
                # # A4 motor TS4862DC24V
                {
                    "nest": "arm",
                    "position":       np.array([30, -14, -33])*1e-3,
                    "orientation":    np.array([0, -np.pi/2, 0]),
                    "cm":             np.array([0, 0, -25]) * 1e-3,
                    "m":              0.06,
                    "J_rotor":        0.096e-6,
                    "iT":             np.array([0, 0, 0, 0, 0, 0]) * 1e-6,
                    "characteristic": {
                        'max': [[0, 6000],
                                [0.0477, 0.0477]],
                        's1':  [[0, 3000, 6000],
                                [0.0159, 0.0159, 0.007]]
                    }
                },
                # A5 motor TS4864DC24V
                # {
                #     "nest": "handbase",
                #     "position": np.array([60, 10, 0])*1e-3,
                #     "orientation": np.array([0, -np.pi/2, 0]),
                #     "cm": np.array([0, 0, 35])*1e-3,
                #     "m": 0.09,
                #     "J_rotor": 0.17e-6,
                #     "iT": np.array([0, 0, 0, 0, 0, 0])*1e-6,
                #     "characteristic": {
                #         'max': [[0, 6000],
                #                 [0.096, 0.096]],
                #         's1': [[0, 3000, 6000],
                #                [0.032, 0.032, 0.0125]]
                #     }
                # },
                # # A5 motor TS4862DC24V
                {
                    "nest":           "handbase",
                    "position":       np.array([0, -35, -32]) * 1e-3,
                    "orientation":    np.array([0, 0, np.pi/2]),
                    "cm":             np.array([0, 0, -25]) * 1e-3,
                    "m":              0.06,
                    "J_rotor":        0.096e-6,
                    "iT":             np.array([0, 0, 0, 0, 0, 0]) * 1e-6,
                    "characteristic": {
                        'max': [[0, 6000],
                                [0.0477, 0.0477]],
                        's1':  [[0, 3000, 6000],
                                [0.0159, 0.0159, 0.007]]
                    }
                },
                # A6 motor TS4862DC24V
                # {
                #     "nest":           "handwrist",
                #     "position":       np.array([20, 0, 8.5]) * 1e-3,
                #     "orientation":    np.array([0, np.pi/2, 0]),
                #     "cm":             np.array([0, 0, -25]) * 1e-3,
                #     "m":              0.06,
                #     "J_rotor":        0.098e-6,
                #     "iT":             np.array([0, 0, 0, 0, 0, 0]) * 1e-6,
                #     "characteristic": {
                #         'max': [[0, 6000],
                #                 [0.0477, 0.0477]],
                #         's1':  [[0, 3000, 6000],
                #                 [0.0159, 0.0159, 0.0159]]
                #     }
                # },
                # # A6 motor TS4861DC24V
                {
                    "nest": "handwrist",
                    "position": np.array([20, 0, 8.5])*1e-3,
                    "orientation": np.array([0, np.pi/2, 0]),
                    "cm": np.array([0, 0, -22])*1e-3,
                    "m": 0.05,
                    "J_rotor": 0.063e-6,
                    "iT": np.array([0, 0, 0, 0, 0, 0])*1e-6,
                    "characteristic": {
                        'max': [[0, 6000],
                                [0.0285, 0.0285]],
                        's1': [[0, 3000, 6000],
                               [0.0095, 0.0095, 0.0049]]
                    }
                }
            ]

frictionPara = [
                {"nest": "rotationcolumn", "friction": [1.36, 0.008, 1]},
                {"nest": "linkarm", "friction": [1.5, 0.008, 1]},
                {"nest": "arm", "friction": [0.7, 0.002, 1]},
                {"nest": "handbase", "friction": [0.345, 0.001, 1]},
                {"nest": "handwrist", "friction": [0.345, 0.001, 1]},
                {"nest": "handflange", "friction": [0.15, 0.0006, 1]}
               ]

gearPara = [
               # CobaltLine-14-CPM-80
               {
                "nest": "groundbase",
                "ratio": 80,
                "rated_tau": 10,
                "acc_tau": 14,
                "max_tau": 30,
                "limit_factor": 1.35,
                "max_omega": 8500,
                "offset": 0,
                "case": 9,
                "stator":
                    {
                     "inertia_drive": 3.3e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0.54
                     },
                "rotor":
                    {
                     "inertia_drive": 5e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0
                     },
                },
               # CobaltLine-14-CPM-100
               {
                "nest": "rotationcolumn",
                "ratio": 100,
                "offset": 0,
                "rated_tau": 10,
                "acc_tau": 14,
                "max_tau": 36,
                "limit_factor": 1.35,
                "max_omega": 8500,
                "case": 9,
                "stator":
                    {
                     "inertia_drive": 3.3e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0.54
                     },
                "rotor":
                    {
                     "inertia_drive": 5e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0
                     },
                },
               # CobaltLine-14-CPM-80
               {
                "nest": "linkarm",
                "ratio": 80,
                "offset": 0,
                "rated_tau": 3.5,
                "acc_tau":   5.5,
                "max_tau": 8.3,
                "limit_factor": 1.35,
                "max_omega": 8500,
                "case": 9,
                "stator":
                    {
                     "inertia_drive": 0.05e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0.176
                     },
                "rotor":
                    {
                     "inertia_drive": 0.05e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0
                     },
                },
               # CSF8-2XH-50
               {
                "nest": "arm",
                "ratio": 75,
                "offset": 0,
                "rated_tau": 1.8,
                "acc_tau": 2.3,
                "max_tau": 3.3,
                "limit_factor": 1.2,
                "max_omega": 8500,
                "case": 9,
                "stator":
                    {
                     "inertia_drive": 0.01e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0.11
                     },
                "rotor":
                    {
                     "inertia_drive": 0.01e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0
                     },
                },
               # CSF8-2XH-50
               {
                "nest": "handbase",
                "ratio": 75,
                "offset": 0,
                "rated_tau": 1.8,
                "acc_tau": 2.3,
                "max_tau": 3.3,
                "limit_factor": 1.2,
                "max_omega": 6000,
                "case": 9,
                "stator":
                    {
                     "inertia_drive": 0.01e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0.11
                     },
                "rotor":
                    {
                     "inertia_drive": 0.01e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0
                     },
                },
               # CSF8-2XH-50
               {
                "nest": "handwrist",
                "ratio": 50,
                "offset": 0,
                "rated_tau": 0.9,
                "acc_tau": 1.4,
                "max_tau": 1.8,
                "limit_factor": 1.2,
                "max_omega": 8500,
                "case": 9,
                "stator":
                    {
                     "inertia_drive": 0.005e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0.11
                     },
                "rotor":
                    {
                     "inertia_drive": 0.005e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0
                     },
                }
            ]