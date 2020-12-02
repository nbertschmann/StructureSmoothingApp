import pandas as pd
def combineTilts(data):
    data_out = pd.DataFrame()

    for x in data['x'].unique():

        for y in data.loc[(data['x'] == x), 'y'].unique():

            for z in data.loc[(data['x'] == x) & (data['y'] == y), 'z'].unique():
                datamatrix = data.loc[(data['x'] == x) & (data['y'] == y) & (data['z'] == z), 'DM'].max()

                pitch = data.loc[(data['x'] == x) & (data['y'] == y) & (data['z'] == z), 'pitch']
                pitch_sum = pitch.sum()
                pitch_average = pitch_sum / len(pitch)

                roll = data.loc[(data['x'] == x) & (data['y'] == y) & (data['z'] == z), 'roll']
                roll_sum = roll.sum()
                roll_average = roll_sum / len(roll)

                temp_results = {'DM': datamatrix, 'x': [x], 'y': [y], 'z': [z], 'pitch': [pitch_average],
                                'roll': [roll_average]}
                temp_df = pd.DataFrame(temp_results)

                data_out = data_out.append(temp_df)

    data_sorted = data_out.sort_values(by=['x', 'y'], ascending=True)
    pass
    return data_sorted
