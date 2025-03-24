import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd

# Load dataset
df = pd.read_csv("data/nba_2022-23_all_stats_with_salary.csv")
df = df[['Player Name', 'Salary', '3P%']].dropna()
df = df.rename(columns={'Player Name': 'Player', '3P%': 'Three_Point_Percentage'})

# Comparison Page Layout
compare_layout = dbc.Container([
    dbc.Row([dbc.Col(html.H1("Compare NBA Players", className="text-center mt-4"), width=12)]),
    
    dbc.Row([
        dbc.Col([
            html.Label("Select Player 1:", className="fw-bold"),
            dcc.Dropdown(id="player_1", options=[{"label": p, "value": p} for p in df["Player"]], value=df["Player"].iloc[0]),
            
            html.Label("Select Player 2:", className="fw-bold mt-2"),
            dcc.Dropdown(id="player_2", options=[{"label": p, "value": p} for p in df["Player"]], value=df["Player"].iloc[1]),
            
            dbc.Button("Compare", id="compare_button", color="primary", className="mt-3"),
            dcc.Graph(id="compare_output", style={"height": "400px"})  # Output graph
        ], width=6, className="mx-auto")
    ], className="justify-content-center mt-4"),
    
    dbc.Row([dbc.Col(html.Footer("Built with Dash & Plotly | © 2025", className="text-center text-muted mt-5"), width=12)])
], fluid=True)
