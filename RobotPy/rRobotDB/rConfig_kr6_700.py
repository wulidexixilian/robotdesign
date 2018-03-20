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
             "displacement": np.array([0, 0, 208])*1e-3,
             },
            {
             "name": "rotationcolumn",
             "displacement": np.array([25, -90.7, -192])*1e-3,
             },
            {
             "name": "linkarm",
             "displacement": np.array([355, 0, -4.2])*1e-3,
             },
            {
             "name": "arm",
             "displacement": np.array([141, -25, -86.5])*1e-3,
             },
            {
             "name": "handbase",
             "displacement": np.array([0, 50, -224])*1e-3,
             },
            {
             "name": "handwrist",
             "displacement": np.array([61.5, 0, -50.5])*1e-3,
             },
            {
             "name": "handflange",
             "displacement": np.array([0, 0, -28.5])*1e-3,
             },
            ]

massPara = [
            # groundbase structure
            {
             "nest":"groundbase", "cm":np.array([0, 0, -100])*1e-3, "m":16.257,
             "iT":np.array([1, 1, 1, 0, 0, 0])*1e-6
            },
            # rotation column structure
            {
             "nest":"rotationcolumn", "cm":np.array([7.8903, -22.52, -108.4429])*1e-3, "m":10.044,
             "iT":np.array([129500, 99300, 85100, 64, -2300, 65])*1e-6
            },
            # linkarm structure
            {
             "nest":"linkarm", "cm":np.array([112.295, -4.202, -72.6038])*1e-3, "m":15.1339,
             "iT":np.array([74300, 330600, 294300, 3600, -3500, 255])*1e-6
            },
            # arm structure
            {
             "nest":"arm", "cm":np.array([24.7958, -12.4222, -75.59])*1e-3, "m":4.754,
             "iT":np.array([15600, 24400, 25900, -1700, 1600, -659])*1e-6
            },
            # wrist structure
            {
             "nest":"handbase", "cm":np.array([5.3696, 14.2314, -97.7160])*1e-3, "m":4.835,
             "iT":np.array([41300, 38600, 11500, -1195, -250, 1000])*1e-6
            },
            # wrist hand structure
            {
             "nest":"handwrist", "cm":np.array([19.3999, 0.7687, -33.0579])*1e-3, "m":1.6438,
             "iT":np.array([2000, 3000, 2500, -5.5, 435, 2.9])*1e-6
            },
            # flange structure
            {
             "nest":"handflange", "cm":np.array([0, 0, -13.8912])*1e-3, "m":0.4640,
             "iT":np.array([176, 177, 296, 0, 0, 0])*1e-6
            },
            # load
            {
                "nest": "tcp", "cm": np.array([0, 60, 80]) * 1e-3, "m": 6,
                "iT": np.array([45000, 45000, 45000, 0, 0, 0]) * 1e-6
            }
           ]

motorPara = [
                # A1 motor
                {
                    "nest": "groundbase",
                    "position": np.array([0, 0, 152])*1e-3,
                    "orientation": np.array([0, 0, np.pi]),
                    "cm": np.array([0, 0, 69])*1e-3,
                    "m": 0,
                    "iT": np.array([2840, 2840, 2840, 0, 0, 0])*1e-6*0,
                    "characteristic": {
                        'max': [[0, 3040, 5520, 8000, 8001],
                                [5.98, 5.98, 4.22, 1.79, 0]],
                        's1': [[0, 3000, 6000],
                               [2.39, 2.39, 1.2]]
                    }
                },
                # A2 motor
                {
                    "nest": "rotationcolumn",
                    "position": np.array([25, -56, -179.5])*1e-3,
                    "orientation": np.array([0, 0, -np.pi/2]),
                    "cm": np.array([0, 0, 69])*1e-3,
                    "m": 0,
                    "iT": np.array([2840, 2840, 1050, 0, 0, 0])*1e-6*0,
                    "characteristic": {
                        'max': [[0, 3040, 5520, 8000, 8001],
                                [5.98, 5.98, 4.22, 1.79, 0]],
                        's1': [[0, 3000, 6000],
                               [2.39, 2.39, 1.2]]
                    }
                },
                # A3 motor
                {
                    "nest": "linkarm",
                    "position": np.array([294, -12, 44])*1e-3,
                    "orientation": np.array([0, 0, np.pi]),
                    "cm": np.array([0, 0, 63])*1e-3,
                    "m": 0,
                    "iT": np.array([1800, 1800, 700, 0, 0, 0])*1e-6*0,
                    "characteristic": {
                        'max': [[0, 4320, 6160, 8000, 8001],
                                [3.256, 3.2, 2.6, 2, 0]],
                        's1': [[0, 3000, 6000],
                               [1.27, 1.1, 0.65]]
                    }
                },
                # A4 motor
                {
                    "nest": "arm",
                    "position": np.array([33.2, -25, -55.5])*1e-3,
                    "orientation": np.array([0, -np.pi/2, 0]),
                    "cm": np.array([0, 0, 56])*1e-3,
                    "m": 0,
                    "iT": np.array([1000, 1000, 150, 0, 0, 0])*1e-6*0,
                    "characteristic": {
                        'max': [[0, 3200, 5600, 8000, 8001],
                                [0.92, 0.92, 0.54, 0.38, 0]],
                        's1': [[0, 3000, 6000],
                               [0.318, 0.26076, 0.18]]
                    }
                },
                # A5 motor
                {
                    "nest": "handbase",
                    "position": np.array([0, 53, -112.75])*1e-3,
                    "orientation": np.array([0, 0, np.pi/2]),
                    "cm": np.array([0,0, 56])*1e-3,
                    "m": 0,
                    "iT": np.array([1000, 1000, 150, 0, 0, 0])*1e-6*0,
                    "characteristic": {
                        'max': [[0, 3200, 5600, 8000, 8001],
                                [0.92, 0.92, 0.54, 0.38, 0]],
                        's1': [[0, 3000, 6000],
                               [0.318, 0.26076, 0.18]]
                    }
                },
                # A6 motor
                {
                    "nest": "handwrist",
                    "position": np.array([48.4, 0, -32])*1e-3,
                    "orientation": np.array([0, -np.pi/2, 0]),
                    "cm": np.array([0, 0, 41])*1e-3,
                    "m": 0,
                    "iT": np.array([320, 320, 123, 0, 0, 0])*1e-6*0,
                    "characteristic": {
                        'max': [[0, 5200, 6600, 8000, 8001],
                                [0.46, 0.46, 0.4, 0.36, 0]],
                        's1': [[0, 3000, 6000],
                               [0.16, 0.13, 0.08]]
                    }
                }
            ]

frictionPara = [
                {"nest":"rotationcolumn", "friction":[46.3, 13, 1]},
                {"nest":"linkarm", "friction":[41.4, 15.5, 1]},
                {"nest":"arm", "friction":[20.1, 4.9, 1]},
                {"nest":"handbase", "friction":[4.5, 0.7, 1]},
                {"nest":"handwrist", "friction":[6.5, 1, 1]},
                {"nest":"handflange", "friction":[6.6, 0.6, 1]}
               ]

gearPara = [
               {
                "nest":"groundbase",
                "ratio":100,
                "offset":0,
                "case":9,
                "stator":
                    {
                     "inertia_drive":0,
                     "inertia_body":[0, 0, 0],
                     "cm":-39e-3,
                     "m":0
                     },
                "rotor":
                    {
                     "inertia_drive":0,
                     "inertia_body":[0, 0, 0],
                     "cm":-16e-3,
                     "m":0
                     },
                },

               {
                "nest":"rotationcolumn",
                "ratio":120,
                "offset":0,
                "case":15,
                "stator":
                    {
                     "inertia_drive":0,
                     "inertia_body":[0, 0, 0],
                     "cm":-30.62e-3,
                     "m":0
                     },
                "rotor":
                    {
                     "inertia_drive":0,
                     "inertia_body":[0, 0, 0],
                     "cm":-14.48e-3,
                     "m":0
                     },
                },

               {
                "nest":"linkarm",
                "ratio":105.4,
                "offset":0,
                "case":13,
                "stator":
                    {
                     "inertia_drive":0,
                     "inertia_body":[0, 0, 0],
                     "cm":-24.6e-3,
                     "m":0
                     },
                "rotor":
                    {
                     "inertia_drive":0,
                     "inertia_body":[0, 0, 0],
                     "cm":-11.6e-3,
                     "m":0
                     },
                },

               {
                "nest":"arm",
                "ratio":80,
                "offset":0,
                "case":9,
                "stator":
                    {
                     "inertia_drive":0,
                     "inertia_body":[0, 0, 0],
                     "cm":-15.9e-3,
                     "m":0
                     },
                "rotor":
                    {
                     "inertia_drive":0,
                     "inertia_body":[0, 0, 0],
                     "cm":-9.4e-3,
                     "m":0
                     },
                },

               {
                "nest":"handbase",
                "ratio":77.4783,
                "offset":0,
                "case":13,
                "stator":
                    {
                     "inertia_drive":0,
                     "inertia_body":[0, 0, 0],
                     "cm":-16.11e-3,
                     "m":0
                     },
                "rotor":
                    {
                     "inertia_drive":0,
                     "inertia_body":[0, 0, 0],
                     "cm":-9.4e-3,
                     "m":0
                     },
                },

               {
                "nest":"handwrist",
                "ratio":81,
                "offset":0,
                "case":13,
                "stator":
                    {
                     "inertia_drive":0,
                     "inertia_body":[0, 0, 0],
                     "cm":-16.11e-3,
                     "m":0
                     },
                "rotor":
                    {
                     "inertia_drive":0,
                     "inertia_body":[0, 0, 0],
                     "cm":-9.4e-3,
                     "m":0
                     },
                }
            ]
