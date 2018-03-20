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
             "displacement": np.array([220.3, 0, -30])*1e-3,
             },
            {
             "name": "arm",
             "displacement": np.array([75, -9, -22])*1e-3,
             },
            {
             "name": "handbase",
             "displacement": np.array([0, -8.5, -110])*1e-3,
             },
            {
             "name": "handwrist",
             "displacement": np.array([40.7, 0, 8.5])*1e-3,
             },
            {
             "name": "handflange",
             "displacement": np.array([0, 0, -5])*1e-3,
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
             "nest": "linkarm", "cm": np.array([100, -13.54, -47.15])*1e-3, "m": 1.8,
             "iT": np.array([8038.03, 19211.05, 14393.16, 0, 0, 0])*1e-6
            },
            # arm structure
            {
             "nest": "arm", "cm": np.array([-18.74, -15.62, -38])*1e-3, "m": 0.7,
             "iT": np.array([1335.47, 1678.4, 1286.26, 0, 0, 0])*1e-6
            },
            # wrist structure
            {
             "nest": "handbase", "cm":np.array([-1.43, -4.01, -60])*1e-3, "m":0.7,
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
                # A1 motor TSM3104 DC48V
                {
                    "nest": "groundbase",
                    "position": np.array([0, 0, 75.5])*1e-3,
                    "orientation": np.array([0, 0, np.pi]),
                    "cm": np.array([0, 0, -50])*1e-3,
                    "m": 0.7,
                    "J_rotor": 6.2e-6,
                    "iT": np.array([0, 0, 0, 0, 0, 0])*1e-6,
                    "characteristic": {
                        'max': [[0, 2800, 6000],
                                [1.11, 1.11, 0.4]],
                        's1': [[0, 3000, 6000],
                               [0.318, 0.318, 0.18]]
                    }
                },

                # A2 motor TSM3104 DC48V
                {
                    "nest": "rotationcolumn",
                    "position": np.array([0, -25, -82.5])*1e-3,
                    "orientation": np.array([0, 0, np.pi/2]),
                    "cm": np.array([0, 0, -50])*1e-3,
                    "m": 0.7,
                    "J_rotor": 6.2e-6,
                    "iT": np.array([0, 0, 0, 0, 0, 0])*1e-6,
                    "characteristic": {
                        'max': [[0, 2800, 6000],
                                [1.11, 1.11, 0.4]],
                        's1':  [[0, 3000, 6000],
                                [0.318, 0.318, 0.18]]
                    }
                },

                # A3 motor TS3102 DC48V
                {
                    "nest": "linkarm",
                    "position": np.array([75.7, -30, -5])*1e-3,
                    "orientation": np.array([0, 0, 0]),
                    "cm": np.array([0, 0, -45])*1e-3,
                    "m": 0.6,
                    "J_rotor": 2.3e-6,
                    "iT": np.array([0, 0, 0, 0, 0, 0])*1e-6,
                    "characteristic": {
                        'max': [[0, 1800, 6000],
                                [0.56, 0.56, 0.12]],
                        's1': [[0, 3000, 6000],
                               [0.159, 0.159, 0.08]]
                    }
                },

                # A4 motor TS4866DC24V
                {
                    "nest":           "arm",
                    "position":       np.array([30, -14, -33]) * 1e-3,
                    "orientation":    np.array([0, -np.pi / 2, 0]),
                    "cm":             np.array([0, 0, -35]) * 1e-3,
                    "m":              0.12,
                    "J_rotor":        0.26e-6,
                    "iT":             np.array([0, 0, 0, 0, 0, 0]) * 1e-6,
                    "characteristic": {
                        'max': [[0, 6000],
                                [0.1431, 0.1431]],
                        's1':  [[0, 3000, 6000],
                                [0.0477, 0.0477, 0.025]]
                    }
                },

                # A5 motor TS4864DC24V
                {
                    "nest": "handbase",
                    "position": np.array([60, 10, 0])*1e-3,
                    "orientation": np.array([0, -np.pi/2, 0]),
                    "cm": np.array([0, 0, 35])*1e-3,
                    "m": 0.09,
                    "J_rotor": 0.17e-6,
                    "iT": np.array([0, 0, 0, 0, 0, 0])*1e-6,
                    "characteristic": {
                        'max': [[0, 6000],
                                [0.096, 0.096]],
                        's1': [[0, 3000, 6000],
                               [0.032, 0.032, 0.0125]]
                    }
                },

                # A6 motor TS4862DC24V
                {
                    "nest":           "handwrist",
                    "position":       np.array([20, 0, 8.5]) * 1e-3,
                    "orientation":    np.array([0, np.pi/2, 0]),
                    "cm":             np.array([0, 0, -25]) * 1e-3,
                    "m":              0.06,
                    "J_rotor":        0.098e-6,
                    "iT":             np.array([0, 0, 0, 0, 0, 0]) * 1e-6,
                    "characteristic": {
                        'max': [[0, 6000],
                                [0.0477, 0.0477]],
                        's1':  [[0, 3000, 6000],
                                [0.0159, 0.0159, 0.008]]
                    }
                }
            ]

frictionPara = [
                {"nest": "rotationcolumn", "friction": [2, 0.01, 1]},
                {"nest": "linkarm", "friction": [2, 0.01, 1]},
                {"nest": "arm", "friction": [1.5, 0.008, 1]},
                {"nest": "handbase", "friction": [0.345, 0.001, 1]},
                {"nest": "handwrist", "friction": [0.345, 0.001, 1]},
                {"nest": "handflange", "friction": [0.15, 0.0006, 1]}
               ]

gearPara = [
               # A1 CobaltLine-17-CPM-100
               {
                "nest": "groundbase",
                "ratio": 100,
                "rated_tau": 29,
                "acc_tau": 35,
                "max_tau": 56,
                "limit_factor": 1.35,
                "max_omega": 7300,
                "offset": 0,
                "case": 9,
                "stator":
                    {
                     "inertia_drive": 7.9e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0.79
                     },
                "rotor":
                    {
                     "inertia_drive": 0.1e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0
                     },
                },
               # A2 CobaltLine-17-CPM-100
               {
                "nest": "rotationcolumn",
                "ratio": 100,
                "rated_tau": 29,
                "acc_tau": 35,
                "max_tau": 56,
                "limit_factor": 1.35,
                "max_omega": 7300,
                "offset": 0,
                "case": 9,
                "stator":
                    {
                     "inertia_drive": 7.9e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0.79
                     },
                "rotor":
                    {
                     "inertia_drive": 0.1e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0
                     },
                },
               # A3 CobaltLine-14-CPM-80
               {
                "nest": "linkarm",
                "ratio": 80,
                "offset": 0,
                "rated_tau": 10,
                "acc_tau": 14,
                "max_tau": 30,
                "limit_factor": 1.35,
                "max_omega": 7300,
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
                     "inertia_drive": 0.05e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0
                     },
                },
               # A4 CSF11-2XH-50
               {
                "nest": "arm",
                "ratio": 50,
                "offset": 0,
                "rated_tau": 3.5,
                "acc_tau": 5.5,
                "max_tau": 8.3,
                "limit_factor": 1.35,
                "max_omega": 8500,
                "case": 9,
                "stator":
                    {
                     "inertia_drive": 1.4e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0.176
                     },
                "rotor":
                    {
                     "inertia_drive": 0.01e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0
                     },
                },
               # A5 CSF11-2XH-50
               {
                "nest": "handbase",
                "ratio": 72,
                "offset": 0,
                "rated_tau": 3.5,
                "acc_tau": 5.5,
                "max_tau": 8.3,
                "limit_factor": 1.35,
                "max_omega": 8500,
                "case": 9,
                "stator":
                    {
                     "inertia_drive": 1.4e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0.176
                     },
                "rotor":
                    {
                     "inertia_drive": 0.01e-6,
                     "inertia_body": [0, 0, 0],
                     "cm": 0,
                     "m": 0
                     },
                },
               # A6 CSF8-2XH-50
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