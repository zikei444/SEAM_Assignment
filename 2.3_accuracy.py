# %% [markdown]
## **2.3 Data Cleaning**

# %%

import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

# Load dataset
df = pd.read_csv('dirty_supermarket_sales.csv')


## **Data Cleaning**
# **Missing Values**
print("Missing values before:", df.isnull().sum().sum())

df = df.dropna()

print("Missing values after:", df.isnull().sum().sum())


# **Rebuild Total Amount**
df['Total_Amount'] = df['Unit price'] * df['Quantity']

# **Rebuild Tax 5%**
df['Tax 5%'] = df['Total_Amount'] * 0.05

# **Rebuild Sales**
df['Sales'] = df['Total_Amount'] + df['Tax 5%']

# **Clean Invalid Dates**
df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

df = df.dropna(subset=['Date'])

# **Extract Year, Month, Day from Date**
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['Day'] = df['Date'].dt.day

# **Standardize Categorical Columns**
df['Payment'] = df['Payment'].str.title().str.strip()
df['Customer type'] = df['Customer type'].str.title().str.strip()
df['Gender'] = df['Gender'].str.title().str.strip()
df['Product line'] = df['Product line'].str.title().str.strip()
df['Branch'] = df['Branch'].str.upper().str.strip()
df['City'] = df['City'].str.title().str.strip()

# **Rmove Duplicates**
df = df.drop_duplicates()

# **Reset Index**
df = df.sort_values(by='Date').reset_index(drop=True)

# **Save Cleaned Data**
df.to_csv('cleaned_supermarket_sales.csv', index=False)