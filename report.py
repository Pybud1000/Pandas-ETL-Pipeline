import pandas as pd
import numpy as np

orders = pd.read_csv(r'C:\Users\PCXPC\Documents\super secret hehehe\Projects\Pandas ETL\data\clean\clean_orders.csv')
returns = pd.read_csv(r'C:\Users\PCXPC\Documents\super secret hehehe\Projects\Pandas ETL\data\clean\clean_returns.csv')
tickets = pd.read_csv(r'C:\Users\PCXPC\Documents\super secret hehehe\Projects\Pandas ETL\data\clean\clean_tickets.csv')

orders = orders[orders['order_status'] != 'Cancelled']

ini_merged = orders.merge(returns, on='order_id', how='left')
ini_merged['order_count'] = 1
ini_merged['return_count'] = ini_merged['return_id'].fillna(0)
ini_merged['return_count'] = ini_merged['return_count'].map(lambda x: 0 if x == 0 else 1)

f_merge = ini_merged.merge(tickets, on='customer_id', how='left')
f_merge['ticket_count'] = f_merge['ticket_id'].fillna(0)
f_merge['ticket_count'] = f_merge['ticket_count'].map(lambda x: 0 if x== 0 else 1)

customer_summary = f_merge[['customer_id','quantity','total_amount', 'refund_amount','order_count', 'return_count', 'ticket_count']]

customer_summary = customer_summary.groupby(['customer_id'], as_index=False).agg(
    quantity=('quantity','sum'),
    total_amount=('total_amount','sum'),
    refund_amount=('refund_amount','sum'),
    Order_count=('order_count','sum'),
    Return_count=('return_count','sum'),
    Ticket_count=('ticket_count','sum')
)

# Format as percentage string with 1 decimal place
customer_summary['Return_rate'] = (customer_summary['Return_count'] / customer_summary['Order_count'] * 100).map('{:.1f}%'.format)

customer_summary.to_csv(r'C:\Users\PCXPC\Documents\super secret hehehe\Projects\Pandas ETL\data\summary\customer_summary.csv', index=False)