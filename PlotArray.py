import numpy as np
import plotly.graph_objects as go

def plotArray(input_array, z_low, z_high):

    size_x = len(input_array[0])
    size_y = len(input_array)

    x_array = np.zeros((size_y, size_x), int)
    x_array[:] = np.NaN

    y_array = np.zeros((size_y, size_x), int)
    y_array[:] = np.NaN

    xtick_array = np.zeros(size_x)
    ytick_array = np.zeros(size_y)

    for x in range(size_x):
        xtick_array[x] = x

    for y in range(size_y):
        ytick_array[y] = y

    # populate y and x array used for 3D plot
    for y in range(size_y):
        for x in range(size_x):

            x_array[y, x] = x
            y_array[y, x] = y


    fig = go.Figure(data=[go.Surface(x=x_array, y=y_array, z=input_array)])

    fig.update_layout(
        scene=dict(
            xaxis=dict(tickmode='array', tickvals=xtick_array),
            yaxis=dict(tickmode='array', tickvals=ytick_array),
            zaxis=dict(nticks=4, range=[z_low, z_high])))

    return fig