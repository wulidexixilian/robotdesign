import scipy.io
import numpy as np


def get_structure(st, nest):
    dimension = np.reshape(st.KS_Next[0, 0].p[0.0].Wert, 3)
    mass = list()
    motor_position = list()
    elements = st.__dict__
    elements.pop('NoParts')
    elements.pop('Kommentar')
    for idx in range(6):
        motor_id = 'Achse{}_Motor'.format(idx)
        if motor_id in elements:
            motor_position_temp = elements.pop(motor_id)
            motor_position.append(motor_position_temp[0, 0])
    for item in elements:
        mass_element = dict()
        mass_temp = elements[item][0, 0]
        mass_element['m'] = mass_temp.Masse[0, 0].Wert
        mass_element['cm'] = mass_temp.cm[0, 0].Wert
        mass_element['iT'] = mass_temp.J[0, 0].Wert
        mass_element['nest'] = nest
        mass.append(mass_element)
    return mass, motor_position


mat = scipy.io.loadmat('../resource/RobertaExchange/kr12r1810.mat', struct_as_record=False)
obj = mat['Projekt'][0, 0]
robot = obj.Roboter[0, 0]
axis = [getattr(robot.Achsen[0, 0], 'Achse{}'.format(idx+1))[0, 0]
        for idx in range(6)]
structure_name = ['Grundgestell', 'Karussell', 'Schwinge',
                  'Arm', 'Handgrundgestell', 'Handschwenkgehaeuse',
                  'Handflansch']
structure = [getattr(robot.Struktur[0, 0], structure_name[idx])[0, 0]
             for idx in range(6)]
joint = [getattr(robot.Struktur[0, 0], 'Gelenk_A{}'.format(idx+1))[0, 0]
         for idx in range(6)]
name_in_eng = {
    'Grundgestell': 'groundbase',
    'Karussell': 'rotationcolumn',
    'Schwinge': 'linkarm',
    'Arm': 'arm',
    'Handgrundgestell': 'handbase',
    'Handschwenkgehaeuse': 'handwrist',
    'handflansch': 'handflange'
}
for idx, st in enumerate(structure):
    result_st = get_structure(st, name_in_eng[structure_name[idx]])


#
# {
#     "nest": "handflange",
#     "cm":   np.array([0, 0, -3]) * 1e-3, "m": 0.01,
#     "iT":   np.array([50, 50, 50, 0, 0, 0]) * 1e-6
# },
