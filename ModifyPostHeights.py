import pandas as pd

def modifyPostHeights(Zheight_delta):

    delta_data = {'X': [], 'Y': [], 'Z': [], 'Delta': [], 'Rotations': []}

    pitch = 2.5
    size_x = len(Zheight_delta[0])
    size_y = len(Zheight_delta)
    z = 0

    for x in range(size_x):

        for y in range(size_y):

            delta = Zheight_delta[y, x]
            rotations = delta / pitch

            delta = round(delta, 2)
            rotations = round(rotations, 2)

            delta_data['X'].append(x)
            delta_data['Y'].append(y)
            delta_data['Z'].append(z)
            delta_data['Delta (mm)'].append(delta)
            delta_data['Rotations (N)'].append(rotations)



    delta_df = pd.DataFrame(delta_data)

    return delta_df




