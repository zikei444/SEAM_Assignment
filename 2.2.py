# %% [markdown]
## **2.2**

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


df = pd.read_csv('dirty_financial_transactions.csv')

# %% [markdown]
## **Completeness Analysis**
# %%
missing = df.isnull().sum()

# Rows with missing value
missing_rows = df[df.isnull().any(axis=1)]
print("\nRows with missing values:")
print(missing_rows.head())

# Chart with count labels
plt.figure(figsize=(8,5))
ax = missing.plot(kind='bar')
plt.title('Missing Values by Column')
plt.ylabel('Count')
plt.xticks(rotation=45)

# Add count labels on top of bars
for i, count in enumerate(missing):
    ax.text(i, count + 0.5, str(count), ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

# %% [markdown]
## **Consistency Analysis**

# %%
# %%
for col in ['Product_Name', 'Payment_Method', 'Transaction_Status']:
    print(f"\n{col} unique values ({df[col].nunique()}):")
    print(df[col].unique())

# Product Name
plt.figure(figsize=(12,4))
ax = df['Product_Name'].value_counts().plot(kind='bar')
plt.title('Product Name Distribution (Inconsistency)')
plt.xticks(rotation=90, fontsize=8)
for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() + p.get_width()/2, p.get_height()),
                ha='center', va='bottom', fontsize=8)
plt.tight_layout()
plt.show()

# Payment Method
plt.figure(figsize=(8,4))
ax = df['Payment_Method'].value_counts().plot(kind='bar')
plt.title('Payment Method Distribution (Inconsistency)')
plt.xticks(rotation=45, fontsize=8)
for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() + p.get_width()/2, p.get_height()),
                ha='center', va='bottom', fontsize=8)
plt.tight_layout()
plt.show()

# Transaction Status
plt.figure(figsize=(8,4))
ax = df['Transaction_Status'].value_counts().plot(kind='bar')
plt.title('Transaction Status Distribution (Inconsistency)')
plt.xticks(rotation=45, fontsize=8)
for p in ax.patches:
    ax.annotate(str(p.get_height()), (p.get_x() + p.get_width()/2, p.get_height()),
                ha='center', va='bottom', fontsize=8)
plt.tight_layout()
plt.show()

# %% [markdown]
## **Accuracy Check**

# %%
# Invalid Quantity
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
invalid_qty_df = df[(df['Quantity'] <= 0) | (df['Quantity'].isnull())]

# Data Records
print("\nInvalid Quantity Records:")
print(invalid_qty_df.head())

# Chart
invalid_qty = invalid_qty_df.shape[0]
valid_qty = df.shape[0] - invalid_qty

plt.figure()
plt.pie([invalid_qty, valid_qty], labels=['Invalid', 'Valid'], autopct=lambda p: f'{int(p*len(df)/100)} ({p:.1f}%)')
plt.title('Quantity Validity')
plt.show()

# Invalid Price
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
invalid_price_df = df[(df['Price'] <= 0) | (df['Price'].isnull())]

# Data Records
print("\nInvalid Price Records:")
print(invalid_price_df.head())

# Chart
invalid_price = invalid_price_df.shape[0]
valid_price = df.shape[0] - invalid_price

plt.figure()
plt.pie([invalid_price, valid_price], labels=['Invalid', 'Valid'], autopct=lambda p: f'{int(p*len(df)/100)} ({p:.1f}%)')
plt.title('Price Validity')
plt.show()

# Invalid Date
temp_date = pd.to_datetime(df['Transaction_Date'], errors='coerce')
invalid_dates_df = df[temp_date.isnull()]

# Data Records
print("\nInvalid Date Records:")
print(invalid_dates_df[['Transaction_Date']].head())

# Chart
invalid_count = invalid_dates_df.shape[0]
valid_dates = df.shape[0] - invalid_count

plt.figure()
plt.pie([invalid_count, valid_dates], labels=['Invalid Dates', 'Valid Dates'], autopct=lambda p: f'{int(p*len(df)/100)} ({p:.1f}%)')
plt.title('Transaction Date Validity')
plt.show()

# %% [markdown]
## **Duplication Record Analysis**

# %%
# Data Records
dup_df = df[df.duplicated()]

print("\nDuplicate Records:")
print(dup_df.head())

dup_count = df.duplicated().sum()
non_dup = len(df) - dup_count

plt.figure()
plt.pie([dup_count, non_dup], labels=['Duplicate', 'Unique'], autopct=lambda p: f'{int(p*len(df)/100)} ({p:.1f}%)')
plt.title('Duplicate Records Distribution')
plt.show()
# %%