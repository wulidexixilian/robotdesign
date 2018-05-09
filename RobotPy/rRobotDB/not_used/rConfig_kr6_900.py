# -*- coding: utf-8 -*-
"""
robot configurations kr6 900
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
             "displacement": np.array([191, -25, -55.5])*1e-3,
             },
            {
             "name":"handbase",
             "displacement": np.array([0, 58.5, -219])*1e-3,
             },
            {
             "name":"handwrist",
             "displacement": np.array([53.5, 0, -32])*1e-3,
             },
            {
             "name":"handflange",
             "displacement": np.array([0, 0, -10])*1e-3,
             },
            ]

massPara = [
            # groundbase structure
            {
             "nest":"groundbase", "cm":np.array([-24, 0.11, 94.5])*1e-3, "m":6.5,
             "iT":np.array([59577, 73973, 71691, 91, -4423, -78])*1e-6
            },
            # rotation column structure
            {
             "nest":"rotationcolumn", "cm":np.array([5.9, -0.9, -97.2])*1e-3, "m":7.8,
             "iT":np.array([103036, 70800, 78664, 5324, -4510, -1018])*1e-6
            },
            # linkarm structure
            {
             "nest":"linkarm", "cm":np.array([202.8, -6.8, -41.7])*1e-3, "m":6.84,
             "iT":np.array([40365, 235940, 222805, 465, 8747, -750])*1e-6
            },
            # linkarm cover
            {
             "nest":"linkarm", "cm":np.array([383.2, -5.7, -51])*1e-3, "m":0.6,
             "iT":np.array([9431, 12276, 4386, -0.4, 1.3, 225])*1e-6
            },
            # linkarm drivetrain + screws
            {
             "nest":"linkarm", "cm":np.array([330.9, -2.9, 33.4])*1e-3, "m":0.5,
             "iT":np.array([646.5, 16535, 16460, -39, 1410, 51.2])*1e-6
            },
            # linkarm other
            {
             "nest":"linkarm", "cm":np.array([218, 0.5, -79.4])*1e-3, "m":0.3,
             "iT":np.array([1633.2, 14875.2, 14377.7, 52.2, 1910.6, 135])*1e-6
            },
            # arm structure
            {
             "nest":"arm", "cm":np.array([63.6, -13.5, -50.2])*1e-3, "m":3.5,
             "iT":np.array([12423, 30203, 29545, 235, -317, -207])*1e-6
            },
            # arm cabel assembly
            {
             "nest":"arm", "cm":np.array([60, -3, -85])*1e-3, "m":0.11,
             "iT":np.array([120, 600, 650, 0, 90, -42])*1e-6
            },

            # wrist structure
            {
             "nest":"handbase", "cm":np.array([0, 2.5, -101.45])*1e-3, "m":2.15,
             "iT":np.array([13348, 12263, 6332, -1195, 3.4, -1])*1e-6
            },
            # wrist cable
            {
             "nest":"handbase", "cm":np.array([7, -30, -104])*1e-3, "m":0.082,
             "iT":np.array([36, 304, 104, -85, 0, 0])*1e-6
            },

            # wrist hand structure
            {
             "nest":"handwrist", "cm":np.array([-1.2, 0.1, 5.8])*1e-3, "m":0.32,
             "iT":np.array([464, 507, 528, 0, -13, -0.1])*1e-6
            },
            # wrist hand installation material + cable
            {
             "nest":"handwrist", "cm":np.array([11.5, 12, -6.8])*1e-3, "m":0.1,
             "iT":np.array([126, 100, 121, 10, -64, -11.9])*1e-6
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
             "nest":"tcp", "cm":np.array([0, 60, 80])*1e-3, "m":6,
             "iT":np.array([45000, 45000, 45000, 0, 0, 0])*1e-6
            }
           ]

motorPara = [
                # A1 motor
                {
                    "nest": "groundbase",
                    "position": np.array([0, 0, 152])*1e-3,
                    "orientation": np.array([0, 0, np.pi]),
                    "cm": np.array([0, 0, 69])*1e-3,
                    "m": 3.4,
                    "iT": np.array([2840, 2840, 2840, 0, 0, 0])*1e-6,
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
                    "m": 3.4,
                    "iT": np.array([2840, 2840, 1050, 0, 0, 0])*1e-6,
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
                    "m": 1.8,
                    "iT": np.array([1800, 1800, 700, 0, 0, 0])*1e-6,
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
                    "m": 0.9,
                    "iT": np.array([1000, 1000, 150, 0, 0, 0])*1e-6,
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
                    "m": 0.9,
                    "iT": np.array([1000, 1000, 150, 0, 0, 0])*1e-6,
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
                {"nest":"rotationcolumn", "friction":[74.7, 2.9, 1]},
                {"nest":"linkarm", "friction":[61.1876, 17.735, 1]},
                {"nest":"arm", "friction":[32.89, 7.12, 0.95]},
                {"nest":"handbase", "friction":[4.4, 1.29, 1]},
                {"nest":"handwrist", "friction":[4.48, 1.93, 1]},
                {"nest":"handflange", "friction":[3.3, 0.76, 1]}
               ]

gearPara = [
               {
                "nest":"groundbase",
                "ratio":100,
                "offset":68.5e-3,
                "case":9,
                "stator":
                    {
                     "inertia_drive":172e-6,
                     "inertia_body":[5829e-6, 3725e-6, 3725e-6],
                     "cm":-39e-3,
                     "m":2.307
                     },
                "rotor":
                    {
                     "inertia_drive":172e-6,
                     "inertia_body":[1026e-6, 883e-6, 883e-6],
                     "cm":-16e-3,
                     "m":0.89
                     },
                },

               {
                "nest":"rotationcolumn",
                "ratio":120,
                "offset":51.7e-3,
                "case":15,
                "stator":
                    {
                     "inertia_drive":169e-6,
                     "inertia_body":[259e-6, 187e-6, 187e-6],
                     "cm":-30.62e-3,
                     "m":1.88
                     },
                "rotor":
                    {
                     "inertia_drive":169e-6,
                     "inertia_body":[667e-6, 384e-6, 384e-6],
                     "cm":-14.48e-3,
                     "m":1.289
                     },
                },

               {
                "nest":"linkarm",
                "ratio":144,
                "offset":41e-3,
                "case":13,
                "stator":
                    {
                     "inertia_drive":41.3e-6,
                     "inertia_body":[259e-6, 187e-6, 187e-6],
                     "cm":-24.6e-3,
                     "m":0.78
                     },
                "rotor":
                    {
                     "inertia_drive":41.3e-6,
                     "inertia_body":[667e-6, 384e-6, 384e-6],
                     "cm":-11.6e-3,
                     "m":0.625
                     },
                },

               {
                "nest":"arm",
                "ratio":50,
                "offset":10e-3,
                "case":9,
                "stator":
                    {
                     "inertia_drive":7.9e-6,
                     "inertia_body":[259e-6, 187e-6, 187e-6],
                     "cm":-15.9e-3,
                     "m":0.149
                     },
                "rotor":
                    {
                     "inertia_drive":7.9e-6,
                     "inertia_body":[667e-6, 384e-6, 384e-6],
                     "cm":-9.4e-3,
                     "m":0.147
                     },
                },

               {
                "nest":"handbase",
                "ratio":80,
                "offset":26.5e-3,
                "case":13,
                "stator":
                    {
                     "inertia_drive":7.9e-6,
                     "inertia_body":[397e-6, 224e-6, 224e-6],
                     "cm":-16.11e-3,
                     "m":0.232
                     },
                "rotor":
                    {
                     "inertia_drive":-9.4e-6,
                     "inertia_body":[109e-6, 75e-6, 75e-6],
                     "cm":-9.4e-3,
                     "m":0.326
                     },
                },

               {
                "nest":"handwrist",
                "ratio":80,
                "offset":26.5e-3,
                "case":13,
                "stator":
                    {
                     "inertia_drive":7.9e-6,
                     "inertia_body":[267e-6, 194e-6, 194e-6],
                     "cm":-16.11e-3,
                     "m":0.232
                     },
                "rotor":
                    {
                     "inertia_drive":7.9e-6,
                     "inertia_body":[54e-6, 66e-6, 66e-6],
                     "cm":-9.4e-3,
                     "m":0.326
                     },
                }
            ]