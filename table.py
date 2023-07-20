import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import inspect
from scipy.interpolate import interp1d

# Read the .xlsx file
df = pd.read_excel('rawdata.xlsx')

# Store 'A' column data in list_a
time = df['Time (ms)'].tolist()

# Store 'B' column data in list_b
LeftShoulder = df['LeftShoulder'].tolist()
RightShoulder = df['RightShoulder'].tolist()
LeftElbow = df['LeftElbow'].tolist()
RightElbow = df['RightElbow'].tolist()
LeftHip = df['LeftHip'].tolist()
RightHip = df['RightHip'].tolist()
LeftKnee = df['LeftKnee'].tolist()
RightKnee = df['RightKnee'].tolist()
LeftAnkle = df['LeftAnkle'].tolist()
RightAnkle = df['RightAnkle'].tolist()

# IT IS OUR SETTINGS SECTION ALL CHANGES ONLY HERE
graph = RightKnee  # CHANGE THIS ONLY
graph_name = [k for k, v in locals().items() if v is graph][0]

print(time)
print(graph)


# Calculate the time differences and angular displacements
time_diff = np.diff(time)
angular_displacement = np.diff(graph)

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
plt.title("Smoothed Angular Velocity " + graph_name)
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

# Find the indices of maximum and minimum values
max_index = np.argmax(smooth_angular_velocity)
min_index = np.argmin(smooth_angular_velocity)

angular_velocity_max = smooth_angular_velocity[max_index]
print("angular_velocity_max" + str(angular_velocity_max))
angular_velocity_min = smooth_angular_velocity[min_index]
print("angular_velocity_min" + str(angular_velocity_min))

top_threshold = angular_velocity_max * 1.5
down_threshold = angular_velocity_min * 1.5
# Set the y-axis display range from -3 to +3
plt.ylim(down_threshold, top_threshold)

# Plot maximum and minimum points
plt.plot(fine_time[max_index], smooth_angular_velocity[max_index], 'ro')
plt.plot(fine_time[min_index], smooth_angular_velocity[min_index], 'ro')

# Display values for maximum and minimum points
plt.text(fine_time[max_index], smooth_angular_velocity[max_index], f'({fine_time[max_index]:.2f}, {angular_velocity_max:.2f})',
         verticalalignment='bottom', horizontalalignment='right')
plt.text(fine_time[min_index], smooth_angular_velocity[min_index], f'({fine_time[min_index]:.2f}, {angular_velocity_min:.2f})',
         verticalalignment='top', horizontalalignment='left')

plt.gcf().canvas.mpl_connect('button_press_event', onclick)

# Show the plot
plt.show()



































3
