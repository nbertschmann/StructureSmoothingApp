import numpy as np

def blur(np_array, val):

    b_x = val
    b_y = val

    size_x = len(np_array[0])
    size_y = len(np_array)

    blur_array = np.zeros((size_y, size_x), float)
    blur_array[:] = np.NaN

    for y in range(size_y):
        for x in range(size_x):

            min_x = max(0, x - b_x)
            max_x = min(size_x, x + b_x)
            min_y = max(0, y - b_y)
            max_y = min(size_y, y + b_y)

            sub_array = np_array[min_y:max_y+1, min_x:max_x+1]
            array_sum = sum(sum(sub_array))
            array_size = len(sub_array[0])*len(sub_array)
            mean_val = array_sum/array_size

            blur_array[y, x] = mean_val

            pass

    return blur_array

