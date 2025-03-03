import pandas as pd
import numpy as np
from datetime import datetime

# Load the CSV file
df = pd.read_csv('messy_data.csv')

# Replace 'Missing' and empty strings with NaN
df.replace({'Missing': np.nan, '': np.nan}, inplace=True)

# Fill blank values in the 'Name' column with 'NoName'
df['Name'].fillna('NoName', inplace=True)

# Convert 'Age' to numeric, coercing errors to NaN
df['Age'] = pd.to_numeric(df['Age'], errors='coerce')

# Convert 'Salary' to numeric, coercing errors to NaN
df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')

# Convert 'Score' to numeric, coercing errors to NaN
df['Score'] = pd.to_numeric(df['Score'], errors='coerce')

# Function to parse different date formats
def parse_date(date_str):
    if pd.isna(date_str):
        return np.nan
    for fmt in ('%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%B %d, %Y'):
        try:
            return datetime.strptime(date_str, fmt).strftime('%Y-%m-%d')
        except ValueError:
            continue
    return np.nan

# Apply the date parsing function to 'Joining Date'
df['Joining Date'] = df['Joining Date'].apply(parse_date)

# Fill missing 'Age' with the median
df['Age'].fillna(df['Age'].median(), inplace=True)

# Fill missing 'Department' with the mode
df['Department'].fillna(df['Department'].mode()[0], inplace=True)

# Fill missing 'Salary' based on the median salary of each department
df['Salary'] = df.groupby('Department')['Salary'].transform(lambda x: x.fillna(x.median()))

# Fill missing 'Score' with the mean
df['Score'].fillna(df['Score'].mean(), inplace=True)

# Drop rows where 'Age' or 'Salary' is still missing (if any)
df.dropna(subset=['Age', 'Salary'], inplace=True)

# Reset the index after dropping rows
df.reset_index(drop=True, inplace=True)

# Save the cleaned data to a new CSV file
df.to_csv('cleaned_data.csv', index=False)

print(df)
