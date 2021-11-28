# coding: utf-8

import numpy as np
import pandas as pd
import math
# import statistics as st

def workday_OR_weekend(max_resident, day):

    # only consider the cases in a week
    workday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    weekend = ["Saturday", "Sunday"]
    # residents prefer to wash in weekend
    workday_probability = 0.3
    weekend_probability = 0.6

    if day in workday:
        # today is workday, and residents
        pass

# code reference https://github.com/Zainabzav/final_projects/blob/master/montecarlo_module.py
class Laundry:
    '''
    This class contains the basic and initial information of washing machines and dryers of the laundry.
    We only consider the operation of the laundry room for a week, including five working days and a weekends.
    '''
    def __init__(self, num_WashMachine, num_Dryer, max_resident, time_interval, washTime, dryTime, frequency):
        '''
        This function assigns the initial value for the attributes.
        :param num_WashMachine: number of washing machines
        :param num_Dryer: number of dryers
        :param max_resident: maximum number of residents
        :param time_interval: The time to wait for the user to take out the clothes each time the washing machine or dryer finishes its work (0 min< time< 15 mins)
        :param washTime: Each washing time of the washing machine (25 mins<time<70 mins)
        :param dryTime: Each working time of the dryer (35 mins<time<140 mins)
        :param frequency: The washing frequency of each unit.
        '''
        self.num_WashMachine = num_WashMachine
        self.num_Dryer = num_Dryer
        self.max_resident = max_resident
        self.time_interval = time_interval
        self.washTime = washTime
        self.dryTime = dryTime
        self.frequency = frequency

    @classmethod
    def attribute_assign(cls):
        '''
        Call the class object within the function.
        :return: class object (Laundry)
        '''
        num_WashMachine = int(input("The Number of washing machines (Integer greater than 0):"))
        num_Dryer = int(input("The Number of dryers (Integer greater than 0):"))
        max_resident = int(input("The Maximum Number of resident (greater than 0):"))
        time_interval = input("The time to wait for the user to take out the clothes each time the washing machine or dryer finishes its work (0 min< time< 15 mins):")
        washTime = input("Each washing time of the washing machine (25 mins<time<70 mins):")
        dryTime = input("Each working time of the dryer (35 mins<time<140 mins):")
        frequency = input("The washing frequency of each unit (* times/a week):")

        return cls(num_WashMachine, num_Dryer, max_resident, time_interval, washTime, dryTime, frequency)

    def random_simulation(self, num_WashMachine, num_Dryer, max_resident, time_interval, washTime, dryTime, frequency):
        '''
        This function creat random variables to simulates the operation of the laundry within a week.
        :param num_WashMachine:
        :param num_Dryer:
        :param max_resident:
        :param time_interval:
        :param washTime:
        :param dryTime:
        :param frequency:
        :return:
        '''
        # set the timeline of a week
        pass

