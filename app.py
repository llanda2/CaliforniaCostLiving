import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "California Cost of Living Dashboard"

# Load datasets
min_wage_df = pd.read_csv('data/CaliMinWage.csv')
min_wage_df['observation_date'] = pd.to_datetime(min_wage_df['observation_date'])

energy_gas_df = pd.read_csv('data/energyGasPC.csv')
energy_gas_df['observation_date'] = pd.to_datetime(energy_gas_df['observation_date'])

healthcare_df = pd.read_csv('data/healthCarePC.csv')
healthcare_df['observation_date'] = pd.to_datetime(healthcare_df['observation_date'])

housing_df = pd.read_csv('data/housingUtliPC.csv')
housing_df['observation_date'] = pd.to_datetime(housing_df['observation_date'])

leisure_df = pd.read_csv('data/leisureGoodsPC.csv')
leisure_df['observation_date'] = pd.to_datetime(leisure_df['observation_date'])

income_df = pd.read_csv('data/medianHouseIncomeCal.csv')
income_df['observation_date'] = pd.to_datetime(income_df['observation_date'])

# App layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("California Cost of Living Dashboard", className="text-center my-3"),
            html.P("Explore changes in income, expenses, and affordability factors over time",
                   className="text-center lead")
        ])
    ]),

    html.Hr(),

    # Date Range Selector
    dbc.Row([
        dbc.Col([
            html.H5("Select Date Range"),
            dcc.RangeSlider(
                id='year-slider',
                min=min(min_wage_df['observation_date'].dt.year.min(),
                        income_df['observation_date'].dt.year.min()),
                max=max(min_wage_df['observation_date'].dt.year.max(),
                        income_df['observation_date'].dt.year.max()),
                step=1,
                marks={i: str(i) for i in range(
                    min(min_wage_df['observation_date'].dt.year.min(),
                        income_df['observation_date'].dt.year.min()),
                    max(min_wage_df['observation_date'].dt.year.max(),
                        income_df['observation_date'].dt.year.max()) + 1,
                    5)},
                value=[1990, 2020]  # Default selection
            ),
        ], width=12, md=10, className="mx-auto mb-4")
    ]),

    # Analysis Controls
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Analysis Options"),
                dbc.CardBody([
                    html.Label("Select Expense Categories:"),
                    dbc.Checklist(
                        id='expense-checklist',
                        options=[
                            {'label': ' Energy & Gas', 'value': 'energy'},
                            {'label': ' Healthcare', 'value': 'healthcare'},
                            {'label': ' Housing & Utilities', 'value': 'housing'},
                            {'label': ' Leisure Goods', 'value': 'leisure'}
                        ],
                        value=['energy', 'healthcare', 'housing'],
                        inline=True
                    ),
                    html.Br(),
                    html.Label("View Option:"),
                    dbc.RadioItems(
                        id='view-radio',
                        options=[
                            {'label': ' Actual Values', 'value': 'actual'},
                            {'label': ' Percentage Change', 'value': 'percent'},
                            {'label': ' Inflation Adjusted', 'value': 'adjusted'}
                        ],
                        value='actual',
                        inline=True
                    ),
                ])
            ]),
        ], width=12, lg=5),

        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Key Metrics"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            html.H6("Median Income Growth", className="text-muted"),
                            html.H4(id='income-growth-value', className="text-primary"),
                        ], width=6),
                        dbc.Col([
                            html.H6("Housing Cost Growth", className="text-muted"),
                            html.H4(id='housing-growth-value', className="text-danger"),
                        ], width=6),
                    ]),
                    html.Br(),
                    dbc.Row([
                        dbc.Col([
                            html.H6("Income-to-Housing Ratio", className="text-muted"),
                            html.H4(id='income-housing-ratio', className="text-success"),
                        ], width=6),
                        dbc.Col([
                            html.H6("Minimum Wage Growth", className="text-muted"),
                            html.H4(id='min-wage-growth', className="text-info"),
                        ], width=6),
                    ]),
                ])
            ]),
        ], width=12, lg=7),
    ], className="mb-4"),

    # Tabs
    dbc.Tabs([
        dbc.Tab(label="Income Analysis", tab_id="income-tab", children=[
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='income-chart'),
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H5("Median Household Income Data", className="mt-3"),
                    dash_table.DataTable(
                        id='income-table',
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'textAlign': 'left',
                            'padding': '10px',
                            'minWidth': '100px', 'width': '150px', 'maxWidth': '200px',
                        },
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        },
                        page_size=10,
                    ),
                ], width=12)
            ]),
        ]),

        dbc.Tab(label="Expenses Analysis", tab_id="expenses-tab", children=[
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='expenses-chart'),
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H5("Expense Comparison", className="mt-3"),
                    dash_table.DataTable(
                        id='expenses-table',
                        style_table={'overflowX': 'auto'},
                        style_cell={
                            'textAlign': 'left',
                            'padding': '10px',
                            'minWidth': '100px', 'width': '150px', 'maxWidth': '200px',
                        },
                        style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                        },
                        page_size=10,
                    ),
                ], width=12)
            ]),
        ]),

        dbc.Tab(label="Comparative Analysis", tab_id="comparative-tab", children=[
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='comparison-chart'),
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col([
                    html.H5("Income vs. Expenses Analysis", className="mt-3"),
                    html.P("This chart shows how income has changed relative to various expenses over time."),
                    html.P(
                        "A higher income-to-expense ratio indicates better affordability, while a declining ratio suggests expenses are growing faster than income."),
                ], width=12, md=6),
                dbc.Col([
                    dcc.Graph(id='ratio-chart'),
                ], width=12, md=6)
            ]),
        ]),

        dbc.Tab(label="Data Sources", tab_id="data-tab", children=[
            dbc.Row([
                dbc.Col([
                    html.H4("Data Sources and Documentation", className="mt-3"),
                    html.Hr(),
                    html.H5("California Economic Data Sets"),
                    html.Ul([
                        html.Li([
                            html.Strong("Minimum Wage Data: "),
                            "Federal Reserve Economic Data (FRED), State Minimum Wage Rate for California"
                        ]),
                        html.Li([
                            html.Strong("Energy & Gas Data: "),
                            "Federal Reserve Economic Data (FRED), Per Capita Personal Consumption Expenditures: Gasoline and Other Energy Goods in California"
                        ]),
                        html.Li([
                            html.Strong("Healthcare Data: "),
                            "Federal Reserve Economic Data (FRED), Per Capita Personal Consumption Expenditures: Healthcare in California"
                        ]),
                        html.Li([
                            html.Strong("Housing & Utilities Data: "),
                            "Federal Reserve Economic Data (FRED), Per Capita Personal Consumption Expenditures: Housing and Utilities in California"
                        ]),
                        html.Li([
                            html.Strong("Leisure Goods Data: "),
                            "Federal Reserve Economic Data (FRED), Per Capita Personal Consumption Expenditures: Recreational Goods and Vehicles in California"
                        ]),
                        html.Li([
                            html.Strong("Median Household Income Data: "),
                            "Federal Reserve Economic Data (FRED), Median Household Income in California"
                        ]),
                    ]),
                    html.Hr(),
                    html.H5("Data License Information"),
                    html.P([
                        "All datasets used in this dashboard are from the Federal Reserve Bank of St. Louis' FRED database, available under their ",
                        html.A("Terms of Use", href="https://fred.stlouisfed.org/legal/"),
                        ". FRED® data is available under a mixed license where some components are licensed under an ODC-BY license, while others require attribution to the original source."
                    ]),
                    html.P([
                        "Citation: Federal Reserve Bank of St. Louis, Various Economic Data Series for California, retrieved from FRED, Federal Reserve Bank of St. Louis, [Accessed ",
                        f"{datetime.now().strftime('%B %d, %Y')}",
                        "]."
                    ]),
                ], width=12)
            ]),
        ]),

    ], id="tabs", active_tab="income-tab", className="mb-4"),

    # Footer
    html.Hr(),
    dbc.Row([
        dbc.Col([
            html.Footer([
                html.P("© 2023 California Cost of Living Dashboard", className="mb-0"),
                html.P([
                    "Data sources: Federal Reserve Economic Data (FRED) | ",
                    html.A("GitHub Repository", href="#")
                ], className="small text-muted")
            ], className="text-center py-3")
        ])
    ])
], fluid=True)

# Import callbacks
from callbacks import register_callbacks

register_callbacks(app, min_wage_df, energy_gas_df, healthcare_df, housing_df, leisure_df, income_df)

# Start the app
if __name__ == '__main__':
    # Method 1: Direct use of Werkzeug
    import werkzeug.serving
    print("Dash is running on http://127.0.0.1:8050/")
    werkzeug.serving.run_simple('127.0.0.1', 8050, app.server, use_reloader=True, use_debugger=True)