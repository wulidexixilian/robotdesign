import numpy as np
from model.m_analysis import StaticAnalysis, SimulationAnalysis


class StaticAnalysisScara(StaticAnalysis):
    def get_stall_torque(self, qd_max, load):
        qd = -0.01 * qd_max
        qdd = np.zeros(self.num_axes)
        q = np.zeros(self.num_axes)
        gravity = np.array([0, 0, -9.8])
        result = self.instant_load(q, qd, qdd, gravity)
        characteristic = self.get_motor_characteristic()
        tau_motor_s1 = [char['s1'][1][0] for char in characteristic]
        tcp = result['tcp']
        final_result = {
            'tcp': tcp,
            'tau_motor': np.abs(result['tau_motor']),
            'tau_joint': np.array(result['tau_joint'])
        }
        final_result['motor_percent'] = (final_result['tau_motor'] /
                                         tau_motor_s1 * 100)
        return final_result

class SimulationAnalysisScara(SimulationAnalysis, StaticAnalysisScara):
    pass