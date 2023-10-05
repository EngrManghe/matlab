import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Read the .xlsx file
df = pd.read_excel('1.1_angles_ballet.xlsx')

# Store 'A' column data in list_a
time = df['Time (ms)'].tolist()

# Store 'B' column data for left body parts
leftAnkle = df['LeftAnkle'].tolist()
leftKnee = df['LeftKnee'].tolist()
leftHip = df['LeftHip'].tolist()
leftShoulder = df['LeftShoulder'].tolist()
leftElbow = df['LeftElbow'].tolist()

# Store 'B' column data for right body parts
rightAnkle = df['RightAnkle'].tolist()
rightKnee = df['RightKnee'].tolist()
rightHip = df['RightHip'].tolist()
rightShoulder = df['RightShoulder'].tolist()
rightElbow = df['RightElbow'].tolist()

# Create a figure with multiple subplots (one for each body part)
fig, axs = plt.subplots(2, 5, figsize=(15, 6))
fig.suptitle("Smoothed Angular Velocity Scatter Plots")

# Create a list of left and right body part names
left_body_parts = [leftAnkle, leftKnee, leftHip, leftShoulder, leftElbow]
right_body_parts = [rightAnkle, rightKnee, rightHip, rightShoulder, rightElbow]
body_part_names = ['Ankle', 'Knee', 'Hip', 'Shoulder', 'Elbow']

# Iterate through body parts and create plots
for i in range(len(body_part_names)):
    ax_left = axs[0, i]
    ax_right = axs[1, i]
    
    # Left Body Part
    left_body_part = left_body_parts[i]
    time_diff_left = np.diff(time)
    angular_displacement_left = np.diff(left_body_part)
    angular_velocity_left = angular_displacement_left / time_diff_left
    
    interpolated_func_left = interp1d(time[1:], angular_velocity_left, kind='cubic')
    fine_time_left = np.linspace(time[1], time[-1], num=2000)
    smooth_angular_velocity_left = interpolated_func_left(fine_time_left)
    
    ax_left.plot(fine_time_left, smooth_angular_velocity_left, color='red', label=f'Left {body_part_names[i]}')
    ax_left.set_title(f'Left {body_part_names[i]}')
    ax_left.set_xlabel("Time (ms)")
    ax_left.set_ylabel("Angular Velocity (rad/s)")
    
    # Right Body Part
    right_body_part = right_body_parts[i]
    time_diff_right = np.diff(time)
    angular_displacement_right = np.diff(right_body_part)
    angular_velocity_right = angular_displacement_right / time_diff_right
    
    interpolated_func_right = interp1d(time[1:], angular_velocity_right, kind='cubic')
    fine_time_right = np.linspace(time[1], time[-1], num=2000)
    smooth_angular_velocity_right = interpolated_func_right(fine_time_right)
    
    ax_right.plot(fine_time_right, smooth_angular_velocity_right, color='blue', label=f'Right {body_part_names[i]}')
    ax_right.set_title(f'Right {body_part_names[i]}')
    ax_right.set_xlabel("Time (ms)")
    ax_right.set_ylabel("Angular Velocity (rad/s)")

# Adjust spacing between subplots
plt.tight_layout()
plt.subplots_adjust(top=0.85)

# Show the plot
plt.show()
