# -*- coding: utf-8 -*-
"""
robot configurations
Created on Fri Mar 24 11:03:07 2017

@author: pei.sun
"""

import numpy as np

structurePara = [
            {
             "name":"groundbase",
             "displacement": np.array([0, 0, 152])*1e-3,
             },
            {
             "name":"rotationcolumn",
             "displacement": np.array([25, -102.7, -179.5])*1e-3,
             },
            {
             "name":"linkarm",
             "displacement": np.array([455, 0, 45.5])*1e-3,
             },
            {
             "name":"arm",
             "displacement": np.array([77, -35, -55.5])*1e-3,
             },
            {
             "name":"handbase",
             "displacement": np.array([0, 58.5, -343])*1e-3,
             },
            {
             "name":"handwrist",
             "displacement": np.array([80, 0, -32])*1e-3,
             },
            {
             "name":"handflange",
             "displacement": np.array([0, 0, -10])*1e-3,
             },
            ]

massPara = [
            # groundbase structure
            {
             "nest":"groundbase", "cm":np.array([-24, 0.11, 94.5])*1e-3, "m":6.22,
             "iT":np.array([59577, 73973, 71691, 91, -4423, -78])*1e-6
            },
            # rotation column structure
            {
             "nest":"rotationcolumn", "cm":np.array([10.626, -5.68, -133.73])*1e-3, "m":17.55,
             "iT":np.array([103036, 70800, 78664, 5324, -4510, -1018])*1e-6
            },
            # linkarm structure
            {
             "nest":"linkarm", "cm":np.array([223.874, 0, 7.783])*1e-3, "m":11.83,
             "iT":np.array([39099.1, 221732.3, 211717.2, 352.5, 10819.7, -64.7])*1e-6
            },
            # arm structure
            {
             "nest":"arm", "cm":np.array([19.574, 0, 0])*1e-3, "m":3.71,
             "iT":np.array([7876, 15988, 16799, 82, -317, -2077])*1e-6
            },
            # wrist structure
            {
             "nest":"handbase", "cm":np.array([0, 0, -148.875])*1e-3, "m":6.5,
             "iT":np.array([13348, 12263, 6332, -1195, 3.4, -1])*1e-6
            },
            # wrist hand structure
            {
             "nest":"handwrist", "cm":np.array([-1.2, 0.1, 5.8])*1e-3, "m":0.32,
             "iT":np.array([464, 507, 528, 0, -13, -0.1])*1e-6
            },
            # wrist hand installation material + cable
            {
             "nest":"handwrist", "cm":np.array([11.5, 12, -6.8])*1e-3, "m":0.166,
             "iT":np.array([126, 163, 130, 1.1, -15.1, -2.2])*1e-6
            },
            # wrist hand adapter
            {
             "nest":"handwrist", "cm":np.array([48.8, 0, 0])*1e-3, "m":0.079,
             "iT":np.array([87, 43, 45, 0, 0, 0])*1e-6
            },
            # wrist hand other
            {
             "nest":"handwrist", "cm":np.array([28.3, 0.4, 6])*1e-3, "m":0.079,
             "iT":np.array([126, 163, 130, 1.1, -15.1, -2.2])*1e-6
            },
            # A6 motor
            {
             "nest":"handwrist", "cm":np.array([41.1 - 28, 0, -30])*1e-3, "m":0.6,
             "iT":np.array([2500, 2500, 2500, 0, 0, 0])*1e-6
            },
            # flange structure
            {
             "nest":"handflange", "cm":np.array([0, 0, -1.4])*1e-3, "m":0.21,
             "iT":np.array([81, 81, 155, 0, 0, 0])*1e-6
            },
            # flange screws
            {
             "nest":"handflange", "cm":np.array([0, 0, 1])*1e-3, "m":0.022,
             "iT":np.array([7.8, 9, 16, 0, 0, 0])*1e-6
            },
            # load
            {
             "nest":"tcp", "cm":np.array([-60, 0, 70])*1e-3, "m":3,
             "iT":np.array([10121.53, 8704.276, 12707.248, 0, 0, 0])*1e-6
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
                    "m": 0.6,
                    "iT": np.array([320, 320, 123, 0, 0, 0])*1e-6,
                    "characteristic": {
                        'max': [[0, 5200, 6600, 8000, 8001],
                                [0.46, 0.46, 0.4, 0.36, 0]],
                        's1': [[0, 3000, 6000],
                               [0.16, 0.13, 0.08]]
                    }
                }
            ]

frictionPara = [
                {"nest":"rotationcolumn", "friction":[26.9, 4.0, 1]},
                {"nest":"linkarm", "friction":[37.95, 4.39, 1]},
                {"nest":"arm", "friction":[24.90, 6.10, 1]},
                {"nest":"handbase", "friction":[6.14, 1.15, 1]},
                {"nest":"handwrist", "friction":[9.24, 2.48, 1]},
                {"nest":"handflange", "friction":[8.75, 1.33, 1]}
               ]

gearPara = [
               {
                "nest":"groundbase",
                "ratio":-100,
                "offset":68.5e-3,
                "orientation":np.array([0, 0, 0]),
                "case":9,
                "stator":
                    {
                     "inertia_drive":172e-6,
                     "inertia_body":[5829e-6, 3725e-6, 3725e-6],
                     "cm":-36.5e-3,
                     "m":2.2
                     },
                "rotor":
                    {
                     "inertia_drive":172e-6,
                     "inertia_body":[1026e-6, 883e-6, 883e-6],
                     "cm":-26e-3,
                     "m":1.07
                     },
                },

               {
                "nest":"rotationcolumn",
                "ratio":-120,
                "offset":51.7e-3,
                "orientation":np.array([0, 0, np.pi/2]),
                "case":11,
                "stator":
                    {
                     "inertia_drive":169e-6,
                     "inertia_body":[259e-6, 187e-6, 187e-6],
                     "cm":-15e-3,
                     "m":0.48
                     },
                "rotor":
                    {
                     "inertia_drive":169e-6,
                     "inertia_body":[667e-6, 384e-6, 384e-6],
                     "cm":-15e-3,
                     "m":0
                     },
                },

               {
                "nest":"linkarm",
                "ratio":100,
                "offset":41e-3,
                "orientation":np.array([0, 0, np.pi]),
                "case":9,
                "stator":
                    {
                     "inertia_drive":41.3e-6,
                     "inertia_body":[259e-6, 187e-6, 187e-6],
                     "cm":-15e-3,
                     "m":0.48
                     },
                "rotor":
                    {
                     "inertia_drive":41.3e-6,
                     "inertia_body":[667e-6, 384e-6, 384e-6],
                     "cm":-15e-3,
                     "m":0
                     },
                },

               {
                "nest":"arm",
                "ratio":-850/9,
                "offset":10e-3,
                "orientation":np.array([0, np.pi/2, 0]),
                "case":9,
                "stator":
                    {
                     "inertia_drive":7.9e-6,
                     "inertia_body":[259e-6, 187e-6, 187e-6],
                     "cm":-17e-3,
                     "m":0.68
                     },
                "rotor":
                    {
                     "inertia_drive":7.9e-6,
                     "inertia_body":[667e-6, 384e-6, 384e-6],
                     "cm":-14.5e-3,
                     "m":0
                     },
                },

               {
                "nest":"handbase",
                "ratio":-66096/713,
                "offset":26.5e-3,
                "orientation":np.array([0, 0, -np.pi/2]),
                "case":9,
                "stator":
                    {
                     "inertia_drive":7.9e-6,
                     "inertia_body":[397e-6, 224e-6, 224e-6],
                     "cm":-16.5e-3,
                     "m":0.18
                     },
                "rotor":
                    {
                     "inertia_drive":7.9e-6,
                     "inertia_body":[109e-6, 75e-6, 75e-6],
                     "cm":-11e-3,
                     "m":0
                     },
                },

               {
                "nest":"handwrist",
                "ratio":-520960/8901,
                "offset":26.5e-3,
                "orientation":np.array([0, -np.pi/2, 0]),
                "case":9,
                "stator":
                    {
                     "inertia_drive":7.9e-6,
                     "inertia_body":[267e-6, 194e-6, 194e-6],
                     "cm":-22e-3,
                     "m":0.18
                     },
                "rotor":
                    {
                     "inertia_drive":7.9e-6,
                     "inertia_body":[54e-6, 66e-6, 66e-6],
                     "cm":-18e-3,
                     "m":0
                     },
                }
            ]