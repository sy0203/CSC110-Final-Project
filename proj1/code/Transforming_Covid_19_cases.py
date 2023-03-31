"""Transforming Covid-19 dataset to make the data ready for computations"""
import pandas
import pandas as pd

# brazil
brazil_data = pd.read_csv('Covid-19 cases.csv')

extra_countries = set()

brazil_data = brazil_data.set_index('location')

for i in range(0, len(brazil_data.index)):
    if brazil_data.index[i] not in {'Brazil'}:
        extra_countries.add(brazil_data.index[i])

brazil_data.drop(extra_countries, axis=0, inplace=True)
brazil_data.index = range(616)
print(brazil_data)

date_list = ['2020-01-22', '2020-01-23', '2020-01-24', '2020-01-25', '2020-01-26',
             '2020-01-27', '2020-01-28', '2020-01-29', '2020-01-30', '2020-01-31',
             '2020-02-01', '2020-02-02', '2020-02-03', '2020-02-04', '2020-02-05',
             '2020-02-06', '2020-02-07', '2020-02-08', '2020-02-09', '2020-02-10',
             '2020-02-11', '2020-02-12', '2020-02-13', '2020-02-14', '2020-02-15',
             '2020-02-16', '2020-02-17', '2020-02-18', '2020-02-19', '2020-02-20',
             '2020-02-21', '2020-02-22', '2020-02-23', '2020-02-24', '2020-02-25']
case_date = []

for date in range(0, 616):
    case_date.append(brazil_data.values[date][0])

total_cases_lst = []
for x in range(0, 616):
    total_cases_lst.append(brazil_data.values[x][1])

new_case_lst = []
for y in range(0, 616):
    new_case_lst.append(brazil_data.values[y][2])

num = 0
y = 0
while num < (len(date_list) + 616):
    if num < len(date_list):
        brazil_data.iloc[num] = [date_list[num], 0, 0]
        num += 1
    else:
        brazil_data.loc[num] = [case_date[y], total_cases_lst[y], new_case_lst[y]]
        y += 1
        num += 1

brazil_data.drop_duplicates()
print(brazil_data)

average_weekly_cases = []
weekly_intervals = []
i = 0
while i < 644:
    weekly_cases = (brazil_data.values[i + 7][1] - brazil_data.values[i][1])
    weekly_intervals.append(brazil_data.values[i][0] + ' - ' + brazil_data.values[i + 6][0])
    average_weekly_cases.append(weekly_cases // 7)
    i += 7

data = pd.DataFrame()
data['Week'] = weekly_intervals
data['Average Weekly Cases'] = average_weekly_cases
data.to_csv('Brazil_cases.csv')

# Japan

japan_data = pd.read_csv('Covid-19 cases.csv')

extra_countries = set()

japan_data = japan_data.set_index('location')

for i in range(0, len(japan_data.index)):
    if japan_data.index[i] not in {'Japan'}:
        extra_countries.add(japan_data.index[i])

japan_data.drop(extra_countries, axis=0, inplace=True)
japan_data.index = range(651)
print(japan_data)

average_weekly_cases_j = []
weekly_intervals_j = []
i = 0
while i < 644:
    weekly_cases = (japan_data.values[i + 7][1] - japan_data.values[i][1])
    weekly_intervals_j.append(japan_data.values[i][0] + ' - ' + japan_data.values[i + 6][0])
    average_weekly_cases_j.append(weekly_cases // 7)
    i += 7

data_japan = pd.DataFrame()
data_japan['Week'] = weekly_intervals_j
data_japan['Average Weekly Cases'] = average_weekly_cases_j
data_japan.to_csv('Japan_cases.csv')

# USA

usa_data = pd.read_csv('Covid-19 cases.csv')

extra_countries = set()

usa_data = usa_data.set_index('location')

for i in range(0, len(usa_data.index)):
    if usa_data.index[i] not in {'United States'}:
        extra_countries.add(usa_data.index[i])

usa_data.drop(extra_countries, axis=0, inplace=True)
usa_data.index = range(651)
print(usa_data)

average_weekly_cases_usa = []
weekly_intervals_usa = []
i = 0
while i < 644:
    weekly_cases = (usa_data.values[i + 7][1] - usa_data.values[i][1])
    weekly_intervals_usa.append(usa_data.values[i][0] + ' - ' + usa_data.values[i + 6][0])
    average_weekly_cases_usa.append(weekly_cases // 7)
    i += 7

data_usa = pd.DataFrame()
data_usa['Week'] = weekly_intervals_usa
data_usa['Average Weekly Cases'] = average_weekly_cases_usa
data_usa.to_csv('USA_cases.csv')

# France

france_data = pd.read_csv('Covid-19 cases.csv')

extra_countries = set()

france_data = france_data.set_index('location')

for i in range(0, len(france_data.index)):
    if france_data.index[i] not in {'France'}:
        extra_countries.add(france_data.index[i])

france_data.drop(extra_countries, axis=0, inplace=True)
france_data.index = range(649)
print(france_data)

date_list_f = ['2020-01-22', '2020-01-23']
case_date_f = []

for date in range(0, 649):
    case_date_f.append(france_data.values[date][0])

total_cases_lst_f = []
for x in range(0, 649):
    total_cases_lst_f.append(france_data.values[x][1])

new_case_lst_f = []
for y in range(0, 649):
    new_case_lst_f.append(france_data.values[y][2])

num = 0
y = 0
while num < (len(date_list_f) + 649):
    if num < len(date_list_f):
        france_data.iloc[num] = [date_list_f[num], 0, 0]
        num += 1
    else:
        france_data.loc[num] = [case_date_f[y], total_cases_lst_f[y], new_case_lst_f[y]]
        y += 1
        num += 1

france_data.drop_duplicates()
print(france_data)

average_weekly_cases_f = []
weekly_intervals_f = []
i = 0
while i < 644:
    weekly_cases = (france_data.values[i + 7][1] - france_data.values[i][1])
    weekly_intervals_f.append(france_data.values[i][0] + ' - ' + france_data.values[i + 6][0])
    average_weekly_cases_f.append(weekly_cases // 7)
    i += 7

data = pd.DataFrame()
data['Week'] = weekly_intervals
data['Average Weekly Cases'] = average_weekly_cases
data.to_csv('France_cases.csv')

# India
india_data = pd.read_csv('Covid-19 cases.csv')
extra_countries = set()

india_data = india_data.set_index('location')

for i in range(0, len(india_data.index)):
    if india_data.index[i] not in {'India'}:
        extra_countries.add(india_data.index[i])

india_data.drop(extra_countries, axis=0, inplace=True)
india_data.index = range(643)
print(india_data)

date_list_i = ['2020-01-22', '2020-01-23', '2020-01-24', '2020-01-25', '2020-01-26', '2020-01-27',
               '2020-01-28', '2020-01-29']
case_date_i = []

for date in range(0, 643):
    case_date_i.append(india_data.values[date][0])

total_cases_lst_i = []
for x in range(0, 643):
    total_cases_lst_i.append(india_data.values[x][1])

new_case_lst_i = []
for y in range(0, 643):
    new_case_lst_i.append(india_data.values[y][2])

num_i = 0
y_1 = 0
while num_i < (len(date_list_i) + 643):
    if num_i < len(date_list_i):
        india_data.iloc[num_i] = [date_list_i[num_i], 0, 0]
        num_i += 1
    else:
        india_data.loc[num_i] = [case_date_i[y_1], total_cases_lst_i[y_1], new_case_lst_i[y_1]]
        y_1 += 1
        num_i += 1

india_data.drop_duplicates()
print(india_data)

average_weekly_cases_i = []
weekly_intervals_1 = []
i = 0
while i < 644:
    weekly_cases = (india_data.values[i + 7][1] - india_data.values[i][1])
    weekly_intervals_1.append(india_data.values[i][0] + ' - ' + india_data.values[i + 6][0])
    average_weekly_cases_i.append(weekly_cases // 7)
    i += 7

data = pd.DataFrame()
data['Week'] = weekly_intervals_1
data['Average Weekly Cases'] = average_weekly_cases_i
data.to_csv('India_cases.csv')
