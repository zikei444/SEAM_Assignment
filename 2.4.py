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

df.head(10)
# %%
df.info()
# %%
df.describe()
# %%
df.shape

# %%
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
    'Before Data Re-engineering': missing_before,
    'After Data Re-engineering': missing_after
})

ax = missing_compare.plot(kind='bar', figsize=(12,6))

add_bar_labels(ax)

plt.title('Missing Values Before vs After Data Re-engineering')
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
ax1.set_title('Before Data Re-engineering')
ax1.tick_params(axis='x', rotation=90, labelsize=6)
add_bar_labels(ax1)

ax2 = df['Product_Name'].value_counts().plot(kind='bar', ax=axes[1])
ax2.set_title('After Data Re-engineering')
add_bar_labels(ax2)

plt.suptitle('Product Name Consistency')
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
ax1 = df_dirty['Payment_Method'].value_counts().plot(kind='bar', ax=axes[0], title='Before Data Re-engineering')
ax2 = df['Payment_Method'].value_counts().plot(kind='bar', ax=axes[1], title='After Data Re-engineering')
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
ax1.set_title('Before Data Re-engineering')
add_bar_labels(ax1)

ax2 = df['Transaction_Status'].value_counts().plot(kind='bar', ax=axes[1])
ax2.set_title('After Data Re-engineering')
add_bar_labels(ax2)

plt.suptitle('Transaction Status Consistency')
plt.tight_layout()
plt.show()

# %% [markdown]
### **Correctness**
# %% [markdown]
# **Quantity**

# %%
print("\n QUANTITY CORRECTNESS COMPARISON")

# BEFORE
df_dirty['quantity_num'] = pd.to_numeric(df_dirty['Quantity'], errors='coerce')
nulls_qty_before = df_dirty['Quantity'].isnull().sum()
negative_qty_before = (df_dirty['quantity_num'] < 0).sum()
valid_qty_before = len(df_dirty) - (nulls_qty_before + negative_qty_before)
invalid_qty_before = nulls_qty_before + negative_qty_before
correctness_qty_before = (valid_qty_before / len(df_dirty)) * 100

# AFTER
df['quantity_num'] = pd.to_numeric(df['Quantity'], errors='coerce')
nulls_qty_after = df['Quantity'].isnull().sum()
negative_qty_after = (df['quantity_num'] < 0).sum()
invalid_qty_after = nulls_qty_after + negative_qty_after
valid_qty_after = len(df) - (nulls_qty_after + negative_qty_after)
correctness_qty_after = (valid_qty_after / len(df)) * 100
improvement_quantity = correctness_qty_after - correctness_qty_before

print(f"\nBEFORE:")
print(f"Invalid values: {invalid_qty_before}")
print(f"Valid values: {valid_qty_before}")
print(f"Correctness: {correctness_qty_before:.2f}%")

print(f"\nAFTER:")
print(f"Invalid values: {invalid_qty_after}")
print(f"Valid values: {valid_qty_after}")
print(f"Correctness: {correctness_qty_after:.2f}%")
print(f"\nIMPROVEMENT:")
print(f"Increase in Correctness: {improvement_quantity:.2f}%")

# Visualize - Before vs After
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Before
issues = ['Valid', 'Invalid']
counts_before = [valid_qty_before, invalid_qty_before]
bars1 = axes[0].bar(issues, counts_before)
axes[0].set_title('BEFORE Data Re-engineering')
axes[0].set_ylabel('Count')
for bar, count in zip(bars1, counts_before):
    if count > 0:
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
                     str(count), ha='center', fontsize=10)

# After
counts_after = [valid_qty_after, invalid_qty_after]
bars2 = axes[1].bar(issues, counts_after)
axes[1].set_title('AFTER Data Re-engineering')
axes[1].set_ylabel('Count')
for bar, count in zip(bars2, counts_after):
    if count > 0:
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
                     str(count), ha='center', fontsize=10)

plt.suptitle('Quantity Correctness Comparison', fontsize=14)
plt.tight_layout()
plt.show()
# %% [markdown]
# **Price**

# %%
print("PRICE CORRECTNESS COMPARISON")

# BEFORE
df_dirty['price_cleaned'] = df_dirty['Price'].astype(str).str.replace('$', '').str.replace(',', '')
df_dirty['price_num'] = pd.to_numeric(df_dirty['price_cleaned'], errors='coerce')

nulls_price_before = df_dirty['Price'].isnull().sum()
negative_price_before = (df_dirty['price_num'] < 0).sum()
invalid_price_before = nulls_price_before + negative_price_before
valid_price_before = len(df_dirty) - invalid_price_before
correctness_price_before = (valid_price_before / len(df_dirty)) * 100

# AFTER
df['price_cleaned'] = df['Price'].astype(str).str.replace('$', '').str.replace(',', '')
df['price_num'] = pd.to_numeric(df['price_cleaned'], errors='coerce')

nulls_price_after = df['Price'].isnull().sum()
negative_price_after = (df['price_num'] < 0).sum()
invalid_price_after = nulls_price_after + negative_price_after
valid_price_after = len(df) - invalid_price_after
correctness_price_after = (valid_price_after / len(df)) * 100
improvement_price = correctness_price_after - correctness_price_before

print(f"\nBEFORE:")
print(f"Invalid values: {invalid_price_before}")
print(f"Correctness: {correctness_price_before:.2f}%")

print(f"\nAFTER:")
print(f"Invalid values: {invalid_price_after}") 
print(f"Correctness: {correctness_price_after:.2f}%")

print(f"\nIMPROVEMENT:")
print(f"Increase in Correctness: {improvement_price:.2f}%")

# Visualize
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Before
issues = ['Valid', 'Invalid']
counts_before = [valid_price_before, invalid_price_before]
bars1 = axes[0].bar(issues, counts_before)
axes[0].set_title('BEFORE Data Re-engineering')
axes[0].set_ylabel('Count')
for bar, count in zip(bars1, counts_before):
    if count > 0:
        axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
                     str(count), ha='center', fontsize=10)

# After
counts_after = [valid_price_after, invalid_price_after]
bars2 = axes[1].bar(issues, counts_after)
axes[1].set_title('AFTER Data Re-engineering')
axes[1].set_ylabel('Count')
for bar, count in zip(bars2, counts_after):
    if count > 0:
        axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
                     str(count), ha='center', fontsize=10)

plt.suptitle('Price Correctness Comparison', fontsize=14)
plt.tight_layout()
plt.show()
# %% [markdown]
# **Transaction_Date**

# %%
print("TRANSACTION DATE CORRECTNESS COMPARISON")

# BEFORE
df_dirty['date_parsed'] = pd.to_datetime(df_dirty['Transaction_Date'], errors='coerce')
current_date = pd.Timestamp.now()

invalid_dates_before = df_dirty['date_parsed'].isna().sum()
future_dates_before = (df_dirty['date_parsed'] > current_date).sum()
valid_dates_before = len(df_dirty) - (invalid_dates_before + future_dates_before)
correctness_date_before = (valid_dates_before / len(df_dirty)) * 100

# AFTER
df['date_parsed'] = pd.to_datetime(df['Transaction_Date'], errors='coerce')

invalid_dates_after = df['date_parsed'].isna().sum()
future_dates_after = (df['date_parsed'] > current_date).sum()
valid_dates_after = len(df) - (invalid_dates_after + future_dates_after)
correctness_date_after = (valid_dates_after / len(df)) * 100
improvement_date = correctness_date_after - correctness_date_before


print(f"\nBEFORE:")
print(f"Invalid date formats: {invalid_dates_before}")
print(f"Future dates: {future_dates_before}")
print(f"Correctness: {correctness_date_before:.2f}%")

print(f"\nAFTER:")
print(f"Invalid date formats: {invalid_dates_after}")
print(f"Future dates: {future_dates_after}")
print(f"Correctness: {correctness_date_after:.2f}%")

print(f"\nIMPROVEMENT:")
print(f"Increase in Correctness: {improvement_date:.2f}%")


# VISUALIZATION
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# BEFORE
axes[0].bar(
    ['Valid', 'Invalid/Future'],
    [valid_dates_before, invalid_dates_before + future_dates_before]
)

axes[0].set_title('BEFORE Data Re-engineering')

before_counts = [valid_dates_before, invalid_dates_before + future_dates_before]
before_pcts = [correctness_date_before, 100 - correctness_date_before]

for i, (count, pct) in enumerate(zip(before_counts, before_pcts)):
    axes[0].text(i, count, str(count), ha='center')
    axes[0].text(i, count + max(before_counts)*0.02, f"{pct:.2f}%", ha='center')

# AFTER
axes[1].bar(
    ['Valid', 'Invalid/Future'],
    [valid_dates_after, invalid_dates_after + future_dates_after]
)

axes[1].set_title('AFTER Data Re-engineering')

after_counts = [valid_dates_after, invalid_dates_after + future_dates_after]
after_pcts = [correctness_date_after, 100 - correctness_date_after]

for i, (count, pct) in enumerate(zip(after_counts, after_pcts)):
    axes[1].text(i, count, str(count), ha='center')
    axes[1].text(i, count + max(after_counts)*0.02, f"{pct:.2f}%", ha='center')

plt.suptitle('Transaction Date Correctness Comparison', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.show()
# %% [markdown]
## **Duplicate Reocrd**


# %%
# Duplicates
duplicates_before = df_dirty[original_cols].duplicated().sum()
duplicates_after = df[original_cols].duplicated().sum()
print(f"\nDuplicate Rows: Before = {duplicates_before}, After = {duplicates_after}")

# Visualize - Duplicates Before vs After
fig, ax = plt.subplots(figsize=(6, 5))
issues = ['Before Re-engineering', 'After Re-engineering']
counts = [duplicates_before, duplicates_after]
bars = ax.bar(issues, counts)

# add labels
for bar, count in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
            str(count), ha='center', fontsize=10)

plt.title('Duplicate Records Before vs After Re-engineering')
plt.ylabel('Count')
plt.tight_layout()
plt.show()

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
