import numpy as np
import re
import csv
import pandas as pd
import os

def parseLogs(log_path, structureVerification_path):

    log_file = open(log_path, "r", encoding='utf8', errors='ignore')
    data = {'DM': [], 'X': [], 'Y': [], 'Z': [], 'Pitch': [], 'Roll': []}

    for line in log_file:

        try:
            if "[IMU] Tilt:P:" in line:

                pitch_val = re.search("(?<=P:)[' ']?[-]?[0-9].[0-9]{1,3}", line).group()
                print('Pitch: ' + pitch_val)

                pitch_val = float(pitch_val.lstrip(' '))
                # pitch value must be modified to match correct tilt
                pitch_val *= -1
                pitch_val = str(pitch_val)
                data['Pitch'].append(float(pitch_val))


                roll_val = re.search("(?<=R:)[' ']?[-]?[0-9].[0-9]{1,3}", line).group()
                print('Roll: ' + roll_val)
                roll_val = roll_val.lstrip(' ')
                data['Roll'].append(float(roll_val))

                dm_val = re.search("(?<=DM:)[' ']?[-]?[0-9].[0-9]{1,3}", line).group()
                dm_val = dm_val.lstrip(' ')
                data['DM'].append(dm_val)

                print(line)

                structureVerification_file = csv.reader(open(structureVerification_path, 'r'), delimiter=",")

                for row in structureVerification_file:

                    if dm_val == row[4]:
                        data['X'].append(int(row[1]))
                        data['Y'].append(int(row[2]))
                        data['Z'].append(int(row[3]))

                if len(data['X']) != len(data['code']):
                    data['X'].append(float('NaN'))
                    data['Y'].append(float('NaN'))
                    data['Z'].append(float('NaN'))

        except Exception as e:
            print("[ERROR]: exception={}".format(e))
            print("[ERROR]:  at line =" + line)

    my_data = pd.DataFrame(data)
    return my_data