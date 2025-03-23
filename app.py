import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Load datasets
min_wage_df = pd.read_csv('data/CaliMinWage.csv')
energy_gas_df = pd.read_csv('data/energyGasPC.csv')
healthcare_df = pd.read_csv('data/healthCarePC.csv')
housing_df = pd.read_csv('data/housingUtliPC.csv')
leisure_df = pd.read_csv('data/leisureGoodsPC.csv')
income_df = pd.read_csv('data/medianHouseIncomeCal.csv')

# App layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col(html.H1("California Cost of Living Dashboard"), className="text-center my-4")
    ]),

    # Tabs
    dbc.Row([
        dbc.Col(
            dcc.Tabs(id="tabs", value="income-tab", children=[
                dcc.Tab(label="Income Analysis", value="income-tab"),
                dcc.Tab(label="Expenses Analysis", value="expenses-tab"),
                dcc.Tab(label="Comparative Analysis", value="comparative-tab"),
            ])
        )
    ]),

    # Tab content container
    dbc.Row([
        dbc.Col(html.Div(id="tab-content"))
    ]),

    # Footer
    dbc.Row([
        dbc.Col(html.Footer("Data sources: California Economic Data"), className="text-center mt-4")
    ])
], fluid=True)

# Import callbacks
from callbacks import register_callbacks

register_callbacks(app, min_wage_df, energy_gas_df, healthcare_df, housing_df, leisure_df, income_df)

# Custom server run approach to avoid dotenv issues
if __name__ == '__main__':
    # Method 1: Direct use of Werkzeug
    import werkzeug.serving
    print("Dash is running on http://127.0.0.1:8050/")
    werkzeug.serving.run_simple('127.0.0.1', 8050, app.server, use_reloader=True, use_debugger=True)