import matplotlib.pyplot as plt
import numpy as np
import sympy.physics.mechanics as me
from pydy.codegen.ode_function_generators import generate_ode_function
from scipy.integrate import odeint
from sympy import tanh
from sympy.physics.vector import init_vprinting

init_vprinting(use_latex='mathjax', pretty_print=False)


def vif(vec, frame, simplify=False):
    """
    convert a vector to a point in the given frame
    """
    if simplify is True:
        return vec[0] * frame.x + vec[2] *frame.z
    else:
        return vec[0] * frame.x + vec[1] * frame.y + vec[2] *frame.z


def func_friction(v, rh, rv, h, axis):
    return - (tanh(1.5 * v / h) * rh + rv * v) * axis


class SymDyRobot():
    """
    Derive symbolic dynamic differential equation in sympy and simulate in PyDy.
    Controller Design is also included to form a closed-loop simulation
    """
    def __init__(self, dimensions, fr_paras, mass_centers, masses, moments, g,
                 if_simplify=True):
        """
        Establish symbolic rigid bodies system
        :ivar
            dimensions : list of rComponentLib.Body object containing all kinematics
                         and mass information
            fr_paras : friction parameters from Config files
            masses : equivalent mass for each joint, external load is counted in the
                     mass of A6
            inertia : equivalent moment inertia for each joint, external load is
                      counted in the mass of A6
        :var
            q : list of generalized coordinates, joints angles here
            q_dot : list of joints' angular speeds
            world : world coordinate
            frames : list of local frames
            joints : list of points for joints
            cms : list of mass centers
            bodies : list of rigid bodies
            loads : forces exerted on rigid bodies, including gravity,
                    driving torque, and frictions
            kde : kinematics differential equation \dot{q} = q_dot
            kane : results of sympy.physics.mechanics.kane()
        """
        print('symbolic dynamic: set up rigid bodies')
        q = me.dynamicsymbols('q:6')
        world = me.ReferenceFrame('C0')
        rotationcolumn = world.orientnew('C1', 'Axis', [q[0], world.z])
        linkarm = rotationcolumn.orientnew('C2', 'Axis', [q[1], rotationcolumn.y])
        arm = linkarm.orientnew('C3', 'Axis', [q[2], linkarm.y])
        handbase = arm.orientnew('C4', 'Axis', [q[3], arm.x])
        handwrist = handbase.orientnew('C5', 'Axis', [q[4], handbase.y])
        handflange = handwrist.orientnew('C6', 'Axis', [q[5], handwrist.x])
        frames = [world, rotationcolumn, linkarm, arm,
                  handbase, handwrist, handflange]
        rotation_axes = [world.z, rotationcolumn.y, linkarm.y, arm.x, handbase.y,
                         handwrist.x]

        joints = [me.Point('A'+str(i)) for i in range(6)]
        for i, jt in enumerate(joints[1:]):
            jt.set_pos(joints[i], vif(dimensions[i], frames[i+1],
                       simplify=if_simplify))

        cms = [me.Point('R' + str(i)) for i in range(6)]
        for i, cm in enumerate(cms[0:-1]):
            cm.set_pos(joints[i], vif(mass_centers[i], frames[i+1],
                       simplify=if_simplify))
        cms[-1].set_pos(joints[-1], vif(mass_centers[-1], frames[-1],
                        simplify=False))

        moments = np.array(moments)
        if if_simplify is True:
            its = map(me.inertia, frames[1:],
                      moments.T[0], moments.T[1], moments.T[2])
        else:
            its = map(me.inertia, frames[1:],
                      moments.T[0], moments.T[1], moments.T[2],
                      moments.T[3], moments.T[4], moments.T[5])
        its_w_centers = list(zip(its, cms))

        bodies = list(map(me.RigidBody, ['b'+str(i) for i in range(6)], cms,
                          frames[1:], masses, its_w_centers))

        q_dot = me.dynamicsymbols('omega:6')
        kde = [(q_dot[i] - q[i].diff()) for i in range(6)]

        for i, frm in enumerate(frames[1:]):
            frm.set_ang_vel(frames[i], q_dot[i] * rotation_axes[i])

        joints[0].set_vel(world, 0)
        for i, jt in enumerate(joints[1:]):
            jt.v2pt_theory(joints[i], world, frames[i+1])
        for i, cm in enumerate(cms):
            cm.v2pt_theory(joints[i], world, frames[i+1])

        grav_w_centers = list(zip(cms,
                                    map(lambda m: -m * vif(g, world), masses)))
        tau = me.dynamicsymbols('T:6')
        frictions = list(map(func_friction, q_dot,
                             fr_paras['Rh'], fr_paras['Rv'], fr_paras['Threshold'],
                             rotation_axes))
        forces = []
        for i in range(5):
            T = (tau[i] * rotation_axes[i] + frictions[i] -
                 tau[i + 1] * rotation_axes[i + 1] - frictions[i + 1])
            forces.append(T)
        forces.append(tau[5] * rotation_axes[5] + frictions[5])
        forces_w_frames = list(zip(frames[1:], forces))
        loads = grav_w_centers + forces_w_frames

        self.q = q
        self.q_dot = q_dot
        self.tau = tau
        self.kde = kde
        self.frames = frames
        self.joints = joints
        self.cms = cms
        self.its_w_center = its_w_centers
        self.bodies = bodies
        self.loads = loads
        # to be defined later



    def generate_equation(self):
        """
        New attributes:
            rhs : right hand side
        :return:
        """
        print('symbolic dynamic: generating symbolic equations')
        kane = me.KanesMethod(self.frames[0], self.q, self.q_dot, self.kde)
        fr, frstar = kane.kanes_equations(self.loads, self.bodies)
        mass_matrix = kane.mass_matrix_full
        forcing_vector = kane.forcing_full
        right_hand_side = generate_ode_function(forcing_vector, self.q, self.q_dot,
                                                [], mass_matrix=mass_matrix,
                                                specifieds=self.tau)
        self.kane = kane
        self.rhs = right_hand_side

    def environment(self, tr, r, ts, t_end, x0):
        print('symbolic dynamic: set up inputs, time series, and initial state')
        N = int(t_end/ts)
        self.t_samples, self.ts = np.linspace(0.0, t_end, N, retstep=True)
        M = len(r[0,:])
        # self.r = r[0:len(self.t)]
        t_trace = np.linspace(0.0, tr * M, M)
        self.r_samples = np.zeros([12, N])
        for i in range(12):
            self.r_samples[i,:] = np.interp(self.t_samples, t_trace, r[i,:])
        self.x0 = x0

    def design_control(self, kpd, ki, i0, i_bound):
        """
        define the controller, independent PID in the beginning
        Nes attributes:
            controller : function in the form of func(x,t) serves as the controller
            t_ref : list, record time steps of odient algorithm
            integrator : I term
            u : list, record of control output
        """
        print('symbolic dynamic: design controller')
        kpd_batch = np.zeros([6, 12])
        for i in range(6):
            kpd_batch[i, [i, 5+i]] = np.array(kpd[i])
        self.t_old = 0
        self.t_solver = np.array([])
        self.integral = np.zeros(6)
        self.i_bound = i_bound
        self.fw = i0
        self.u_record = i0
        self.rn = np.zeros(12)

        def control(x, t):
            for i in range(6):
                self.rn[i] = np.interp(t, self.t_samples, self.r_samples[i, :])
            dx = self.rn - x
            dt = t - self.t_old
            if dt > 0:
                self.integral = self.integral + ki * dx[0:6] * dt
            for i, item in enumerate(self.integral):
                if abs(item)>i_bound[i]:
                    item = np.sign(item) * i_bound[i]
            self.t_old = t
            u = kpd_batch @ dx + self.integral + self.fw
            self.u_record = np.vstack((self.u_record, u))
            self.t_solver = np.hstack((self.t_solver, t))
            return u

        self.control = control

    def define_brake(self, mechanic_tau, max_short_circuit_tau, speed_max_tau):
        def stop0(x, t):
            speed = x[6:]
            short_circuit_tau = - (2 * max_short_circuit_tau * speed *
                                   speed_max_tau / (speed**2 + speed_max_tau**2))
            u = - mechanic_tau * np.sign(speed) + short_circuit_tau
            return u
        self.stop0 = stop0

    def run(self, action = 'control'):
        """
        run simulation
        :return:
            y : simulated trajectory
        """
        print('symbolic dynamic: simulating...')
        if action.lower() is 'control':
            print('Action: closed loop position control')
            action = self.control
        elif action.lower() is 'stop0':
            print('Action: stop0')
            action = self.stop0

        (self.y, self.odeint_info) = odeint(self.rhs, self.x0, self.t_samples,
                                            args=(action, {}),
                                            rtol=1e-5,
                                            atol=1e-5,
                                            full_output=True)

    def show(self):
        plt.figure()

        plt.subplot(6, 2, 1)
        plt.plot(self.t_samples, self.y[:, 0], 'b-')
        plt.plot(self.t_samples, self.r_samples[0,:], 'm--')
        plt.grid()
        plt.subplot(6, 2, 2)
        plt.plot(self.t_samples, self.y[:, 1], 'b-')
        plt.plot(self.t_samples, self.r_samples[1, :], 'm--')
        plt.grid()

        plt.subplot(6, 2, 3)
        plt.plot(self.t_solver, self.u_record[0:-1, 0], 'r--')
        plt.grid()
        plt.subplot(6, 2, 4)
        plt.plot(self.t_solver, self.u_record[0:-1, 1], 'r--')
        plt.grid()

        plt.subplot(6, 2, 5)
        plt.plot(self.t_samples, self.y[:, 2], 'b-')
        plt.plot(self.t_samples, self.r_samples[2, :], 'm--')
        plt.grid()
        plt.subplot(6, 2, 6)
        plt.plot(self.t_samples, self.y[:, 3], 'b-')
        plt.plot(self.t_samples, self.r_samples[3, :], 'm--')
        plt.grid()

        plt.subplot(6, 2, 7)
        plt.plot(self.t_solver, self.u_record[0:-1, 2], 'r--')
        plt.grid()
        plt.subplot(6, 2, 8)
        plt.plot(self.t_solver, self.u_record[0:-1, 3], 'r--')
        plt.grid()

        plt.subplot(6, 2, 9)
        plt.plot(self.t_samples, self.y[:, 4], 'b-')
        plt.plot(self.t_samples, self.r_samples[4, :], 'm--')
        plt.grid()
        plt.subplot(6, 2, 10)
        plt.plot(self.t_samples, self.y[:, 5], 'b-')
        plt.plot(self.t_samples, self.r_samples[5, :], 'm--')
        plt.grid()

        plt.subplot(6, 2, 11)
        plt.plot(self.t_solver, self.u_record[0:-1, 4], 'r--')
        plt.grid()
        plt.subplot(6, 2, 12)
        plt.plot(self.t_solver, self.u_record[0:-1, 5], 'r--')
        plt.grid()

        plt.show()