import numpy as np
from model.m_math import rotation


class TrajectoryGenerator:
    def __init__(self):
        self.adept_length = 25 * np.pi + 255
        self.adept_length_1stSeg = 0.5 * 25 * np.pi
        self.adept_length_2ndSeg = 0.5 * 25 * np.pi + 255
        self.adept_r = 25
        self.trajectory = None
        self.t = None

    def linear_plan(self, v_max, T):
        l = self.adept_length
        if v_max * T < l:
            raise Exception('LinearPlanError!')
        t_const = 2 * l / v_max - T
        t_acc = (T - t_const) / 2
        acc = v_max / t_acc

        def s(t):
            if t <= t_acc:
                return 0.5 * acc * t**2
            elif t_acc < t <= t_acc + t_const:
                return 0.5 * v_max * t_acc + v_max * (t - t_acc)
            elif t_acc + t_const < t <= T:
                t_dec = t - t_const - t_acc
                return (0.5 * v_max * t_acc + v_max * t_const +
                        0.5 * (2 * v_max - acc * t_dec) * t_dec)
        return s

    def adept_s_map(self, s):
        if s <= self.adept_length_1stSeg:
            return (self.adept_r * (1 - np.cos(s/self.adept_r)),
                    0,
                    self.adept_r * np.sin(s/self.adept_r))
        elif self.adept_length_1stSeg < s <= self.adept_length_2ndSeg:
            return (s - self.adept_length_1stSeg + self.adept_r,
                    0,
                    self.adept_r)
        elif s > self.adept_length_2ndSeg:
            s_seg = s - self.adept_length_2ndSeg
            theta = np.pi/2 - s_seg / self.adept_r
            return (self.adept_r + 255 + self.adept_r * np.cos(theta),
                    0,
                    self.adept_r * np.sin(theta))

    def adept(self, v_max, T, N, offset, angle, orientation):
        try:
            s_callback = self.linear_plan(v_max, T)
        except Exception:
            raise
        t = np.linspace(0, T, N)
        s = map(s_callback, t)
        trajectory_origin = np.array(list(map(self.adept_s_map, s)))
        tcp_position = rotation(*angle) @ (trajectory_origin + offset).T / 1000
        tcp_orientation = np.array([np.array(orientation)]).T @ np.ones([1, np.shape(tcp_position)[1]])
        self.trajectory = np.vstack((tcp_position, tcp_orientation))
        self.t = t
