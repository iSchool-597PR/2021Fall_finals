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