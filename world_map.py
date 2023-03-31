"""
Generate a world map
"""
import pycountry
from dataclasses import dataclass
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np


df = pd.read_csv('Covid_Info.csv')
df.head()



@dataclass
class CovidInfo:
    """A custom data type that represents data for covid-19 cases."""

    country_region: str
    confirmed_cases: int
    fatalities: int
    code: int


def add_country_code(info: list[CovidInfo]) -> None:
    """Using pycountry library, each object of the Covid_Info will get a code"""
    for item in info:
        item.code = pycountry.countries.get(name=item.country_region).alpha_3


# fig = px.scatter(df, x='Confirmed_Cases', y='Fatalities', color='CODE')
# fig.show()

data = dict(type='choropleth',
            locations=df['CODE'],
            z=df['Confirmed_Cases'],
            autocolorscale=True)
layout = dict(title='World Map', geo=dict(showframe=True, projection={'type': 'miller'}))
choromap = go.Figure(data=[data], layout=layout)
choromap.show()



