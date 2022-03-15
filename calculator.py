from numpy import number
import pandas as pd

# load a report
report_df = pd.read_csv('report/txn_report_mixed.csv')

# initial values
history = {}
wallet = {}
profit = 0

# getting currency
currencies = []
print('History amount: {}'.format(len(report_df)))
for i in range(len(report_df)):
    currency = report_df['Currency'][i]
    if currency not in currencies:
        currencies.append(currency)
        wallet[currency] = []
        history[currency] = []
print('Currency {}'.format(str(currencies)))

# creating history dict
for i in range(len(report_df)):
    type = report_df['Type'][i]
    currency = report_df['Currency'][i]

    if type == 'buy' and currency != 'THB':
        value = float(report_df['Description'][i][(10+len(currency)):])
        amount = report_df['Amount'][i]
        history[currency].append({
            'type': type,
            'value': value,
            'amount': amount
        })

    elif type == 'sell' and currency != 'THB':
        history[currency].append({
            'type': type,
            'value': float(report_df['Description'][i][(10+len(currency)):]),
            'amount': -1 * report_df['Amount'][i]
        })
