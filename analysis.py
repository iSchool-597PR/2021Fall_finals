import pandas as pd
# import numpy as np
import matplotlib.pyplot as plt
# import seaborn as sns
# import xlrd
# import openpyxl
import geopandas
# from shapely import wkt
import plotly.express as px

def read_file(year, filename):
    file = "data/" + str(year) + "/" + str(filename) + ".csv"
    # file1 = "data/" + str(i) + "/ACCIDENT.csv"
    try:
        df = pd.read_csv(file)
    except:
        df = pd.read_csv(file, encoding='unicode_escape')

    return df


def read_file_excel(year, filename, head=0):
    file = "data/" + str(year) + "/" + str(filename) + ".xlsx"
    # file1 = "data/" + str(i) + "/ACCIDENT.csv"
    try:
        df = pd.read_excel(file, header=head)
    except:
        df = pd.read_excel(file, header=head, encoding='unicode_escape')

    return df


def bar_line_chart(df, graph_details):
    x = []
    for year in range(graph_details["start_year"], 2020, 2):
        x.append(year)
    plt.figure(1, figsize=(15, 10))
    plt.title('{} and {} Rate per 100 Million VMT, {}-2019'.format(graph_details["ylabel"], graph_details["line_bar_key"],
                                                                   graph_details["start_year"]))
    barchart = plt.bar(df['Year'], df['Total {}'.format(graph_details["ylabel"])], color='green')
    plt.xlabel(graph_details["xlabel"])
    plt.ylabel(graph_details["ylabel"])
    plt.twinx()
    linechart = plt.plot(df['Year'], df['{} Rate per 100 Million VMT'.format(graph_details["line_bar_key"])], color='red')
    plt.xticks(x)
    plt.ylabel('{} Rate Per 100 Million VMT'.format(graph_details["line_bar_key"]))


def plot_line(df, col1, col2):
    fig = px.line(df, x="Year", y= df.columns[col1:col2])
    fig.show()


def values(df):
    total_killed = {}
    for index, row in df.iterrows():
        if (row['Vehicle Type'] != 'Total') and (row['Person Type'] == 'Subtotal'):
            total_killed[row['Vehicle Type']] = row['Occupants Killed']
        elif ((row['Vehicle Type'] == 'Motorcyclists' or row['Vehicle Type'] == 'Nonoccupants') and (
                row['Person Type'] == 'Total')):
            total_killed[row['Vehicle Type']] = row['Occupants Killed']
        else:
            continue
    return total_killed


def plotpie(dict1, year):
    labels = []
    number = []
    plt.figure(1, figsize=(7, 7))

    # Referred from
    # https://stackoverflow.com/questions/62593913/plotting-a-pie-chart-out-of-a-dictionary
    for x, y in dict1.items():
        labels.append(x)
        number.append(y)
    plt.pie(number, labels=labels, startangle=90, autopct='%1.1f%%',
            explode=(0.1, 0.1, 0.1, 0.1, 0.1), labeldistance=1.05)
    plt.axis('equal')
    plt.title(' Fatality Composition, by Person Type: {}'.format(year))
    plt.legend(labels, bbox_to_anchor=(1.7, 0.8), loc='center right')
    plt.show()


def states_shape_merge(df, year):

    states_shp = geopandas.read_file('data/geopandas/usa-states-census-2014.shp')
    states_shp = states_shp.merge(df[year], on="NAME")
    states_shp['fatalities{}'.format(year-1)] = states_shp['fatalities{}'.format(year-1)].str.replace(',', '').astype(int)
    return states_shp


def percent_change_plot(states_shp, col_name, year):
    fig = plt.figure(1, figsize=(25, 15))
    ax = fig.add_subplot()
    states_shp.apply(lambda x: ax.annotate(
    s=x.STUSPS + "\n" + str(x["fatalities{}".format(year-1)]) + "\n" + str(x["{}{}".format(col_name, year)]) + "%",
    xy=x.geometry.centroid.coords[0],
    ha='center', fontsize=15), axis=1)
    states_shp.boundary.plot(ax=ax, color='Black', linewidth=.10)
    states_shp.plot(ax=ax, cmap='Pastel2', figsize=(12, 12))
    plt.title('Fatalities in {} and percent change from {} to {}'.format(year, year-1, year))


def chloropleth(states_shp, col_name, year):
    fig, ax = plt.subplots(1, figsize=(12, 8))
    states_shp.apply(lambda x: ax.annotate(s=x.STUSPS, xy=x.geometry.centroid.coords[0], ha='center', fontsize=9), axis=1)
    states_shp.plot(column='{}{}'.format(col_name, year), cmap='Blues', linewidth=1, ax=ax, edgecolor='0.9', legend=True)
    plt.title('Fatalities in the USA in {}'.format(year))
    ax.axis('off')

def group_by_time(df):
    time_slots = ['12am - 2:59am', '3am - 5:59am', '6am - 8:59am', '9am - 11:59am',
                  '12pm - 2:59pm', '3pm - 5:59pm', '6pm - 8:59pm', '9pm - 11:59pm']
    for hour in range(0, 24, 3):
        df.loc[(df['HOUR'] >= hour) & (df['HOUR'] < hour + 3), 'category'] = time_slots[int(hour / 3)]
    dict_by_time = dict(df["category"].value_counts())
    return dict_by_time