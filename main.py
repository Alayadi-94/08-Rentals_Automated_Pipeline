from functions.display import display_table
from tables.clean_import import get_cleaned_table


cleaned_df = get_cleaned_table()
display_table(cleaned_df, mode='Revenue', year=2022)
