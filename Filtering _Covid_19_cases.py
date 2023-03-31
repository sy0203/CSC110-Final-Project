"""
CSC110 Fall 2021 Final Project: Filtering of Covid Data

Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of TAs and instructors
overseeing CSC110 at the University of Toronto St. George campus.
This file is Copyright (c) 2021 Selina Phadiya, Natasha Sharan, Seyoung Yoo
"""
from datetime import datetime

import pandas
import pandas as pd
from pandas import to_datetime
import csv

data = pd.read_csv('Raw_data.csv')

extra_data = []
extra_countries = set()

for header in data.columns:
    if header not in {'iso_code', 'location', 'date', 'total_cases', 'new_cases'}:
        extra_data.append(header)

data.drop(extra_data, axis=1, inplace=True)

data = data.set_index('iso_code')

for i in range(0, len(data.index)):
    if data.index[i] not in {'USA', 'BRA', 'FRA', 'IND', 'JPN'}:
        extra_countries.add(data.index[i])

data.drop(extra_countries, axis=0, inplace=True)
data = data.set_index('location')

data.to_csv("Covid-19 cases.csv")
