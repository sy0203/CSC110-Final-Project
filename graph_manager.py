"""
CSC110 Fall 2021 Final Project: Graph Manager

This file handles all the graphs needed in this project.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and instructors
overseeing CSC110 at the University of Toronto St. George campus.
This file is Copyright (c) 2021 Selina Phadiya, Natasha Sharan, Seyoung Yoo
"""
import plotly.express as px
import plotly.graph_objects as go
import calc_helper as calc
from calc_helper import Country


def choropleth_graph(countries: list[Country]):
    """Choropleth world map to present how many countries’ index funds
    recovered and exceeded their pre-pandemic closing prices. """

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
        if recovery_percentage[i] >= 30:
            z[i] = 5
        elif recovery_percentage[i] >= 25:
            z[i] = 4
        elif recovery_percentage[i] >= 10:
            z[i] = 3
        elif recovery_percentage[i] >= 0:
            z[i] = 2
        else:
            z[i] = 1

    scl = [[0.0, 'rgb(242,240,247)'], [0.2, 'rgb(218,218,235)'], [0.4, 'rgb(188,189,220)'],
           [0.6, 'rgb(158,154,200)'], [0.8, 'rgb(117,107,177)'], [1.0, 'rgb(84,39,143)']]
    data = dict(type='choropleth',
                locations=country,
                locationmode='ISO-3',
                colorscale=scl,
                z=z,
                hovertext=recovery_percentage,
                autocolorscale=False,
                marker=dict(line=dict(color='rgb(255,255,255)', width=2)), )
    layout = dict(title="World Map of Trend of Countries' Index Funds",
                  geo=dict(showframe=True, projection={'type': 'miller'}))
    choropleth_map = go.Figure(data=[data], layout=layout)
    choropleth_map.show()


def line_graph_all_vs_time(countries: list[Country]):
    """Line Graph to plot all 5 index funds closing price against time."""

    x = countries[0].dates

    country_y = []
    for country in countries:
        country_y.append([val for val in (calc.percentage_list(country.prices)) * 100])

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=country_y[0], name=countries[0].name + " Index Fund Price"))
    fig.add_trace(go.Scatter(x=x, y=country_y[1], name=countries[1].name + " Index Fund Price"))
    fig.add_trace(go.Scatter(x=x, y=country_y[2], name=countries[2].name + " Index Fund Price"))
    fig.add_trace(go.Scatter(x=x, y=country_y[3], name=countries[3].name + " Index Fund Price"))
    fig.add_trace(go.Scatter(x=x, y=country_y[4], name=countries[4].name + " Index Fund Price"))

    fig.update_layout(title='<Closing Price of Index Funds Over Time>', legend_title_text='Countries',
                      xaxis_title='Time', yaxis_title='Closing Price')
    fig.show()


def helper(country: Country) -> list:
    """Calculates cases per 1000."""
    help_func = [country.cases[i] // 1000 for i in range(len(country.cases))]
    return help_func


def line_graph(country: Country):
    """Line Graph to plot the benchmark index fund prices
    and the number of Covid-19 cases against time."""

    x = country.dates_c
    y1 = [val for val in (calc.percentage_list(country.prices)) * 100]
    y2 = helper(country)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y1, name=country.name + " Index Fund Price"))
    fig.add_trace(go.Scatter(x=x, y=y2, name=country.name + " Covid Cases"))

    fig.update_layout(title='<Closing Price of Index Funds Over Time>', legend_title_text='Countries',
                      xaxis_title='Time')

    fig.show()


def scatter_plot(country: Country):
    """Scatter Plot to present the correlation between
    number of Covid-19 cases and drop in the index funds’ price (%)."""

    x = [country.cases[i] for i in range(len(country.prices) - 57)]

    y = calc.percentage_list_index(country.prices)

    percentage_change = []
    for i in range(33, len(country.percent_changes) - 1):
        percentage_change.append(country.percent_changes[i])

    fig = px.scatter(x=x, y=y)
    fig.update_layout(title="<Drop in " + country.name + "'s" + " Index Funds' Price Over Covid 19 Cases>",
                      xaxis_title='Number of Covid 19 Cases',
                      yaxis_title='Drop in Index Fund Price (%)')
    fig.show()


def recovery_table(countries: list[Country]):
    """Table to show recovery (%) of each index fund over time.
    (e.g. 1 week, 1 month, 3 month, 6 month, 1 year)"""

    x = [country.name for country in countries]
    z = [country.prices[56] for country in countries]
    y0 = [country.percent_changes[0] for country in countries]
    y1 = [country.percent_changes[3] for country in countries]
    y2 = [country.percent_changes[8] for country in countries]
    y3 = [country.percent_changes[17] for country in countries]
    y4 = [country.percent_changes[51] for country in countries]

    fig = go.Figure(data=[go.Table(header=dict(values=['Country', 'Pre-Pandemic Price',
                                                       'Percentage Change After 7 days',
                                                       'Percentage Change After 28 days',
                                                       'Percentage Change After 63 days',
                                                       'Percentage Change After 126 days',
                                                       'Percentage Change After 364 days']),
                                   cells=dict(values=[[x[0], x[1], x[2], x[3], x[4]],
                                                      z, y0, y1, y2, y3, y4]))])
    fig.show()
