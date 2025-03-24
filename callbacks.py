from dash import Output, Input, State
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

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

# Generate regression line points
X_range = np.linspace(df['Salary'].min(), df['Salary'].max(), 100).reshape(-1, 1)
X_range_poly = poly.transform(X_range)
y_range_predicted = model.predict(X_range_poly) * 100  # Convert to percentage

# Create Initial Figure (Fixes Display Issues)
fig = px.scatter(df, x='Salary', y=df['Three_Point_Percentage'] * 100,  
                 hover_name='Player',
                 title="NBA Player Salary vs. Three-Point Accuracy",
                 labels={'Salary': "Salary ($)", 'Three_Point_Percentage': "3PT Accuracy (%)"},
                 color='Three_Point_Percentage',
                 color_continuous_scale='blues')

# Adjust layout to fix legend overlap
fig.update_layout(
    coloraxis_colorbar=dict(title="3PT Accuracy (%)", x=1.1),  # Move color bar slightly to the right
    legend=dict(
        title="Legend",
        x=1,  # Move legend to the right side of the plot
        y=1,  # Move legend down to avoid overlapping
        xanchor="right",  # Anchor to right side
        yanchor="top",  # Anchor to top side
        bgcolor="rgba(255,255,255,0.8)"  # Background for readability
    )
)

# Add regression line (excluded from color scale)
fig.add_trace(go.Scatter(x=X_range.flatten(), y=y_range_predicted, 
                         mode='lines', name='Regression Line',
                         line=dict(color='red', width=2),
                         showlegend=True))

def register_callbacks(app):
    @app.callback(
        [Output("prediction_output", "children"),  # Updates text output
         Output("scatter_plot", "figure")],        # Updates the graph dynamically
        Input("predict_button", "n_clicks"),  
        State("salary_input", "value")  
    )
    def predict_3pt(n_clicks, salary):
        if n_clicks is None:
            return "", fig  # Do not update the graph on first load
        
        if salary is None or salary <= 0:
            return "⚠️ Please enter a valid salary greater than 0.", fig

        # Convert salary from millions to actual dollars
        salary_millions = salary * 1_000_000
        salary_poly = poly.transform(np.array([[salary_millions]]))
        prediction = model.predict(salary_poly)[0] * 100  # Convert decimal to percentage

        # Create updated scatter plot (Fixing Display Issues)
        updated_fig = px.scatter(df, x='Salary', y=df['Three_Point_Percentage'] * 100,
                                 hover_name='Player',
                                 title="NBA Player Salary vs. Three-Point Accuracy",
                                 labels={'Salary': "Salary ($)", 'Three_Point_Percentage': "3PT Accuracy (%)"},
                                 color='Three_Point_Percentage',
                                 color_continuous_scale='blues')

        # Adjust layout (Legend & Color Bar Fix)
        updated_fig.update_layout(
            coloraxis_colorbar=dict(title="3PT Accuracy (%)", x=1.1),  # Move color bar to the right
            legend=dict(
                title="Legend",
                x=1,  # Move legend to right
                y=1,  # Move legend below color bar
                xanchor="right",  # Anchor to right side
                yanchor="top",  # Anchor to top side
                bgcolor="rgba(255,255,255,0.8)"
            )
        )

        # Add regression line (excluded from color scale)
        updated_fig.add_trace(go.Scatter(x=X_range.flatten(), y=y_range_predicted, 
                                         mode='lines', name='Regression Line',
                                         line=dict(color='red', width=2),
                                         showlegend=True))

        # Add dynamically predicted point (excluded from color scale)
        updated_fig.add_trace(go.Scatter(x=[salary_millions], y=[prediction], 
                                         mode='markers', name='Predicted Point',
                                         marker=dict(color='red', size=12, symbol='star'),
                                         hovertext=f"Salary: ${salary}M, Predicted 3PT%: {prediction:.2f}%",
                                         showlegend=True))

        return f"Predicted Three-Point Accuracy: {prediction:.2f}%", updated_fig
    
    @app.callback(
        Output("compare_output", "figure"), 
        Input("compare_button", "n_clicks"),
        State("player_1", "value"), 
        State("player_2", "value")
    )
    def compare_players(n_clicks, player1, player2):
        if n_clicks is None or n_clicks == 0:
            return go.Figure().update_layout(title="⚠️ Please select two players to compare.")  # Do nothing before clicking

        if not player1 or not player2:
            return go.Figure().update_layout(title="⚠️ Please select two players to compare.")

        player1_stats = df[df["Player"] == player1]
        player2_stats = df[df["Player"] == player2]

        if player1_stats.empty or player2_stats.empty:
            return go.Figure().update_layout(title="⚠️ Player not found.")

        # Grab rows
        p1 = player1_stats.iloc[0]
        p2 = player2_stats.iloc[0]

        # Extract values
        salary1 = float(p1["Salary"])
        salary2 = float(p2["Salary"])
        acc1 = float(p1["Three_Point_Percentage"]) * 100
        acc2 = float(p2["Three_Point_Percentage"]) * 100

        # Create figure
        fig = go.Figure()

        # Salary bars
        fig.add_trace(go.Bar(
            x=[player1, player2],
            y=[salary1, salary2],
            name="Salary ($)",
            marker_color="royalblue",
            yaxis="y1"
        ))

        fig.add_trace(go.Bar(
            name="3PT Accuracy (%)",
            x=[player1, player2],
            y=[acc1, acc2],
            marker_color="orange",
            yaxis="y2"
        ))

        fig.update_layout(
            title=f"{player1} vs {player2}",
            barmode='group',
            yaxis=dict(
                title="Salary ($)",
                side="left",
                showgrid=False
            ),
            yaxis2=dict(
                title="3PT Accuracy (%)",
                overlaying="y",
                side="right",
                showgrid=False
            ),
            legend_title="Metrics",
            height=450
        )


        return fig
