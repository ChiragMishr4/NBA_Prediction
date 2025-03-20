import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/")),
        dbc.NavItem(dbc.NavLink("Player Comparison", href="/compare")),
    ],
    brand="NBA Salary & Performance Analysis",
    brand_href="/",
    color="dark",
    dark=True,
    className="mb-4"
)
