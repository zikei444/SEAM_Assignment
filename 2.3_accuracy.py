# %% [markdown]
## **2.3 - Accuracy**

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('dirty_supermarket_sales.csv')

# %% [markdown]
## **Data Cleaning**

# %%
# Remove missing values
df = df.dropna()

# %%
# Remove duplicates data
df = df.drop_duplicates()

# Ensure numeric columns
df['Unit price'] = pd.to_numeric(df['Unit price'], errors='coerce')
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

# %%
# calculate Total_Amount, Tax 5% and calculated_sales
df['Total_Amount'] = df['Unit price'] * df['Quantity']
df['Tax 5%'] = df['Total_Amount'] * 0.05
# %%
# Recalculate Sales based on Total_Amount and Tax 5%
# %%
# Saved in a new column 'calculated_sales' to compare with original 'Sales'
df['calculated_sales'] = df['Total_Amount'] + df['Tax 5%']
# %%
# Sorting and Index Reset
df = df.sort_values(by='Date').reset_index(drop=True)

# Error calculation
df['error'] = abs(df['Sales'] - df['calculated_sales'])

tolerance = 0.01

df['is_incorrect'] = df['error'] > tolerance

# Get 10 incorrect samples
incorrect_samples = df[df['is_incorrect']].head(10)

# Columns to display
cols = ['Unit price', 'Quantity', 'Tax 5%', 'Sales', 'calculated_sales']

print("\n--- 10 INCORRECT SALES RECORDS ---")
print(incorrect_samples[cols])

rows_after = df.shape[0]
missing_after = df.isnull().sum().sum()

# %% [markdown]
# **Save Cleaned**
df.to_csv('cleaned_supermarket_sales.csv', index=False)