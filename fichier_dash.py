from dash import Dash, html, dcc, Input, Output, Patch, clientside_callback, callback
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.io as pio
from dash_bootstrap_templates import load_figure_template

# Load data
url = "https://raw.githubusercontent.com/chriszapp/datasets/main/books.csv"
dataset = pd.read_csv(url, nrows=1000)
authors = dataset['authors'].unique()

# Color mode switch
color_mode_switch = html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="color-mode-switch"),
        dbc.Switch(id="color-mode-switch", value=False, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="color-mode-switch"),
    ]
)

# App setup
app = Dash(__name__, external_stylesheets=[dbc.themes.MINTY, dbc.icons.FONT_AWESOME])
load_figure_template(["minty", "minty_dark"])  # Load both templates

# Layout
app.layout = html.Div([
    html.H1("Pikapplication boostée avec Bootstrap"),
    html.P("\n"),
    html.P("Mode jour ou Mode nuit ?"),
    color_mode_switch,
    html.P("\n"),
    html.P(html.I(html.B("Sélectionnez un auteur et un nombre maximum de pages avec le slider."))),
    dbc.Row([  
        dbc.Col(dcc.Dropdown(  # Colonne pour le dropdown
            id="mon-dropdown",
            options=[{'label': author, 'value': author} for author in authors],
            value=authors[0],
            multi = True,
        ), width=6),  
        dbc.Col(dcc.Slider(  # Colonne pour le slider
            id="data-slider",
            min=0,
            max=dataset['  num_pages'].max(),
            step=1,
            value=dataset['  num_pages'].max(),
            marks={i: str(i) for i in range(0, dataset['  num_pages'].max() + 1, max(1, dataset['  num_pages'].max() // 10))},
        ), width=6),  
        
    ]),
    dcc.Graph(id="plotly-graph"),
])

# Callback for graph updates
@app.callback(
    Output("plotly-graph", "figure"),
    Input("mon-dropdown", "value"),
    Input("data-slider", "value"),
    
    Input("color-mode-switch", "value")  # Add switch value as input
)
def update_graph(dropdown_value, max_pages ,switch_on):
    filtered_data = dataset[dataset['authors'].isin(dropdown_value)]
    filtered_data = filtered_data[filtered_data['  num_pages'] <= max_pages]
    fig = px.bar(
        filtered_data,
        x='title',
        y='  num_pages',
        title=f"Nombre de Pages par livre pour les livres jusqu'à {max_pages} pages (Auteur: {dropdown_value})"
    )
    fig.update_layout(xaxis_title="Titre du livre", yaxis_title="Nombre de pages")

    # Apply template based on switch value
    template = "minty_dark" if switch_on else "minty"
    fig.update_layout(template=template) # Directly update the figure's template

    return fig


# Clientside callback for theme change (Corrected)
clientside_callback(
    """
    (switchOn) => {
        document.documentElement.setAttribute('data-bs-theme', switchOn ? 'dark' : 'light');
        return window.dash_clientside.no_update;
    }
    """,
    Output("color-mode-switch", "id"),  # Output to the switch itself (doesn't actually change anything)
    Input("color-mode-switch", "value"), # Input from the switch
)


if __name__ == '__main__':
    app.run_server(debug=True)
