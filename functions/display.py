import pandas as pd
import numpy as np
import calendar
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.patches import Patch


from tables.clean_import import revenue_threshold, get_pivot, get_perf_table

def rev_color_grid(df, thresholds):
    '''Returns a color grid for the revenue analysis'''
    # Dictionary to store the coloring criteria
    color_criteria = np.zeros_like(df, dtype=float)

    # Apply color logic based on comparison with row means
    for i in range(len(df)):
        row_threshold = thresholds.iloc[i][0]  # Get the mean for the current row

        for j in range(len(df.columns)):
            value = df.iloc[i, j]

            if pd.notnull(value):  # If the value is not NaN
                if value == 0:
                    color_criteria[i, j] = 0 # Grey
                elif value >= (row_threshold * 1.3):  # Greater than 20% above the row mean
                    color_criteria[i, j] = 2  # Green
                elif value <= row_threshold:  # Less than 20% below the row mean
                    color_criteria[i, j] = -2  # Red
                elif (value > row_threshold) and (value < row_threshold*1.3):
                    color_criteria[i, j] = 1  # Yellow
            else:
                color_criteria[i, j] = 0  # Leave NaN as 0 for transparent
    return color_criteria

def occ_color_grid(df):
    '''Returns a color grid for the occupancy analysis'''
    # Dictionary to store the coloring criteria
    color_criteria = np.zeros_like(df, dtype=float)

    for j, n in enumerate(df.columns):
        col_threshold = round(calendar.monthrange(n.year, n.month)[1]*0.8,0)

        for i in range(len(df)):
            value = df.iloc[i, j]

            if pd.notnull(value):  # If the value is not NaN
                if value == 0:
                    color_criteria[i, j] = 0 # Grey
                elif value >= (col_threshold * 1.2):  # Greater than 20% above the monthly threshold
                    color_criteria[i, j] = 2  # Green
                elif value <= (col_threshold * 0.8):  # Less than 20% below the monthly threshold
                    color_criteria[i, j] = -2  # Red
                else:  # Between -20% and +20% of the row mean
                    color_criteria[i, j] = 1  # Yellow
            else:
                color_criteria[i, j] = 0  # Leave NaN as 0 for transparent

    return color_criteria

def create_yearly_overview(mode='Revenue', year=2022, owner='all'):
    '''Creates yearly overvew'''
    full_pivot = get_pivot(pivot_type = mode, owner=owner)

    #Select only data for the selected year
    selected_time_range = full_pivot.columns[full_pivot.columns.year == year]
    yearly_overview = full_pivot[selected_time_range].round(0).astype(int)

    return yearly_overview

def display_table(mode='Revenue', year=2022, owner='all'):
    '''Displays the table colored as an image'''
    df = create_yearly_overview(mode, year, owner)

    if mode == 'Revenue':
        thresholds=revenue_threshold()
        color_criteria = rev_color_grid(df, thresholds)
    elif mode == 'Occupancy':
        color_criteria = occ_color_grid(df)
    else:
        return 'Mode not recognized'

    # Define custom colors: Red, Grey, Yellow, Green
    colors_list = ["#E52916", "#dfe6e9", "#F1C40F", "#27AE60"]
    custom_colors = ListedColormap(colors_list)


    # Define boundaries for color mapping: -2, 0, 1, 2
    boundaries = [-2.5, -0.5, 0.5, 1.5, 2.5]  # The boundaries define where each color will start and end

    # Use BoundaryNorm to map the values (-2, 0, 1, 2) to the colors
    norm = BoundaryNorm(boundaries, custom_colors.N)

    # Display the DataFrame using imshow with custom colors
    fig, ax = plt.subplots(figsize=(12, 5))
    im = ax.imshow(color_criteria, cmap=custom_colors, norm=norm, aspect="auto")

    # Add text annotations for each cell
    for i in range(len(df)):
        for j in range(len(df.columns)):
            cell_value = df.iloc[i, j]
            ax.text(j, i, cell_value, ha="center", va="center", color="black")


    # Customize x-ticks and y-ticks
    ax.set_xticks(np.arange(len(df.columns)))
    ax.set_xticklabels(df.columns, rotation=45, ha="left", weight="bold")  # Rotate x-ticks
    ax.tick_params(axis="x", top=True, labeltop=True, bottom=False, labelbottom=False)  # Move x-ticks to the top
    ax.set_yticks(np.arange(len(df.index)))
    ax.set_yticklabels(df.index, weight="bold")  # Make y-ticks smaller

    # Create custom legend patches
    legend_elements = [
        Patch(color=colors_list[0], label=f"Inferieur au loyer de base"),
        Patch(color=colors_list[1], label="NA - No data"),
        Patch(color=colors_list[2], label=f"Autour du loyer de base"),
        Patch(color=colors_list[3], label=f"Plus de 30% superieur au loyer de base")
        ]
    # Add the legend below the table
    ax.legend(handles=legend_elements, loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=2)

    # Set title and adjust layout
    ax.set_title("Overview of the year")
    plt.tight_layout()
    plt.show()

    print(im)

    return 0

def perf_color_grid(df):
    '''Returns a color grid for the performance analysis'''
    color_criteria = np.zeros_like(df, dtype=float)

    for j, n in enumerate(df.columns):
        if n == 'Real_Earnings':
            for i in range(len(df)):
                value = df.iloc[i, j]
                if value < 0:
                    color_criteria[i, j]=-2
                elif value > 0:
                    color_criteria[i, j]=2
        elif n == 'Performance (%)':
            for i in range(len(df)):
                value = df.iloc[i, j]
                if value < 0:
                    color_criteria[i, j]=-2
                elif value > 0 and value < 30:
                    color_criteria[i, j]=1
                elif value > 30:
                    color_criteria[i, j]=2

    return color_criteria

def display_perf(df):
    '''Displays the overall performance table'''
    color_criteria = perf_color_grid(df)
    # Define custom colors: Red, Grey, Yellow, Green
    colors_list = ["#E52916", "#dfe6e9", "#F1C40F", "#27AE60"]
    custom_colors = ListedColormap(colors_list)


    # Define boundaries for color mapping: -2, 0, 1, 2
    boundaries = [-2.5, -0.5, 0.5, 1.5, 2.5]  # The boundaries define where each color will start and end

    # Use BoundaryNorm to map the values (-2, 0, 1, 2) to the colors
    norm = BoundaryNorm(boundaries, custom_colors.N)

    # Display the DataFrame using imshow with custom colors
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(color_criteria, cmap=custom_colors, norm=norm, aspect="auto")

    # Add text annotations for each cell
    for i in range(len(df)):
        for j in range(len(df.columns)):
            cell_value = df.iloc[i, j]
            ax.text(j, i, cell_value, ha="center", va="center", color="black")


    # Customize x-ticks and y-ticks
    ax.set_xticks(np.arange(len(df.columns)))
    ax.set_xticklabels(df.columns, rotation=45, ha="left", weight="bold")  # Rotate x-ticks
    ax.tick_params(axis="x", top=True, labeltop=True, bottom=False, labelbottom=False)  # Move x-ticks to the top
    ax.set_yticks(np.arange(len(df.index)))
    ax.set_yticklabels(df.index, weight="bold")  # Make y-ticks smaller

    # Create custom legend patches
    legend_elements = [
        Patch(color=colors_list[0], label=f"Negative performance"),
        Patch(color=colors_list[2], label=f"Average performance"),
        Patch(color=colors_list[3], label=f"Good performance")
        ]
    # Add the legend below the table
    ax.legend(handles=legend_elements, loc="upper center", bbox_to_anchor=(0.5, -0.05), ncol=2)

    # Set title and adjust layout
    ax.set_title("Overall performance")
    plt.tight_layout()
    plt.show()

    print(im)

    return 0

def plot_revenue(apartment_code):
    '''plot overall revenue'''

    # Create a pandas Series with text indices
    pivot = get_pivot().drop(columns=['2024-09', '2024-10', '2024-11', '2024-12'])
    series = pivot.loc[apartment_code][pivot.loc[apartment_code] != 0]
    index = list(series.index.astype(str))
    curve = pd.Series(list(series), index=index)

    # Define the dotted line (constant value)
    dotted_line = revenue_threshold().loc[apartment_code]['Threshold (EUR)']

    # Create the figure
    fig = go.Figure()

    # Add the curve
    fig.add_trace(go.Scatter(
        x=curve.index, y=curve,
        mode='lines',
        name='AirBnB Revenue',
        line=dict(color='blue', width=2)
    ))

    # Add the dotted line
    fig.add_trace(go.Scatter(
        x=curve.index, y=[dotted_line] * len(curve),
        mode='lines',
        name='Baseline',
        fill='tonexty',
        fillcolor='rgba(255, 0, 0, 0.2)',
        line=dict(color='black', width=2, dash='dot')
    ))

    # Customize the layout
    fig.update_layout(
        title='Revenue overview',
        xaxis_title='Index',
        yaxis_title='Values',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )

    # Show the figure
    #fig.show()
    return fig


def plot_area(year=2022):
    selcted_columns = get_pivot().columns[get_pivot().columns.year==year]
    pivot = get_pivot()[selcted_columns]
    pivot.reset_index(inplace=True)
    pivot.rename_axis(None, axis=1, inplace=True)
    df = pivot.melt(id_vars=['Apartment_code'], var_name='Month', value_name='Revenue')
    df.Month = df.Month.astype(str)
    fig = px.area(df, x="Month", y="Revenue", color='Apartment_code')
    return fig
