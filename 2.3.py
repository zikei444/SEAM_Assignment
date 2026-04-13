# %% [markdown]
## **2.3**

# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')


df = pd.read_csv('dirty_financial_transactions.csv')
# %% [markdown]
## **Data Cleanning**

# %% [markdown]
# **Duplication**

# %%
# Remove duplicates data
df = df.drop_duplicates()
# %% [markdown]
# **Transaction ID**
# %%
# Remove extra spaces
df['Transaction_ID'] = df['Transaction_ID'].astype(str).str.strip()

# Extract numeric part from Transaction_ID
df['Transaction_ID'] = df['Transaction_ID'].str.extract(r'(\d+)')[0]

# Convert to numeric
df['Transaction_ID'] = pd.to_numeric(df['Transaction_ID'], errors='coerce')

# Fill missing sequence
df['Transaction_ID'] = range(1, len(df) + 1)

# Converting back
df['Transaction_ID'] = 'T' + df['Transaction_ID'].astype(str).str.zfill(4)
df.head(10)

# %% [markdown]
# **Transaction Date**
# %%
# Convert String into Datetime ,and invalid dates become Nan
df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'],errors='coerce')

# Fill missing Transaction_Date with median date
df['Transaction_Date'].fillna(df['Transaction_Date'].median(), inplace=True)
# %% [markdown]
# **Customer ID**
# %%
# Fill missing Customer_ID with a placeholder
df['Customer_ID'] = df['Customer_ID'].fillna('Missing_ID')

# %% [markdown]
# **Quantity**
# %%
# Mark negative Quantity as missing
df.loc[df['Quantity'] < 0, 'Quantity'] = None

# Fill missing Quantity with median - robust to outliers
df['Quantity'].fillna(df['Quantity'].median(), inplace=True)

# %% [markdown]
# **Price**
# %%
# Remove dollar sign
df['Price'] = df['Price'].astype(str).str.replace('$', '', regex=False)

# Convert Price to numeric
df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

# Replace negative prices with NaN
df.loc[df['Price'] < 0, 'Price'] = None

# Fill missing Price with median
df['Price'].fillna(df['Price'].median(), inplace=True)

# %% [markdown]
# **Payment Method**
# %%
# Convert to lowercase and remove extra spaces
df['Payment_Method'] = df['Payment_Method'].str.lower().str.strip()

# Remove spaces inside strings (like 'credit card' → 'creditcard')
df['Payment_Method'] = df['Payment_Method'].str.replace(' ', '')

# Replace with consistent naming
df['Payment_Method'] = df['Payment_Method'].replace({
    'creditcard': 'Credit Card',
    'paypal': 'PayPal',
    'cash': 'Cash'
})

#  %% [markdown]
# **Transaction Status**
# %%
# Fill missing Transaction_Status with mode
df['Transaction_Status'].fillna(df['Transaction_Status'].mode()[0], inplace=True)
# Convert to lowercase and strip spaces
df['Transaction_Status'] = df['Transaction_Status'].str.lower().str.strip()

# Remove spaces inside strings
df['Transaction_Status'] = df['Transaction_Status'].str.replace(' ', '')

# Replace with consistent naming
df['Transaction_Status'] = df['Transaction_Status'].replace({
    'failed': 'Failed',
    'pending': 'Pending',
    'completed': 'Completed',
    'complete': 'Completed'
})

# %% [markdown]
# **Product Name**
# %%
#Lowercase and strip the column temporarily
df['Product_Name_temp'] = df['Product_Name'].str.lower().str.strip()

# replacing the wrong product name with original
replace_name = {
    'tab' : 'Tablet',
    'coffee ma' : 'Coffee Machine',
    'coffee' : 'Coffee Machine',
    'cof' : 'Coffee Machine',
    'smar' : 'Smartphone',
    'coffee m' : 'Coffee Machine',
    't' : 'Tablet',
    'smartpho' : 'Smartphone',
    'headp' : 'Headphones',
    'smart' : 'Smartphone',
    'smartph':'Smartphone',
    'la' : 'Laptop',
    'lapt' : 'Laptop',
    'tabl' : 'Tablet',
    'l' : 'Laptop',
    'c' : 'Coffee Machine',
    'co' : 'Coffee Machine',
    'headphone': 'Headphones',
    'coffee mac' : 'Coffee Machine',
    'sm' : 'Smartphone',
    'headph' : 'Headphones',
    's' : 'Smartphone',
    'coffee mach' : 'Coffee Machine',
    'smartphon' : 'Smartphone',
    'headpho' : 'Headphones',
    'coffee machin' : 'Coffee Machine',
    'coff' : 'Coffee Machine',
    'lap' : 'Laptop',
    'h' : 'Headphones',
    'he' : 'Headphones',
    'ta': 'Tablet',
    'coffee machi' : 'Coffee Machine',
    'coffe' : 'Coffee Machine',
    'sma' : 'Smartphone',
    'smartp' : 'Smartphone',
    'hea' : 'Headphones',
    'headphon': 'Headphones',
    'head' : 'Headphones',
    'lapto' :  'Laptop',
    'table' : 'Tablet'
}

# replacing using lowercase column
df['Product_Name_temp'] = df['Product_Name_temp'].replace(replace_name)

# Converting back to capital letter
df['Product_Name'] = df['Product_Name_temp'].str.title()

#Drop temporary column
df.drop(columns=['Product_Name_temp'], inplace=True)

# %% [markdown]
## **Transformation (Derive Column)**

# %%
# Total transaction value
df['Total_Amount'] = df['Quantity'] * df['Price']

# Extract date features
df['Year'] = df['Transaction_Date'].dt.year
df['Month'] = df['Transaction_Date'].dt.month

# %% [markdown]
## **Sorting and Index Reset**

# %%
df = df.sort_values(by='Transaction_Date').reset_index(drop=True)

# %% [markdown]
# **Save Cleaned**
df.to_csv('cleaned_financial_transactions.csv', index=False)
# %%
