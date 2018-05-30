import matplotlib.pyplot as plt
# compare with OPC


def compare(s, trace_file, percentage):
    figMotorTorque = plt.figure()
    figMotorTorque.suptitle('motor torque [sec - Nm]')
    pm = [plt.subplot(321+i) for i in range(6)]
    for i in range(6):
        moment_trace = s.read_trace(
            trace_file,
            'DriveMotorTorq_CmdIpo{}'.format(i+1),
            percentage
        )[0]
        pm[i].plot(
            s.t_ser[0:len(moment_trace)],
            -moment_trace, 'r-', label="trace"
        )
        pm[i].plot(
            s.t_ser, s.tau_motor_ser[:,i],
            'b--', label="sim"
        )
        pm[i].grid(True)
        pm[i].legend()

    figJointTorque = plt.figure()
    figJointTorque.suptitle('gear torque [sec - Nm]')
    pm = [plt.subplot(321+i) for i in range(6)]
    for i in range(6):
        moment_trace = s.read_trace(
            trace_file,
            'GearTorq_CmdModel{}'.format(i+1),
            percentage
        )[0]
        pm[i].plot(
            s.t_ser[0:len(moment_trace)],
            -moment_trace, 'r-',
            label="trace"
        )
        pm[i].plot(
            s.t_ser, -s.tau_joint_ser[:,i],
            'b--', label="sim"
        )
        pm[i].grid(True)
        pm[i].legend()
    plt.show()
