import numpy as np

def formatData(data):

    column_x = data['X']
    max_x = column_x.max()

    column_y = data['Y']
    max_y = column_y.max()

    xtilt_real = np.zeros((max_y, max_x), float)
    ytilt_real = np.zeros((max_y, max_x), float)

    for y in range(max_y):
        for x in range(max_x):
            x_tilt = data.loc[(data['X'] == x) & (data['Y'] == y) & (data['Z'] == 0), 'Pitch']
            y_tilt = data.loc[(data['X'] == x) & (data['Y'] == y) & (data['Z'] == 0), 'Roll']

            size_x = len(x_tilt)
            size_y = len(y_tilt)

            x_list = list(x_tilt)
            y_list = list(y_tilt)

            if size_x != 0:
                x_val = x_list[0]
                xtilt_real[y, x] = x_val
            if size_y != 0:
                y_val = y_list[0]
                ytilt_real[y, x] = y_val


    return xtilt_real, ytilt_real