# %% [markdown]
## **2.4 - Accuracy**

import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

df_dirty = pd.read_csv('dirty_supermarket_sales.csv')
df_clean = pd.read_csv('cleaned_supermarket_sales.csv')

def accuracy(valid, total):
    return (valid / total) * 100

df_dirty['Unit price'] = pd.to_numeric(df_dirty['Unit price'], errors='coerce')
df_dirty['Quantity'] = pd.to_numeric(df_dirty['Quantity'], errors='coerce')
df_dirty['Tax 5%'] = pd.to_numeric(df_dirty['Tax 5%'], errors='coerce')
df_dirty['Sales'] = pd.to_numeric(df_dirty['Sales'], errors='coerce')

expected_before = (df_dirty['Unit price'] * df_dirty['Quantity']) + df_dirty['Tax 5%']
error_before = abs(df_dirty['Sales'] - expected_before)

invalid_before = (error_before > 0.01).sum()
valid_before = len(df_dirty) - invalid_before
accuracy_before = accuracy(valid_before, len(df_dirty))

df_clean['Unit price'] = pd.to_numeric(df_clean['Unit price'], errors='coerce')
df_clean['Quantity'] = pd.to_numeric(df_clean['Quantity'], errors='coerce')
df_clean['Tax 5%'] = pd.to_numeric(df_clean['Tax 5%'], errors='coerce')
df_clean['Sales'] = pd.to_numeric(df_clean['Sales'], errors='coerce')

expected_after = (df_clean['Unit price'] * df_clean['Quantity']) + df_clean['Tax 5%']
error_after = abs(df_clean['Sales'] - expected_after)

invalid_after = (error_after > 0.01).sum()
valid_after = len(df_clean) - invalid_after
accuracy_after = accuracy(valid_after, len(df_clean))

accuracy_increase = accuracy_after - accuracy_before

print("\nSALES ACCURACY")
print(f"Before Cleaning: {accuracy_before:.2f}%")
print(f"After Cleaning: {accuracy_after:.2f}%")
print(f"Improvement: {accuracy_increase:.2f}%")

plt.figure(figsize=(6,4))

values = [accuracy_before, accuracy_after]
labels = ['Before', 'After']

plt.bar(labels, values)

plt.title("Sales Accuracy")
plt.ylabel("Accuracy %")

for i, v in enumerate(values):
    plt.text(i, v, f"{v:.2f}%", ha='center', va='bottom')

plt.ylim(0, 100)

plt.tight_layout()
plt.show()