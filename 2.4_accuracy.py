# %% [markdown]
## **2.4 - Accuracy**

import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

df_dirty = pd.read_csv('dirty_supermarket_sales.csv')
df_clean = pd.read_csv('cleaned_supermarket_sales.csv')

# Convert to numeric for both datasets
df_dirty['Unit price'] = pd.to_numeric(df_dirty['Unit price'], errors='coerce')
df_dirty['Quantity'] = pd.to_numeric(df_dirty['Quantity'], errors='coerce')
df_dirty['Tax 5%'] = pd.to_numeric(df_dirty['Tax 5%'], errors='coerce')
df_dirty['Sales'] = pd.to_numeric(df_dirty['Sales'], errors='coerce')

df_clean['Unit price'] = pd.to_numeric(df_clean['Unit price'], errors='coerce')
df_clean['Quantity'] = pd.to_numeric(df_clean['Quantity'], errors='coerce')
df_clean['Tax 5%'] = pd.to_numeric(df_clean['Tax 5%'], errors='coerce')
df_clean['Sales'] = pd.to_numeric(df_clean['Sales'], errors='coerce')

# Calculate expected sales and identify incorrect records in cleaned dataset
df_clean['calculated_sales'] = (df_clean['Unit price'] * df_clean['Quantity']) + df_clean['Tax 5%']
df_clean['is_correct'] = abs(df_clean['Sales'] - df_clean['calculated_sales']) <= 0.01

# Find incorrect records in cleaned dataset
incorrect_in_clean = df_clean[~df_clean['is_correct']]

# Display only 5 sample incorrect records with specified columns
print("--- 5 SAMPLE INCORRECT RECORDS ---")
print(incorrect_in_clean[['Unit price', 'Quantity', 'Tax 5%', 'Sales', 'calculated_sales']].head(5))