# %% [markdown]
## **2.4**

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


df_dirty = pd.read_csv('dirty_financial_transactions.csv')
df = pd.read_csv('cleaned_financial_transactions.csv')

# Add labels on bar charts
def add_bar_labels(ax):
    for p in ax.patches:
        height = p.get_height()
        ax.annotate(f'{int(height)}',
                    (p.get_x() + p.get_width() / 2, height),
                    ha='center', va='bottom', fontsize=10)

# Add labels for histogram bars
def add_hist_labels(ax):
    for p in ax.patches:
        height = p.get_height()
        if height > 0:
            ax.annotate(f'{int(height)}',
                        (p.get_x() + p.get_width() / 2, height),
                        ha='center', va='bottom', fontsize=10)
# Original Columns     
original_cols = ['Transaction_ID','Transaction_Date','Customer_ID','Product_Name',
                 'Quantity','Price','Payment_Method','Transaction_Status']
# %% [markdown]
## **After Re-engineering**

# %% [markdown]
### **Completeness**

# %%
# BEFORE & AFTER
missing_before = df_dirty[original_cols].isnull().sum()
missing_after = df[original_cols].isnull().sum()

print("Missing Value Comparison: ")
for col in original_cols:
    print(f"{col}: Before = {missing_before[col]}, After = {missing_after[col]}")

missing_compare = pd.DataFrame({
    'Before Cleaning': missing_before,
    'After Cleaning': missing_after
})

ax = missing_compare.plot(kind='bar', figsize=(12,6))

add_bar_labels(ax)

plt.title('Missing Values Before vs After Cleaning')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %% [markdown]
### **Consistency**

# %% [markdown]
# **Product Name**

# %%
print("Product Name Unique Values: ")
unique_before = df_dirty['Product_Name'].unique()
unique_after = df['Product_Name'].unique()
unique_before_count = df_dirty['Product_Name'].nunique()
unique_after_count = df['Product_Name'].nunique()
print(f"Unique Product Names: \nBefore = {unique_before}, \nAfter = {unique_after}")
print(f"\nUnique Product Names Count: Before = {unique_before_count}, After = {unique_after_count}")


fig, axes = plt.subplots(1, 2, figsize=(14,5))
ax1 = df_dirty['Product_Name'].value_counts().plot(kind='bar', ax=axes[0])
ax1.set_title('Before Cleaning')
ax1.tick_params(axis='x', rotation=90, labelsize=6)
add_bar_labels(ax1)

ax2 = df['Product_Name'].value_counts().plot(kind='bar', ax=axes[1])
ax2.set_title('After Cleaning')
add_bar_labels(ax2)

plt.suptitle('Product Name Standardization')
plt.tight_layout()
plt.show()
# %% [markdown]
# **Payment Method**

# %%
print("Payment Method Unique Values:")
unique_before = df_dirty['Payment_Method'].unique()
unique_after = df['Payment_Method'].unique()
unique_before_count = df_dirty['Payment_Method'].nunique()
unique_after_count = df['Payment_Method'].nunique()
print(f"Unique Payment Method: \nBefore = {unique_before}, \nAfter = {unique_after}")
print(f"\nUnique Payment Method Count: Before = {unique_before_count}, After = {unique_after_count}")


fig, axes = plt.subplots(1, 2, figsize=(12,5))
ax1 = df_dirty['Payment_Method'].value_counts().plot(kind='bar', ax=axes[0], title='Before Cleaning')
ax2 = df['Payment_Method'].value_counts().plot(kind='bar', ax=axes[1], title='After Cleaning')
add_bar_labels(ax1)
add_bar_labels(ax2)
plt.suptitle('Payment Method Consistency')
plt.tight_layout()
plt.show()

# %% [markdown]
# **Transaction Status**

# %%
print("Transaction Status Unique Values:")
unique_before = df_dirty['Transaction_Status'].unique()
unique_after = df['Transaction_Status'].unique()
unique_before_count = df_dirty['Transaction_Status'].nunique()
unique_after_count = df['Transaction_Status'].nunique()
print(f"Unique Transaction Status: \nBefore = {unique_before}, \nAfter = {unique_after}")
print(f"\nUnique Transaction Status Count: Before = {unique_before_count}, After = {unique_after_count}")

fig, axes = plt.subplots(1, 2, figsize=(12,5))
ax1 = df_dirty['Transaction_Status'].value_counts().plot(kind='bar', ax=axes[0])
ax1.set_title('Before Cleaning')
add_bar_labels(ax1)

ax2 = df['Transaction_Status'].value_counts().plot(kind='bar', ax=axes[1])
ax2.set_title('After Cleaning')
add_bar_labels(ax2)

plt.suptitle('Transaction Status Consistency')
plt.tight_layout()
plt.show()

# %% [markdown]
### **Accuracy**

# %% [markdown]
# **Quantity**

# %%
invalid_qty_before = ((df_dirty['Quantity'] <= 0) | (df_dirty['Quantity'].isnull())).sum()
invalid_qty_after = ((df['Quantity'] <= 0) | (df['Quantity'].isnull())).sum()
print(f"\nQuantity Accuracy:")
print(f"Invalid Quantity: Before = {invalid_qty_before}, After = {invalid_qty_after}")

fig, axes = plt.subplots(1, 2, figsize=(12,5))
ax1 = df_dirty['Quantity'].plot(kind='hist', bins=30, ax=axes[0])
ax1.set_title('Before Cleaning')
add_hist_labels(ax1)

ax2 = df['Quantity'].plot(kind='hist', bins=30, ax=axes[1])
ax2.set_title('After Cleaning')
add_hist_labels(ax2)
plt.suptitle('Quantity Distribution (Invalid Values Removed)')
plt.tight_layout()
plt.show()

# %% [markdown]
# **Price**

# %%
dirty_price = pd.to_numeric(df_dirty['Price'], errors='coerce')
invalid_price_before = (dirty_price <= 0).sum()
invalid_price_after = (df['Price'] <= 0).sum()
print(f" Price Accuracy")
print(f"Invalid Price: Before = {invalid_price_before}, After = {invalid_price_after}")

fig, axes = plt.subplots(1, 2, figsize=(12,5))
ax1 = dirty_price.plot(kind='hist', bins=30, ax=axes[0])
ax1.set_title('Before Cleaning')
add_hist_labels(ax1)

ax2 = df['Price'].plot(kind='hist', bins=30, ax=axes[1])
ax2.set_title('After Cleaning')
add_hist_labels(ax2)
plt.suptitle('Price Distribution (Cleaned)')
plt.tight_layout()
plt.show()

# %% [markdown]
# **Transaction Date**

# %%
invalid_dates_before = pd.to_datetime(df_dirty['Transaction_Date'], errors='coerce').isnull().sum()
invalid_dates_after = df['Transaction_Date'].isnull().sum()
print(f"Transaction Date Accuracy:")
print(f"Invalid Dates: Before = {invalid_dates_before}, After = {invalid_dates_after}")

fig, ax = plt.subplots()
bars = ax.bar(['Before', 'After'], [invalid_dates_before, invalid_dates_after])
add_bar_labels(ax)
plt.title('Invalid Dates Before vs After Cleaning')
plt.ylabel('Count')
plt.show()

# %% [markdown]
## **Duplicate Reocrd**


# %%
# Duplicates
duplicates_before = df_dirty[original_cols].duplicated().sum()
duplicates_after = df[original_cols].duplicated().sum()
print(f"\nDuplicate Rows: Before = {duplicates_before}, After = {duplicates_after}")

# %% [markdown]
## **Derived Column Quality**

# %%
print("Derived Columns Quality: ")
invalid_total = (df['Total_Amount'] <= 0).sum()
invalid_year = ((df['Year'] < 2000) | (df['Year'].isnull())).sum()
invalid_month = ((df['Month'] < 1) | (df['Month'] > 12) | (df['Month'].isnull())).sum()

print(f"Invalid Total_Amount: {invalid_total}")
print(f"Invalid Year: {invalid_year}")
print(f"Invalid Month: {invalid_month}")

# Plot Total_Amount
fig, ax = plt.subplots()
ax.hist(df['Total_Amount'], bins=30)
ax.set_title('Total_Amount Distribution')
ax.set_xlabel('Total_Amount')
ax.set_ylabel('Count')
add_hist_labels(ax)
plt.show()
quality_metrics = pd.DataFrame({
    'Metric': ['Missing Values', 'Invalid Quantity', 'Invalid Price', 'Invalid Dates'],
    'Before': [
        df_dirty.isnull().sum().sum(),
        ((df_dirty['Quantity'] <= 0) | (df_dirty['Quantity'].isnull())).sum(),
        (pd.to_numeric(df_dirty['Price'], errors='coerce') <= 0).sum(),
        pd.to_datetime(df_dirty['Transaction_Date'], errors='coerce').isnull().sum()
    ],
    'After': [
        df.isnull().sum().sum(),
        ((df['Quantity'] <= 0) | (df['Quantity'].isnull())).sum(),
        (df['Price'] <= 0).sum(),
        df['Transaction_Date'].isnull().sum()
    ]
})

# %% [markdown]
## **Overall Quality**

# %%
quality_metrics = pd.DataFrame({
    'Metric': ['Missing Values', 'Invalid Quantity', 'Invalid Price', 'Invalid Dates', 'Duplicate Rows'],
    'Before': [
        df_dirty[original_cols].isnull().sum().sum(),
        ((df_dirty['Quantity'] <= 0) | (df_dirty['Quantity'].isnull())).sum(),
        (pd.to_numeric(df_dirty['Price'], errors='coerce') <= 0).sum(),
        pd.to_datetime(df_dirty['Transaction_Date'], errors='coerce').isnull().sum(),
        df_dirty[original_cols].duplicated().sum()
    ],
    'After': [
        df[original_cols].isnull().sum().sum(),
        ((df['Quantity'] <= 0) | (df['Quantity'].isnull())).sum(),
        (df['Price'] <= 0).sum(),
        df['Transaction_Date'].isnull().sum(),
        df[original_cols].duplicated().sum()
    ]
})

print("Overall Data Quality Metrics")
print(quality_metrics)

ax = quality_metrics.set_index('Metric').plot(kind='bar', figsize=(12,6))
add_bar_labels(ax)
plt.title('Overall Data Quality Improvement')
plt.ylabel('Count')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
# %%
