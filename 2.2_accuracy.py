# %% [markdown]
## **2.2 Accuracy**

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('dirty_supermarket_sales.csv')

# %% [markdown]
## **Accuracy Analysis**
# %%
missing = df.isnull().sum()
print("Dataset Shape:", df.shape)

# Select only the required columns
cols = ['Quantity', 'Unit price', 'Tax 5%', 'Sales']

missing = df[cols].isnull().sum()
print("\nMissing Values:\n", missing)

plt.figure(figsize=(8,5))
missing.plot(kind='bar')
plt.title("Missing Values in Key Columns")
plt.ylabel("Count")

for i, v in enumerate(missing):
    plt.text(i, v, str(v), ha='center', va='bottom')

plt.tight_layout()
plt.show()

# Duplicate Records
dup = df.duplicated().sum()
unique = len(df) - dup

print("\nDuplicates:", dup)

plt.figure()
plt.pie([dup, unique],
        labels=['Duplicate', 'Unique'],
        autopct='%1.1f%%')
plt.title("Duplicate Records")
plt.show()

# Sales Accuracy Check
df['Unit price'] = pd.to_numeric(df['Unit price'], errors='coerce')
df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
df['Tax 5%'] = pd.to_numeric(df['Tax 5%'], errors='coerce')
df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')

# Sales formula
df['calculated_sales'] = (df['Unit price'] * df['Quantity']) + df['Tax 5%']

# Identify incorrect sales
sales_error = abs(df['Sales'] - df['calculated_sales'])
tolerance = 0.01

df['is_incorrect'] = sales_error > tolerance

# Get 10 incorrect samples
incorrect_samples = df[df['is_incorrect']].head(10)

print("\n--- 10 INCORRECT SALES RECORDS ---")
cols = ['Unit price', 'Quantity', 'Tax 5%', 'Sales', 'calculated_sales']

print(incorrect_samples[cols])