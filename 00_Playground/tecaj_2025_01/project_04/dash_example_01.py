from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Dash, Input, Output, callback, dash_table, dcc, html

MAIN_PATH = Path(__file__).parent
file_path = MAIN_PATH / "gapminder_unfiltered.csv"

df = pd.read_csv(file_path)

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = Dash(external_stylesheets=external_stylesheets)

app.layout = [
    html.Div(children="My First App with Data", className="row", style={"textAlign": "center", "color": "blue", "fontSize": 30}),
    html.Div(
        className="row",
        children=[
            dcc.RadioItems(options=["pop", "lifeExp", "gdpPercap"], value="lifeExp", inline=True, id="my-radio-buttons-final"),
        ],
    ),
    html.Div(
        className="row",
        children=[
            html.Div(
                className="six columns",
                children=[
                    dash_table.DataTable(data=df.to_dict("records"), page_size=11, style_table={"overflowX": "auto"}),
                ],
            ),
            html.Div(
                className="six columns",
                children=[
                    dcc.Graph(figure={}, id="histo-chart-final"),
                ],
            ),
        ],
    ),
]


@callback(
    Output(component_id="histo-chart-final", component_property="figure"),
    Input(component_id="my-radio-buttons-final", component_property="value"),
)
def update_graph(col_chosen):
    fig = px.histogram(df, x="continent", y=col_chosen, histfunc="avg")
    return fig


if __name__ == "__main__":
    app.run(debug=True)
