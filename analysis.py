import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xlrd
# import openpyxl
# import geopandas
# from shapely import wkt

def read_file(year, filename):
    dataframes_dict = {}
    file = "data/" + str(year) + "/" + str(filename) + ".csv"
    # file1 = "data/" + str(i) + "/ACCIDENT.csv"
    try:
        df = pd.read_csv(file)
    except:
        df = pd.read_csv(file, encoding='unicode_escape')

    return df

def read_file_excel(year, filename, head = 0):
    dataframes_dict = {}
    file = "data/" + str(year) + "/" + str(filename) + ".xlsx"
    # file1 = "data/" + str(i) + "/ACCIDENT.csv"
    try:
        df = pd.read_excel(file, header = head)
    except:
        df = pd.read_excel(file, header = head, encoding='unicode_escape')

    return df