import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Load the CSV file
df = pd.read_csv('messy_data.csv')
st.write("CSV Data  ", df)
# Strip column names
df.columns = df.columns.str.strip()

# Standardize missing values
df.replace({'Missing': pd.NA, '': pd.NA}, inplace=True)

# Convert data types automatically
df = df.convert_dtypes()

# Fill missing 'Name' values
df['Name'] = df['Name'].fillna('NoName')

# Convert numeric columns
df[['Age', 'Salary', 'Score']] = df[['Age', 'Salary', 'Score']].apply(pd.to_numeric, errors='coerce')

# Convert 'Joining Date' using Pandas datetime handling
df['Joining Date'] = pd.to_datetime(df['Joining Date'], errors='coerce').dt.strftime('%Y-%m-%d')

# Fill missing values
df['Age'] = df['Age'].fillna(df['Age'].median())
df['Department'] = df['Department'].fillna(df['Department'].mode()[0])
df['Salary'] = df.groupby('Department')['Salary'].transform(lambda x: x.fillna(x.median()))
df['Score'] = df['Score'].fillna(df['Score'].mean())

# Downcast numeric columns explicitly
df['Age'] = pd.to_numeric(df['Age'], downcast='integer')
df['Score'] = pd.to_numeric(df['Score'], downcast='float')

# Drop rows where 'Age' or 'Salary' is still missing
df.dropna(subset=['Age', 'Salary'], inplace=True)

# Reset index
df.reset_index(drop=True, inplace=True)

# Save cleaned data
df.to_csv('cleaned_data.csv', index=False)

print(df)
st.write("Clean Data ")

st.write("Data  ", df)
