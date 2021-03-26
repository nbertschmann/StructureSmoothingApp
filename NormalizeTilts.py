import pandas as pd


def normalizeTilts(data):

    data_new = pd.DataFrame()

    for bot in data['BotID'].unique():

        df = data.loc[data['BotID'] == bot]
        pitch_vals = data.loc[data['BotID'] == bot, 'Pitch']
        roll_vals = data.loc[data['BotID'] == bot, 'Roll']

        pitch_sum = pitch_vals.sum()
        pitch_ct = len(pitch_vals)
        pitch_ave = pitch_sum/pitch_ct
        pitch_ave = round(pitch_ave, 4)

        roll_sum = roll_vals.sum()
        roll_ct = len(roll_vals)
        roll_ave = roll_sum/roll_ct
        roll_ave = round(roll_ave, 4)

        # df['Pitch'].apply(lambda x: x + pitch_ave)
        # df['Roll'].apply(lambda y: y + roll_ave)

        df['Roll'] -= roll_ave
        df['Pitch'] -= pitch_ave

        data_new = data_new.append(df, ignore_index=True)

    return data_new

    pass