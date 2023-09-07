import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Read the .xlsx file
df = pd.read_excel('rawdata.xlsx')

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

# Create a figure and subplot for left body parts
fig_left, axs_left = plt.subplots(figsize=(10, 8))
fig_left.suptitle("Smoothed Angular Velocity Scatter Plot (Left Body Parts)")

# Create a list of left body part data
left_body_parts = [leftAnkle, leftKnee, leftHip, leftShoulder, leftElbow]
body_part_names = ['Ankle', 'Knee', 'Hip', 'Shoulder', 'Elbow']

# Plot all left body parts in the left subplot
# Plot all left body parts in the left subplot
for i in range(len(body_part_names)):
    left_body_part = left_body_parts[i]
    time_diff_left = np.diff(time)
    angular_displacement_left = np.diff(left_body_part)
    angular_velocity_left = angular_displacement_left / time_diff_left

    interpolated_func_left = interp1d(time[1:], angular_velocity_left, kind='cubic')
    fine_time_left = np.linspace(time[1], time[-1], num=2000)
    smooth_angular_velocity_left = interpolated_func_left(fine_time_left)

    max_index_left = np.argmax(smooth_angular_velocity_left)
    min_index_left = np.argmin(smooth_angular_velocity_left)

    axs_left.plot(fine_time_left, smooth_angular_velocity_left, label=f'Left {body_part_names[i]}')

    # Plot maximum and minimum points
    axs_left.plot(fine_time_left[max_index_left], smooth_angular_velocity_left[max_index_left], 'ro', label='Max')
    axs_left.plot(fine_time_left[min_index_left], smooth_angular_velocity_left[min_index_left], 'bo', label='Min')

    # Display values for maximum and minimum points
    max_text = f'Max: ({fine_time_left[max_index_left]:.2f} ms, {smooth_angular_velocity_left[max_index_left]:.2f} rad/s)'
    min_text = f'Min: ({fine_time_left[min_index_left]:.2f} ms, {smooth_angular_velocity_left[min_index_left]:.2f} rad/s)'
    axs_left.text(fine_time_left[max_index_left], smooth_angular_velocity_left[max_index_left], max_text,
                  verticalalignment='bottom', horizontalalignment='left')
    axs_left.text(fine_time_left[min_index_left], smooth_angular_velocity_left[min_index_left], min_text,
                  verticalalignment='top', horizontalalignment='left')

axs_left.set_xlabel("Time (ms)")
axs_left.set_ylabel("Angular Velocity (rad/s)")
axs_left.legend()

# Create a figure and subplot for right body parts
fig_right, axs_right = plt.subplots(figsize=(10, 8))
fig_right.suptitle("Smoothed Angular Velocity Scatter Plot (Right Body Parts)")

# Create a list of right body part data
right_body_parts = [rightAnkle, rightKnee, rightHip, rightShoulder, rightElbow]

# Plot all right body parts in the right subplot
for i in range(len(body_part_names)):
    right_body_part = right_body_parts[i]
    time_diff_right = np.diff(time)
    angular_displacement_right = np.diff(right_body_part)
    angular_velocity_right = angular_displacement_right / time_diff_right

    interpolated_func_right = interp1d(time[1:], angular_velocity_right, kind='cubic')
    fine_time_right = np.linspace(time[1], time[-1], num=2000)
    smooth_angular_velocity_right = interpolated_func_right(fine_time_right)

    max_index_right = np.argmax(smooth_angular_velocity_right)
    min_index_right = np.argmin(smooth_angular_velocity_right)

    axs_right.plot(fine_time_right, smooth_angular_velocity_right, label=f'right {body_part_names[i]}')

    # Plot maximum and minimum points
    axs_right.plot(fine_time_right[max_index_right], smooth_angular_velocity_right[max_index_right], 'ro', label='Max')
    axs_right.plot(fine_time_right[min_index_right], smooth_angular_velocity_right[min_index_right], 'bo', label='Min')

    # Display values for maximum and minimum points
    max_text = f'Max: ({fine_time_right[max_index_right]:.2f} ms, {smooth_angular_velocity_right[max_index_right]:.2f} rad/s)'
    min_text = f'Min: ({fine_time_right[min_index_right]:.2f} ms, {smooth_angular_velocity_right[min_index_right]:.2f} rad/s)'
    axs_right.text(fine_time_right[max_index_right], smooth_angular_velocity_right[max_index_right], max_text,
                  verticalalignment='bottom', horizontalalignment='right')
    axs_right.text(fine_time_right[min_index_right], smooth_angular_velocity_right[min_index_right], min_text,
                  verticalalignment='top', horizontalalignment='right')

axs_left.set_xlabel("Time (ms)")
axs_left.set_ylabel("Angular Velocity (rad/s)")
axs_left.legend()

axs_right.set_xlabel("Time (ms)")
axs_right.set_ylabel("Angular Velocity (rad/s)")
axs_right.legend()

# Show the left plot in a separate window
plt.figure(fig_left.number)
plt.show()

# Show the right plot in a separate window
plt.figure(fig_right.number)
plt.show()