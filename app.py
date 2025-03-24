# -*- coding: utf-8 -*-
from dash import Dash, dcc, html, dash_table, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.SKETCHY, dbc.icons.FONT_AWESOME],
)

# make dataframe from spreadsheet:
df = pd.read_csv("assets/Occupational employment and wages by major occupational group.csv")
df2 = pd.read_csv("assets/Median Earnings by Industry.csv")

# Rename the relevant columns for clarity
df2 = df2.rename(columns={
    "Industry Group": "Industry",
    "Gender": "Gender",
    "Median Earnings by Industry and Gender": "Median Earnings"
})

# Compute the average median earnings for each industry (combining men and women)
df_avg_earnings = df2.groupby("Industry")["Median Earnings"].mean().reset_index()

# Extract the "Major occupational group" column from the dataframe
major_occupational_groups = df["Major occupational group"].dropna().unique()

# Filter out "Total, all occupations" from the list
major_occupational_groups = [group for group in major_occupational_groups if group != "Total, all occupations"]

# Create options for the Dropdown
dropdown_options = [{"label": group, "value": group} for group in major_occupational_groups]

"""
==========================================================================
Figures
"""

# Line chart component
line_chart = dcc.Graph(
    id="income-line-chart",
    className="mt-4",
    config={"displayModeBar": False},
)

# Column chart component
column_chart = dcc.Graph(
    id="earnings-column-chart",
    className="mt-4",
    config={"displayModeBar": False},
)


"""
==========================================================================
Markdown Text
"""

learn_text = dcc.Markdown(
    """
    Welcome to the Santa Barbara Affordability Checker! This interactive dashboard helps you assess whether moving to Santa Barbara is a good financial fit for you. By comparing your income, cost of living, and industry earnings, you can make informed decisions about relocating. 
    
    Use the tools to explore key insights such as wage comparisons, median earnings by industry, and much more. Whether you're evaluating a new job offer or just curious about the area, this dashboard provides valuable information to help you plan your future with confidence.
    """
)

explore_text = dcc.Markdown(
    """
    Deciding whether to move to a new location can be a difficult decision, especially when considering factors like your income, cost of living, and career. With so many variables to weigh, it can be hard to know if a place will truly be the right fit. Use this explorer to assess if Santa Barbara is the home you've been searching for!
    """
)

data_table = dash_table.DataTable(
    columns=[{"name": col, "id": col} for col in df.columns],
    data=df.to_dict("records"),
    page_size=10,
    style_table={'overflowX': 'auto'},
)

footer = html.Div(
    dcc.Markdown(
        """
         This information is intended solely as general information for educational
        and entertainment purposes only and is not a substitute for professional advice and
        services from qualified financial services providers familiar with your financial
        situation.    
        """
    ),
    className="p-2 mt-5 bg-primary text-white small",
)

"""
==========================================================================
Make Tabs
"""

# ========= Learn Tab Components
learn_card = dbc.Card(
    [
        dbc.CardHeader("Begin Your Relocation Now"),
        dbc.CardBody(learn_text),
    ],
    className="mt-4",
)

# ========= Explore Tab Components
explore_card = dbc.Card(
    [
        dbc.CardHeader("Is Santa Barbara the Right Place for You? Find Out Now!"),
        dbc.CardBody([
            explore_text,

            # Row for input and label - hourly wage
            dbc.Row([
                dbc.Col([
                    html.Label("Enter Your Current Hourly Wage:"),
                ], width=6),

                dbc.Col([
                    dcc.Input(
                        id="current-hourly-wage",
                        type="number",
                        placeholder="Enter hourly wage",
                        min=0,
                        step=0.01,  # allows for decimal values
                        style={"width": "100%"}
                    ),
                ], width=6),
            ], className="mb-3"),

            # Row for input and label - cost of living
            dbc.Row([
                dbc.Col([
                    html.Label("Enter Your Estimated Total Cost of Living:"),
                    html.Label("(If you don't know your cost, you will be under Santa Barbara's average)")
                ], width=6),

                dbc.Col([
                    dcc.Input(
                        id="cost-of-living",
                        type="number",
                        placeholder="Enter total cost of living",
                        min=0,
                        step=0.01,
                        style={"width": "100%"}
                    ),
                ], width=6),
            ], className="mb-3"),

            # Dropdown for selecting major occupational group
            dcc.Dropdown(
                id="occupational-group-dropdown",
                options=dropdown_options,
                placeholder="Select an Industry",
                multi=False,  # single selection (change to True for multiple selections)
            ),

            # Button to trigger assessment
            dbc.Button(
                "Assess",
                id="assess-button",
                color="primary",
                className="mt-3",
                n_clicks=0
            ),

            # Output area for assessment result
            html.Div(
                id="assessment-result",
                className="mt-3",
                style={"font-weight": "bold"}
            )
        ]),
    ],
    className="mt-4",
)

# ========= Data Tab Components
data_card = dbc.Card(
    [
        dbc.CardHeader("Raw Data"),
        dbc.CardBody([
            data_table,
            html.Hr(),
            html.H4("Median Earnings by Industry"),
            dash_table.DataTable(
                columns=[{"name": col, "id": col} for col in df_avg_earnings.columns],
                data=df_avg_earnings.to_dict("records"),
                page_size=10,
                style_table={'overflowX': 'auto'},
            ),
        ]),
    ],
    className="mt-4",
)

# ========= Build tabs
tabs = dbc.Tabs(
    [
        dbc.Tab(learn_card, tab_id="tab1", label="Learn"),
        dbc.Tab(explore_card, tab_id="tab2", label="Explore"),
        dbc.Tab(data_card, tab_id="tab3", label="Data"),
    ],
    id="tabs",
    active_tab="tab1",
    className="mt-2",
)

"""
==========================================================================
Main Layout
"""

app.layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col([
                html.H2(
                    "Santa Barbara Affordability Checker",
                    className="text-center bg-primary text-white p-2",
                ),
                html.H4(
                    "Benjamin Yeom CS-150 Topics",
                    className="text-center mt-2"
                )
            ])
        ),
        dbc.Row(
            [
                dbc.Col(tabs, width=8, lg=7, className="mt-4 border"),
                dbc.Col(
                    dcc.Graph(
                        id="wage-bar-chart",
                        className="mt-4",
                        config={"displayModeBar": False},  # hide mode bar to keep it clean
                    ),
                    width=5,
                    className="mt-4"
                ),
            ],
            className="ms-1",
        ),
        dbc.Row(
            dbc.Col(column_chart, width=12, className="mt-4"),
        ),
        dbc.Row(dbc.Col(footer)),
    ],
    fluid=True,
)


"""
==========================================================================
Callbacks
"""
# ========= Callback to handle assessment logic and update both charts
@app.callback(
    [Output("assessment-result", "children"),
     Output("wage-bar-chart", "figure"),
     Output("earnings-column-chart", "figure")],
    Input("assess-button", "n_clicks"),
    State("current-hourly-wage", "value"),
    State("cost-of-living", "value"),
    State("occupational-group-dropdown", "value"),
)
def assess_fit_and_create_chart(n_clicks, hourly_wage, cost_of_living, occupation):
    if n_clicks > 0 and hourly_wage is not None and occupation is not None:
        try:
            # Convert inputs to float
            hourly_wage = float(hourly_wage)
            cost_of_living = float(cost_of_living) if cost_of_living is not None else 9667

            # Get the mean hourly wage for the selected occupation
            occupation_data = df[df["Major occupational group"] == occupation]
            if not occupation_data.empty:
                mean_hourly_wage = float(occupation_data["Unnamed: 4"].values[0])

                # Monthly wage calculation
                wage_times_160 = hourly_wage * 160

                if wage_times_160 < cost_of_living:
                    assessment_result = "You may not be a good fit for Santa Barbara."
                elif hourly_wage > mean_hourly_wage:
                    assessment_result = "You are a great fit for Santa Barbara!"
                else:
                    assessment_result = f"You may be a good fit but consider all your options! You are making less than the average {occupation} professional."

                assessment_result = html.Div(
                    assessment_result,
                    style={"fontSize": "24px", "fontWeight": "bold"}  # Change the font size here
                )

                # Create bar chart for wage comparison
                wage_figure = {
                    "data": [
                        go.Bar(x=["Your Wage", "Average Wage"],
                               y=[hourly_wage, mean_hourly_wage],
                               marker=dict(color=["blue", "green"])),
                    ],
                    "layout": go.Layout(
                        title=f"Hourly Wage Comparison: {occupation}",
                        xaxis=dict(title="Wage Type"),
                        yaxis=dict(title="Hourly Wage ($)"),
                        showlegend=False
                    ),
                }

                # Convert hourly wage to annual salary
                annual_salary = hourly_wage * 2080

                # Create earnings column chart with "Your Annual Salary"
                fig = go.Figure()

                # Add industry earnings data
                fig.add_trace(go.Bar(
                    x=df_avg_earnings["Median Earnings"],
                    y=df_avg_earnings["Industry"],
                    orientation="h",
                    marker=dict(color="blue")
                ))

                # Add "Your Annual Salary" to the column chart
                fig.add_trace(go.Bar(
                    x=[annual_salary],
                    y=["Your Annual Salary"],
                    orientation="h",
                    marker=dict(color="red")
                ))

                fig.update_layout(
                    title=dict(text="<b>Average Median Earnings by Industry</b>", x=0.5),
                    xaxis_title="<b>Earnings ($)</b>",
                    yaxis_title="<b>Industry</b>",
                )

                return assessment_result, wage_figure, fig
        except ValueError:
            return "Please enter valid numerical values for hourly wage and cost of living.", {}, {}
    return "", {}, {}


if __name__ == "__main__":
    app.run(debug=True)
