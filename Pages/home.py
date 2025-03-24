import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from callbacks import fig  # Import the initial figure


df = pd.read_csv("data/nba_2022-23_all_stats_with_salary.csv")
df = df[['Player Name', 'Salary', '3P%']].dropna()
df = df.rename(columns={'Player Name': 'Player', '3P%': 'Three_Point_Percentage'})

# Layout of the Home Page
home_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("NBA Three-Point Accuracy vs. Salary", className="text-center mt-4"), width=12)
    ]),

    # Dashboard Explanation
    dbc.Row([
        dbc.Col(html.P(
            "This dashboard explores the relationship between NBA player salaries and their three-point shooting accuracy. "
            "Using real NBA data, the model predicts a player's 3PT accuracy based on their salary. "
            "You can enter a salary to estimate a player's expected 3PT percentage or compare two players to see how they match up.",
            className="text-center mt-2 text-muted",
            style={"fontSize": "16px"}
        ), width=10, className="mx-auto")
    ], className="justify-content-center mt-3"),
    
    # Graph (Now Updates Dynamically)
    dbc.Row([
        dbc.Col([
            dcc.Graph(id="scatter_plot", figure=fig)  # Ensure the graph has the correct ID
        ], width=12)
    ], className="mb-4"),

    # Salary Input & Prediction
    dbc.Row([
        dbc.Col([
            html.Label("Enter Salary (in Millions $M):", className="fw-bold"),
            dbc.Input(id="salary_input", type="number", value=15, className="mb-2", style={'width': '100%'}),
            dbc.Button("Predict", id="predict_button", color="primary", className="mb-3"),
            html.Div(id="prediction_output", className="fw-bold text-primary", style={'fontSize': '20px'})
        ], width=4, className="mx-auto text-center")
    ], className="justify-content-center mt-4"),

    dbc.Row([
        dbc.Col(html.Footer("Built with Dash & Plotly | © 2024", className="text-center text-muted mt-5"), width=12)
    ])
], fluid=True)

