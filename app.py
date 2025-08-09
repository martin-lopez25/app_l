import dash
from dash import html, dcc, Output, Input, State, ctx
import dash_bootstrap_components as dbc
import time

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    style={
        "backgroundImage": "url('/assets/fondo.jpg')",
        "backgroundSize": "cover",
        "backgroundPosition": "center",
        "height": "100vh",
        "padding": "20px",
        "textAlign": "center",
        "color": "black"  # letras negras
    },
    children=[
        html.H1("Uso de lavadora ", style={"marginBottom": "30px"}),

        html.Div(
            id="slider-container",
            children=[
                html.Label(
                    "Tiempo de uso (minutos):",
                    style={"fontSize": "20px", "fontWeight": "bold"}
                ),
                dcc.Slider(
                    id="tiempo-slider",
                    min=1,
                    max=120,
                    step=1,
                    value=30,
                    marks={i: str(i) for i in range(0, 121, 15)},
                    tooltip={"placement": "bottom", "always_visible": True},
                    updatemode="drag",
                ),
            ],
            style={"width": "60%", "margin": "0 auto 40px auto"}
        ),

        html.Div(id="cronometro", style={"fontSize": "40px", "marginBottom": "20px"}),

        dbc.Button(
            "Activar",
            id="lavadora-btn",
            color="success",
            style={
                "fontSize": "20px",
                "padding": "15px 40px",
                "border": "3px solid black",  # borde negro para contraste
                "marginBottom": "20px"
            }
        ),

        html.Div(id="gif-container"),

        dcc.Interval(id="interval", interval=1000, disabled=True),

        dcc.Store(id="estado-lavadora", data={"running": False, "end_time": None})
    ]
)

@app.callback(
    Output("cronometro", "children"),
    Output("lavadora-btn", "color"),
    Output("lavadora-btn", "children"),
    Output("lavadora-btn", "disabled"),
    Output("interval", "disabled"),
    Output("gif-container", "children"),
    Output("estado-lavadora", "data"),
    Output("slider-container", "style"),
    Input("lavadora-btn", "n_clicks"),
    Input("interval", "n_intervals"),
    State("tiempo-slider", "value"),
    State("lavadora-btn", "color"),
    State("estado-lavadora", "data"),
    prevent_initial_call=True,
)
def controlar_lavadora(n_clicks, n_intervals, minutos, color_actual, estado):
    trigger = ctx.triggered_id

    if trigger == "lavadora-btn":
        if color_actual == "success":  # Si está disponible, activamos
            fin = time.time() + minutos * 60
            estado = {"running": True, "end_time": fin}
            return (
                f"{minutos:02d}:00",
                "danger",
                "En uso",
                True,
                False,
                html.Img(src="/assets/cat-laundry.gif", style={"width": "200px"}),
                estado,
                {"display": "none"}  # Oculta slider al activar
            )
        else:  # Ya en uso, no hacemos nada
            return dash.no_update

    if trigger == "interval" and estado["running"]:
        restante = int(estado["end_time"] - time.time())
        if restante <= 0:
            estado = {"running": False, "end_time": None}
            return (
                "Tiempo finalizado. Lavadora disponible.",
                "success",
                "Activar",
                False,
                True,
                None,
                estado,
                {"display": "block"}  # Mostrar slider al terminar
            )
        else:
            mins = restante // 60
            segs = restante % 60
            return (
                f"{mins:02d}:{segs:02d}",
                "danger",
                "En uso",
                True,
                False,
                html.Img(src="/assets/cat-laundry.gif", style={"width": "200px"}),
                estado,
                {"display": "none"}  # Oculta slider mientras corre
            )

    return dash.no_update

if __name__ == "__main__":
    app.run(debug=True)

