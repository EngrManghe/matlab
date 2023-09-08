import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import sys

class AngularVelocityPlotter:
    def __init__(self, file_path):
        self.df = pd.read_excel(file_path)
        self.time = self.df['Time (ms)'].tolist()
        self.body_parts = ['LeftAnkle', 'LeftKnee', 'LeftHip', 'LeftShoulder', 'LeftElbow',
                        'RightAnkle', 'RightKnee', 'RightHip', 'RightShoulder', 'RightElbow']

        self.body_part_names = ['Left Ankle', 'Left Knee', 'Left Hip', 'Left Shoulder', 'Left Elbow',
                                'Right Ankle', 'Right Knee', 'Right Hip', 'Right Shoulder', 'Right Elbow']

        self.selected_line = None
        self.max_min_text = None  # Initialize max_min_text to None

    def calculate_angular_velocity(self, body_part_data):
        time_diff = np.diff(self.time)
        angular_displacement = np.diff(body_part_data)
        return angular_displacement / time_diff

    def plot_smoothed_angular_velocity(self, axs, body_part_name, body_part_data, title):
        angular_velocity = self.calculate_angular_velocity(body_part_data)
        interpolated_func = interp1d(self.time[1:], angular_velocity, kind='cubic')
        fine_time = np.linspace(self.time[1], self.time[-1], num=2000)
        smooth_angular_velocity = interpolated_func(fine_time)

        max_index = np.argmax(smooth_angular_velocity)
        min_index = np.argmin(smooth_angular_velocity)

        line, = axs.plot(fine_time, smooth_angular_velocity, label=body_part_name, picker=5)
        line.set_picker(10)  # Increase the pick radius for easier clicking
        line.figure.canvas.mpl_connect('pick_event', self.on_line_click)  # Connect the pick event to the click handler

        # Add red dots for Maximum and blue dots for Minimum points
        axs.plot(fine_time[max_index], smooth_angular_velocity[max_index], 'ro', label=f'Max ({fine_time[max_index]:.2f} ms, {smooth_angular_velocity[max_index]:.2f} rad/s)')
        axs.plot(fine_time[min_index], smooth_angular_velocity[min_index], 'bo', label=f'Min ({fine_time[min_index]:.2f} ms, {smooth_angular_velocity[min_index]:.2f} rad/s)')

        axs.set_xlabel("Time (ms)")
        axs.set_ylabel("Angular Velocity (rad/s)")
        axs.legend()
        axs.set_title(title)

        return max_index, min_index, smooth_angular_velocity[max_index], smooth_angular_velocity[min_index]

    def plot_left_and_right(self, side):
        fig, axs = plt.subplots(figsize=(10, 8))
        max_indices, min_indices = [], []
        for i, body_part in enumerate(self.body_parts):
            if (side == 'left' and i < len(self.body_parts) // 2) or (side == 'right' and i >= len(self.body_parts) // 2):
                max_idx, min_idx, max_val, min_val = self.plot_smoothed_angular_velocity(axs, self.body_part_names[i], self.df[body_part].tolist(),
                                                    f"Smoothed Angular Velocity Scatter Plot ({side.capitalize()} Joints)")
                max_indices.append((max_idx, max_val))
                min_indices.append((min_idx, min_val))

        plt.show()  # Show the plot
        return max_indices, min_indices

    def on_line_click(self, event):
        if event.mouseevent.button == 1:  # Check if the left mouse button is clicked
            line = event.artist
            if self.selected_line:
                self.selected_line.set_linewidth(1.0)  # Reset the line thickness of the previously selected line
                if self.max_min_text:  # Check if max_min_text is not None before removing it
                    self.max_min_text.remove()  # Remove the previous max and min text
            self.selected_line = line
            line.set_linewidth(3.0)  # Increase line thickness
            line.figure.canvas.draw()

            max_val, min_val = line.get_data()
            max_index = np.argmax(max_val)
            min_index = np.argmin(min_val)

            max_time = self.time[max_index]
            min_time = self.time[min_index]

            max_angular_velocity = max_val[max_index]
            min_angular_velocity = min_val[min_index]

            # Add text for max and min values
            self.max_min_text = line.axes.text(max_time, max_angular_velocity, f'Max ({max_time:.2f} ms, {max_angular_velocity:.2f} rad/s)', color='r')
            line.axes.text(min_time, min_angular_velocity, f'Min ({min_time:.2f} ms, {min_angular_velocity:.2f} rad/s)', color='b')
            line.figure.canvas.draw()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: py script.py filename.xlsx [left|right]")
        sys.exit(1)

    file_path = sys.argv[1]
    side = sys.argv[2].lower()

    if side not in ['left', 'right']:
        print("Invalid side argument. Please use 'left' or 'right'.")
        sys.exit(1)

    plotter = AngularVelocityPlotter(file_path)
    max_indices, min_indices = plotter.plot_left_and_right(side)

    for i, body_part_name in enumerate(plotter.body_part_names):
        if (side == 'left' and i < len(plotter.body_part_names) // 2) or (side == 'right' and i >= len(plotter.body_part_names) // 2):
            print(f'{side.capitalize()} {body_part_name} - Max: {max_indices[i][1]:.2f} ms, {max_indices[i][0]:.2f} rad/s, Min: {min_indices[i][1]:.2f} ms, {min_indices[i][0]:.2f} rad/s')
