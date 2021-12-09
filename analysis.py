import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import xlrd
# import openpyxl
# import geopandas
# from shapely import wkt

def read_files(filename):
    dataframes_dict = {}
    for i in range(2010,2020):
        file = "data/" + str(i) + "/" + str(filename) + ".csv"
        # file1 = "data/" + str(i) + "/ACCIDENT.csv"
        try:
            df = pd.read_csv(file)
        except:
            df = pd.read_csv(file, encoding= 'unicode_escape')
        dataframes_dict[i] = df
    return dataframes_dict