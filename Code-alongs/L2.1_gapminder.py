import plotly_express as px

gapminder = px.data.gapminder()

fig = px.scatter(
    gapminder,
    x="gdpPercap",
    y="lifeExp",
    size="pop",
    log_x=True,
    size_max=70,
    color="country",
    animation_frame="year",
    animation_group="country",
    title="Gapminder",
    range_y=[25, 90],
    range_x=[100, 100_000],
)

fig.write_html("Code-alongs/L2.1_gapminder.html", auto_open=True)
