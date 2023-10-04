import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.interpolate import interp1d
import argparse

class AngularVelocityAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_excel(file_path)
        self.time_seconds = self.df['Time (ms)'] / 1000  # Convert milliseconds to seconds

    def calculate_velocity(self, body_part='LeftShoulder'):
        angular_displacement = np.diff(self.df[body_part])
        angular_displacement = np.insert(angular_displacement, 0, 0)
        velocity_rad_per_s = angular_displacement / self.time_seconds

        return self.time_seconds, velocity_rad_per_s

    def plot_smoothed_velocity_vs_time(self, body_part='LeftShoulder'):
        time_seconds, velocity_rad_per_s = self.calculate_velocity(body_part)

        # Create a cubic spline interpolation
        spline = interp1d(time_seconds, velocity_rad_per_s, kind='cubic')

        # Generate a finer time grid for a smoother curve
        finer_time_seconds = np.linspace(time_seconds.min(), time_seconds.max(), num=1000)
        smoothed_velocity_rad_per_s = spline(finer_time_seconds)

        slope, intercept, r_value, p_value, std_err = linregress(time_seconds, velocity_rad_per_s)
        regression_line = slope * time_seconds + intercept

        # Create a plot
        plt.plot(time_seconds, velocity_rad_per_s, 'o', label='Data Points', markersize=4, alpha=0.5)
        plt.plot(finer_time_seconds, smoothed_velocity_rad_per_s, '-', label='Smoothed Curve', color='blue', linewidth=2)
        plt.plot(time_seconds, regression_line, color='red', label='Regression Line', linestyle='dashed')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity (rad/s)')
        plt.title(f'Regression Fit: {body_part} Velocity vs. Time with Smoothed Curve')
        plt.legend()
        plt.grid(True)

        # Show the plot
        plt.show()

        # Calculate the velocity in m/s (convert from rad/s to m/s)
        velocity_m_per_s = velocity_rad_per_s * 0.149  # Replace with the appropriate conversion factor

        # Display the calculated velocity
        print(f"Calculated velocity: {velocity_m_per_s.mean():.2f} m/s")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot Angular Velocity and Regression Line')
    parser.add_argument('file_path', type=str, help='Path to the Excel file')
    parser.add_argument('body_part', type=str, help='Body part (e.g., LeftShoulder, RightShoulder)')
    args = parser.parse_args()

    file_path = args.file_path
    body_part = args.body_part
    analyzer = AngularVelocityAnalyzer(file_path)
    analyzer.plot_smoothed_velocity_vs_time(body_part)
