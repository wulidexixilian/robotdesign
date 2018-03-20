# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 10:01:45 2017

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
             "displacement": np.array([560, 0, 45.5])*1e-3,
             },
            {
             "name":"arm",
             "displacement": np.array([191, -25, -55.5])*1e-3,
             },
            {
             "name":"handbase",
             "displacement": np.array([0, 58.5, -314])*1e-3,
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
             "nest":"linkarm", "cm":np.array([252, -6.85, -43.8])*1e-3, "m":7.85,
             "iT":np.array([44725.9, 364878.2, 358045.1, 632.39, 12060.3, -2503.5])*1e-6
            },
            # linkarm cover
            {
             "nest":"linkarm", "cm":np.array([488.2, -5.6, -51])*1e-3, "m":0.6,
             "iT":np.array([9431.2, 12276.5, 4386.1, -1.3043, 0.10265, 225.326])*1e-6
            },
            # linkarm drivetrain + screws
            {
             "nest":"linkarm", "cm":np.array([379.73, -1.7, 28.38])*1e-3, "m":0.587,
             "iT":np.array([917.6, 33726.31, 33607.9, -48.344, 3024.15, 63.76])*1e-6
            },
            # linkarm other
            {
             "nest":"linkarm", "cm":np.array([239.37, -1.54, -98.65])*1e-3, "m":0.534,
             "iT":np.array([2328.2, 34916.55, 34342.4, 61.38, 1921.7, -63.16])*1e-6
            },
            # arm structure
            {
             "nest":"arm", "cm":np.array([68, -12.8, -53.5])*1e-3, "m":2.1,
             "iT":np.array([7876, 15988, 16799, 82, -317, -2077])*1e-6
            },
            # arm cabel assembly
            {
             "nest":"arm", "cm":np.array([39, 3, -64])*1e-3, "m":0.45,
             "iT":np.array([725, 3148, 3648, 156, 297, -213])*1e-6
            },
            # arm big screws
            {
             "nest":"arm", "cm":np.array([23, -10, -62.5])*1e-3, "m":0.33,
             "iT":np.array([1131, 1399, 821, -36, 106, -122])*1e-6
            },
            # arm CS WG screws
            {
             "nest":"arm", "cm":np.array([42, -25, -55.5])*1e-3, "m":0.23,
             "iT":np.array([175.6, 92.5, 92.5, 0, 0, 0])*1e-6
            },
            # arm cabel cover
            {
             "nest":"arm", "cm":np.array([-51.3, -30.5, -58.6])*1e-3, "m":0.18,
             "iT":np.array([418, 322, 226, 0, -1.5, -85])*1e-6
            },
            # wrist structure
            {
             "nest":"handbase", "cm":np.array([1.51, 7.82, -117.15])*1e-3, "m":4.04,
             "iT":np.array([76102.15, 73818.51, 10760.24, -3289.83, 1716.94, -126.68])*1e-6
            },
            # wrist bridge
            {
             "nest":"handbase", "cm":np.array([7, -30, -150])*1e-3, "m":0.1,
             "iT":np.array([400, 360, 104, 85, 31, 15])*1e-6
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
             "nest":"handflange", "cm":np.array([0, -80, -100])*1e-3, "m":10,
             "iT":np.array([45000, 45000, 45000, 0, 0, 0])*1e-6
            }
           ]

motorPara = [
                # A1 motor
                {
                 "nest":"groundbase",
                 "position":np.array([0, 0, 152])*1e-3,
                 "orientation":np.array([0, 0, np.pi]),
                 "cm":np.array([0, 0, 51])*1e-3,
                 "m":3.4,
                 "iT":np.array([3500, 3500, 3500, 0, 0, 0])*1e-6
                },
                # A2 motor
                {
                 "nest":"rotationcolumn",
                 "position":np.array([25, -102.7, -179.5])*1e-3,
                 "orientation":np.array([0, 0, np.pi/2]),
                 "cm":np.array([0, 0, 51])*1e-3,
                 "m":3.4,
                 "iT":np.array([3500, 3500, 3500, 0, 0, 0])*1e-6
                },
                # A3 motor
                {
                 "nest":"rotationcolumn",
                 "position":np.array([399, -12, 44])*1e-3,
                 "orientation":np.array([0, 0, np.pi]),
                 "cm":np.array([0, 0, 45])*1e-3,
                 "m":1.8,
                 "iT":np.array([2500, 2500, 2500, 0, 0, 0])*1e-6
                },
                # A4 motor
                {
                 "nest":"arm",
                 "position":np.array([30, -25, 55.5])*1e-3,
                 "orientation":np.array([0, -np.pi, 0]),
                 "cm":np.array([0, 0, 29])*1e-3,
                 "m":0.9,
                 "iT":np.array([1000, 1000, 1000, 0, 0, 0])*1e-6
                },
                # A5 motor
                {
                 "nest":"handbase",
                 "position":np.array([0, 53, -207.75])*1e-3,
                 "orientation":np.array([0, 0, np.pi]),
                 "cm":np.array([0,0, 29])*1e-3,
                 "m":0.9,
                 "iT":np.array([1000, 1000, 1000, 0, 0, 0])*1e-6
                },
                # A6 motor
                {
                 "nest":"handwrist",
                 "position":np.array([48.4, 0, -32])*1e-3,
                 "orientation":np.array([0, -np.pi, 0]),
                 "cm":np.array([0, 0, 28])*1e-3,
                 "m":0.6,
                 "iT":np.array([320, 320, 320, 0, 0, 0])*1e-6
                }
            ]

frictionPara = [
                {"nest":"rotationcolumn", "friction":[109.9, 5.2, 1]},
                {"nest":"linkarm", "friction":[134.3, 33.6, 1]},
                {"nest":"arm", "friction":[59.3, 12.54, 0.95]},
                {"nest":"handbase", "friction":[4.4, 1.18, 1]},
                {"nest":"handwrist", "friction":[4.84, 1.93, 1]},
                {"nest":"handflange", "friction":[3.3, 0.76, 1]}
               ]

gearPara = [
               {
                "nest":"groundbase",
                "ratio":120,
                "offset":68.5e-3,
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
                     "inertia_body":[1602e-6, 883e-6, 883e-6],
                     "cm":-26e-3,
                     "m":1.07
                     },
                },

               {
                "nest":"rotationcolumn",
                "ratio":160,
                "offset":51.7e-3,
                "case":14,
                "stator":
                    {
                     "inertia_drive":169e-6,
                     "inertia_body":[259e-6, 187e-6, 187e-6],
                     "cm":-15e-3,
                     "m":0.97
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
                "ratio":160 * 1.44,
                "offset":41e-3,
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
                "ratio":100,
                "offset":10e-3,
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
                "ratio":100,
                "offset":26.5e-3,
                "case":14,
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
                "ratio":100,
                "offset":26.5e-3,
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