from database import DatabaseInterface
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output

# -----------------------------------------------------------------------------

db = DatabaseInterface()

# -----------------------------------------------------------------------------

app = Dash(__name__)

app.layout = html.Div([
    html.H1('Super Dashboard Visor'),
    dcc.Graph(id="graph"),
    dcc.Graph(id="graph2"),
    dcc.Graph(id="graph3"),
    dcc.Interval(id="refresh", interval=5000, n_intervals=0),
])


@app.callback(
    Output("graph", "figure"),
    [Input("refresh", "n_intervals")]
)
def refresh(n):
    speeds = db.read_all_table('speeds')

    fig_velocidad = go.Figure(
        data=go.Scatter(
            x=[str(speed.Timestamp) for speed in speeds],
            y=[speed.Speed for speed in speeds],
            mode='lines+markers'
        )
    )

    fig_velocidad.update_xaxes(title_text="Fecha")
    fig_velocidad.update_yaxes(title_text="Velocidad (Mbps)")

    fig_velocidad.update_layout(
        title_text="Velocidad de la red"
    )

    return fig_velocidad


@app.callback(
    Output("graph2", "figure"),
    [Input("refresh", "n_intervals")]
)
def refresh2(n):

    totalConsumption = 0

    nodes = db.read_all_table('nodes')

    for node in nodes:
        totalConsumption += node.Consumption

    fig_consumo_total = go.Figure(
        data=go.Bar(x=[str(totalConsumption)], y=[totalConsumption])
    )

    fig_consumo_total.update_xaxes(title_text="Total")
    fig_consumo_total.update_yaxes(title_text="Consumo (MB)")

    fig_consumo_total.update_layout(
        title_text="Consumo de ancho de banda"
    )

    return fig_consumo_total


@app.callback(
    Output("graph3", "figure"),
    [Input("refresh", "n_intervals")]
)
def refresh3(n):
    nodos = []

    consumo_nodos = []

    nodos_activos = []

    nodes = db.read_all_table('nodes')

    for node in nodes:
        nodos.append(node.Ip)
        consumo_nodos.append(node.Consumption)
        nodos_activos.append(node.Active)

    fig_consumo_nodos = go.Figure(
        data=go.Bar(
            x=nodos,
            y=consumo_nodos,
            marker=dict(color=nodos_activos))
    )

    fig_consumo_nodos.update_xaxes(title_text="Nodos")
    fig_consumo_nodos.update_yaxes(title_text="Consumo (MB)")

    fig_consumo_nodos.update_layout(
        title_text="Consumo de ancho de banda por nodo"
    )

    return fig_consumo_nodos


if __name__ == '__main__':
    app.run_server(debug=True, host="0.0.0.0", port=5000)
