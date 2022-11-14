from dash import (
    html,
    dcc,
)  # to avoid having to write dash.html and dash.dcc (dash core components)
import dash_bootstrap_components as dbc


class Layout:
    def __init__(self, symbol_dict: dict) -> None:
        self_symbol_dict = symbol_dict

        self._stock_options_dropdown = [
            {"label": name, "value": symbol} for symbol, name in symbol_dict.items()
        ]  # label is shown name, value is value of the label

        self._ohlc_options = [
            {"label": option, "value": option}
            for option in ("open", "high", "low", "close")
        ]

        self._slider_marks = {
            i: mark
            for i, mark in enumerate(
                ["1 day", "1 week", "1 month", "3 months", "1 year", "5 years", "Max"]
            )
        }

    def layout(self):
        # returning html main is everything on the webpage in this case
        # so for this case, this return is essentially the entire dashboard visual
        # and main does app callbacks (listeners) for events
        # "html.Main"

        # returning dbc.Container instead returns a container place in main (?)
        return dbc.Container(
            [
                dbc.Card(
                    dbc.CardBody(html.H1("Techy Stocks Viewer")), className="mt-5"
                ),
                dbc.Row(
                    [
                        dbc.Col(html.P("Choose a stock")),
                        dbc.Col(
                            dcc.Dropdown(
                                id="stockpicker-dropdown",
                                options=self._stock_options_dropdown,
                                value="AAPL",  # default value of dropdown
                            )
                        ),
                        dbc.Col(),
                    ]
                ),
                html.P(id="highest-value"),
                html.P(id="lowest-value"),
                dcc.RadioItems(
                    id="ohlc-radio",
                    options=self._ohlc_options,  # ohlc - open high low close
                    value="close",
                ),
                dcc.Graph(id="stock-graph"),
                dcc.Slider(
                    id="time-slider",
                    min=0,
                    max=6,
                    marks=self._slider_marks,
                    value=2,  # default position of slider (index of slider marks)
                    step=None,  # slider cannot select values between marks
                ),
                # storing intermediate value on clients browser in order to share between several callbacks
                dcc.Store(id="filtered-df"),
            ]
        )
