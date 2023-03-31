"""Contains the functions that are used to perform calculations"""
import numpy
import math
from dataclasses import dataclass


def percentage_change(start: float, end: float) -> float:
    """
    Determines the percentage loss in index funds over a time period.

    >>> percentage_change(100.0, 80.0) == 20.0
    True
    >>> percentage_change(991, 40) == 95.96
    True
    """
    if start > end:
        val = round((1 - end / start) * 100, 2)
    else:
        val = round((1 + end / start) * 100, 2)
    return val


def percentage_list(indexes: list[float]) -> list[float]:
    """
    Returns a list of percentage loss across the data

    >>> values = [100, 80, 70, 60, 39]
    >>> percentage_list(values)
    [20.0, 30.0, 40.0, 61.0]
    """
    start = indexes[0]
    percent_changes = []
    for x in range(1, len(indexes)):
        percent_changes.append(percentage_change(start, indexes[x]))

    return percent_changes


def correlation_coeff(x: list, y: list) -> float:
    """
    Calculates a value in [-1,1] to determine how related the x and y values are

    >>> x = [1, 2, 3, 4, 5]
    >>> y = [2, 4, 6, 8, 10]  # direct linear relation
    >>> y1 = [2, 3, 5, 9, 11]  # closely related but not linear
    >>> y2 = [0, 0, 0.5, 0.09, 0]  #
    >>> correlation_coeff(x, y)
    1.0
    >>> correlation_coeff(x, y1)
    0.9798
    >>> correlation_coeff(x, y2)
    0.0656
    """
    n = len(x)
    print(x[0], ' ', y[0])
    xy = [x[i] * y[i] for i in range(n)]
    x2 = [num ** 2 for num in x]
    y2 = [num ** 2 for num in y]

    numerator = (n * sum(xy)) - (sum(x) * sum(y))
    denominator1 = ((n * sum(x2)) - (sum(x) ** 2))
    denominator2 = ((n * sum(y2)) - (sum(y) ** 2))

    # later deleted
    try:
        denominator = math.sqrt(denominator1 * denominator2)
        value = round(numerator / denominator, 4)
    except:
        value = 0

    return value


def get_stats(percent_changes: list[float]) -> tuple:
    """
    Returns the mean, median and standard deviation of the data

    >>> values = [1, 2, 4, 6]
    >>> get_stats(values)
    (3.25, 3.0, 1.9203)
    """
    mean = numpy.mean(percent_changes)
    median = numpy.median(percent_changes)
    st_dev = numpy.std(percent_changes)

    return (round(mean, 4), round(median, 4), round(st_dev, 4))


def index_recovered(start: float, current: float) -> bool:
    """
    Determines whether the stock index recovered after the crash

    >>> precovid_stock = 4000
    >>> current_stock = 4001
    >>> index_recovered(precovid_stock, current_stock)
    True
    """
    return current >= start


def count_months(dates: list[str], indexes: list[float]) -> int:
    """
    Counts the months it took for the stock index to recover after the crash

    >>> dates = ["January 21, 2020","February 4, 2020", "March 3, 2020", "April 7, 2020", "May 10, 2020", "June 15, 2020"]
    >>> dates2 = ["January 21, 2020","February 4, 2020", "March 3, 2020", "March 9, 2020", "April 11, 2020", "May 16, 2020"]
    >>> indexes = [5000, 4000, 100, 2000, 3000, 50001]
    >>> count_months(dates, indexes)
    3
    >>> count_months(dates2, indexes)
    2
    """
    # creating a list of months
    months = [date.split(' ')[0] for date in dates]

    # will eventually hold the index of the lowest index in the list
    i = 0

    # arbitrary number for the comparison
    min_val = float('inf')

    # finding the minimum value and its index
    for x in range(len(indexes)):
        if indexes[x] < min_val:
            i = x  # the index will update here
            min_val = indexes[x]

    # the value from before the crash
    start = indexes[0]

    # the month on the date of the minimum index value
    last_month = months[i]

    # this will keep track of the months that have since passed
    count = 1

    # the loop will iterate until the stock recovers
    while indexes[i] < start:
        if months[i] != last_month:
            count += 1
            last_month = months[i]
        i += 1

    return count


@dataclass
class Country:
    """
    A country, described by its financial state and covid cases.

        Instance Attributes:
            - name: The name of the country
            - dates: The dates at which the stock index prices were recorded
            - cases: The weekly average of cases
            - dates_c: The dates at which the weekly averages are centered at
            - prices: The prices of the stock indexes
            - percent_changes: The percentage changes in stock index prices every week
            - mean: The average percentage change in stock index prices
            - median: The median value of percentage changes in stock index prices
            - standard_deviation: The standard deviation of percentage changes in stock index prices
            - correlation_coefficient: A measure of how closely related covid cases and stock index prices are
            - recovered: Whether or not the country's stock index prices recovered

        Representation Invariants:
            - self.name != ''
            - len(dates) == len(prices)
            - len(cases) == len(dates_c)

        Sample Usage:
        >>> dates = ['March 2, 2021', 'April 3, 2021', 'May 4, 2021']
        >>> prices = [1000, 2000, 3000]
        >>> cases = [50, 70]
        >>> cdates = ['April 3, 2021', 'May 4, 2021']
        >>> per_change = percentage_list(prices)
        >>> mean, median, stan_dev = get_stats(per_change)
        >>> r2 = correlation_coeff(cases, prices)
        >>> rec = index_recovered(prices[0], prices[len(prices) - 1])
        >>> usa = Country('United States', dates, cases, cdates, prices, per_change, mean, median, stan_dev, r2, rec)
        """
    name: str
    dates: list[str]
    cases: list
    dates_c: list[str]
    prices: list[float]
    percent_changes: list[float]
    mean: float
    median: float
    standard_deviation: float
    correlation_coefficient: float
    recovered: bool
