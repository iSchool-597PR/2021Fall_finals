# coding: utf-8

import numpy as np
import pandas as pd
import math
# import statistics as st

# code reference https://github.com/Zainabzav/final_projects/blob/master/montecarlo_module.py
class Laundry:
    '''
    This class contains the basic and initial information of washing machines and dryers of the laundry.
    We only consider the operation of the laundry room for a week, including five working days and a weekends.
    '''
    def __init__(self, num_WashMachine, num_Dryer, num_resident, time_interval, washTime, dryTime, frequency):
        '''
        This function assigns the initial value for the attributes.
        :param num_WashMachine: number of washing machines
        :param num_Dryer: number of dryers
        :param num_resident: number of residents
        :param time_interval: The time to wait for the user to take out the clothes each time the washing machine or dryer finishes its work (0 min< time< 15 mins)
        :param washTime: Each washing time of the washing machine (25 mins<time<70 mins)
        :param dryTime: Each working time of the dryer (35 mins<time<140 mins)
        :param frequency: The washing frequency of each unit.
        '''
        self.num_WashMachine = num_WashMachine
        self.num_Dryer = num_Dryer
        self.num_resident = num_resident
        self.time_interval = time_interval
        self.washTime = washTime
        self.dryTime = dryTime
        self.frequency = frequency

    @classmethod
    def attribute_assign(cls):
        '''
        Call the class object within the function
        :return: class object (Laundry)
        '''
        num_WashMachine = int(input("The Number of washing machines (Integer greater than 0):"))
        num_Dryer = int(input("The Number of dryers (Integer greater than 0):"))
        num_resident = int(input("The Number of resident (greater than 0):"))
        time_interval = input("The time to wait for the user to take out the clothes each time the washing machine or dryer finishes its work (0 min< time< 15 mins):")
        washTime = input("Each washing time of the washing machine (25 mins<time<70 mins):")
        dryTime = input("Each working time of the dryer (35 mins<time<140 mins):")
        frequency = input("The washing frequency of each unit (* times/a week):")

        return cls(num_WashMachine, num_Dryer, num_resident, time_interval, washTime, dryTime, frequency)

    def random_simulation(self, num_WashMachine, num_Dryer, num_resident, time_interval, washTime, dryTime, frequency):
        pass