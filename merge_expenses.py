# %%
import os
import pandas as pd


# %%
expense_report_files = [
    f for f in os.listdir('data/raw/') if 'Expenses.csv' in f
]

pv_expenses = pd.read_csv('data/processed/pv_expenses.csv', parse_dates=True)
# %%
date_filt = [d.split('/')[-1]=='2022' for d in pv_expenses.Date]
pv_expenses = pv_expenses[date_filt]
# %%
reports = {}
for fname in expense_report_files:
    address = fname.split(',')[0]
    reports[address] = pd.read_csv(f'data/raw/{fname}', parse_dates=True).fillna('')
    old_lawn_care = reports[address].Vendor.str.contains('Park View')
    reports[address] = reports[address][~old_lawn_care]
    reports[address].Vendor = [
        ' - '.join(['Park View Lawn Care', v.split(' - ')[1]])
        if 'Park View' in v else v
        for v in reports[address].Vendor
    ]
    expenses = pv_expenses.loc[pv_expenses.Address.str.contains(address)]
    reports[address] = pd.concat([reports[address], expenses])

    aggfunc = lambda x: ', '.join(list(set(x)))
    reports[address] = reports[address].groupby(by=['Date', 'Vendor', 'Amount', 'Address'], as_index=False).agg({'Description': aggfunc, 'Category': aggfunc, 'Receipts': aggfunc})

    reports[address].to_csv(f'data/processed/{fname}-UPDATED.csv')
# %%
