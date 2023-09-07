import os
import sys
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d

if len(sys.argv) < 2:
    print("Please provide the folder name where .xlsx files are located")
    sys.exit(1)

# Get the filename from the command-line argument
directory = sys.argv[1]
all_data = []

for f in os.listdir(directory):
    filename = os.path.join(directory, f)
    if os.path.isfile(filename):
        try:
            df = pd.read_excel(filename)
        except:
            continue

        # Check if the filename contains 'angles' or 'positions'
        if 'angles' in f:
            output_csv = "angles.csv"
        elif 'positions' in f:
            output_csv = "positions.csv"
        else:
            output_csv = "others.csv"

        # Extract column names (body parts) excluding 'Time (ms)'
        body_part_columns = [col for col in df.columns if col != 'Time (ms)']

        for current_graph_name in body_part_columns:
            current_graph = df[current_graph_name].tolist()
            try:
                time = df['Time (ms)'].tolist()
            except:
                continue
            time_diff = np.diff(time)
            angular_displacement = np.diff(current_graph)
            angular_velocity = angular_displacement / time_diff

            interpolated_func = interp1d(time[1:], angular_velocity, kind='cubic')
            fine_time = np.linspace(time[1], time[-1], num=2000)
            smooth_angular_velocity = interpolated_func(fine_time)

            max_index = np.argmax(smooth_angular_velocity)
            min_index = np.argmin(smooth_angular_velocity)

            angular_velocity_max = round(smooth_angular_velocity[max_index], 2)
            angular_velocity_min = round(smooth_angular_velocity[min_index], 2)

            data = [current_graph_name, str(angular_velocity_min), str(angular_velocity_max),
                    str(round(fine_time[min_index], 2)), str(round(fine_time[max_index], 2))]

            # Append data to the appropriate CSV file
            with open(output_csv, 'a') as csvfile:
                csvfile.write(','.join(data) + '\n')

# You can also print a message indicating which CSV file was generated
print(f"Data written to {output_csv}")
