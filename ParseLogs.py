import numpy as np
import re
import csv
import pandas as pd
import os

def parseLogs(log_path, structureVerification_path, log_ct, log_total, progress_callback):

    file_name = log_path.strip().split('\\')[-1]
    progress_text = "Processing File " + str(log_ct + 1) + ' / ' + str(log_total) + ': ' + file_name
    progress_callback.emit(0, progress_text)

    log_file_ct = open(log_path, "r", encoding='utf8', errors='ignore')
    log_file = open(log_path, "r", encoding='utf8', errors='ignore')

    data = {'DM': [], 'X': [], 'Y': [], 'Z': [], 'Pitch': [], 'Roll': [], 'BotID': []}

    row_count = sum(1 for row in log_file_ct)
    count = 0
    last_progress = 0

    for line in log_file:

        count += 1

        progress_percent = (count/row_count) * 100
        progress_percent = round(progress_percent, 0)
        progress_percent = int(progress_percent)

        if progress_percent > last_progress:
            last_progress = progress_percent
            progress_callback.emit(progress_percent, progress_text)

        try:

            if "[IMU] Tilt:P:" in line:

                pitch_val = re.search("(?<=P:)[' ']?[-]?[0-9].[0-9]{1,3}", line).group()
                # print('Pitch: ' + pitch_val)

                pitch_val = float(pitch_val.lstrip(' '))
                # pitch value must be modified to match correct tilt
                if pitch_val != 0:
                    pitch_val *= -1

                pitch_val = str(pitch_val)

                roll_val = re.search("(?<=R:)[' ']?[-]?[0-9].[0-9]{1,3}", line).group()
                # print('Roll: ' + roll_val)
                roll_val = roll_val.lstrip(' ')

                dm_val = re.search("(?<=DM:)[' ']?[-]?[0-9].[0-9]{1,3}", line).group()
                dm_val = dm_val.lstrip(' ')

                botID = ''

                try:

                    botID = re.search("(?<=I:)\s?[A-Z][a-z]{1,10}:", line).group()
                    botID = botID.lstrip(' ')
                    botID = botID.rstrip(':')

                except Exception as e:

                    # print('BotID exception: ' + str(e))
                    pass

                try:

                    botID = re.search("[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}", line).group()


                except Exception as e:

                    # print('BotID exception: ' + str(e))
                    pass



                data['Pitch'].append(float(pitch_val))
                data['Roll'].append(float(roll_val))
                data['DM'].append(dm_val)
                data['BotID'].append(botID)


                structureVerification_file = csv.reader(open(structureVerification_path, 'r'), delimiter=",")

                for row in structureVerification_file:

                    if dm_val == row[4]:
                        data['X'].append(int(row[1]))
                        data['Y'].append(int(row[2]))
                        data['Z'].append(int(row[3]))

                if len(data['X']) != len(data['DM']):
                    data['X'].append(float('NaN'))
                    data['Y'].append(float('NaN'))
                    data['Z'].append(float('NaN'))


        except Exception as e:

            pass
            # print("[ERROR]: exception={}".format(e))
            # print("[ERROR]:  at line =" + line)

    # print(count)
    my_data = pd.DataFrame(data)
    return my_data