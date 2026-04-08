# %% [markdown]
## **2.2**

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
from datetime import datetime
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

# =================
### **1. Transaction_ID Accuracy**
print("\n1. TRANSACTION ID ACCURACY")

# T followed by any digits
expected_pattern = r'^T\d+$' 
df['txn_valid_format'] = df['Transaction_ID'].astype(str).str.match(expected_pattern, na=False)

format_violations = (~df['txn_valid_format']).sum()
duplicates = df['Transaction_ID'].duplicated().sum()
nulls = df['Transaction_ID'].isnull().sum()

print(f"Total records: {len(df)}")
print(f"Format violations: {format_violations}")
print(f"Duplicate IDs: {duplicates}")
print(f"Null values: {nulls}")

valid_count = len(df) - (format_violations + duplicates + nulls)
accuracy_txn = (valid_count / len(df)) * 100
print(f"\n Accuracy: {accuracy_txn:.2f}%")

display_columns = ['Transaction_ID', 'Transaction_Date', 'Customer_ID', 
                   'Product_Name', 'Quantity', 'Price', 'Payment_Method', 
                   'Transaction_Status']

txn_violations = df[~df['txn_valid_format'] | 
                    df['Transaction_ID'].duplicated() | 
                    df['Transaction_ID'].isnull()]

print(f"\n 5 Example Records with Transaction_ID Violations:")
print(txn_violations[display_columns].head(5).to_string(index=True))

# Visualize
fig, ax = plt.subplots(figsize=(10, 6))

categories = ['Valid Format', 'Format\nViolations', 'Duplicated', 'Null/Missing']
counts = [valid_count, format_violations, duplicates, nulls]
colors = ['green', 'red', 'orange', 'gray']

bars = ax.bar(categories, counts, color=colors)
ax.set_title('Transaction ID Accuracy')
ax.set_ylabel('Count', fontsize=12)

for bar, count in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, 
            str(count), ha='center', va='bottom')

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.show()

### **2. Transaction_Date Accuracy**

print("\n2. TRANSACTION DATE ACCURACY")

df['date_parsed'] = pd.to_datetime(df['Transaction_Date'], errors='coerce')
current_date = pd.Timestamp.now()

invalid_dates = df['date_parsed'].isna().sum()
future_dates = (df['date_parsed'] > current_date).sum()

print(f"Invalid date formats: {invalid_dates}")
print(f"Future dates: {future_dates}")

valid_dates = len(df) - (invalid_dates + future_dates)
accuracy_date = (valid_dates / len(df)) * 100
print(f"\n Accuracy: {accuracy_date:.2f}%")

print("\n 5 Example Records with Transaction_Date Violations:")
date_violations = df[(df['date_parsed'].isna()) | (df['date_parsed'] > current_date)]
if len(date_violations) > 0:
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(date_violations[display_columns].head(5).to_string(index=True))
else:
    print("No date violations found")

# Visualize
fig, ax = plt.subplots(figsize=(6,4))
ax.bar(['Valid', 'Invalid/Future'], [valid_dates, invalid_dates+future_dates], 
       color=['green','red'])
ax.set_title('Transaction Date Accuracy')
for i, v in enumerate([valid_dates, invalid_dates+future_dates]):
    ax.text(i, v+5, str(v), ha='center')
plt.show()

### **3. Customer_ID Accuracy**

print("\n3. CUSTOMER ID ACCURACY")

# C followed by digits
expected_customer_pattern = r'^C\d+$'
df['cust_valid_format'] = df['Customer_ID'].astype(str).str.match(expected_customer_pattern, na=False)

null_cust = df['Customer_ID'].isnull().sum()
format_invalid_cust = (~df['cust_valid_format']).sum()
unique_customers = df['Customer_ID'].nunique()

print(f"Null values: {null_cust}")
print(f"Format violations (not C + digits): {format_invalid_cust}")
print(f"Unique customers: {unique_customers}")

valid_cust = len(df) - (null_cust + format_invalid_cust)
accuracy_cust = (valid_cust / len(df)) * 100
print(f"\n Accuracy: {accuracy_cust:.2f}%")

print("\n📋 5 Example Records with Customer_ID Violations:")
cust_violations = df[(df['Customer_ID'].isnull()) | (~df['cust_valid_format'])]
if len(cust_violations) > 0:
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(cust_violations[display_columns].head(5).to_string(index=True))
else:
    print("No Customer_ID violations found")

# Visualize
plt.figure(figsize=(8,5))
cust_status = ['Valid', 'Null', 'Invalid Format']
cust_counts = [valid_cust, null_cust, format_invalid_cust]
colors = ['green', 'gray', 'red']
bars = plt.bar(cust_status, cust_counts, color=colors)
plt.title('Customer ID Accuracy')
plt.ylabel('Count')
for bar, count in zip(bars, cust_counts):
    if count > 0:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, str(count), ha='center')
plt.show()

### **4. Quantity Accuracy**

print("\n4. QUANTITY ACCURACY")

df['quantity_num'] = pd.to_numeric(df['Quantity'], errors='coerce')

nulls_qty = df['Quantity'].isnull().sum()
negative_qty = (df['quantity_num'] < 0).sum()

print(f"Null values: {nulls_qty}")
print(f"Negative quantities: {negative_qty}")

valid_qty = len(df) - (nulls_qty  + negative_qty)
accuracy_qty = (valid_qty / len(df)) * 100
print(f"\n Accuracy: {accuracy_qty:.2f}%")

print("\n 5 Example Records with Quantity Violations:")
qty_violations = df[(df['Quantity'].isnull()) | 
                    (df['quantity_num'].isna()) | 
                    (df['quantity_num'] <= 0)]
if len(qty_violations) > 0:
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(qty_violations[display_columns].head(5).to_string(index=True))
else:
    print("No Quantity violations found")

# Visualize
plt.figure(figsize=(10,5))
issues = ['Valid', 'Null', 'Negative']
counts = [valid_qty, nulls_qty, negative_qty]
colors = ['green', 'gray','orange']
bars = plt.bar(issues, counts, color=colors)
plt.title('Quantity Accuracy')
plt.ylabel('Count')
for bar, count in zip(bars, counts):
    if count > 0:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
                 str(count), ha='center', fontsize=10)
plt.show()

### **5. Price Accuracy**

# %%
print("\n5. PRICE ACCURACY")

# Clean price by removing $ and ,
df['price_cleaned'] = df['Price'].astype(str).str.replace('$', '').str.replace(',', '')
df['price_num'] = pd.to_numeric(df['price_cleaned'], errors='coerce')

nulls_price = df['Price'].isnull().sum()
negative_price = (df['price_num'] < 0).sum()

print(f"Null values: {nulls_price}")
print(f"Negative prices: {negative_price}")

valid_price = len(df) - (nulls_price + negative_price)
accuracy_price = (valid_price / len(df)) * 100
print(f"\n Accuracy: {accuracy_price:.2f}%")

print("\n📋 5 Example Records with Price Violations:")
price_violations = df[(df['Price'].isnull()) | 
                      (df['price_num'].isna()) | 
                      (df['price_num'] <= 0)]
if len(price_violations) > 0:
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    print(price_violations[display_columns].head(5).to_string(index=True))
else:
    print("No Price violations found")

# Visualize
plt.figure(figsize=(10,5))
issues = ['Valid', 'Null', 'Negative']
counts = [valid_price, nulls_price, negative_price]
colors = ['green', 'gray', 'orange']
bars = plt.bar(issues, counts, color=colors)
plt.title('Price Accuracy')
plt.ylabel('Count')
for bar, count in zip(bars, counts):
    if count > 0:
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, 
                 str(count), ha='center', fontsize=10)
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