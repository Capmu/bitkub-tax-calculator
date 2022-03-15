import pandas as pd
import sys


def calculate_profit(operation, currency):
    buying_order = 0
    principle = 0
    amount_checker = operation['amount']
    to_remove = 0

    #--------------------------------------------------------
    # Using FIFO (First-In-First-Out) logic
    #--------------------------------------------------------
    # finding overall principle price
    while amount_checker > 0:
        try:
            oldest_purchese = wallet[currency][buying_order]
            if amount_checker >= oldest_purchese['amount']:
                principle += (oldest_purchese['amount'] * oldest_purchese['value'])
                amount_checker -= oldest_purchese['amount']
                print('     An oldest value is out: {} -> remaing amount: {}'.format(oldest_purchese['amount'], amount_checker))
                to_remove += 1
            else:
                principle += (amount_checker * oldest_purchese['value'])
                wallet[currency][buying_order]['amount'] -= amount_checker
                amount_checker = 0
            buying_order += 1
        except Exception as ex:
            if str(ex) == 'list index out of range':
                print('     Floating issue!! remove remaining amount: {}'.format(amount_checker))
                amount_checker = 0
            else:
                print('ERROR! Something went wrong.')
                sys.exit()
    
    # remove the outed (amount) values
    if to_remove > 0:
        for _ in to_remove:
            del wallet[currency][0]
    
    # calculate the profit
    profit = principle - (operation['amount'] * operation['value'])
    print('PROF ({}): {}'.format(currency, profit))
    if profit > 0:
        return profit
    else:
        return 0


# load a report
report_df = pd.read_csv('report/txn_report_mixed.csv')

# initial values
history = {}
wallet = {}
fee = 0
sum_profit = 0

# getting currency
currencies = []
print('History amount: {}'.format(len(report_df)))
for i in range(len(report_df)):
    currency = report_df['Currency'][i]
    if currency not in currencies:
        currencies.append(currency)
        wallet[currency] = []
print('Currency {}'.format(str(currencies)))

# creating history dict
for i in range(len(report_df)):
    type = report_df['Type'][i]
    currency = report_df['Currency'][i]

    if type == 'buy' and currency != 'THB':
        value = float(report_df['Description'][i][(10+len(currency)):])
        amount = report_df['Amount'][i]
        wallet[currency].append({
            'value': value,
            'amount': amount
        })
        print('\n++++++++++++ BUYD ({}): {} VALUE: {}'.format(currency, amount, value))

    elif type == 'sell' and currency != 'THB':
        having = 0
        for wood in wallet[currency]:
            having += wood['amount']
        print('\nHAVE ({}): {}'.format(currency, having))
        print('SELL ({}): {} VALUE: {}'.format(currency, -1 * report_df['Amount'][i], float(report_df['Description'][i][(8+len(currency)):])))
        
        operation = {
            'type': type,
            'value': float(report_df['Description'][i][(8+len(currency)):]),
            'amount': -1 * report_df['Amount'][i]
        }
        profit = calculate_profit(operation, currency)
        if profit > 0:
            sum_profit += profit
        print('LEFT ({}): {}'.format(currency, wallet[currency]))
    
    elif type == 'fee' and currency == 'THB':
        fee += -1 * report_df['Amount'][i]

print('\n-------------------------------')
print('summary profit: {:.2f} THB'.format(sum_profit - fee))
print('-------------------------------')