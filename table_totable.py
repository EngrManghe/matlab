import os
import sys
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

if len(sys.argv) < 2:
    print("Please provide the folder name where .xlsx files located")
    sys.exit(1)

# Get the filename from the command-line argument
directory = sys.argv[1]
all_data = []
for f in os.listdir(directory):
    filename = os.path.join(directory, f)
    if os.path.isfile(filename):
        print(filename)
        df = pd.read_excel(filename) 
        time = df['Time (ms)'].tolist()

        # Create a dictionary to store body part data
        body_parts = {}
        for column in df.columns[1:]:  # Exclude the 'Time (ms)' column
            body_parts[column] = df[column].tolist()

        # Initialize the first graph as 'RightKnee'
        #current_graph_name = 'RightKnee'
        #current_graph = body_parts[current_graph_name]

        # Calculate the time differences and angular displacements
        time_diff = np.diff(time)

        # Calculate the initial current_graph
        current_graph_name = list(body_parts.keys())[0]
        current_graph = body_parts[current_graph_name]
        angular_displacement = np.diff(current_graph)

        # Calculate the angular velocity
        angular_velocity = angular_displacement / time_diff

        # Create an interpolation function for smoothing the line
        interpolated_func = interp1d(time[1:], angular_velocity, kind='cubic')

        # Create a finer time array for smoother line
        fine_time = np.linspace(time[1], time[-1], num=2000)

        # Interpolate the angular velocity values for the finer time array
        smooth_angular_velocity = interpolated_func(fine_time)

        smooth_angular_velocity = interpolated_func(fine_time)

        max_index = np.argmax(smooth_angular_velocity)
        min_index = np.argmin(smooth_angular_velocity)

        angular_velocity_max = smooth_angular_velocity[max_index]
        #print("angular_velocity_max" + str(angular_velocity_max))
        angular_velocity_min = smooth_angular_velocity[min_index]
        #print("angular_velocity_min" + str(angular_velocity_min))
        data = [current_graph_name, str(angular_velocity_min),str(angular_velocity_max), str(fine_time[min_index]), str(fine_time[max_index])]
        all_data.append(data)
dataframe = pd.DataFrame(all_data, columns=['Gait', 'VelocityMin','VelocityMax','TimeMin','TimeMax'])
print(dataframe.to_string())