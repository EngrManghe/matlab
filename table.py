import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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
graph = LeftShoulder  # CHANGE THIS ONLY
graph_name = "LeftShoulder"  # CHANGE THIS ALSO

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

# Set the y-axis display range from -3 to +3
plt.ylim(-3, 3)

# Create a scatter plot with smoothed line
plt.plot(fine_time, smooth_angular_velocity, '-')

# Customize the plot
plt.title("Smoothed Angular Velocity " + graph_name)
plt.xlabel("Time (ms)")
plt.ylabel("Angular Velocity")

plt.xticks(np.arange(fine_time[0], fine_time[-1] + 1, 500))

def onclick(event):
    if event.button == 1:  # Check if left mouse button is clicked
        x = event.xdata
        y = interpolated_func(x)
        if y is not None:  # Check if y-value is not None (i.e., clicked within the curve)
            plt.plot(x, y, 'ro')
            plt.text(x, y, f'({x:.2f}, {y:.2f})', verticalalignment='bottom', horizontalalignment='right')
            plt.draw()

plt.gcf().canvas.mpl_connect('button_press_event', onclick)

# Show the plot
plt.show()
