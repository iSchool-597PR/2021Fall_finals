# coding: utf-8

import numpy as np
import pandas as pd
import math
from collections import deque, OrderedDict
from collections import Counter
# import statistics as st

def num_assign(num_resident):
    # frequency = k 执行k次num_assign();
    # according to "readme.md" -- The orchard downs contains almost same number of 2B2B and 1B1B. About 40% of 2B2B
    # tenants are families (more than 3 people), about 20% are one person, and about 40% are two people. For 1B1B,
    # about 50% are two people living, and about 50% are living alone.

    num_2b2b = math.floor(num_resident/2)
    num_1b1b = num_resident - num_2b2b

    family = math.floor(0.4 * num_2b2b)
    solitude = math.floor(0.4 * num_2b2b + 0.5 * num_1b1b)
    couple = num_resident - family - solitude

    # 因为人们有更大的概率在周末洗衣服，假设在周末洗衣服概率为0.7，在工作日洗衣服概率为0.3
    # 假设在周末 人们洗衣服的人数 -- 0 代表在周末洗衣服；1 代表在工作日洗衣服
    num_family_weekday, num_solitude_weekday, num_couple_weekday = \
        np.random.binomial(family,0.3), np.random.binomial(solitude,0.3), np.random.binomial(couple,0.3) # 在工作日洗衣服的人数
    num_family_weekend, num_solitude_weekend, num_couple_weekend = \
        family - num_family_weekday, family - num_solitude_weekday, family - num_couple_weekday # 在周末洗衣服的人数
    # return num_family_weekday, num_family_weekend, num_solitude_weekday, num_solitude_weekend, num_couple_weekday, num_couple_weekend

    # 随机分配 具体洗衣时间 工作日（周一~周五）， 周末（周六~周日）
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
    return Monday_num, Tuesday_num, Wednesday_num, Thursday_num, Friday_num, Saturday_num, Sunday_num


def workday_OR_weekend(num_resident, day, frequency=1):

    # 首先分配

    # only consider the cases in a week
    workday = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    weekend = ["Saturday", "Sunday"]
    # residents prefer to wash in weekend
    workday_probability = 0.3
    weekend_probability = 0.6

    if day in workday:
        # today is workday, and residents
        random_value = []

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

    def random_simulation(self, num_WashMachine, num_Dryer, num_resident, time_interval, washTime, dryTime, frequency):
        '''
        This function creat random variables to simulates the operation of the laundry within a week.
        :param num_WashMachine:
        :param num_Dryer:
        :param num_resident:
        :param time_interval:
        :param washTime:
        :param dryTime:
        :param frequency:
        :return:
        '''
        # set the timeline of a week
        pass


    # 银行排队模型
    from collections import deque, OrderedDict
    def QueBank(tmp):
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
