import time

from database import DatabaseInterface

import plotly.graph_objects as go
from plotly.subplots import make_subplots

# -----------------------------------------------------------------------------

db = DatabaseInterface()


def main():

    totalConsumption = 0

    nodos = []

    consumo_nodos = []

    nodos_activos = []

    while True:

        # Velocidad Mbps
        speeds = db.read_all_table('speeds')

        if len(speeds) > 0:

            lastSpeed = speeds[-1]
        
        else:
            lastSpeed = None

        # Total consumo en GB
        # Informacion de cada nodo
        nodes = db.read_all_table('nodes')

        for node in nodes:
            totalConsumption += node.Consumption

            nodos.append(node.Ip)
            consumo_nodos.append(node.Consumption)
            nodos_activos.append(node.Active)

        # Graficar
        fig_velocidad = go.Figure(data=go.Scatter(x=[str(lastSpeed.Timestamp)], y=[lastSpeed.Speed], mode='lines+markers'))

        fig_consumo_total = go.Figure(data=go.Bar(x=[str(totalConsumption)], y=[totalConsumption]))

        fig_consumo_nodos = go.Figure(data=go.Scatter(x=nodos, y=consumo_nodos, mode='markers', marker=dict(color=nodos_activos)))
        
        # Configurar diseño de subplots
        fig = make_subplots(rows=3, cols=1,subplot_titles=("Velocidad de la red", "Total de consumo de ancho de banda", "Información por nodo"))

        # Agregar gráficos a los subplots
        fig.add_trace(fig_velocidad.data[0], row=1, col=1)
        fig.add_trace(fig_consumo_total.data[0], row=2, col=1)
        fig.add_trace(fig_consumo_nodos.data[0], row=3, col=1)

        # Configurar etiquetas de los ejes
        fig.update_xaxes(title_text="Fecha", row=1, col=1)
        fig.update_yaxes(title_text="Velocidad (Mbps)", row=1, col=1)

        fig.update_xaxes(title_text="Total", row=2, col=1)
        fig.update_yaxes(title_text="Consumo (GB)", row=2, col=1)

        fig.update_xaxes(title_text="Nodos", row=3, col=1)
        fig.update_yaxes(title_text="Consumo (GB)", row=3, col=1)

        # Actualizar diseño de la figura
        fig.update_layout(height=900, width=800, title_text="Visualizaciones de red y ancho de banda")

        # Mostrar la figura
        fig.show()

        time.sleep(5)

        totalConsumption = 0
        nodos.clear()
        consumo_nodos.clear()
        nodos_activos.clear()


if __name__ == '__main__':
    main()