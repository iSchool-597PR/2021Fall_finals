# coding: utf-8

import numpy as np
import pandas as pd
import math
from collections import deque, OrderedDict
from collections import Counter
# import statistics as st

def num_assign(num_resident):
    # frequency = k execute k times num_assign();
    # according to "readme.md" -- The orchard downs contains almost same number of 2B2B and 1B1B. About 40% of 2B2B
    # tenants are families (more than 3 people), about 20% are one person, and about 40% are two people. For 1B1B,
    # about 50% are two people living, and about 50% are living alone.

    num_2b2b = math.floor(num_resident/2)
    num_1b1b = num_resident - num_2b2b

    family = math.floor(0.4 * num_2b2b)
    solitude = math.floor(0.4 * num_2b2b + 0.5 * num_1b1b)
    couple = num_resident - family - solitude

    # Because people have a greater probability of doing laundry on weekends, suppose the probability of doing laundry on weekends is 0.7, and the probability of doing laundry on workdays is 0.3
    num_family_weekday, num_solitude_weekday, num_couple_weekday = \
        np.random.binomial(family,0.3), np.random.binomial(solitude,0.3), np.random.binomial(couple,0.3) # Number of people doing laundry on weekdays
    num_family_weekend, num_solitude_weekend, num_couple_weekend = \
        family - num_family_weekday, family - num_solitude_weekday, family - num_couple_weekday # Number of people doing laundry on weekends

    # Random allocation Specific laundry days -- Workdays (Monday~Friday), Weekends (Saturday~Sunday)
    family_weekday_assign = dict(Counter((np.random.randint(1, 6, size=num_family_weekday))))
    solitude_weekday_assign = dict(Counter((np.random.randint(1, 6, size=num_solitude_weekday))))
    couple_weekday_assign = dict(Counter((np.random.randint(1, 6, size=num_couple_weekday))))
    family_weekend_assign = dict(Counter((np.random.randint(6, 8, size=num_family_weekend))))
    solitude_weekend_assign = dict(Counter((np.random.randint(6, 8, size=num_solitude_weekend))))
    couple_weekend_assign = dict(Counter((np.random.randint(6, 8, size=num_couple_weekend))))

    # for each list stores [family_num, solitude_num, couple_num]
    Monday_num = [family_weekday_assign[1],solitude_weekday_assign[1],couple_weekday_assign[1]]
    Tuesday_num = [family_weekday_assign[2], solitude_weekday_assign[2], couple_weekday_assign[2]]
    Wednesday_num = [family_weekday_assign[3], solitude_weekday_assign[3], couple_weekday_assign[3]]
    Thursday_num = [family_weekday_assign[4], solitude_weekday_assign[4], couple_weekday_assign[4]]
    Friday_num = [family_weekday_assign[5], solitude_weekday_assign[5], couple_weekday_assign[5]]
    Saturday_num = [family_weekend_assign[6], solitude_weekend_assign[6], couple_weekend_assign[6]]
    Sunday_num = [family_weekend_assign[7], solitude_weekend_assign[7], couple_weekend_assign[7]]

    # Return the number of people in three different units per day
    return Monday_num, Tuesday_num, Wednesday_num, Thursday_num, Friday_num, Saturday_num, Sunday_num


def total_num_of_eachday(num_resident, frequency=1):
    Monday_num, Tuesday_num, Wednesday_num, Thursday_num, Friday_num, Saturday_num, Sunday_num = 0, 0, 0, 0, 0, 0, 0

    # The number of people in line according to "frequency"
    for _ in range(frequency):
        m1, t1, w1, t2, f1, s1, s2 = num_assign(num_resident)
        Monday_num += m1
        Tuesday_num += t1
        Wednesday_num += w1
        Thursday_num += t2
        Friday_num += f1
        Saturday_num += s1
        Sunday_num += s2

    return Monday_num, Tuesday_num, Wednesday_num, Thursday_num, Friday_num, Saturday_num, Sunday_num


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
        :param frequency: The washing frequencnum_residenty of each unit.
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
        Call the class object within the function.
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

    # 银行排队模型
    def Que_Module(self, total_num_of_users):
        # First we plan to separate each day into seven time intervals:
        #       8am-10am, 10am-12pm, 12pm-2pm, 2pm-4pm, 4pm-6pm, 6pm-8pm, 8pm-10pm
        #   A new batch of laundry customers will be added at the initial time of each interval (like 8am, 10am, 12pm, 2pm, ...)


        pass

    def QueBank(self, tmp):
        empty = deque([])
        count1 = deque([])
        count2 = deque([])
        count3 = deque([])
        count4 = deque([])
        wait_dict = dict()
        count1_waitime = 0
        count2_waitime = 0
        count3_waitime = 0
        count4_waitime = 0
        results = []
        for i in range(len(tmp)):
            count_waitime = [count1_waitime, count2_waitime, count3_waitime, count4_waitime]
            Best_count = count_waitime.index(min(count_waitime))
            if Best_count == 0:
                count1.append(i + 1)
                count1_waitime += int(tmp[i]) * 5
                if count1_waitime not in wait_dict:
                    wait_dict[count1_waitime] = [(i + 1, 1)]
                else:
                    wait_dict[count1_waitime].append((i + 1, 1))
            elif Best_count == 1:
                count2.append(i + 1)
                count2_waitime += int(tmp[i]) * 5
                if count2_waitime not in wait_dict:
                    wait_dict[count2_waitime] = [(i + 1, 2)]
                else:
                    wait_dict[count2_waitime].append((i + 1, 2))
            elif Best_count == 2:
                count3.append(i + 1)
                count3_waitime += int(tmp[i]) * 5
                if count3_waitime not in wait_dict:
                    wait_dict[count3_waitime] = [(i + 1, 3)]
                else:
                    wait_dict[count3_waitime].append((i + 1, 3))
            elif Best_count == 3:
                count4.append(i + 1)
                count4_waitime += int(tmp[i]) * 5
                if count4_waitime not in wait_dict:
                    wait_dict[count4_waitime] = [(i + 1, 4)]
                else:
                    wait_dict[count4_waitime].append((i + 1, 4))
        order = sorted(wait_dict)
        results = []
        for key in order:
            sort_value = sorted(wait_dict[key], key=lambda t: t[1])
            results.append([each[0] for each in sort_value])
        tmp = []
        for each in results:
            tmp += each
        return tmp

    tmp = input().split(" ")

    tmp = [str(each) for each in QueBank(tmp)]
    print(" ".join(tmp))
