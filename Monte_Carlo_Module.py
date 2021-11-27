# coding: utf-8

import numpy as np
import pandas as pd
import math
# import statistics as st

class Laundry:
    '''
    This class contains the basic and initial information of washing machines and dryers of the laundry.
    '''
    def __init__(self, num_WashMachine, num_Dryer, num_user, time_interval, washTime, dryTime, frequency):
        '''
        This function assigns the initial value for the attributes.
        :param num_WashMachine: number of washing machines
        :param num_Dryer: number of dryers
        :param num_user: number of people doing laundry each day
        :param time_interval: The time to wait for the user to take out the clothes each time the washing machine or dryer finishes its work (0 min< time< 15 mins)
        :param washTime: Each washing time of the washing machine (25 mins<time<70 mins)
        :param dryTime: Each working time of the dryer (35 mins<time<140 mins)
        :param frequency: The washing frequency of each unit.
        '''
        self.num_WashMachine = num_WashMachine
        self.num_Dryer = num_Dryer
        self.num_user = num_user
        self.time_interval = time_interval
        self.washTime = washTime
        self.dryTime = dryTime
        self.frequency = frequency