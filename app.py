import dash
import dash_bootstrap_components as dbc
from navbar import navbar
from Pages.home import home_layout
from Pages.compare import compare_layout
from callbacks import register_callbacks
from dash import dcc, html, Input, Output


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)

app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    navbar,
    html.Div(id="page_content")
])

@app.callback(
    Output("page_content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/compare":
        return compare_layout
    else:
        return home_layout

register_callbacks(app)

if __name__ == "__main__":
    app.run(debug=True)
