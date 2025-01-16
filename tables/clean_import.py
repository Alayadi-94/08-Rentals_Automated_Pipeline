import pandas as pd

def get_cleaned_table():
    '''Returns the cleaned historical data without cleaning fee and commition'''

    cleaned_df = pd.read_csv('data/historic_data_cleaned.csv')
    cleaned_df['Revenue'] = cleaned_df.apply(
        lambda row: (row.Revenue - 50) if row.Apartment_code in ["Oumnia A2 17", "Palmeraie B9 A1"]
        else (row.Revenue - 20), axis=1)
    cleaned_df['Revenue'] = cleaned_df['Revenue']*0.8

    return cleaned_df

def revenue_threshold():
    thresholds = pd.DataFrame({
    'Apartment_code': ['Alia 22', 'Alia 36', 'Alia 37', 'Alia 41', 'Menara 12',
                  'Menara 15', 'Oumnia A2 17', 'Palmeraie B9 A1'],
    'Threshold': [650, 850, 650, 800, 1000, 1000, 1800, 2000]})
    thresholds = thresholds.set_index('Apartment_code')
    return thresholds
