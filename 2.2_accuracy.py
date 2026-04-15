# %% [markdown]
## **2.2 Accuracy Check**

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('dirty_supermarket_sales.csv')

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
df['expected_sales'] = (df['Unit price'] * df['Quantity']) + df['Tax 5%']

# Error calculation
sales_error = abs(df['Sales'] - df['expected_sales'])

tolerance = 0.01

incorrect_sales = (sales_error > tolerance).sum()
valid_sales = len(df) - incorrect_sales

sales_accuracy = (valid_sales / len(df)) * 100

# Results
print("\nSALES ACCURACY RESULT")
print(f"Valid Sales Records: {valid_sales}")
print(f"Incorrect Sales Records: {incorrect_sales}")
print(f"Sales Accuracy: {sales_accuracy:.2f}%")

# Visualization
plt.figure()
plt.bar(['Valid', 'Incorrect'], [valid_sales, incorrect_sales])
plt.title("Sales Accuracy Check")
plt.ylabel("Number of Records")

for i, v in enumerate([valid_sales, incorrect_sales]):
    plt.text(i, v, str(v), ha='center')

plt.show()