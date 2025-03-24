from dash import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import html

def register_callbacks(app, min_wage_df, energy_gas_df, healthcare_df, housing_df, leisure_df, income_df):
    """Register all callbacks for the dashboard"""

    # Helper functions
    def filter_by_year_range(df, start_year, end_year):
        """Filter dataframe by year range"""
        return df[(df['observation_date'].dt.year >= start_year) &
                  (df['observation_date'].dt.year <= end_year)]

    def calculate_growth_percentage(series):
        """Calculate percentage growth from first to last value"""
        if len(series) < 2:
            return 0
        first_val = series.iloc[0]
        last_val = series.iloc[-1]
        if first_val == 0:
            return 0
        return ((last_val - first_val) / first_val) * 100

    def adjust_for_inflation(df, value_column, base_year=2020):
        """Apply inflation adjustment to convert values to base_year dollars"""
        # This is a simplified inflation adjustment
        # In a real app, you would use actual CPI or inflation data
        df_copy = df.copy()

        # Simplified inflation factors (approx. 2.5% annual inflation)
        years = df_copy['observation_date'].dt.year
        # Create adjustment factors (further from base_year = larger adjustment)
        adjustment_factors = np.power(1.025, base_year - years)

        # Apply adjustment
        df_copy[value_column] = df_copy[value_column] * adjustment_factors
        return df_copy

    # Callback for Income Chart and Table
    @app.callback(
        [Output('income-chart', 'figure'),
         Output('income-table', 'data'),
         Output('income-table', 'columns'),
         Output('income-growth-value', 'children')],
        [Input('year-slider', 'value'),
         Input('view-radio', 'value')]
    )
    def update_income_tab(years, view_option):
        start_year, end_year = years
        filtered_df = filter_by_year_range(income_df, start_year, end_year)

        # Create a copy for display
        display_df = filtered_df.copy()

        # Calculate growth percentage
        if len(filtered_df) > 1:
            income_col = [col for col in filtered_df.columns if col != 'observation_date'][0]
            growth_pct = calculate_growth_percentage(filtered_df[income_col])
            growth_text = f"{growth_pct:.1f}%"
        else:
            growth_text = "N/A"

        # Handle view options
        if view_option == 'percent':
            if len(filtered_df) > 1:
                income_col = [col for col in filtered_df.columns if col != 'observation_date'][0]
                first_val = filtered_df[income_col].iloc[0]
                display_df[income_col] = ((filtered_df[income_col] - first_val) / first_val) * 100
                y_title = "Percent Change (%)"
            else:
                y_title = "Median Household Income ($)"
        elif view_option == 'adjusted':
            # Apply inflation adjustment
            income_col = [col for col in filtered_df.columns if col != 'observation_date'][0]
            display_df = adjust_for_inflation(filtered_df, income_col)
            y_title = "Inflation-Adjusted Median Household Income (2020 $)"
        else:
            y_title = "Median Household Income ($)"

        # Create figure
        fig = px.line(
            display_df,
            x='observation_date',
            y=[col for col in display_df.columns if col != 'observation_date'][0],
            title=f"California Median Household Income ({start_year}-{end_year})",
            labels={'observation_date': 'Year', 'value': y_title}
        )

        # Add this line to format the y-axis ticks with commas
        fig.update_layout(
            xaxis_title="Year",
            yaxis_title=y_title,
            template="plotly_white",
            legend_title_text="",
            hovermode="x unified",
            yaxis=dict(
                tickformat=",d"  # This formats numbers with commas as thousand separators
            )
        )

        # Prepare table data
        display_df['Year'] = display_df['observation_date'].dt.year
        table_df = display_df.drop('observation_date', axis=1)

        # Format the table column headers
        income_col = [col for col in table_df.columns if col != 'Year'][0]
        columns = [{"name": "Year", "id": "Year"}]

        if view_option == 'percent':
            columns.append({"name": "Percent Change (%)", "id": income_col})
        elif view_option == 'adjusted':
            columns.append({"name": "Adjusted Income (2020 $)", "id": income_col})
        else:
            columns.append({"name": "Median Income ($)", "id": income_col})

        # Sort by year
        table_df = table_df.sort_values('Year')

        return fig, table_df.to_dict('records'), columns, growth_text

    # Remaining callbacks (kept the same)...
    # Callback for Expenses Chart and Table
    @app.callback(
        [Output('expenses-chart', 'figure'),
         Output('expenses-table', 'data'),
         Output('expenses-table', 'columns'),
         Output('housing-growth-value', 'children')],
        [Input('year-slider', 'value'),
         Input('expense-checklist', 'value'),
         Input('view-radio', 'value')]
    )
    def update_expenses_tab(years, selected_expenses, view_option):
        start_year, end_year = years

        # Map expense selection to dataframes
        expense_map = {
            'energy': ('Energy & Gas', energy_gas_df),
            'healthcare': ('Healthcare', healthcare_df),
            'housing': ('Housing & Utilities', housing_df),
            'leisure': ('Leisure Goods', leisure_df)
        }

        # Filter selected expenses by year range
        filtered_expenses = {}
        for key, (label, df) in expense_map.items():
            if key in selected_expenses:
                filtered_df = filter_by_year_range(df, start_year, end_year)
                filtered_expenses[label] = filtered_df

        # Calculate housing growth for the KPI
        if 'housing' in selected_expenses and len(filtered_expenses['Housing & Utilities']) > 1:
            housing_col = \
                [col for col in filtered_expenses['Housing & Utilities'].columns if col != 'observation_date'][0]
            housing_growth = calculate_growth_percentage(filtered_expenses['Housing & Utilities'][housing_col])
            housing_growth_text = f"{housing_growth:.1f}%"
        else:
            housing_growth_text = "N/A"

        # Create figure data
        fig = go.Figure()

        # Prepare table data
        merged_data = []
        all_years = set()

        for label, df in filtered_expenses.items():
            expense_col = [col for col in df.columns if col != 'observation_date'][0]

            # Handle view options
            display_df = df.copy()

            if view_option == 'percent':
                if len(df) > 1:
                    first_val = df[expense_col].iloc[0]
                    if first_val != 0:  # Avoid division by zero
                        display_df[expense_col] = ((df[expense_col] - first_val) / first_val) * 100
                y_axis_title = "Percent Change (%)"
            elif view_option == 'adjusted':
                display_df = adjust_for_inflation(df, expense_col)
                y_axis_title = "Inflation-Adjusted Value (2020 $)"
            else:
                y_axis_title = "Expenses ($)"

            # Add trace to figure
            fig.add_trace(go.Scatter(
                x=display_df['observation_date'],
                y=display_df[expense_col],
                mode='lines+markers',
                name=label
            ))

            # Collect data for table
            for _, row in display_df.iterrows():
                year = row['observation_date'].year
                all_years.add(year)

                # Find or create entry for this year
                year_entry = next((entry for entry in merged_data if entry.get('Year') == year), None)
                if year_entry is None:
                    year_entry = {'Year': year}
                    merged_data.append(year_entry)

                # Add value for this expense category
                year_entry[label] = round(row[expense_col], 2)

        # Sort years for table
        merged_data.sort(key=lambda x: x['Year'])

        # Create column definitions for table
        table_columns = [{"name": "Year", "id": "Year"}]
        for label in filtered_expenses.keys():
            if view_option == 'percent':
                display_name = f"{label} (% Change)"
            elif view_option == 'adjusted':
                display_name = f"{label} (2020 $)"
            else:
                display_name = label
            table_columns.append({"name": display_name, "id": label})

        # Update layout
        fig.update_layout(
            title=f"California Expenses Comparison ({start_year}-{end_year})",
            xaxis_title="Year",
            yaxis_title=y_axis_title,
            template="plotly_white",
            hovermode="x unified",
            yaxis=dict(
                tickformat=',',  # This adds commas to the y-axis values
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        return fig, merged_data, table_columns, housing_growth_text

    # Callback for Comparative Analysis Charts
    @app.callback(
        [Output('comparison-chart', 'figure'),
         Output('ratio-chart', 'figure'),
         Output('income-housing-ratio', 'children'),
         Output('min-wage-growth', 'children')],
        [Input('year-slider', 'value'),
         Input('expense-checklist', 'value'),
         Input('view-radio', 'value')]
    )
    def update_comparative_tab(years, selected_expenses, view_option):
        start_year, end_year = years

        # Filter data
        filtered_income = filter_by_year_range(income_df, start_year, end_year)
        filtered_min_wage = filter_by_year_range(min_wage_df, start_year, end_year)

        # Map expense selection to dataframes
        expense_map = {
            'energy': ('Energy & Gas', energy_gas_df),
            'healthcare': ('Healthcare', healthcare_df),
            'housing': ('Housing & Utilities', housing_df),
            'leisure': ('Leisure Goods', leisure_df)
        }

        # Filter selected expenses by year range
        filtered_expenses = {}
        for key, (label, df) in expense_map.items():
            if key in selected_expenses:
                filtered_df = filter_by_year_range(df, start_year, end_year)
                filtered_expenses[label] = filtered_df

        # Prepare comparative analysis
        comparison_fig = go.Figure()
        ratio_fig = go.Figure()

        # Get income column name
        income_col = [col for col in filtered_income.columns if col != 'observation_date'][0]

        # Get min wage column name
        min_wage_col = [col for col in filtered_min_wage.columns if col != 'observation_date'][0]

        # Calculate min wage growth for KPI
        if len(filtered_min_wage) > 1:
            min_wage_growth = calculate_growth_percentage(filtered_min_wage[min_wage_col])
            min_wage_growth_text = f"{min_wage_growth:.1f}%"
        else:
            min_wage_growth_text = "N/A"

        # Add income trace
        display_income = filtered_income.copy()

        if view_option == 'percent':
            if len(filtered_income) > 1:
                first_val = filtered_income[income_col].iloc[0]
                display_income[income_col] = ((filtered_income[income_col] - first_val) / first_val) * 100
            y_title = "Percent Change (%)"
        elif view_option == 'adjusted':
            display_income = adjust_for_inflation(filtered_income, income_col)
            y_title = "Inflation-Adjusted Value (2020 $)"
        else:
            y_title = "Value ($)"

        comparison_fig.add_trace(go.Scatter(
            x=display_income['observation_date'],
            y=display_income[income_col],
            mode='lines',
            name='Median Income',
            line=dict(color='rgb(0, 128, 0)', width=3)
        ))

        # Add minimum wage trace
        display_min_wage = filtered_min_wage.copy()

        if view_option == 'percent':
            if len(filtered_min_wage) > 1:
                first_val = filtered_min_wage[min_wage_col].iloc[0]
                display_min_wage[min_wage_col] = ((filtered_min_wage[min_wage_col] - first_val) / first_val) * 100
        elif view_option == 'adjusted':
            display_min_wage = adjust_for_inflation(filtered_min_wage, min_wage_col)

        # Scale min wage to annual full-time equivalent (40hrs * 52 weeks)
        display_min_wage[min_wage_col] = display_min_wage[min_wage_col] * 40 * 52

        comparison_fig.add_trace(go.Scatter(
            x=display_min_wage['observation_date'],
            y=display_min_wage[min_wage_col],
            mode='lines',
            name='Full-time Min. Wage',
            line=dict(color='rgb(128, 128, 0)', width=2, dash='dot')
        ))

        # Add expense traces and calculate ratios
        housing_income_ratio = "N/A"  # Default value

        ratios_data = {}
        years_list = []

        # Add expense traces
        for label, df in filtered_expenses.items():
            expense_col = [col for col in df.columns if col != 'observation_date'][0]
            display_df = df.copy()

            if view_option == 'percent':
                if len(df) > 1:
                    first_val = df[expense_col].iloc[0]
                    display_df[expense_col] = ((df[expense_col] - first_val) / first_val) * 100
            elif view_option == 'adjusted':
                display_df = adjust_for_inflation(df, expense_col)

            comparison_fig.add_trace(go.Scatter(
                x=display_df['observation_date'],
                y=display_df[expense_col],
                mode='lines',
                name=label
            ))

            # Calculate income-to-expense ratios
            if label == 'Housing & Utilities' and len(df) > 0 and len(filtered_income) > 0:
                # For the KPI, calculate the most recent income-to-housing ratio
                if len(df) > 0 and len(filtered_income) > 0:
                    # Get the common years
                    housing_years = set(df['observation_date'].dt.year)
                    income_years = set(filtered_income['observation_date'].dt.year)
                    common_years = sorted(housing_years.intersection(income_years))

                    if common_years:
                        latest_year = max(common_years)
                        latest_housing = df[df['observation_date'].dt.year == latest_year][expense_col].iloc[0]
                        latest_income = \
                            filtered_income[filtered_income['observation_date'].dt.year == latest_year][
                                income_col].iloc[0]

                        # Calculate ratio (income divided by annual housing cost)
                        if latest_housing > 0:
                            ratio = latest_income / latest_housing
                            housing_income_ratio = f"{ratio:.2f}"

            # Calculate ratio for each year where both income and expense data exist
            ratio_series = []

            # Initialize lists for years and ratio values
            year_list = []
            ratio_list = []

            # Find common years between income and this expense category
            for year in sorted(set(df['observation_date'].dt.year)):
                income_year_data = filtered_income[filtered_income['observation_date'].dt.year == year]
                expense_year_data = df[df['observation_date'].dt.year == year]

                if not income_year_data.empty and not expense_year_data.empty:
                    year_income = income_year_data[income_col].iloc[0]
                    year_expense = expense_year_data[expense_col].iloc[0]

                    if year_expense > 0:
                        ratio = year_income / year_expense

                        year_list.append(year)
                        ratio_list.append(ratio)

            if year_list:
                ratios_data[label] = ratio_list
                if not years_list:
                    years_list = year_list

        # Update comparison chart layout
        comparison_fig.update_layout(
            title=f"Income vs. Expenses Comparison ({start_year}-{end_year})",
            xaxis_title="Year",
            yaxis_title=y_title,
            template="plotly_white",
            hovermode="x unified",
            yaxis=dict(
                tickformat=',',  # This adds commas to the y-axis values
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        # Create ratios chart
        for label, ratio_values in ratios_data.items():
            ratio_fig.add_trace(go.Scatter(
                x=[pd.Timestamp(year=year, month=1, day=1) for year in years_list],
                y=ratio_values,
                mode='lines+markers',
                name=f"Income-to-{label} Ratio"
            ))

        ratio_fig.update_layout(
            title=f"Income-to-Expense Ratios ({start_year}-{end_year})",
            xaxis_title="Year",
            yaxis_title="Ratio (Income / Expense)",
            template="plotly_white",
            hovermode="x unified",
            yaxis=dict(
                tickformat=',',  # This adds commas to the y-axis values
            ),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        return comparison_fig, ratio_fig, housing_income_ratio, min_wage_growth_text

    # New callback for income comparison
    @app.callback(
        [Output("income-comparison-result", "children"),
         Output("income-comparison-chart", "figure")],
        [Input("personal-income-input", "value"),
         Input("year-slider", "value")]
    )
    def update_income_comparison(personal_income, years_range):
        if not personal_income:
            return html.Div(), {}

        # Define COLORS dictionary if it doesn't exist in your current scope
        COLORS = {
            "stocks": "#1f77b4",  # Blue
            "inflation": "#ff7f0e",  # Orange
            "housing": "#2ca02c",  # Green
            "energy": "#d62728",  # Red
            "healthcare": "#9467bd",  # Purple
            "leisure": "#8c564b"  # Brown
        }

        # Filter income data based on selected years
        start_year, end_year = years_range
        filtered_income = filter_by_year_range(income_df, start_year, end_year)

        # Get latest median income value
        income_col = [col for col in filtered_income.columns if col != 'observation_date'][0]
        latest_income = filtered_income.iloc[-1][income_col]
        latest_year = filtered_income.iloc[-1]['observation_date'].year

        # Calculate income comparison metrics
        income_ratio = (personal_income / latest_income) * 100
        income_difference = personal_income - latest_income

        # Determine affordability tier and message
        if income_ratio < 50:
            tier = "significantly below"
            tier_class = "text-danger"
            message = f"Your income is significantly below California's median, which may present affordability challenges in many parts of the state."
        elif income_ratio < 80:
            tier = "below"
            tier_class = "text-warning"
            message = f"Your income is below California's median, which may limit housing options in higher-cost regions."
        elif income_ratio < 120:
            tier = "near"
            tier_class = "text-info"
            message = f"Your income is near California's median, providing moderate affordability in many areas."
        else:
            tier = "above"
            tier_class = "text-success"
            message = f"Your income exceeds California's median, offering greater flexibility in most housing markets."

        # Create comparison result component
        comparison_result = html.Div([
            html.H5([
                f"Your income is ",
                html.Span(f"{tier} ", className=tier_class),
                f"California's {latest_year} median income of ${latest_income:,.0f}"
            ]),
            html.P([
                f"You earn ",
                html.Strong(f"${abs(income_difference):,.0f} {'more' if income_difference >= 0 else 'less'} "),
                f"than the median California household. ",
                f"Your income is ",
                html.Strong(f"{income_ratio:.1f}% "),
                f"of the state median."
            ]),
            html.P(message, className="mt-2 font-italic")
        ])

        # Create comparison chart
        income_years = filtered_income['observation_date'].dt.year.tolist()
        income_values = filtered_income[income_col].tolist()

        # Create the figure
        fig = go.Figure()

        # Add income trend line
        fig.add_trace(go.Scatter(
            x=income_years,
            y=income_values,
            mode='lines+markers',
            name='CA Median Income',
            line=dict(color=COLORS["stocks"], width=3),
        ))

        # Add user's income as a horizontal line
        fig.add_trace(go.Scatter(
            x=[min(income_years), max(income_years)],
            y=[personal_income, personal_income],
            mode='lines',
            name='Your Income',
            line=dict(color=COLORS["inflation"], width=2, dash='dash'),
        ))

        # Update layout
        fig.update_layout(
            title=f"Your Income vs. California Median Household Income",
            xaxis_title="Year",
            yaxis_title="Annual Income ($)",
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=40, r=40, t=40, b=40),
            height=300,
            template="plotly_white",
            hovermode="x unified"
        )

        # Add dollar sign format to y-axis
        fig.update_yaxes(tickprefix="$", tickformat=",")

        return comparison_result, fig