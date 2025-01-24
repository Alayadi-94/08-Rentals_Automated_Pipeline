import pandas as pd
import numpy as np

def get_table():
    '''Returns raw data'''
    cleaned_df = pd.read_csv('data/historic_data_cleaned.csv')
    return cleaned_df

def get_cleaned_table(owner='all'):
    '''Returns the cleaned historical data without cleaning fee and commition'''

    cleaned_df = get_table()
    if (owner=='Mohamed') | (owner=='Mounia'):
        cleaned_df = cleaned_df[cleaned_df['Owner']==owner]
    cleaned_df['Revenue'] = cleaned_df.apply(
        lambda row: (row.Revenue - 50) if row.Apartment_code in ["Oumnia A2 17", "Palmeraie B9 A1"]
        else (row.Revenue - 20), axis=1)
    cleaned_df['Revenue'] = cleaned_df['Revenue']*0.8

    return cleaned_df

def revenue_threshold():
    '''Returns the thresholds used to measur performance'''
    rents = [7000, 8500, 7000, 9000, 10000, 10000, 18000, 18000]
    thresholds = pd.DataFrame({
    'Apartment_code': ['Alia 22', 'Alia 36', 'Alia 37', 'Alia 41', 'Menara 12',
                  'Menara 15', 'Oumnia A2 17', 'Palmeraie B9 A1'],
    'Threshold (EUR)': [i/10.5 for i in rents],
    'Threshold (MAD)': rents}
    )
    thresholds = thresholds.set_index('Apartment_code')
    return thresholds

def get_pivot(pivot_type = 'Revenue', owner='all'):
    '''Creates a pivot table based on the full dataset'''
    df=get_cleaned_table(owner=owner)

    if pivot_type == 'Occupancy':
        mode = 'count'
    else:
        mode = 'sum'

    #split data table into rows per days and create table for each day
    rows = []
    for i, row in df.iterrows():
        for single_date in pd.date_range(start=row.Start_Date, end=row.End_Date, inclusive= 'left'):
            rows.append({
                'Confirmation_Code': row['Confirmation_Code'],
                'Date': single_date,
                'Apartment_code': row['Apartment_code'],
                'Owner': row['Owner'],
                'Status': row['Status'],
                'Reserved': row['Reserved'],
                'Revenue': row['Revenue'] / (row['Number_of_Nights'])  # Split revenue equally per day
            })

    df_days = pd.DataFrame(rows)
    # Add a Month column for aggregation
    df_days['Month'] = df_days['Date'].dt.to_period('M')

    # Pivot table to aggregate revenue per apartment and month
    pivot_table = df_days.pivot_table(
        index='Apartment_code',
        columns='Month',
        values='Revenue',
        aggfunc= mode,
        fill_value=0
    )
    return pivot_table

def get_perf_table():
    '''Create an overall performance analysis'''
    analysis_table = revenue_threshold()
    revenue_pivot = get_pivot(pivot_type = 'Revenue')

    Number_of_months = []
    for code in analysis_table.index:
        Number_of_months.append((revenue_pivot.drop(columns=['2024-09', '2024-10', '2024-11', '2024-12']).loc[code] != 0).sum())

    analysis_table['Number_of_months'] = Number_of_months
    analysis_table['Total_threshold'] = analysis_table['Number_of_months']*analysis_table['Threshold (EUR)']
    analysis_table['Total_revenue (EUR)'] = revenue_pivot.sum(axis=1)
    analysis_table['Real_Earnings (EUR)'] = analysis_table['Total_revenue (EUR)']-analysis_table['Total_threshold']
    analysis_table['Performance (%)']=analysis_table['Real_Earnings (EUR)']/analysis_table['Number_of_months']/analysis_table['Threshold (EUR)']*100
    analysis_table.drop(columns=['Number_of_months', 'Total_threshold'], inplace=True)
    analysis_table.drop(index=['Menara 12', 'Palmeraie B9 A1'], inplace=True)
    analysis_table = analysis_table.astype(int)
    return analysis_table

def create_overview():
    '''creates an overview yearly'''
    thresholds = revenue_threshold().drop(index=['Palmeraie B9 A1','Menara 12'])
    thres = np.array(thresholds['Threshold (EUR)'].to_list())
    pivot = get_pivot(pivot_type = 'Revenue')
    pivot = pivot.drop(columns=['2024-09', '2024-10', '2024-11', '2024-12'], index=['Palmeraie B9 A1','Menara 12' ])

    data = {}
    for year in [2022, 2023, 2024]:
        selected_range = pivot.columns[pivot.columns.year == year]
        months = np.array((pivot[selected_range] != 0).sum(axis=1).to_list())
        rev = np.array(pivot[selected_range].sum(axis=1).to_list())
        performance = np.nan_to_num(np.divide(rev - (months * thres), (months * thres))*100, nan = 0)

        data[(str(year), '# of months')] = months.tolist()
        data[(str(year), 'Total revenue')] = rev.tolist()
        data[(str(year), 'Performance (%)')] = performance.tolist()

        # Create a DataFrame from the results
    data_df = pd.DataFrame(data, index = thresholds.index).astype(int)
    return data_df
