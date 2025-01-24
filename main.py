from functions.display import display_table, display_perf, plot_revenue, plot_area
from tables.clean_import import get_cleaned_table, create_overview, get_pivot


#display_table(mode='Revenue', year=2024, owner='Mounia')
#display_perf(create_overview())
fig = plot_area(year=2022)
fig.show()
