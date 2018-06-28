import numpy as np
from model import m_manipulator

np.set_printoptions(suppress=True)
np.set_printoptions(precision=4)
dimension_list = [
    {
        "nest": "base",
        "displacement": np.array([0, 0, 140.3])*1e-3,
        'offset': np.array([0, 0, 0])
    },
    {
        "nest": "link1",
        "displacement": np.array([0, -1.2, 199.7])*1e-3,
        'offset': np.array([0, 0, 0])
    },
    {
        "nest": "link2",
        "displacement": np.array([0, -184, 1.2])*1e-3,
        'offset': np.array([0, 0, 0])
    },
    {
        "nest": "link3",
        "displacement": np.array([0, -1.2, 216])*1e-3,
        'offset': np.array([0, 0, 0])
    },
    {
        "nest": "link4",
        "displacement": np.array([0, 184, -1.2])*1e-3,
        'offset': np.array([0, 0, 0])
     },
    {
        "nest": "link5",
        "displacement": np.array([0, -68.4, 216])*1e-3,
        'offset': np.array([0, 0, 0])
    },
    {
        "nest": "link6",
        "displacement": np.array([0, -126, 68.4]) * 1e-3,
        'offset': np.array([0, 0, 0])
    },
    {
        "nest": "flange",
        "displacement": np.array([0, 0, 0]) * 1e-3,
        'offset': np.array([0, 0, 0])
    }
]
frame_config = {
    "base":     {
        'frame0': np.array([0, 0, 0]),
        'frame1': np.array([0, 0, 0]),
    },
    "link1": {
        'frame0': np.array([0, 0, 0]),
        'frame1': np.array([-np.pi/2, 0, 0])
    },
    "link2":        {
        'frame0': np.array([-np.pi/2, 0, 0]),
        'frame1': np.array([np.pi/2, 0, 0])
    },
    "link3":            {
        'frame0': np.array([0, 0, 0]),
        'frame1': np.array([np.pi/2, 0, 0])
    },
    "link4":       {
        'frame0': np.array([np.pi/2, 0, 0]),
        'frame1': np.array([-np.pi/2, 0, 0])
    },
    "link5":      {
        'frame0': np.array([0, 0, 0]),
        'frame1': np.array([-np.pi/2, 0, 0])
    },
    "link6":     {
        'frame0': np.array([-np.pi/2, 0, 0]),
        'frame1': np.array([np.pi/2, 0, 0])
    },
    "flange": {
        'frame0': np.array([0, 0, 0]),
        'frame1': np.array([0, 0, 0])
    },
    "tcp": {
        'frame0': np.array([0, 0, 0]),
        'frame1': np.array([0, 0, 0])
    }
}
robot = m_manipulator.Kinematics(dimension_list, frame_config)

for joint in robot.joints:
    print(joint.origin1)
robot.k([np.pi/6, np.pi/6, np.pi/6, np.pi/6, np.pi/6, np.pi/6, np.pi/6])
for joint in robot.joints:
    print(joint.origin1)