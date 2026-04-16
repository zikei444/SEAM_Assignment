# %% [markdown]
## **2.4 - Accuracy**

import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Load datasets
df_dirty = pd.read_csv('dirty_supermarket_sales.csv')
df_clean = pd.read_csv('cleaned_supermarket_sales.csv')

df_dirty['Unit price'] = pd.to_numeric(df_dirty['Unit price'], errors='coerce')
df_dirty['Quantity'] = pd.to_numeric(df_dirty['Quantity'], errors='coerce')
df_dirty['Tax 5%'] = pd.to_numeric(df_dirty['Tax 5%'], errors='coerce')
df_dirty['Sales'] = pd.to_numeric(df_dirty['Sales'], errors='coerce')

df_clean['Unit price'] = pd.to_numeric(df_clean['Unit price'], errors='coerce')
df_clean['Quantity'] = pd.to_numeric(df_clean['Quantity'], errors='coerce')
df_clean['Tax 5%'] = pd.to_numeric(df_clean['Tax 5%'], errors='coerce')
df_clean['Sales'] = pd.to_numeric(df_clean['Sales'], errors='coerce')

df_clean['calculated_sales'] = (df_clean['Unit price'] * df_clean['Quantity']) + df_clean['Tax 5%']

# Round to avoid floating point issues
df_clean['calculated_sales'] = df_clean['calculated_sales'].round(6)

# Define tolerance
tolerance = 0.01

# Check correctness
df_clean['is_correct'] = abs(df_clean['Sales'] - df_clean['calculated_sales']) <= tolerance

# %% 
# Show sample of corrected records
corrected_samples = df_clean[df_clean['is_correct']].head(10)

cols = ['Unit price', 'Quantity', 'Tax 5%', 'Sales', 'calculated_sales']

print("\n--- 10 CORRECTED SALES RECORDS ---")
print(corrected_samples[cols])