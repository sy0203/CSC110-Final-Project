"""This file handles with the presentation of all the graphs needed in this project."""
import pycountry
import info_collection
import plotly.express as px
import plotly.graph_objects as go
import calc_helper as calc
from calc_helper import Country


def choropleth_graph(countries: list[Country]):
    """Choropleth World map to present how many countries’ index funds
    recovered and exceeded their pre-pandemic closing price. """

    countries_lst = [country.name for country in countries]
    sorted_lst = sorted(countries_lst)
    countries_dict = {sorted_lst[0]: 'BRA', sorted_lst[1]: 'FRA', sorted_lst[2]: 'IND', sorted_lst[3]: 'JPN',
                      sorted_lst[4]: 'USA'}

    country = [countries_dict[sorted_lst[0]], countries_dict[sorted_lst[1]], countries_dict[sorted_lst[2]],
               countries_dict[sorted_lst[3]], countries_dict[sorted_lst[4]]]

    z = [1, 1, 1, 1, 1]
    pre_covid = [country.prices[56] for country in countries]
    latest = [country.prices[-1] for country in countries]

    recovery_percentage = []
    for i in range(len(pre_covid)):
        recovery_percentage.append(calc.percentage_change(pre_covid[i], latest[i]))
        if recovery_percentage[i] >= 0:
            return z[i] == 4
        else:
            return z[i] == 1

    scl = [[0.0, 'rgb(242,240,247)'], [0.2, 'rgb(218,218,235)'], [0.4, 'rgb(188,189,220)'],
           [0.6, 'rgb(158,154,200)'], [0.8, 'rgb(117,107,177)'], [1.0, 'rgb(84,39,143)']]
    data = dict(type='choropleth',
                locations=country,
                locationmode='ISO-3',
                colorscale=scl,
                z=z,
                hovertext=recovery_percentage,
                autocolorscale=False,
                marker=dict(line=dict(color='Recovery Percentage', width=2)),)
    layout = dict(title="World Map of Trend of Countries' Index Funds",
                  geo=dict(showframe=True, projection={'type': 'miller'}))
    choropleth_map = go.Figure(data=[data], layout=layout)
    choropleth_map.show()


def line_graph_all_vs_time(countries: list[Country]):
    """Line Graph to plot all 5 index funds closing price against time."""

    x = [country.dates for country in countries]
    y = [country.prices for country in countries]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x[0], y=y[0], name=countries[0].name + " Index Fund Price"))
    fig.add_trace(go.Scatter(x=x[1], y=y[1], name=countries[1].name + " Index Fund Price"))
    fig.add_trace(go.Scatter(x=x[2], y=y[2], name=countries[2].name + " Index Fund Price"))
    fig.add_trace(go.Scatter(x=x[3], y=y[3], name=countries[3].name + " Index Fund Price"))
    fig.add_trace(go.Scatter(x=x[4], y=y[4], name=countries[4].name + " Index Fund Price"))

    fig.update_layout(title='<Closing Price of Index Funds Over Time>', legend_title_text='Countries',
                      xaxis_title='Time', yaxis_title='Closing Price')
    fig.show()


def line_graph(country: Country):
    """Line Graph to plot the benchmark index fund price
    and the number of Covid cases against time."""

    x = country.dates_c
    y1 = [country.prices[i] for i in range(57, len(country.cases) + 1)]
    y2 = country.cases

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y1, name=country.name + " Index Fund Price"))
    fig.add_trace(go.Scatter(x=x, y=y2, name=country.name + " Covid Cases"))

    fig.update_layout(title='<Closing Price of Index Funds Over Time>', legend_title_text='Countries',
                      xaxis_title='Time')

    fig.show()


def scatter_plot(country: Country):
    """Scatter Plot to present the correlation between
    number of Covid cases and drop in the index funds’ price (%)."""

    x = country.cases

    percentage_change = []
    for i in range(57, len(country.percent_changes) + 1):
        percentage_change.append(country.percent_changes[i])

    y = percentage_change

    fig = px.scatter(x=x, y=y)
    fig.update_layout(title="<Drop in Index Funds' Price Over Covid 19 Cases>", xaxis_title='Number of Covid 19 Cases',
                      yaxis_title='Drop in Index Fund Price(%)')
    fig.show()


'''def percent_change(country: Country) -> list[float]:

    a = ((country.prices[56] - country.prices[57]) // country.prices[56]) * 100
    a = ((country.prices[56] - country.prices[57]) // country.prices[56]) * 100
'''


def recovery_table(countries: list[Country]):
    """Table to show recovery (%) of each index fund over time.
    (e.g. 1 week, 1 month, 3 month, 6 month, 1 year)"""

    x = [country.name for country in countries]
    y0 = [country.percent_changes[0] for country in countries]
    y1 = [country.percent_changes[3] for country in countries]
    y2 = [country.percent_changes[8] for country in countries]
    y3 = [country.percent_changes[17] for country in countries]
    y4 = [country.percent_changes[51] for country in countries]

    fig = go.Figure(data=[go.Table(header=dict(values=['Country', '7 days', '28 days', '63 days',
                                                       '126 days', '364 days']),
                                   cells=dict(values=[[x[0], x[1], x[2], x[3], x[4]],
                                                      y0, y1, y2, y3, y4]))])
    fig.show()
