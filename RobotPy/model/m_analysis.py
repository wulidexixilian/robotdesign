import matplotlib.colors as colors
import matplotlib.patches as patches
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.path import Path

from utility.u_math import mass_combine

np.set_printoptions(suppress=True)
np.set_printoptions(precision=4)


def get_all_friction_in_array(robot):
    """
    put joint friction paras into two 1 * 6 numpy arrays for Rh and Rv
    :return: friction array
    """
    Rh = np.array([drive.Rh for drive in robot.drives])
    Rv = np.array([drive.Rv for drive in robot.drives])
    return Rh, Rv


def move_tau_to_joint_side(tau, qd, Rh, Rv, Rz, ratio):
    tau = abs(tau * ratio) - abs(qd * Rv) - Rh
    tau = tau - (1 - Rz) * tau
    return tau


def max_joint_tau(drive, qd, isStatic=True):
    if isStatic:
        characteristic_before_ratio = np.array(
            drive.characteristic_before_ratio['s1']
        )
        characteristic_after_ratio = np.array(
            drive.characteristic_after_ratio['s1']
        )
    else:
        characteristic_before_ratio = np.array(
            drive.characteristic_before_ratio['max']
        )
        characteristic_after_ratio = np.array(
            drive.characteristic_after_ratio['max']
        )

    rpm_before_ratio = np.abs(np.abs(qd) * 60 / np.pi / 2 * drive.ratio)
    tau_before_ratio = np.interp(
        rpm_before_ratio,
        characteristic_before_ratio[0, :],
        characteristic_before_ratio[1, :]
    )
    tau_after_ratio = np.interp(
        np.abs(qd),
        characteristic_after_ratio[0, :],
        characteristic_after_ratio[1, :],
    )
    tau_max = np.minimum(
        tau_after_ratio,
        move_tau_to_joint_side(
            tau_before_ratio, qd, drive.Rh,
            drive.Rv, drive.Rz, drive.ratio
        )
    )
    return tau_max


class StaticAnalysis:

    def __init__(self, robot):
        self.robot = robot
        self.num_axes = robot.num_axes

    def get_weight(self):
        """
        Overall weight of robot
        """
        weight = 0
        for body in self.robot.bodies:
            weight += body.m
        return weight

    def get_all_friction_in_array(self):
        """
        wrapper 
        """
        return get_all_friction_in_array(self.robot)

    def get_motor_characteristic(self):
        characteristic_motor = [
            drive.characteristic_before_ratio for drive in self.robot.drives
        ]
        return characteristic_motor

    def get_gear_characteristic(self):
        characteristic_gear = [
            drive.characteristic_after_ratio for drive in self.robot.drives
        ]
        return characteristic_gear

    def max_joint_tau_batch(self, qd=None, is_static=True):
        """
        combine characteristic both sides of the joint find the max torque
        at given speed
        :param qd: 1 * n_axis array speed
        :param is_static:  true for max sustainable torque, otherwise instant
        :return: 1*6 array, max torque of each joint
        """
        if qd is None:
            qd = np.zeros(self.num_axes)
        tau_max = np.array(
            list(
                map(
                    max_joint_tau,
                    self.robot.drives, qd, [is_static] * self.num_axes
                )
            )
        )
        return tau_max

    def max_joint_tau_output(self, q, qd, gravity=np.array([0, 0, -9.8]), is_static=False):
        tau_max = self.max_joint_tau_batch(qd)
        self.robot.k(q)
        self.robot.ne(qd, np.zeros(self.num_axes), gravity)
        self.robot.solve_drivetrain(qd, np.zeros(self.num_axes))
        tau_gravity = np.array([drive.tau_drive for drive in self.robot.drives])
        tau_limit_upper = np.clip(
            tau_max - tau_gravity,
            np.zeros(np.shape(tau_max)),
            tau_max
        )
        tau_limit_lower = np.clip(
            -tau_max - tau_gravity,
            -tau_max,
            np.zeros(np.shape(tau_max))
        )
        return tau_limit_lower, tau_limit_upper

    def load_diagram_data(self, qd, rated_mass):
        """
        draw load diagram based on given rated mass at given speed
        :param qd: 1*6 array joint speed
        :param rated_mass: scalar in kg
        :return: (w: half side width, h: side distance to tcp)
        """
        tau_max = self.max_joint_tau_batch(qd)
        load = rated_mass * 9.8
        [l4, l5, l6] = tau_max[3:] / load
        w = l6
        d_A5TCP = self.robot.joints[7].origin0[0] - self.robot.joints[5].origin0[0]
        d5 = l5 - d_A5TCP
        d4 = l4 - d_A5TCP
        d_edge = np.sqrt(l4**2 - w**2) - d_A5TCP
        if d5 >= d4:
            points = [
                (0, 0),
                (0, -w),
                (d_edge, -w),
                (d4, 0),
                (d_edge, w),
                (0, w),
                (0, 0)
            ]
            comm = [
                Path.MOVETO,
                Path.LINETO,
                Path.LINETO,
                Path.CURVE3,
                Path.CURVE3,
                Path.LINETO,
                Path.LINETO
            ]
        elif d5 > d_edge:
            w_edge = np.sqrt(l4 ** 2 - l5 ** 2)
            dd = (d5 - d_edge)/2
            d_middle = d_edge + dd
            l_middle = d_middle + d_A5TCP
            w_middle = np.sqrt(l4**2 - l_middle**2)
            points = [
                (0, 0),
                (0, -w),
                (d_edge, -w),
                (d_middle, -w_middle),
                (d5, -w_edge),
                (d5, w_edge),
                (d_middle, w_middle),
                (d_edge, w),
                (0, w),
                (0, 0)
            ]
            comm = [
                Path.MOVETO,
                Path.LINETO,
                Path.LINETO,
                Path.CURVE3,
                Path.CURVE3,
                Path.LINETO,
                Path.CURVE3,
                Path.CURVE3,
                Path.LINETO,
                Path.LINETO,
            ]
        else:
            points = [
                (0, 0),
                (0, w),
                (d5, w),
                (d5, -w),
                (0, -w),
                (0, 0)
            ]
            comm = [
                Path.MOVETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO,
                Path.LINETO
            ]
        path = Path(points, comm)
        return {'data': [w, d4, d5, d_edge], 'path': path}

    def load_diagram_show(self, qd, mass_group):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        for idx, mass in enumerate(sorted(mass_group)):
            result = self.load_diagram_data(qd, mass)
            patch = patches.PathPatch(result['path'], facecolor='green', lw=1)
            ax.add_patch(patch)
            w = result['data'][0]
            d = min(result['data'][1], result['data'][2])
            ax.text(d-0.02, 0.01, '{}kg'.format(mass))
            ax.text(d, -w/15, '{:.1f}'.format(d*1000))
            ax.text(-d/10, w, '{:.1f}'.format(w*1000))
            if idx == 0:
                ax.set_xlim(0, d * 1.2)
                ax.set_ylim(0, w * 1.2)
        plt.xlabel('z [m]')
        plt.ylabel('x [m]')
        plt.title('load diagram')
        plt.grid(True)
        plt.show()

    def instant_load(
        self, q, q_dot=None, q_ddot=None, gravity=np.array([0, 0, -9.8])
    ):
        """
        do one step inverse dynamic, calculate worst case stall torque and tcp position 
        :param q: pose 
        :param q_dot: speed
        :param q_ddot: acc
        :return: {'tcp': 1*3 array tcp position in global coordinate,
                  'tau_motor': 1*6 array motor torque to move the load 
                              against gravity acc, and friction. 
                              Set qd = 1/10 * max_speed, qdd = 0 to calculate 
                              holding torque
                  'tau_joint': instant joint torque output by gearbox}
        """
        if q_dot is None:
            q_dot = np.zeros(self.robot.num_axes)
        if q_ddot is None:
            q_ddot = np.zeros(self.robot.num_axes)
        self.robot.k(q)
        self.robot.ne(q_dot, q_ddot, gravity)
        self.robot.solve_drivetrain(q_dot, q_ddot)
        tcp = self.robot.joints[-1].origin1
        tau_motor = np.array([d.tau_drive for d in self.robot.drives])
        tau_joint = np.array([d.tau_joint for d in self.robot.drives])
        return {'tcp': tcp, 'tau_motor': tau_motor, 'tau_joint': tau_joint}

    def get_stall_torque(self, qd_max, load):
        qd = -0.01 * qd_max
        qdd = np.zeros(self.num_axes)
        # Case 1: q = 0, g = [0, 0, -9.8]; stall torque for A2 A3 A5 A6
        q = np.zeros(self.num_axes)
        gravity = np.array([0, 0, -9.8])
        result = self.instant_load(q, qd, qdd, gravity)
        tcp = result['tcp']
        tau_motor2 = result['tau_motor'][1]
        tau_motor3 = result['tau_motor'][2]
        tau_motor5 = result['tau_motor'][4]
        tau_joint2 = result['tau_joint'][1]
        tau_joint3 = result['tau_joint'][2]
        tau_joint5 = result['tau_joint'][4]
        # Case 2: q = 0, g = [0, -9.8, 0]; stall torque for A1
        gravity = np.array([0, -9.8, 0])
        result = self.instant_load(q, qd, qdd, gravity)
        tau_motor1 = result['tau_motor'][0]
        tau_joint1 = result['tau_joint'][0]
        # Case 3: q = 0, g = [0, 0, -9.8]: stall torque for A5
        gravity = np.array([0, 0, -9.8])
        self.robot.k(np.zeros(6))
        x, y, z = load['cm']
        q4 = -np.pi/2
        d_A5TCP = self.robot.joints[7].origin0[0] - self.robot.joints[5].origin0[0]
        q5 = np.arctan2(z + d_A5TCP, np.sqrt(x ** 2 + y ** 2))
        q6 = np.arctan2(np.abs(load['cm'][1]), np.abs(load['cm'][0]))
        q = np.array([0, 0, 0, q4, q5, q6])
        result = self.instant_load(q, qd, qdd, gravity)
        tau_motor4 = result['tau_motor'][3]
        tau_joint4 = result['tau_joint'][3]
        tau_motor6 = result['tau_motor'][5]
        tau_joint6 = result['tau_joint'][5]

        characteristic = self.get_motor_characteristic()
        tau_motor_s1 = [char['s1'][1][0] for char in characteristic]

        final_result = {
            'tcp': tcp,
            'tau_motor': np.abs(np.array([tau_motor1, tau_motor2, tau_motor3,
                                          tau_motor4, tau_motor5, tau_motor6])),
            'tau_joint': np.array([tau_joint1, tau_joint2, tau_joint3,
                                   tau_joint4, tau_joint5, tau_joint6])
        }
        final_result['motor_percent'] = (final_result['tau_motor'] /
                                         tau_motor_s1 * 100)
        return final_result

    def get_joint_load(self, joint_id):
        """
        calculate effective mass, center of mass,
        and inertia tensor for a joint specified by jointID
        """
        m_eff = 0
        cm_eff = np.array([0, 0, 0])
        iT_eff = np.zeros((3,3))
        for body in self.robot.bodies[joint_id:]:
            (m_eff, cm_eff, iT_eff) = mass_combine(m_eff, body.m,
                                                   cm_eff, body.cm_gl,
                                                   iT_eff, body.iT_gl)
        return m_eff, cm_eff, iT_eff

    def get_kinetic(self, q, qd):
        self.robot.k(q)
        M = self.robot.get_inertia_matrix()
        E = []
        for idx_axis in range(self.num_axes):
            if idx_axis >= 1:
                qd[idx_axis - 1] = 0
            E_indv = 0.5 * np.dot(qd, M @ qd)
            E.append(E_indv)
        return np.array(E)


class SimulationAnalysis(StaticAnalysis):

    def __init__(self, robot, q_ser, q_dot_ser,
                 motor_tau_ser, tau_ser,
                 joint_f_ser, joint_tau_ser,
                 tcp_ser,
                 t_ser,
                 ts):
        """
        A class deals with simulation results
        :param q_ser: axis angle [rad]
        :param q_dot_ser: axis velocity [rad/s]
        :param motor_tau_ser: motor torque [Nm]
        :param tau_ser: axis_torque [Nm]
        :param joint_f_ser: 3D joint force [Nm] 
        :param joint_tau_ser: 3D joint torque [Nm]
        :param tcp_ser: tcp position in Cartesian coordinate [m]
        :param t_ser: time series [s]
        :param ts: sampling time [s]
        :param ratio: drive ratio [1]
        """
        super(SimulationAnalysis, self).__init__(robot)
        self.q_ser = q_ser
        self.q_dot_ser = q_dot_ser
        self.tau_ser = tau_ser
        self.motor_tau_ser = motor_tau_ser
        self.joint_f_ser = joint_f_ser
        self.joint_tau_ser = joint_tau_ser
        self.tcp_ser = tcp_ser
        self.t_ser = t_ser
        self.ts = ts
        self.ratio = [drive.ratio for drive in robot.drives]

    def motor_average_tau(self):
        """
        gearbox average torque, speed weighted cubic average over time
        :return: average torque in list
        """
        num = np.sum((self.motor_tau_ser**2) * self.ts, 0)
        den = self.t_ser[-1]
        tau_av = (num / den)**(1/2)
        return tau_av

    def get_motor_speed(self):
        speed = np.zeros(np.shape(self.q_dot_ser))
        for idx, r in enumerate(self.ratio):
            speed[:, idx] = self.q_dot_ser[:, idx] * r
        return speed

    def motor_average_speed(self):
        speed = np.abs(self.get_motor_speed()) * 60 / np.pi / 2
        num = np.sum(speed * self.ts, 0)
        den = self.t_ser[-1]
        omega_av = num / den
        return omega_av

    def gear_average_tau(self):
        """
        gearbox average torque, speed weighted cubic average over time
        :return: average torque in list
        """
        num = np.sum(np.abs(self.q_dot_ser * (self.tau_ser**3)) * self.ts, 0)
        den = np.sum(np.abs(self.q_dot_ser) * self.ts, 0)
        tau_av = (num / den) ** (1/3)
        return tau_av

    def gear_average_speed(self):
        num = np.sum(np.abs(self.q_dot_ser) * self.ts, 0)
        den = self.t_ser[-1]
        omega_av = num / den
        return omega_av

    def get_gearbox_lifetime(self, ln, tau_rated, omega_rated):
        tau_av = self.gear_average_tau()
        omega_av = self.gear_average_speed()
        l50 = ln * omega_rated / (omega_av * np.abs(self.ratio)) *\
              (tau_rated / tau_av) ** 3
        return l50

    def drive_characteristic(self, step_num_vel, step_num_tau, tau_stall=None):
        """
        visualize velocity-torque diagram on the motor side
        :param step_num_vel: 2D histogram block area size, x
        :param step_num_tau: 2D histogram block area size, y
        :param characteristic: motor characteristic parameters including max and s1
        :return: 
        """
        characteristic = self.get_motor_characteristic()
        n = len(self.q_dot_ser[:, 0])
        fig, ax_arr = plt.subplots(int(self.num_axes / 2), 2)
        fig.suptitle('Drive Characteristic [rpm - Nm]')
        for i, r in enumerate(self.ratio):
            speed_data = np.abs(self.q_dot_ser[:, i] * r
                                / (2 * np.pi) * 60)
            torque_data = np.abs(self.motor_tau_ser[:, i])
            speed_grid = np.linspace(0, max(speed_data), step_num_vel)
            torque_grid = np.linspace(0, max(torque_data), step_num_tau)
            characteristic_timer = np.zeros(
                [len(torque_grid), len(speed_grid), self.num_axes]
            )
            for j in range(n):
                temp_vel = np.where(speed_grid >= speed_data[j])[0]
                if len(temp_vel) > 0:
                    in_box_vel = temp_vel[0]
                else:
                    in_box_vel = len(speed_grid) - 1
                temp_tau = np.where(torque_grid >= torque_data[j])[0]
                if len(temp_tau) > 0:
                    in_box_tau = temp_tau[0]
                else:
                    in_box_tau = len(torque_grid) - 1
                characteristic_timer[in_box_tau, in_box_vel, i] += self.ts
            z = characteristic_timer[:, :, i]
            ax = ax_arr[int(i/2), (i%2)]
            im = ax.imshow(
                z,
                cmap=plt.cm.plasma,
                interpolation='none',
                norm=colors.PowerNorm(gamma=0.6),
                extent=[
                    0, np.max(np.abs(speed_data)), np.max(np.abs(torque_data)), 0
                ],
                aspect='auto'
            )
            ax.invert_yaxis()
            ax.set_title('A'+str(i+1))
            cb = plt.colorbar(im, ax=ax)
            cb.set_label('time [s]')

        if tau_stall is not None:
            for idx, ax in enumerate(ax_arr.flat):
                ax.plot(10, tau_stall[idx], 'c*', ms=10)

        for i, cha in enumerate(characteristic):
            if cha is not None:
                max_line = cha['max']
                s1_line = cha['s1']
                xm = max_line[0]
                ym = max_line[1]
                x1 = s1_line[0]
                y1 = s1_line[1]
                ax = ax_arr[int(i / 2), (i % 2)]
                ax.plot(xm, ym, 'g-')
                ax.plot(x1, y1, 'r-')
                ax.set_facecolor(plt.cm.plasma(0))

        tau_av = self.motor_average_tau()
        omega_av = self.motor_average_speed()
        for idx, ax in enumerate(ax_arr.flat):
            ax.plot(omega_av[idx], tau_av[idx], 'w+', ms=8, mfc='none')

        # plt.show()

    def get_max_drive_tau(self):
        tau_max = np.abs(self.motor_tau_ser).max(axis=0)
        characteristic = self.get_motor_characteristic()
        tau_limit = np.array([cha['max'][1][0] for cha in characteristic])
        percentage = tau_max/tau_limit
        print('max motor tau / motor limit: {}%'.format(percentage * 100))
        return tau_max

    def joint_characteristic(
        self, gearbox_datasheet=None,
        ln=None, l_exp=None, target_lifetime=None, draw_lifetime=True
    ):
        characteristic = self.get_gear_characteristic()
        fig, ax_arr = plt.subplots(int(self.num_axes/2), 2)
        fig.suptitle('Gear Characteristic [rpm - Nm]')
        tau_av = self.gear_average_tau()
        omega_av = self.gear_average_speed()
        for i in range(self.num_axes):
            ax = ax_arr[int(i/2), (i%2)]
            qd = np.abs(self.q_dot_ser[:, i]) / np.pi * 180
            ax.plot(qd, np.abs(self.tau_ser[:, i]))
            char = characteristic[i]
            max_line = char['max']
            s1_line = char['s1']
            ax.plot(s1_line[0, :] / np.pi * 180, s1_line[1, :], 'r-')
            ax.plot(max_line[0, :] / np.pi * 180, max_line[1, :], 'g-')
            ax.plot(omega_av[i] / np.pi * 180, tau_av[i], 'm*', ms=8)
            if gearbox_datasheet is not None:
                tau_rated = gearbox_datasheet[i]['rated_tau']
                tau_average = gearbox_datasheet[i]['acc_tau']
                omega_rated = gearbox_datasheet[i]['rated_omega']
                # datasheet value
                ax.plot(
                    s1_line[0, :] / np.pi * 180,
                    np.ones(np.shape(s1_line[0, :])) * tau_rated,
                    'c--'
                )
                ax.plot(
                    s1_line[0, :] / np.pi * 180,
                    np.ones(np.shape(s1_line[0, :])) * tau_average,
                    'y--'
                )
                # lifetime map
                if draw_lifetime:
                    if ln is None:
                        ln = np.ones(self.num_axes) * 6000
                    if l_exp is None:
                        l_exp = np.ones(self.num_axes) * 3.333
                    if target_lifetime is None:
                        target_lifetime = [40000, 20000, 6000, 4000]
                    for lh in target_lifetime:
                        omega_h = np.linspace(
                            0.1 * np.max(np.abs(qd)),
                            np.max(np.abs(qd)), 10
                        )
                        tau_h = (ln[i] * omega_rated / omega_h / lh)\
                                **(1/l_exp[i]) * tau_rated
                        ax.plot(omega_h, tau_h, 'b--', lw=1)
            ax.grid(True)
            ax.set_title("A"+str(i+1))
        return ax_arr

    def get_max_joint_tau(self):
        tau_max = np.abs(self.tau_ser).max(axis=0)
        characteristic = self.get_gear_characteristic()
        tau_limit = np.array([char['max'][1][0] for char in characteristic])
        percentage = tau_max / tau_limit
        print('max joint tau / gearbox limit: {}%'.format(percentage * 100))
        return tau_max


    def get_fea_input(self):
        """
        :return: 
        """
        fig_f = plt.figure()
        fig_f.suptitle('Constrain Force')
        for i in range(self.num_axes + 1):
            for j in range(3):
                fig_f.add_subplot(self.num_axes + 1, 3, 3 * i + j + 1)
                plt.title('A' + str(i + 1) + '-' + 'xyz'[j])
                plt.plot(self.t_ser, self.joint_f_ser[i, j, :])
        # plt.tight_layout()
        fig_t = plt.figure()
        fig_t.suptitle('Constrain Torque')
        for i in range(self.num_axes + 1):
            for j in range(3):
                fig_t.add_subplot(self.num_axes + 1, 3, 3 * i + j + 1)
                plt.title('A' + str(i + 1) + '-' + 'xyz'[j])
                plt.plot(self.t_ser, self.joint_tau_ser[i, j, :])
        # plt.tight_layout()

    def show_performance(self):
        """
        show simulation results of pose, speed, torque, tcp...
        :return: 
        """
        # pose
        plt.figure()
        p1 = [plt.subplot(int(self.num_axes/2), 2, 1+i) for i in range(self.num_axes)]
        plt.tight_layout()
        for i in range(self.num_axes):
            p1[i].plot(self.t_ser, self.q_ser[:, i]*180/np.pi)
            p1[i].grid(True)
            p1[i].set_title("$q_{"+str(i+1)+"}$")
        # velocity
        plt.figure()
        p3 = [plt.subplot(int(self.num_axes/2), 2, 1+i) for i in range(self.num_axes)]
        plt.tight_layout()
        for i in range(self.num_axes):
            p3[i].plot(self.t_ser, self.q_dot_ser[:, i]*180/np.pi)
            p3[i].grid(True)
            p3[i].set_title("$\dot{q_{"+str(i+1)+"}}$")
        # torque motor side
        plt.figure()
        p2 = [plt.subplot(int(self.num_axes/2), 2, 1+i) for i in range(self.num_axes)]
        plt.tight_layout()
        for i in range(self.num_axes):
            p2[i].plot(self.t_ser, self.motor_tau_ser[:, i])
            p2[i].grid(True)
            p2[i].set_title("$T_{A"+str(i+1)+"}$")
        # torque joint side
        plt.figure()
        p2 = [plt.subplot(int(self.num_axes/2), 2, 1+i) for i in range(self.num_axes)]
        plt.tight_layout()
        for i in range(self.num_axes):
            p2[i].plot(self.t_ser, self.tau_ser[:, i])
            p2[i].grid(True)
            p2[i].set_title("$T_{A"+str(i+1)+"}$")
        # tcp position
        plt.figure()
        ax1 = plt.subplot(311)
        ax1.plot(self.t_ser, self.tcp_ser[:, 0], "r-")
        ax1.grid(True)
        ax1.set_title("$tcp_{x}$")
        ax2 = plt.subplot(312, sharex=ax1, sharey=ax1)
        ax2.plot(self.t_ser, self.tcp_ser[:, 1], "g-")
        ax2.grid(True)
        ax2.set_title("$tcp_{y}$")
        ax3 = plt.subplot(313, sharex=ax1, sharey=ax1)
        ax3.plot(self.t_ser, self.tcp_ser[:, 2], "b-")
        ax3.grid(True)
        ax3.set_title("$tcp_{z}$")
        plt.tight_layout()
        # speed-torque diagram on motor side
        plt.figure()
        plt.title("torque - speed / motor")
        p4 = [plt.subplot(int(self.num_axes/2), 2, 1+i) for i in range(self.num_axes)]
        plt.tight_layout()
        for i in range(self.num_axes):
            p4[i].plot(
                np.abs(self.q_dot_ser[:, i] * self.ratio[i]) / np.pi / 2 * 60,
                np.abs(self.motor_tau_ser[:, i])
            )
            p4[i].grid(True)
            p4[i].set_title("A"+str(i+1))
            p4[i].set_xlabel('speed [rpm]')
            p4[i].set_ylabel('torque [Nm]')
        # # speed-torque diagram on joint side
        # plt.figure()
        # plt.title("torque - speed / joint")
        # p4 = [plt.subplot(321+i) for i in range(6)]
        # plt.tight_layout()
        # for i in range(6):
        #     p4[i].plot(np.abs(self.q_dot_ser[:, i]) / np.pi / 2 * 60,
        #                np.abs(self.tau_ser[:, i]))
        #     p4[i].grid(True)
        #     p4[i].set_title("A"+str(i+1))
        #     plt.xlabel('speed [rpm]')
        #     plt.ylabel('torque [Nm]')