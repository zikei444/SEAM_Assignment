# %% [markdown]
## **2.4 Accuracy Check**
# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

# Load datasets
df_dirty = pd.read_csv('dirty_supermarket_sales.csv')
df_after = pd.read_csv('cleaned_supermarket_sales.csv')

df_after.head(10)

# %%
df_after.info()

# %%
df_after.describe()

# %%
df_after.shape


def accuracy(valid, total):
    return (valid / total) * 100


# **Row count before and after cleaning**
rows_before = len(df_dirty)
rows_after = len(df_after)
rows_removed = rows_before - rows_after

print("ROW COMPARISON")
print(f"Before Re-engineering: {rows_before}")
print(f"After Re-engineering: {rows_after}")
print(f"Rows Removed: {rows_removed}")


# **Sales Accuracy Check (Before Cleaning)**

df_dirty['Unit price'] = pd.to_numeric(df_dirty['Unit price'], errors='coerce')
df_dirty['Quantity'] = pd.to_numeric(df_dirty['Quantity'], errors='coerce')
df_dirty['Tax 5%'] = pd.to_numeric(df_dirty['Tax 5%'], errors='coerce')
df_dirty['Sales'] = pd.to_numeric(df_dirty['Sales'], errors='coerce')

expected_before = (df_dirty['Unit price'] * df_dirty['Quantity']) + df_dirty['Tax 5%']
error_before = abs(df_dirty['Sales'] - expected_before)

invalid_before = (error_before > 0.01).sum()
valid_before = len(df_dirty) - invalid_before
accuracy_before = accuracy(valid_before, len(df_dirty))


# **Sales Accuracy Check (After Cleaning)**

df_after['Unit price'] = pd.to_numeric(df_after['Unit price'], errors='coerce')
df_after['Quantity'] = pd.to_numeric(df_after['Quantity'], errors='coerce')
df_after['Tax 5%'] = pd.to_numeric(df_after['Tax 5%'], errors='coerce')
df_after['Sales'] = pd.to_numeric(df_after['Sales'], errors='coerce')

expected_after = (df_after['Unit price'] * df_after['Quantity']) + df_after['Tax 5%']
error_after = abs(df_after['Sales'] - expected_after)

invalid_after = (error_after > 0.01).sum()
valid_after = len(df_after) - invalid_after
accuracy_after = accuracy(valid_after, len(df_after))


# **Improvement Calculation**
accuracy_increase = accuracy_after - accuracy_before


print("\nSALES ACCURACY COMPARISON")
print(f"Before Re-engineering: {accuracy_before:.2f}%")
print(f"After Re-engineering: {accuracy_after:.2f}%")
print(f"Increase in Accuracy: {accuracy_increase:.2f}%")


# Visualization

plt.figure(figsize=(6,4))

counts = [valid_before, valid_after]

bars = plt.bar(['Before', 'After'], counts)

plt.title("Sales Accuracy Comparison")
plt.ylabel("Number of Valid Records")

total_before = len(df_dirty)
total_after = len(df_after)

percentages = [accuracy_before, accuracy_after]

for bar, count, pct in zip(bars, counts, percentages):
    plt.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height(),
        f"{count}",
        ha='center',
        va='bottom'
    )

plt.show()