import numpy as np

def formatData(data):

    column_x = data['x']
    max_x = column_x.max()

    column_y = data['y']
    max_y = column_y.max()

    xtilt_real = np.zeros((max_y, max_x), float)
    ytilt_real = np.zeros((max_y, max_x), float)

    for y in range(max_y):
        for x in range(max_x):
            x_tilt = data.loc[(data['x'] == x) & (data['y'] == y), 'pitch']
            y_tilt = data.loc[(data['x'] == x) & (data['y'] == y), 'roll']

            size_x = len(x_tilt)
            size_y = len(y_tilt)

            x_val = x_tilt.get(0)
            y_val = y_tilt.get(0)
            if size_x != 0:
                xtilt_real[y, x] = x_val
            if size_y != 0:
                ytilt_real[y, x] = y_val


    return xtilt_real, ytilt_real