import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Read the .xlsx file
df = pd.read_excel('rawdata.xlsx')

# Store 'A' column data in list_a
time = df['Time (ms)'].tolist()

# Create a dictionary to store body part data
body_parts = {
    'LeftShoulder': df['LeftShoulder'].tolist(),
    'RightShoulder': df['RightShoulder'].tolist(),
    'LeftElbow': df['LeftElbow'].tolist(),
    'RightElbow': df['RightElbow'].tolist(),
    'LeftHip': df['LeftHip'].tolist(),
    'RightHip': df['RightHip'].tolist(),
    'LeftKnee': df['LeftKnee'].tolist(),
    'RightKnee': df['RightKnee'].tolist(),
    'LeftAnkle': df['LeftAnkle'].tolist(),
    'RightAnkle': df['RightAnkle'].tolist()
}

# Initialize the first graph as 'RightKnee'
current_graph_name = 'RightKnee'
current_graph = body_parts[current_graph_name]

# Calculate the time differences and angular displacements
time_diff = np.diff(time)
angular_displacement = np.diff(current_graph)

# Calculate the angular velocity
angular_velocity = angular_displacement / time_diff

# Create an interpolation function for smoothing the line
interpolated_func = interp1d(time[1:], angular_velocity, kind='cubic')

# Create a finer time array for smoother line
fine_time = np.linspace(time[1], time[-1], num=2000)

# Interpolate the angular velocity values for the finer time array
smooth_angular_velocity = interpolated_func(fine_time)

# Create a scatter plot with smoothed line
plt.plot(fine_time, smooth_angular_velocity, '-')

# Customize the plot
plt.title("Smoothed Angular Velocity " + current_graph_name)
plt.xlabel("Time (ms)")
plt.ylabel("Angular Velocity")

plt.xticks(np.arange(fine_time[0], fine_time[-1] + 1, 500))

points = []  # Store the clicked points

def onclick(event):
    if event.button == 1:  # Left mouse button
        x = event.xdata
        y = interpolated_func(x)
        if y is not None:
            points.append((x, y))
            plt.plot(x, y, 'ro')
            plt.text(x, y, f'({x:.2f}, {y:.2f})', verticalalignment='bottom', horizontalalignment='right')
        else:
            plt.plot(x, y, 'bo')
        plt.draw()
    elif event.button == 3:  # Right mouse button
        if points:
            last_point = points.pop()
            plt.plot(last_point[0], last_point[1], 'w.', markersize=15)  # Erase last dot
            plt.draw()

def next_graph(event):
    global current_graph_name, current_graph, smooth_angular_velocity, max_index, min_index, angular_velocity_max, angular_velocity_min, top_threshold, down_threshold
    current_graph_name = list(body_parts.keys())[(list(body_parts.keys()).index(current_graph_name) + 1) % len(body_parts)]
    current_graph = body_parts[current_graph_name]
    angular_displacement = np.diff(current_graph)
    angular_velocity = angular_displacement / time_diff
    interpolated_func = interp1d(time[1:], angular_velocity, kind='cubic')
    smooth_angular_velocity = interpolated_func(fine_time)

    max_index = np.argmax(smooth_angular_velocity)
    min_index = np.argmin(smooth_angular_velocity)

    angular_velocity_max = smooth_angular_velocity[max_index]
    #print("angular_velocity_max" + str(angular_velocity_max))
    angular_velocity_min = smooth_angular_velocity[min_index]
    #print("angular_velocity_min" + str(angular_velocity_min))

    top_threshold = angular_velocity_max * 1.5
    down_threshold = angular_velocity_min * 1.5

    plt.clf()
    plt.plot(fine_time, smooth_angular_velocity, '-')
    plt.title("Smoothed Angular Velocity " + current_graph_name)
    plt.xlabel("Time (ms)")
    plt.ylabel("Angular Velocity")
    plt.xticks(np.arange(fine_time[0], fine_time[-1] + 1, 500))
    plt.ylim(down_threshold, top_threshold)
    plt.plot(fine_time[max_index], smooth_angular_velocity[max_index], 'ro')
    plt.plot(fine_time[min_index], smooth_angular_velocity[min_index], 'ro')
    plt.text(fine_time[max_index], smooth_angular_velocity[max_index], f'({fine_time[max_index]:.2f}, {angular_velocity_max:.2f})',
             verticalalignment='bottom', horizontalalignment='right')
    plt.text(fine_time[min_index], smooth_angular_velocity[min_index], f'({fine_time[min_index]:.2f}, {angular_velocity_min:.2f})',
             verticalalignment='top', horizontalalignment='left')
    plt.draw()

# Find the indices of maximum and minimum values
max_index = np.argmax(smooth_angular_velocity)
min_index = np.argmin(smooth_angular_velocity)

angular_velocity_max = smooth_angular_velocity[max_index]
print("angular_velocity_max" + str(angular_velocity_max))
angular_velocity_min = smooth_angular_velocity[min_index]
print("angular_velocity_min" + str(angular_velocity_min))

top_threshold = angular_velocity_max * 1.5
down_threshold = angular_velocity_min * 1.5
plt.ylim(down_threshold, top_threshold)

# Plot maximum and minimum points
plt.plot(fine_time[max_index], smooth_angular_velocity[max_index], 'ro')
plt.plot(fine_time[min_index], smooth_angular_velocity[min_index], 'ro')

# Display values for maximum and minimum points
plt.text(fine_time[max_index], smooth_angular_velocity[max_index], f'({fine_time[max_index]:.2f}, {angular_velocity_max:.2f})',
         verticalalignment='bottom', horizontalalignment='right')
plt.text(fine_time[min_index], smooth_angular_velocity[min_index], f'({fine_time[min_index]:.2f}, {angular_velocity_min:.2f})',
         verticalalignment='top', horizontalalignment='left')

# Connect events
plt.gcf().canvas.mpl_connect('button_press_event', onclick)
plt.gcf().canvas.mpl_connect('key_press_event', next_graph)

# Show the plot
plt.show()
