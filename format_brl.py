import pandas as pd

def format_brl(value):
    if pd.isna(value) or value == 0:
        return '0,00'
    try:
        return f"{float(value):,.2f}".replace('.', 'X').replace(',', '.').replace('X', ',')
    except ValueError:
        return '0,00'