import numpy as np
from math import atan, pi
from BlurArray import blur

def recreateStructure(Xtilt_real, Ytilt_real):

    size_x = len(Xtilt_real[0]) + 1
    size_y = len(Xtilt_real) + 1

    Zheight_recreated = np.zeros((size_y, size_x), float)


    for i in range(1000):

        Xtilt_recreated = np.zeros((size_y - 1, size_x - 1), float)
        Xtilt_recreated[:] = np.NaN

        Ytilt_recreated = np.zeros((size_y - 1, size_x - 1), float)
        Ytilt_recreated[:] = np.NaN

        for y in range(size_y - 1):
            for x in range(size_x - 1):
                y_val = y
                x_val = x

                Ax = Zheight_recreated[y, x + 1]
                Cx = Zheight_recreated[y + 1, x + 1]
                Bx = Zheight_recreated[y, x]
                Dx = Zheight_recreated[y + 1, x]

                tempX = (Zheight_recreated[y, x + 1] + Zheight_recreated[y + 1, x + 1]) / 2 - (
                            Zheight_recreated[y, x] + Zheight_recreated[y + 1, x]) / 2
                tempX_rad = atan(tempX / 725)
                tempX_deg = atan(tempX_rad) * (180 / pi)

                Xtilt_recreated[y, x] = tempX_deg

                Ay = Zheight_recreated[y + 1, x]
                By = Zheight_recreated[y + 1, x + 1]
                Cy = Zheight_recreated[y, x]
                Dy = Zheight_recreated[y, x + 1]

                tempY = (Zheight_recreated[y + 1, x] + Zheight_recreated[y + 1, x + 1]) / 2 - (
                            Zheight_recreated[y, x] + Zheight_recreated[y, x + 1]) / 2
                tempY_rad = atan(tempY / 725)
                tempY_deg = atan(tempY_rad) * (180 / pi)

                Ytilt_recreated[y, x] = tempY_deg

                # Xtilt_recreated[y, x] = (Zheight_recreated[y, x+1] - Zheight_recreated[y, x] + Zheight_recreated[y+1, x+1] - Zheight_recreated[y+1, x])/2
                # Ytilt_recreated[y, x] = (Zheight_recreated[y+1, x] - Zheight_recreated[y, x] + Zheight_recreated[y+1, x+1] - Zheight_recreated[y, x+1])/2

        # calculate difference between real X-tilt values and recreated X-tilt values
        Xtilt_error = np.subtract(Xtilt_real, Xtilt_recreated)
        Ytilt_error = np.subtract(Ytilt_real, Ytilt_recreated)

        convergence = 0

        for x in range(size_x):
            for y in range(size_y):

                print('x:' + str(x) + ' y:' + str(y))

                if (x == 3):
                    pass
                # [[NW, NE], [SW, SE]]
                err_x = np.zeros((2, 2), float)

                err_y = np.zeros((2, 2), float)

                # NW data
                if (x > 0) and (y > 0):
                    err_x[0, 0] = Xtilt_error[y - 1, x - 1]
                    err_y[0, 0] = Ytilt_error[y - 1, x - 1]

                # NE data
                if (x < size_x - 1) and (y > 0):
                    err_x[0, 1] = Xtilt_error[y - 1, x]
                    err_y[0, 1] = Ytilt_error[y - 1, x]

                # SE data
                if (x > 0) and (y < size_y - 1):
                    err_x[1, 0] = Xtilt_error[y, x - 1]
                    err_y[1, 0] = Ytilt_error[y, x - 1]

                # SW data
                if (x < size_x - 2) and (y < size_y - 1):
                    err_x[1, 1] = Xtilt_error[y, x]
                    err_y[1, 1] = Ytilt_error[y, x]

                pass

                # If the gradient error for X is positive on the W side and negative on the E side, the post must be too low
                # NW + SE - NE - SW
                adj_x = err_x[0, 0] + err_x[1, 0] - err_x[0, 1] - err_x[1, 1]
                # If the gradient error for Y is positive on the N side and negative on the S side, the post must be too low
                # NW + NE - SE - SW
                adj_y = err_y[0, 0] + err_y[0, 1] - err_y[1, 0] - err_y[1, 1]

                convergence = abs((adj_x + adj_y) / (size_x * size_y))

                Zheight_recreated[y, x] = Zheight_recreated[y, x] + ((adj_y + adj_x) * 0.25)

    Zheight_recreated = Zheight_recreated - np.mean(Zheight_recreated)

    Zheight_lowpass = Zheight_recreated
    lowpass_samples = 2

    for i in range(lowpass_samples):
        Zheight_lowpass = blur(Zheight_lowpass, 1)

    Zheight_delta = np.subtract(Zheight_lowpass, Zheight_recreated)

    pass
    return Zheight_recreated, Zheight_lowpass, Zheight_delta