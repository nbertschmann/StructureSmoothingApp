import pandas as pd
import math
import numpy as np

def combineTilts(data, location, progress_callback):
    data_out = pd.DataFrame()

    count = 0
    data_size = 0
    last_progress = 0
    location_list = []

    for x in data['X'].unique():

        for y in data.loc[(data['X'] == x), 'Y'].unique():

            data_size += 1

    z_vals = data['Z'].unique()
    z_vals = z_vals[np.logical_not(np.isnan(z_vals))]

    if location == 'Basement':

        if min(z_vals) == 0:
            location_list.append(min(z_vals))

    elif location == 'Attic':

        if max(z_vals) > 0:
            location_list.append(max(z_vals))

    else:
        if len(z_vals) > 1:
            location_list.append(min(z_vals))
            location_list.append(max(z_vals))
        else:
            location_list.append(min(z_vals))

    for x in data['X'].unique():

        for y in data.loc[(data['X'] == x), 'Y'].unique():

            progress_percent = (count / data_size) * 100
            progress_percent = round(progress_percent, 0)
            progress_percent = int(progress_percent)

            if progress_percent > last_progress:
                last_progress = progress_percent

                progress_callback.emit(progress_percent, 'Running Process 1 / 3 ...')

            count += 1

            for z in location_list:

                datamatrix = data.loc[(data['X'] == x) & (data['Y'] == y) & (data['Z'] == z), 'DM'].max()

                if not math.isnan(datamatrix):

                    pitch = data.loc[(data['X'] == x) & (data['Y'] == y) & (data['Z'] == z), 'Pitch']
                    pitch_sum = pitch.sum()
                    pitch_average = pitch_sum / len(pitch)
                    pitch_average = round(pitch_average, 6)

                    roll = data.loc[(data['X'] == x) & (data['Y'] == y) & (data['Z'] == z), 'Roll']
                    roll_sum = roll.sum()
                    roll_average = roll_sum / len(roll)
                    roll_average = round(roll_average, 6)

                    temp_results = {'DM': datamatrix, 'X': [x], 'Y': [y], 'Z': [z], 'Pitch': [pitch_average],
                                    'Roll': [roll_average]}
                    temp_df = pd.DataFrame(temp_results)

                    data_out = data_out.append(temp_df)

    if len(data_out) != 0:
        data_sorted = data_out.sort_values(by=['Z', 'X', 'Y'], ascending=True, ignore_index=True)
    else:
        data_sorted = pd.DataFrame(columns=['DM', 'X', 'Y', 'Z', 'Pitch', 'Roll'])

    return data_sorted
