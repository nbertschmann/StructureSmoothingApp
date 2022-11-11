import pandas as pd

def combineTilts2(data):
    """
    This function averages pitch and roll values from a given square
    :param data: contains DM value, X location, Y location, Pitch Value, Roll Value
    :return data_sorted: contains averaged values from each square
    """

    data_out = pd.DataFrame()

    for x in data['X'].unique():

        for y in data.loc[(data['X'] == x), 'Y'].unique():

            for z in data.loc[(data['X'] == x) & (data['Y'] == y), 'Z'].unique():

                datamatrix = data.loc[(data['X'] == x) & (data['Y'] == y) & (data['Z'] == z), 'DM'].max()

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

    data_sorted = data_out.sort_values(by=['Z', 'X', 'Y'], ascending=True, ignore_index=True)

    return data_sorted
