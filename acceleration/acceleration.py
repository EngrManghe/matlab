import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

class DataAnalyzer:
    def __init__(self, excel_file):
        self.excel_file = excel_file
        self.df = pd.read_excel(excel_file)
        self.time_ms = self.df["Time (ms)"]
        self.output_folder = None
        self.points_info = []
        self.points_info_for_excel = []

    def analyze_data_create_graphs(self):
        # Create a folder with current date and time
        current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.output_folder = f"output_{current_time}"
        os.makedirs(self.output_folder, exist_ok=True)

        # Extracting data from DataFrame
        column_index = 1
        while column_index < len(self.df.columns):
            acceleration_column_name = self.df.columns[column_index]
            acceleration = self.df[acceleration_column_name]

            # Plotting
            plt.plot(self.time_ms, acceleration, marker='o', linestyle='-')
            plt.title('Acceleration vs Time')
            plt.xlabel('Time (ms)')
            plt.ylabel(acceleration_column_name)
            plt.grid(True)

            # Mark maximum and minimum points
            max_index = acceleration.idxmax()
            min_index = acceleration.idxmin()
            max_value = acceleration[max_index]
            min_value = acceleration[min_index]
            max_time = self.time_ms[max_index]
            min_time = self.time_ms[min_index]

            # Save the maximum and minimum points information
            self.points_info.append((acceleration_column_name, min_time, max_time, min_value, max_value))
            self.points_info_for_excel.append((acceleration_column_name, min_time/1000, max_time/1000, min_value/1000, max_value/1000))

            # Plot red dots for maximum and minimum points
            plt.plot(max_time, max_value, 'ro')  # Red dot for maximum
            plt.plot(min_time, min_value, 'ro')  # Red dot for minimum

            # Create a separate block for information
            info_text = f"Max: {max_value/1000:.4f} m/s² / {max_time} ms\nMin: {min_value/1000:.4f} m/s² / {min_time} ms"
            plt.text(0.95, 0.95, info_text, transform=plt.gca().transAxes, ha='right', va='top', bbox=dict(facecolor='white', alpha=0.5))

            # Save the graph into the created folder
            plt.savefig(os.path.join(self.output_folder, f'{acceleration_column_name}_graph.png'))

            # Close the plot to clear the current figure for the next iteration
            plt.close()

            # Increment column index for the next iteration
            column_index += 1

    def save_points_info_to_excel(self):
        # Create a DataFrame for maximum and minimum points information
        df = pd.DataFrame(self.points_info_for_excel, columns=['Column Name', 'Time of Min', 'Time of Max', 'Acceleration of Min (m/sec2)', 'Acceleration of Max (m/sec2)'])

        # Save maximum and minimum points information to an Excel file
        excel_file = os.path.join(self.output_folder, '_points_info.xlsx')
        with pd.ExcelWriter(excel_file) as writer:
            df.to_excel(writer, sheet_name='Max_and_Minimum', index=False)

        print(f"Maximum and minimum points information saved to '{excel_file}'")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Please provide the filename of the .xlsx file as a command-line argument.")
        sys.exit(1)

    excel_file = sys.argv[1]
    analyzer = DataAnalyzer(excel_file)
    analyzer.analyze_data_create_graphs()
    analyzer.save_points_info_to_excel()