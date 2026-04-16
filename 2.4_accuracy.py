# %% [markdown]
## **2.4 - Accuracy**

import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

df_dirty = pd.read_csv('dirty_supermarket_sales.csv')
df_clean = pd.read_csv('cleaned_supermarket_sales.csv')

def accuracy(valid, total):
    return (valid / total) * 100

df_dirty['Unit price'] = pd.to_numeric(df_dirty['Unit price'], errors='coerce')
df_dirty['Quantity'] = pd.to_numeric(df_dirty['Quantity'], errors='coerce')
df_dirty['Tax 5%'] = pd.to_numeric(df_dirty['Tax 5%'], errors='coerce')
df_dirty['Sales'] = pd.to_numeric(df_dirty['Sales'], errors='coerce')

expected_before = (df_dirty['Unit price'] * df_dirty['Quantity']) + df_dirty['Tax 5%']
error_before = abs(df_dirty['Sales'] - expected_before)

invalid_before = (error_before > 0.01).sum()
valid_before = len(df_dirty) - invalid_before
accuracy_before = accuracy(valid_before, len(df_dirty))

df_clean['Unit price'] = pd.to_numeric(df_clean['Unit price'], errors='coerce')
df_clean['Quantity'] = pd.to_numeric(df_clean['Quantity'], errors='coerce')
df_clean['Tax 5%'] = pd.to_numeric(df_clean['Tax 5%'], errors='coerce')
df_clean['Sales'] = pd.to_numeric(df_clean['Sales'], errors='coerce')

expected_after = (df_clean['Unit price'] * df_clean['Quantity']) + df_clean['Tax 5%']
error_after = abs(df_clean['Sales'] - expected_after)

invalid_after = (error_after > 0.01).sum()
valid_after = len(df_clean) - invalid_after
accuracy_after = accuracy(valid_after, len(df_clean))

accuracy_increase = accuracy_after - accuracy_before

df_dirty['expected_sales'] = expected_before
df_dirty['is_correct'] = abs(df_dirty['Sales'] - df_dirty['expected_sales']) <= 0.01

# Keep only rows that still exist in cleaned dataset
valid_indices = df_dirty.index.intersection(df_clean.index)

df_dirty_valid = df_dirty.loc[valid_indices]
df_clean_valid = df_clean.loc[valid_indices]

# Get indices
correct_idx = df_dirty_valid[df_dirty_valid['is_correct']].index[:5]
incorrect_idx = df_dirty_valid[~df_dirty_valid['is_correct']].index[:5]

# Get cleaned records and include calculated_sales
cols = ['Unit price', 'Quantity', 'Tax 5%', 'Sales', 'calculated_sales']

correct_samples = df_clean_valid.loc[correct_idx][cols]
incorrect_samples = df_clean_valid.loc[incorrect_idx][cols]

print("\n--- 5 SAMPLE RECORDS ---")
print(incorrect_samples)
# %%
