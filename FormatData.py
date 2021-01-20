import numpy as np

def formatData(data, data_raw, progress_callback):

    column_x = data_raw['X']
    max_x = column_x.max()
    max_x = int(max_x) + 1

    column_y = data_raw['Y']
    max_y = column_y.max()
    max_y = int(max_y) + 1

    xtilt_real = np.zeros((max_y, max_x), float)
    ytilt_real = np.zeros((max_y, max_x), float)

    data_size = max_x * max_y
    count = 0
    last_progress = 0

    for y in range(max_y):
        for x in range(max_x):
            # x_tilt = data.loc[(data['X'] == x) & (data['Y'] == y) & (data['Z'] == 0), 'Pitch']
            # y_tilt = data.loc[(data['X'] == x) & (data['Y'] == y) & (data['Z'] == 0), 'Roll']

            x_tilt = data.loc[(data['X'] == x) & (data['Y'] == y), 'Pitch']
            y_tilt = data.loc[(data['X'] == x) & (data['Y'] == y), 'Roll']

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

            progress_percent = (count / data_size) * 100
            progress_percent = round(progress_percent, 0)
            progress_percent = int(progress_percent)

            if progress_percent > last_progress:
                last_progress = progress_percent

                progress_callback.emit(progress_percent, 'Running Process 2 / 3 ...')

            count += 1

    return xtilt_real, ytilt_real