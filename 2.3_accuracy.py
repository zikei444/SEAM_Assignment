# %% [markdown]
## **2.3**

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('dirty_supermarket_sales.csv')

rows_before = df.shape[0]
dup_before = df.duplicated().sum()
missing_before = df.isnull().sum().sum()

print("Rows before cleaning:", rows_before)
print("Duplicate rows before cleaning:", dup_before)
print("Missing values before cleaning:", missing_before)

df = df.dropna()

df['Total_Amount'] = df['Unit price'] * df['Quantity']
df['Tax 5%'] = df['Total_Amount'] * 0.05
df['Sales'] = df['Total_Amount'] + df['Tax 5%']

df = df.drop_duplicates()
df = df.sort_values(by='Date').reset_index(drop=True)

rows_after = df.shape[0]
dup_after = df.duplicated().sum()
missing_after = df.isnull().sum().sum()

print("\nRows after cleaning:", rows_after)
print("Duplicate rows after cleaning:", dup_after)
print("Missing values after cleaning:", missing_after)

print("\nRows removed:", rows_before - rows_after)

plt.figure(figsize=(6,4))

values = [rows_before, rows_after]
labels = ['Before Cleaning', 'After Cleaning']

plt.bar(labels, values)

plt.title("Dataset Size Before vs After Cleaning")
plt.ylabel("Number of Rows")

for i, v in enumerate(values):
    plt.text(i, v, str(v), ha='center', va='bottom')

plt.tight_layout()
plt.show()