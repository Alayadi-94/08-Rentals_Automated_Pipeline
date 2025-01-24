from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd

# Assuming these are imported from your custom functions
from functions.display import plot_revenue

# Sample list of strings for the dropdown
dropdown_apartments = ['Alia 22', 'Alia 36', 'Alia 37', 'Alia 41', 'Menara 15', 'Oumnia A2 17']
dropdown_years = ['2022', '2023', '2024']

app = Dash()

# Define the layout of the Dash app
app.layout = html.Div([
    html.H1(children='AirBnB Dashboard', style={'textAlign': 'center'}),

    # Top section: Left (Graph + Dropdown) and Right (3 Dropdowns)
    html.Div([
        # Top Left: Graph with one dropdown above it
        html.Div([
            dcc.Dropdown(
                options=[{'label': opt, 'value': opt} for opt in dropdown_apartments],
                value='Alia 22',  # Default value
                id='dropdown-selection',
                style={'marginBottom': '10px'}  # Space between dropdown and graph
            ),
            dcc.Graph(id='graph-content'),
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),

        # Top Right: 3 Dropdowns
        html.Div([
            html.Label("Select Option 1:"),
            dcc.Dropdown(
                options=[{'label': opt, 'value': opt} for opt in dropdown_apartments],
                value='Alia 22',
                id='image-dropdown-1',
                style={'marginBottom': '10px'}
            ),
            html.Label("Select Option 2:"),
            dcc.Dropdown(
                options=[{'label': opt, 'value': opt} for opt in dropdown_apartments],
                value='Alia 36',
                id='image-dropdown-2',
                style={'marginBottom': '10px'}
            ),
            html.Label("Select Option 3:"),
            dcc.Dropdown(
                options=[{'label': opt, 'value': opt} for opt in dropdown_apartments],
                value='Alia 37',
                id='image-dropdown-3'
            ),
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),
    ], style={'marginBottom': '30px'}),


    # Bottom section:
    html.Div([
        # Botom Left: Graph with one dropdown above it
        html.Div([
            dcc.Dropdown(
                options=[{'label': opt, 'value': opt} for opt in dropdown_apartments],
                value='Alia 22',  # Default value
                id='dropdown-selection',
                style={'marginBottom': '10px'}  # Space between dropdown and graph
            ),
            dcc.Graph(id='graph-content'),
        ], style={'width': '48%', 'display': 'inline-block', 'verticalAlign': 'top', 'padding': '10px'}),


        # Bottom Right
        html.Div([
            html.H3("Bottom Right Content"),
            # Add your content here
        ], style={'width': '48%', 'display': 'inline-block', 'padding': '10px', 'border': '1px solid #ccc'}),
    ]),
])

# Callback to update the graph based on dropdown selection
@callback(
    Output('graph-content', 'figure'),
    Input('dropdown-selection', 'value')
)
def update_graph(value):
    # Call the plot_revenue() function to generate the figure
    return plot_revenue(value)

if __name__ == '__main__':
    app.run(debug=True)
