"""
CSC110 Fall 2021 Final Project: Info Collection

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of TAs and instructors
overseeing CSC110 at the University of Toronto St. George campus.
This file is Copyright (c) 2021 Selina Phadiya, Natasha Sharan, Seyoung Yoo
"""
import csv
import os
import calc_helper as calc
from calc_helper import Country


def load_data(filename: str) -> tuple:
    """Loads the information from the files into the appropriate tuple lists"""
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        pos = 0
        if 'case' in filename:
            pos = 1

        data = ([], [])
        for row in csv_reader:
            if line_count != 0:
                data[0].append(row[pos])
                data[1].append(float(row[pos + 1]))
            line_count += 1

        return data


def set_country(indexes_file: str, cases_file: str) -> Country:
    """
    This function should return a country with values and whatnot
    Use the functions available in the helper package.
    """
    name = ''
    names = {'Brazil': 'Brazil', 'France': 'France', 'India': 'India', 'Japan': 'Japan', 'US': 'United States'}
    for n in names:
        if n in indexes_file:
            name = names[n]
            break
    dates, prices = load_data(indexes_file)
    dates_c, cases = load_data(cases_file)
    percent_changes = calc.percentage_list(prices)
    mean, median, stan_dev = calc.get_stats(percent_changes)
    correlation_coefficient = calc.correlation_coeff(cases, calc.percentage_list_index(prices))
    recovered = calc.index_recovered(percent_changes[0], percent_changes[len(percent_changes) - 1])
    return Country(name, dates, cases, dates_c, prices, percent_changes,
                   mean, median, stan_dev, correlation_coefficient, recovered)


def process_countries() -> list[Country]:
    """
    This function should read from the appropriate files and create a list of countries in a loop
    """
    countries = []

    index_files = ['Brazil_stock.csv', 'France_stock.csv', 'India_stock.csv', 'Japan_stock.csv', 'US_stock.csv']
    covid_files = ['Brazil_cases.csv', 'France_cases.csv', 'India_cases.csv', 'Japan_cases.csv', 'USA_cases.csv']

    for x in range(5):
        index_file = index_files[x]
        covid_file = covid_files[x]
        # checking if it is a file
        if os.path.isfile(index_file) and os.path.isfile(covid_file):
            countries.append(set_country(index_file, covid_file))
    return countries
