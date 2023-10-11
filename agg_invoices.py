# %%
import os

import pandas as pd
import pdftotext

# %%
interim_data = os.listdir('data/interim')
invoice_fnames = [n for n in interim_data if n[:7]=='Invoice']
# %%
def load_pdf(fpath):
    with open(fpath, 'rb') as f:
        return pdftotext.PDF(f)
    
pdfs = [load_pdf(f'data/interim/{f}') for f in invoice_fnames]
# %%
def process_pdf(pdf):
    page = pdf[0]
    invoice_date = page.split('$')[-2].strip('\n').split('\n')[-1]
    invoice_number = page.split('Invoice: ')[1].split('\n')[0]
    vendor = f'Park View Lawn Care - Invoice {invoice_number}'
    description = 'Lawn Care'
    category ='Cleaning & maintenance'
    amount = page.split('Invoice Total:')[1].strip('\n').split('\n')[0]
    address = page.split('PAYMENT COUPON')[1].strip( '\n').split('\n\n')[1].split('\n')[1:]
    street_map = {
        '211': '211 S 13th St',
        '212': '212 Broadmoor Dr',
        '1215': '1215 Kenmore Pl',
        '3100': '3100 Richmond Hill Dr'
    }
    address[0] = street_map[address[0].split()[0]]
    address.append('US')
    address = ', '.join(address)
    receipt = f'Invoice-{invoice_number}.pdf'

    return [invoice_date, vendor, description, category, amount, address, receipt]

columns = [
    'Date','Vendor','Description', 'Category', 'Amount', 'Address', 'Receipts'
]
expenses = pd.DataFrame(
    [process_pdf(pdf) for pdf in pdfs], columns=columns
).set_index('Date').sort_values(by='Vendor')

expenses.to_csv('data/processed/pv_expenses.csv')
# %%
