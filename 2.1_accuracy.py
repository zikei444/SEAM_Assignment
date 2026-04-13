# %% [markdown]
## **2.1**

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# %%
df = pd.read_csv('dirty_supermarket_sales.csv')
df.head(10)

# %%
df.info()

# %%
df.describe()

# %%
df.shape

# Missing Values
# %%
print("Missing Values:")
print(df.isnull().sum())

# Duplication
# %%
print("Duplicate rows:", df.duplicated().sum())

duplicates = df[df.duplicated()]
print(duplicates.head())

# Inconsistency
# %%
categorical_cols = ['Branch', 'City', 'Customer type', 'Gender',
                    'Product line', 'Payment']

for col in categorical_cols:
    print(f"\n{col} unique values:")
    print(df[col].unique())

# Invalid Invoice ID
# %%
print("Missing Invoice ID:", df['Invoice ID'].isnull().sum())

# Invalid Quantity
# %%
print("Invalid Quantity:")

df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
print(df[df['Quantity'] <= 0])

# Invalid Unit Price
# %%
print("Invalid Unit Price:")

df['Unit price'] = pd.to_numeric(df['Unit price'], errors='coerce')
print(df[df['Unit price'] <= 0])

# Invalid Date Format
# %%
temp_date = pd.to_datetime(df['Date'], errors='coerce')

invalid_dates = df[temp_date.isnull()]

print("Number of invalid dates:", invalid_dates.shape[0])
print(invalid_dates['Date'])