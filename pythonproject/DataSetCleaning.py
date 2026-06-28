#Data Cleaning & Transformation

import pandas as pd
import numpy as np

# 1. Load the dataset (replace with your Kaggle csv file path)
# Let's assume the file is named 'kaggle_sales_data.csv'
df = pd.read_csv('kaggle_sales_data.csv')

print("--- Raw Data Info ---")
print(df.info())

# 2. Clean Missing Values
# Fill missing categories with 'Unknown' and drop rows missing critical sales data
df['Product_Category'] = df['Product_Category'].fillna('Unknown')
df = df.dropna(subset=['Sales', 'Order_Date'])

# 3. Transform Data Types
# Convert Order_Date from string to datetime
df['Order_Date'] = pd.to_datetime(df['Order_Date'])

# 4. Feature Engineering (Transformation)
# Extract Year-Month for time-series analysis
df['Year_Month'] = df['Order_Date'].dt.to_period('M').astype(str)

# Calculate Average Price per item
df['Price_Per_Item'] = np.where(df['Quantity'] > 0, df['Sales'] / df['Quantity'], 0)

# 5. Save the cleaned data for the dashboard
df.to_csv('cleaned_sales_data.csv', index=False)
print("\n--- Data Cleaning Complete! Saved as 'cleaned_sales_data.csv' ---")