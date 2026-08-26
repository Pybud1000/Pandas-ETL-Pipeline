import pandas as pd
import numpy as np

orders = pd.read_excel(r'C:\Users\PCXPC\Documents\super secret hehehe\Projects\Pandas ETL\data\raw\orders.xlsx')
returns = pd.read_excel(r'C:\Users\PCXPC\Documents\super secret hehehe\Projects\Pandas ETL\data\raw\returns.xlsx')
tickets = pd.read_excel(r'C:\Users\PCXPC\Documents\super secret hehehe\Projects\Pandas ETL\data\raw\tickets.xlsx')

# CLEANING SECTION

# ORDERS

# Fill in null values for customer ID as "Unknown"
orders['customer_id'] = orders['customer_id'].fillna('Unknown')

# Fill in null values with the most frequent data (Delivered)
orders['order_status'] = orders['order_status'].fillna('Delivered')

# Standardize Payment method
orders.loc[
    orders['payment_method'].str.contains('credit', case=False, na=False), 
    'payment_method'
] = 'Credit card'

# Standardize order status
orders.loc[
    orders['order_status'].str.contains('delivered', case=False, na=False),
    'order_status'
] = 'Delivered'

# remove duplicates
orders = orders.drop_duplicates()

# clean negative values from 'quantity', 'unit_price', and 'total_amount'
orders[['quantity','unit_price','total_amount']] = orders[['quantity','unit_price','total_amount']].abs()

# clean dates column
orders['order_date'] = pd.to_datetime(
    orders['order_date'],
    errors='coerce'
)
orders['order_date'] = orders['order_date'].ffill()

# RETURNS

# Fill the null values for refund_amount
returns['refund_amount'] = returns['refund_amount'].fillna(returns['refund_amount'].median())

# Standardize return_reason
returns.loc[
    returns['return_reason'].str.contains('damaged', case=False, na=False),
    'return_reason'
] = 'Damaged'

returns.loc[
    returns['return_reason'].str.contains('wrong item', case=False, na=False),
    'return_reason'
] = 'Wrong item'

# Standardize return_status
returns.loc[
    returns['return_status'].str.contains('approved', case=True, na=True),
    'return_status'
] = 'Approved'

# Remove duplicates
returns = returns.drop_duplicates()

# Clean negative values on integer columns
returns['refund_amount'] = returns['refund_amount'].abs()

# Clean date column

returns['return_date'] = pd.to_datetime(
    returns['return_date'],
    errors='coerce'
)
returns['return_date'] = returns['return_date'].ffill()