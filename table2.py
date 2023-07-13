import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Read the .xlsx file
df = pd.read_excel('rawdata.xlsx')

# Store 'A' column data in list_a
time = df['Time (ms)'].tolist()

# Store 'B' column data
LeftAnkle = df['LeftAnkle'].tolist()
LeftKnee = df['LeftKnee'].tolist()
LeftHip = df['LeftHip'].tolist()

# Calculate the time differences and angular displacements
time_diff_ankle = np.diff(time)
angular_displacement_ankle = np.diff(LeftAnkle)

time_diff_knee = np.diff(time)
angular_displacement_knee = np.diff(LeftKnee)

time_diff_hip = np.diff(time)
angular_displacement_hip = np.diff(LeftHip)

# Calculate the angular velocity
angular_velocity_ankle = angular_displacement_ankle / time_diff_ankle
angular_velocity_knee = angular_displacement_knee / time_diff_knee
angular_velocity_hip = angular_displacement_hip / time_diff_hip

# Create an interpolation function for smoothing the lines
interpolated_func_ankle = interp1d(time[1:], angular_velocity_ankle, kind='cubic')
interpolated_func_knee = interp1d(time[1:], angular_velocity_knee, kind='cubic')
interpolated_func_hip = interp1d(time[1:], angular_velocity_hip, kind='cubic')

# Create a finer time array for smoother lines
fine_time = np.linspace(time[1], time[-1], num=2000)

# Interpolate the angular velocity values for the finer time array
smooth_angular_velocity_ankle = interpolated_func_ankle(fine_time)
smooth_angular_velocity_knee = interpolated_func_knee(fine_time)
smooth_angular_velocity_hip = interpolated_func_hip(fine_time)

# Set the y-axis display range from -3 to +3
plt.ylim(-3, 3)

# Create scatter plots with smoothed lines
plt.plot(fine_time, smooth_angular_velocity_ankle, color='red', label='LeftAnkle')
plt.plot(fine_time, smooth_angular_velocity_knee, color='blue', label='LeftKnee')
plt.plot(fine_time, smooth_angular_velocity_hip, color='green', label='LeftHip')

# Customize the plot
plt.title("Smoothed Angular Velocity Scatter Plot")
plt.xlabel("Time (ms)")
plt.ylabel("Angular Velocity")
plt.legend()

plt.xticks(np.arange(fine_time[0], fine_time[-1]+1, 200))

points = []  # Store the clicked points

def onclick(event):
    if event.button == 1:  # Left mouse button
        x = event.xdata
        y_ankle = interpolated_func_ankle(x)
        y_knee = interpolated_func_knee(x)
        y_hip = interpolated_func_hip(x)
        if y_ankle is not None:
            points.append((x, y_ankle, y_knee, y_hip))
            plt.plot(x, y_ankle, 'ro')
            plt.plot(x, y_knee, 'bo')
            plt.plot(x, y_hip, 'go')
            plt.text(x, y_ankle, f'Ankle: ({x:.2f}, {y_ankle:.2f})', verticalalignment='bottom', horizontalalignment='right')
            plt.text(x, y_knee, f'Knee: ({x:.2f}, {y_knee:.2f})', verticalalignment='bottom', horizontalalignment='right')
            plt.text(x, y_hip, f'Hip: ({x:.2f}, {y_hip:.2f})', verticalalignment='bottom', horizontalalignment='right')
        plt.draw()
    elif event.button == 3:  # Right mouse button
        if points:
            last_point = points.pop()
            plt.plot(last_point[0], last_point[1], 'w.', markersize=15)  # Erase Ankle dot
            plt.plot(last_point[0], last_point[2], 'w.', markersize=15)  # Erase Knee dot
            plt.plot(last_point[0], last_point[3], 'w.', markersize=15)  # Erase Hip dot
            plt.draw()

plt.gcf().canvas.mpl_connect('button_press_event', onclick)

# Show the plot
plt.show()
