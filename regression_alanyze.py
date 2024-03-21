import pandas as pd
import statsmodels.api as sm

# Load data from Excel file
file_path = '1.1_positions.xlsx'
df = pd.read_excel(file_path, sheet_name='raw (RAW)')

# Specify independent variables (X) and dependent variable (y)
X = df[['Time (ms)', 'ShoulderLeft x (mm)', 'ShoulderLeft y (mm)', 'ShoulderLeft z (mm)',
        'ElbowLeft x (mm)', 'ElbowLeft y (mm)', 'ElbowLeft z (mm)',
        'ElbowRight x (mm)', 'ElbowRight y (mm)', 'ElbowRight z (mm)',
        'HipLeft x (mm)', 'HipLeft y (mm)', 'HipLeft z (mm)',
        'KneeLeft x (mm)', 'KneeLeft y (mm)', 'KneeLeft z (mm)']]
y = df['Dancer']  # Assuming 'Dancer' is the dependent variable

# Add a constant term to the independent variables for the intercept
X = sm.add_constant(X)

# Fit the regression model
model = sm.OLS(y, X).fit()

# Display the regression results
print(model.summary())
