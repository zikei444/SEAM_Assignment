# %% [markdown]
## **2.1 Accuracy**

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

# %%
# Missing Values
# %%
print("Missing Values:")
print(df.isnull().sum())

# %%
# Duplication
# %%
print("Duplicate rows:", df.duplicated().sum())

duplicates = df[df.duplicated()]
print(duplicates.head())

# %%
# Invalid Quantity
# %%
print("Invalid or Missing Quantity:")

invalid_quantity = df[
    (df['Quantity'] <= 0) | (df['Quantity'].isnull())
]

print(invalid_quantity)

# %%
# Invalid Unit Price
# %%
print("Invalid or Missing Unit Price:")

invalid_unit_price = df[
    (df['Unit price'] <= 0) | (df['Unit price'].isnull())
]

print(invalid_unit_price)

# %%
# Invalid Tax
# %%
print("Invalid or Missing Tax:")

invalid_tax = df[
    (df['Tax 5%'] <= 0) | (df['Tax 5%'].isnull())
]

print(invalid_tax)

# %%
# Invalid Sales
# %%
print("Invalid Sales:")

df['Sales'] = pd.to_numeric(df['Sales'], errors='coerce')

print(df[
    (df['Sales'] <= 0) | (df['Sales'].isnull())
])