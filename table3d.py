import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata

# Load data from the Excel file
data = pd.read_excel('rawdata.xlsx')

# Extract relevant columns
time = data['Time (ms)']
LeftHip = data['LeftHip']
LeftKnee = data['LeftKnee']
LeftAnkle = data['LeftAnkle']

# Convert radians to millimeters (you may need to adjust the conversion factor based on your specific scenario)
conversion_factor = 10  # Example conversion factor
left_hip_mm = LeftHip * conversion_factor
left_knee_mm = LeftKnee * conversion_factor
left_ankle_mm = LeftAnkle * conversion_factor
#color of joints
#ok but this is my comment
#this is my comment again - Fidel

# Define the grid
grid_resolution = 50  # Increase the resolution for smoother surface
X_fine = np.linspace(left_hip_mm.min(), left_hip_mm.max(), grid_resolution)
Y_fine = np.linspace(left_knee_mm.min(), left_knee_mm.max(), grid_resolution)
X_fine, Y_fine = np.meshgrid(X_fine, Y_fine)

# Interpolate the Z values onto the grid
points = np.column_stack((left_hip_mm, left_knee_mm))
values = left_ankle_mm
Z_fine = griddata(points, values, (X_fine, Y_fine), method='linear')

# Create a 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Plot the surface
surf = ax.plot_surface(X_fine, Y_fine, Z_fine, cmap='viridis', vmin=left_ankle_mm.min(), vmax=left_ankle_mm.max(), rstride=1, cstride=1)

# Set labels and title
ax.set_xlabel('LeftHip (mm)')
ax.set_ylabel('LeftKnee (mm)')
ax.set_zlabel('LeftAnkle (mm)')
ax.set_title('Body Parts Visualization')

# Add a colorbar
fig.colorbar(surf)

# Display the plot
plt.show()
