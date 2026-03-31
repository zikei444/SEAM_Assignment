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
df = pd.read_csv('dirty_financial_transactions.csv')
df.head(10)
df.info()
df.describe()
df.shape
# %%
### Missing Value
df.isnull().sum()
# %%
### Duplication
# Count duplicate rows
print("Duplicate rows:", df.duplicated().sum())

# View duplicate rows
duplicates = df[df.duplicated()]
print(duplicates.head())

# %%
### Inconsistecy 
# Check unique values for categorical columns
categorical_cols = ['Product_Name', 'Payment_Method', 'Transaction_Status']

for col in categorical_cols:
    print(f"\n{col} unique values:")
    print(df[col].unique())

# %%
# Invalid Transaction_ID (missing or wrong format)
print("Missing Transaction_ID:", df['Transaction_ID'].isnull().sum())

# %%
# Invalid Quantity (should not be <= 0)
print("Invalid Quantity:")
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
print(df[df['Quantity'] <= 0])

# %%
# Invalid Price (should not be <= 0)
print("Invalid Price:")
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
print(df[df['Price'] <= 0])

# %%
# Invalid Date format
# Convert to 
temp_date = pd.to_datetime(df['Transaction_Date'], errors='coerce')

# Invalid = became NaT
invalid_dates = df[temp_date.isnull()]

print("Number of invalid dates:", invalid_dates.shape[0])
print(invalid_dates['Transaction_Date'])
# %%
