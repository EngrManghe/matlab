import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress
from scipy.interpolate import interp1d
import argparse

class PositionAnalyzer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_excel(file_path)
        self.time_seconds = self.df['Time (ms)'] / 1000  # Convert milliseconds to seconds

    def plot_smoothed_position_vs_time(self, position_label='X'):
        position_data = self.df[position_label].values

        # Create a cubic spline interpolation
        spline = interp1d(self.time_seconds, position_data, kind='cubic')

        # Generate a finer time grid for a smoother curve
        finer_time_seconds = np.linspace(self.time_seconds.min(), self.time_seconds.max(), num=1000)
        smoothed_position_data = spline(finer_time_seconds)

        slope, intercept, r_value, p_value, std_err = linregress(self.time_seconds, position_data)
        regression_line = slope * self.time_seconds + intercept

        # Create a plot
        plt.plot(self.time_seconds, position_data, 'o', label='Data Points', markersize=4, alpha=0.5)
        plt.plot(finer_time_seconds, smoothed_position_data, '-', label='Smoothed Curve', color='blue', linewidth=2)
        plt.plot(self.time_seconds, regression_line, color='red', label='Regression Line', linestyle='dashed')
        plt.xlabel('Time (s)')
        plt.ylabel(f'Position ({position_label})')
        plt.title(f'Regression Fit: {position_label} Position vs. Time with Smoothed Curve')
        plt.legend()
        plt.grid(True)

        # Show the plot
        plt.show()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot Position and Regression Line')
    parser.add_argument('file_path', type=str, help='Path to the Excel file')
    parser.add_argument('position_label', type=str, help='Position label (e.g., X, Y, Z)')
    #py .\regression_line.py .\1.1_angles_ballet.xlsx LeftShoulder
    args = parser.parse_args()

    file_path = args.file_path
    position_label = args.position_label
    analyzer = PositionAnalyzer(file_path)
    analyzer.plot_smoothed_position_vs_time(position_label)
