"""This file is responsible for filing through data"""
import csv
import os


def delete_columns(filename: str) -> list[dict[str, float]]:
    """Opens a file and loads relevant data into a list"""
    data = []
    countries = {'France': 'EUR', 'Brazil': 'BRL', 'India': 'INR', 'Japan': 'JPY', 'US': 'USD'}
    currency = ''
    for name in countries:
        if name in filename:
            currency = countries[name]
            break

    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count != 0:
                data.append({"Date": format_date(row[0]), "Adj Close": convert_currency2(currency, format_num(row[5]))})
            line_count += 1
        return data


def format_num(value: str) -> float:
    """Returns a number without commas or spaces"""
    digits = []
    for char in value:
        if char.isnumeric() or (char == '.'):
            digits.append(char)
    numbers = ''.join(digits)
    if numbers == '':
        return 0
    num = float(numbers)
    return num


def convert_currency2(curr: str, value: float) -> float:
    """Converts the currency of the given value to USD but uses my code"""
    conversions = {'BRL': 0.18, 'EUR': 1.13, 'INR': 0.013, 'JPY': 0.0088, 'USD': 1}
    return round(value * conversions[curr], 2)


def format_date(value: str) -> str:
    """Returns the correctly formatted date"""
    months = {'Jan.': 'January', 'Feb.': 'February', 'Mar.': 'March', 'Apr.': 'April',
              'Jun.': 'June', 'Jul.': 'July', 'Aug.': 'August', 'Sep.': 'September',
              'Oct.': 'October', 'Nov.': 'November', 'Dec.': 'December'}
    date = value.split()
    month_abrv = date[0]
    if month_abrv in months:
        date[0] = months[month_abrv]
    return ' '.join(date)


def generate_file(title: str, data: list[dict[str, float]]) -> None:
    """Generates a csv file based on the given data"""
    with open(title, mode='w', newline='') as csv_file:
        fieldnames = ["Date", "Adj Close"]
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        n = len(data)
        writer.writeheader()
        for x in range(n):
            item = data[n - 1 - x]
            writer.writerow(item)


if __name__ == '__main__':
    raw_files = ['Brazil_stock.csv', 'France_stock.csv', 'India_stock.csv', 'Japan_stock.csv', 'US_stock.csv']

    for filename in raw_files:
        # checking if it is a file
        if os.path.isfile(filename):
            print(filename)
            updated = delete_columns(filename)
            print(updated)
            title = filename
            generate_file(title, updated)
