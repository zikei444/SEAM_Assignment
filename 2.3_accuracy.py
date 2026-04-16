# %% [markdown]
## **2.3 - Accuracy**

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Load dataset
df = pd.read_csv('dirty_supermarket_sales.csv')

# %% [markdown]
## **Data Cleaning**
# %%
# Remove missing values
df = df.dropna()
# %%
# Remove duplicate records
df = df.drop_duplicates()

# Ensure numeric columns
df['Unit price'] = pd.to_numeric(df['Unit price'], errors='coerce')
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')

df = df.dropna()

# %%
# Recalculate Correct Values**
# %%
# Recalculate Total Amount
df['Total_Amount'] = df['Unit price'] * df['Quantity']
# %%
# Recalculate Tax (5%)
df['Tax 5%'] = df['Total_Amount'] * 0.05
# %%
# Recalculate Sales
df['calculated_sales'] = (df['Total_Amount'] + df['Tax 5%']).round(6)

# %% [markdown]
## **Accuracy Check & Correction**
# %%
# Calculate error
df['error'] = abs(df['Sales'] - df['calculated_sales'])

tolerance = 0.01

df['is_incorrect'] = df['error'] > tolerance

num_incorrect_before = df['is_incorrect'].sum()
print("Incorrect Sales records (before fixing):", num_incorrect_before)

mask = df['is_incorrect']

df.loc[mask, 'Sales'] = df.loc[mask, 'calculated_sales']

df['error'] = abs(df['Sales'] - df['calculated_sales'])
df['is_incorrect'] = df['error'] > tolerance

num_incorrect_after = df['is_incorrect'].sum()

print("Incorrect Sales records (after fixing):", num_incorrect_after)

corrected_samples = df.loc[mask, ['Unit price', 'Quantity', 'Tax 5%', 'Sales', 'calculated_sales']].head(10)

print("\n--- CORRECTED SALES RECORDS (SAMPLE) ---")
print(corrected_samples)
# %%
# Save Cleaned Dataset**

df.to_csv('cleaned_supermarket_sales.csv', index=False)