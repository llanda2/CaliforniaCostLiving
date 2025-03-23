from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import dcc, html, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


def register_callbacks(app, min_wage_df, energy_gas_df, healthcare_df, housing_df, leisure_df, income_df):
    # Tab selection callback
    @app.callback(
        Output("tab-content", "children"),
        [Input("tabs", "value")]
    )
    def render_tab_content(tab):
        if tab == "income-tab":
            return create_income_tab(income_df, min_wage_df)
        elif tab == "expenses-tab":
            return create_expenses_tab(energy_gas_df, healthcare_df, housing_df, leisure_df)
        elif tab == "comparative-tab":
            return create_comparative_tab(income_df, energy_gas_df, healthcare_df, housing_df, leisure_df)

    # Income tab callbacks
    @app.callback(
        Output("income-chart", "figure"),
        [Input("income-year-slider", "value")]
    )
    def update_income_chart(years):
        filtered_df = income_df[(income_df['Year'] >= years[0]) & (income_df['Year'] <= years[1])]
        fig = px.line(filtered_df, x='Year', y='MedianIncome',
                      title='Median Household Income in California')
        return fig

    # Expenses tab callbacks
    @app.callback(
        Output("expenses-chart", "figure"),
        [Input("expense-categories", "value"),
         Input("expense-year-slider", "value")]
    )
    def update_expenses_chart(categories, years):
        # Create a figure to hold all the expense data
        fig = go.Figure()

        # Add each selected category to the chart
        if 'housing' in categories and 'Year' in housing_df.columns:
            filtered = housing_df[(housing_df['Year'] >= years[0]) & (housing_df['Year'] <= years[1])]
            fig.add_trace(go.Scatter(x=filtered['Year'], y=filtered['Cost'], mode='lines', name='Housing & Utilities'))

        if 'energy' in categories and 'Year' in energy_gas_df.columns:
            filtered = energy_gas_df[(energy_gas_df['Year'] >= years[0]) & (energy_gas_df['Year'] <= years[1])]
            fig.add_trace(go.Scatter(x=filtered['Year'], y=filtered['Cost'], mode='lines', name='Energy & Gas'))

        if 'healthcare' in categories and 'Year' in healthcare_df.columns:
            filtered = healthcare_df[(healthcare_df['Year'] >= years[0]) & (healthcare_df['Year'] <= years[1])]
            fig.add_trace(go.Scatter(x=filtered['Year'], y=filtered['Cost'], mode='lines', name='Healthcare'))

        if 'leisure' in categories and 'Year' in leisure_df.columns:
            filtered = leisure_df[(leisure_df['Year'] >= years[0]) & (leisure_df['Year'] <= years[1])]
            fig.add_trace(go.Scatter(x=filtered['Year'], y=filtered['Cost'], mode='lines', name='Leisure Goods'))

        fig.update_layout(title='Expense Categories Over Time',
                          xaxis_title='Year',
                          yaxis_title='Cost (per capita)')
        return fig

    # Add more callbacks for comparative tab as needed


# Helper functions to create tab layouts
def create_income_tab(income_df, min_wage_df):
    min_year = min(income_df['Year'].min() if 'Year' in income_df.columns else 2000,
                   min_wage_df['Year'].min() if 'Year' in min_wage_df.columns else 2000)
    max_year = max(income_df['Year'].max() if 'Year' in income_df.columns else 2023,
                   min_wage_df['Year'].max() if 'Year' in min_wage_df.columns else 2023)

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3("Income Analysis"),
                html.P("Explore how median household income in California has changed over time.")
            ])
        ]),

        dbc.Row([
            dbc.Col([
                html.Label("Select Year Range:"),
                dcc.RangeSlider(
                    id='income-year-slider',
                    min=min_year,
                    max=max_year,
                    step=1,
                    marks={i: str(i) for i in range(int(min_year), int(max_year) + 1, 2)},
                    value=[min_year, max_year]
                )
            ])
        ]),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='income-chart')
            ], width=12, lg=6),

            dbc.Col([
                html.H4("Raw Income Data"),
                dash_table.DataTable(
                    id='income-table',
                    columns=[{"name": i, "id": i} for i in income_df.columns],
                    data=income_df.to_dict('records'),
                    page_size=10,
                    style_table={'overflowX': 'auto'}
                )
            ], width=12, lg=6)
        ])
    ])


def create_expenses_tab(energy_gas_df, healthcare_df, housing_df, leisure_df):
    # Determine min and max years across all datasets
    year_columns = []
    for df in [energy_gas_df, healthcare_df, housing_df, leisure_df]:
        if 'Year' in df.columns:
            year_columns.append(df['Year'])

    if year_columns:
        all_years = pd.concat(year_columns)
        min_year = all_years.min()
        max_year = all_years.max()
    else:
        min_year = 2000
        max_year = 2023

    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3("Expenses Analysis"),
                html.P("Explore how different expense categories have changed over time in California.")
            ])
        ]),

        dbc.Row([
            dbc.Col([
                html.Label("Select Expense Categories:"),
                dcc.Checklist(
                    id='expense-categories',
                    options=[
                        {'label': ' Housing & Utilities', 'value': 'housing'},
                        {'label': ' Energy & Gas', 'value': 'energy'},
                        {'label': ' Healthcare', 'value': 'healthcare'},
                        {'label': ' Leisure Goods', 'value': 'leisure'}
                    ],
                    value=['housing', 'healthcare', 'energy'],
                    inline=True
                )
            ])
        ]),

        dbc.Row([
            dbc.Col([
                html.Label("Select Year Range:"),
                dcc.RangeSlider(
                    id='expense-year-slider',
                    min=min_year,
                    max=max_year,
                    step=1,
                    marks={i: str(i) for i in range(int(min_year), int(max_year) + 1, 2)},
                    value=[min_year, max_year]
                )
            ])
        ]),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id='expenses-chart')
            ], width=12)
        ])
    ])


def create_comparative_tab(income_df, energy_gas_df, healthcare_df, housing_df, leisure_df):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H3("Comparative Analysis"),
                html.P("Compare income trends with expense categories over time.")
            ])
        ]),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id='comparative-chart',
                    figure=px.line(title="Income vs. Expenses Over Time")
                )
            ])
        ])
    ])