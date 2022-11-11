import pandas as pd


def normalizeTilts(data):
    """
    This function normalizes the pitch and roll values (tilt values) based on BotID to eliminate variations in IMU
    measurements from robot to robot
    :param data: contains BotID, DM value, X location, Y location, Pitch Value, Roll Value
    :return data_new: same as input data but with normalized pitch and roll values
    """
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

        df['Roll'] -= roll_ave
        df['Pitch'] -= pitch_ave

        data_new = data_new.append(df, ignore_index=True)

    return data_new

