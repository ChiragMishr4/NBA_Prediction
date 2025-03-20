import dash
import numpy as np
import pandas as pd
from dash import Output, Input, State
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

# Load dataset
df = pd.read_csv("data/nba_2022-23_all_stats_with_salary.csv")
df = df[['Player Name', 'Salary', '3P%']].dropna()
df = df.rename(columns={'Player Name': 'Player', '3P%': 'Three_Point_Percentage'})

# Train Model
X = df[['Salary']]
y = df['Three_Point_Percentage']
poly = PolynomialFeatures(degree=2)
X_poly = poly.fit_transform(X)
model = LinearRegression()
model.fit(X_poly, y)

def register_callbacks(app):
    """
    Register all callbacks for the Dash app.
    """

    # Callback for the Predict button (Home Page)
    @app.callback(
        Output("prediction_output", "children"),
        Input("predict_button", "n_clicks"),  # Button triggers the callback
        State("salary_input", "value")  # Takes the value but does NOT trigger callback
    )
    def predict_3pt(n_clicks, salary):
        if n_clicks is None:
            return ""  # Show nothing when the page first loads

        if salary is None or salary <= 0:
            return "⚠️ Please enter a valid salary greater than 0."

        salary_millions = salary * 1_000_000  # Convert millions to actual salary
        salary_poly = poly.transform(np.array([[salary_millions]]))  # Transform input for the model
        prediction = model.predict(salary_poly)[0] *  100

        return f"Predicted Three-Point Accuracy: {prediction:.2f}%"

    # Callback for the Compare button (Player Comparison Page)
    @app.callback(
        Output("comparison_output", "children"),
        Input("compare_button", "n_clicks"),  # Button triggers the callback
        State("player_1", "value"),  # Takes selected player but does NOT trigger callback
        State("player_2", "value")   # Takes selected player but does NOT trigger callback
    )
    def compare_players(n_clicks, player_1, player_2):
        if n_clicks is None:
            return ""

        if not player_1 or not player_2:
            return "⚠️ Please select two players to compare."

        # Extract player stats
        stats_1 = df[df["Player"] == player_1].iloc[0]
        stats_2 = df[df["Player"] == player_2].iloc[0]

        return (f"📊 {player_1} - Salary: ${stats_1['Salary']:,}, 3PT%: {stats_1['Three_Point_Percentage']:.2f}%\n"
                f"📊 {player_2} - Salary: ${stats_2['Salary']:,}, 3PT%: {stats_2['Three_Point_Percentage']:.2f}%")

