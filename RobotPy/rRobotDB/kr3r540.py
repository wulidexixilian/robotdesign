import numpy as np
import json
from resource.ExternalDB.gearbox_db import load_gear_db
from resource.ExternalDB.motor_db import load_motor_db


with open('../rRobotDB/kr3r540_json.txt') as f:
    kr3 = json.load(f)

structure_para = kr3['structure_para']
friction_para = kr3['friction_para']
motor_installation = kr3['motor_installation']
motor_para = list(map(load_motor_db, motor_installation))
mass_para = kr3['mass_para']
gear_installation = kr3['gear_installation']
for item in gear_installation:
    item['type'] = str(item['type'])
gear_para = list(map(load_gear_db, gear_installation))
