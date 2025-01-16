import pandas as pd
import numpy as np
import calendar
import matplotlib.pyplot as plt
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
                elif value >= (row_threshold * 1.2):  # Greater than 20% above the row mean
                    color_criteria[i, j] = 2  # Green
                elif value <= (row_threshold * 0.8):  # Less than 20% below the row mean
                    color_criteria[i, j] = -2  # Red
                else:  # Between -20% and +20% of the row mean
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

def display_table(mode='Revenue', year=2022, owner='all'):
    '''Displays the table colored as an image'''
    if (owner=='Mohamed') | (owner=='Mounia'):
        full_df = full_df[full_df['Owner']==owner]

    full_pivot = get_pivot(pivot_type = mode)

    #Select only data for the selected year
    selected_time_range = full_pivot.columns[full_pivot.columns.year == year]
    df = full_pivot[selected_time_range].round(0).astype(int)


    if mode == 'Revenue':
        thresholds=revenue_threshold() #Extracting revenue averages
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
        Patch(color=colors_list[0], label=f"More than 20% over threshold"),
        Patch(color=colors_list[1], label="NA - No data"),
        Patch(color=colors_list[2], label=f"Around threshold"),
        Patch(color=colors_list[3], label=f"More than 20% threshold")
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

def display_perf():
    '''Displays the overall performance table'''
    df=get_perf_table()
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
