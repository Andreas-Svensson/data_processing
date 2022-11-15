import dash
import os
from load_data import StockData

from dash.dependencies import Output, Input
import plotly_express as px
from time_filtering import filter_time
import pandas as pd
from layout import Layout  # class Layout
import dash_bootstrap_components as dbc

dir_path = os.path.dirname(__file__)
path = os.path.join(dir_path, "stocksdata")

stockdata_object = StockData(path)

symbol_dict = {"AAPL": "Apple", "NVDA": "Nvidia", "TSLA": "Tesla", "IBM": "IBM"}

df_dict = {symbol: stockdata_object.stock_dataframe(symbol) for symbol in symbol_dict}

# create a dash app
# dash building on flask
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.MATERIA],
    # meta_tags makes possible for responsivity, rescaling layout based on device width in this case
    # this can then be used to customize how it works in our styling
    meta_tags=[
        dict(name="viewport", content="width=device-width, initial-scale = 1.0")
    ],
)

app.layout = Layout(symbol_dict).layout()


@app.callback(
    Output("filtered-df", "data"),
    Input("stockpicker-dropdown", "value"),
    Input("time-slider", "value"),
)
def filter_df(stock, time_index):
    dff_daily, dff_intraday = df_dict[stock]
    dff = dff_intraday if time_index <= 2 else dff_daily
    days = {i: day for i, day in enumerate([1, 7, 30, 90, 365, 365 * 5])}
    dff = dff if time_index == 6 else filter_time(dff, days=days[time_index])
    return dff.to_json()


@app.callback(
    Output("highest-value", "children"),
    Output("lowest-value", "children"),
    Input("filtered-df", "data"),
    Input("ohlc-radio", "value"),
)
def highest_lowest_value_update(json_df, ohlc):
    dff = pd.read_json(json_df)
    highest_value = dff[ohlc].max()
    lowest_value = dff[ohlc].min()
    return f"${highest_value:.2f}", f"${lowest_value:.2f}"


@app.callback(
    Output("stock-graph", "figure"),
    Input("filtered-df", "data"),
    Input("stockpicker-dropdown", "value"),
    Input("ohlc-radio", "value"),
)
def update_graph(json_df, stock, ohlc):
    dff = pd.read_json(json_df)
    return px.line(dff, x=dff.index, y=ohlc, title=symbol_dict[stock])


if __name__ == "__main__":
    app.run_server(debug=True)  # page is updated on every save, no need to run again
