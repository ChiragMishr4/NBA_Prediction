import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# Load dataset
df = pd.read_csv("data/nba_2022-23_all_stats_with_salary.csv")
df = df[['Player Name', 'Salary', '3P%']].dropna()
df = df.rename(columns={'Player Name': 'Player', '3P%': 'Three_Point_Percentage'})

# Train Regression Model
X = df[['Salary']]
y = df['Three_Point_Percentage']
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)
model = LinearRegression()
model.fit(X_poly, y)

# Scatter Plot
fig = px.scatter(df, x='Salary', y='Three_Point_Percentage', hover_name='Player',
                 title="NBA Player Salary vs. Three-Point Accuracy",
                 labels={'Salary': "Salary ($)", 'Three_Point_Percentage': "3PT Accuracy"},
                 color='Three_Point_Percentage', color_continuous_scale='blues')

fig.update_traces(marker=dict(size=6, opacity=0.7))
fig.add_scatter(x=df['Salary'], y=model.predict(poly.transform(X)), mode='lines', name='Regression Line'),

fig.update_layout(
    coloraxis_colorbar=dict(
        title="3PT Accuracy",  # Title for color bar
        thicknessmode="pixels", thickness=15,  # Set reasonable width
        lenmode="fraction", len=0.6,  # Adjust height
        x=1.1,  # Push color bar further right
        y=0.5,  # Center vertically
        yanchor="middle"
    ),
    legend=dict(
        x=0.75,  # Move legend to the right, away from the color bar
        y=0.9,  # Adjust legend height
        bgcolor="rgba(255, 255, 255, 0.7)",  # Make legend background semi-transparent
        bordercolor="black",
        borderwidth=1
    )
)
# Home Page Layout
home_layout = dbc.Container([
    dbc.Row([dbc.Col(html.H1("NBA Three-Point Accuracy vs. Salary", className="text-center mt-4"), width=12)]),

        dbc.Row([
        dbc.Col(html.P(
            "This dashboard analyzes the relationship between NBA player salaries and their three-point shooting accuracy. "
            "Using real NBA data, the model predicts a player's 3PT accuracy based on their salary. "
            "You can enter a salary to estimate a player's expected 3PT percentage or compare two players to see how they match up.",
            className="text-center mt-2 text-muted",
            style={"fontSize": "16px"}
        ), width=10, className="mx-auto")
    ], className="justify-content-center mt-3"),
    
    dbc.Row([dbc.Col([dcc.Graph(figure=fig)], width=12)], className="mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.Label("Enter Salary (in Millions $M):", className="fw-bold"),
            dbc.Input(id="salary_input", type="number", value=15, className="mb-2", style={'width': '100%'}),  # Ensure ID matches callback
            dbc.Button("Predict", id="predict_button", color="primary", className="mb-3"),  # Ensure ID matches callback
            html.Div(id="prediction_output", className="fw-bold text-primary", style={'fontSize': '20px'})  # Ensure ID matches callback
        ], width=4, className="mx-auto text-center")
    ], className="justify-content-center mt-4"),
    
    dbc.Row([dbc.Col(html.Footer("Built with Dash & Plotly | © 2025", className="text-center text-muted mt-5"), width=12)])
], fluid=True)
