from model.m_simulation import Simulation
from model.m_analysis_scara import StaticAnalysisScara, SimulationAnalysisScara
import numpy as np
from utility.inverse_kinematic import ik_scara

ar = np.array


class SimulationScara(Simulation):
    frame_config = {
        "groundbase": {
            'frame0': ar([0, 0, 0]),
            'frame1': ar([np.pi, 0, 0]),
            'mode': 0
        },
        "link1": {
            'frame0': ar([np.pi, 0, 0]),
            'frame1': ar([0, 0, 0]),
            'mode': 0
        },
        "link2": {
            'frame0': ar([np.pi, 0, 0]),
            'frame1': ar([0, 0, 0]),
            'mode': 0
        },
        "link3": {
            'frame0': ar([np.pi, 0, 0]),
            'frame1': ar([0, 0, 0]),
            'mode': 1
        },
        "link4": {
            'frame0': ar([np.pi, 0, 0]),
            'frame1': ar([0, 0, 0]),
            'mode': 0
        },
        "tcp": {
            'frame0': ar([np.pi, 0, 0]),
            'frame1': ar([0, 0, 0]),
            'mode': 0
        },
    }

    def set_ik(self):
        self.robot.inverse_dynamic = ik_scara

    def get_result(self):
        """
        generate a result object for further analysis
        :return: SimulationResult instance
        """
        if self.q_cmd_ser is None:
            sr = StaticAnalysisScara(self.robot)
        else:
            sr = SimulationAnalysisScara(
                self.robot,
                self.q_cmd_ser, self.q_dot_cmd_ser,
                self.tau_motor_ser, self.tau_joint_ser,
                self.f_joint_ser, self.tau_joint_3d_ser,
                self.tcp_ser,
                self.t_ser,
                self.ts
            )
        return sr
