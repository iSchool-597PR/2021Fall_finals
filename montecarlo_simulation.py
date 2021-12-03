
import pandas as pd
import networkx as nx
import numpy as np
import math
from geopy.distance import geodesic


def cal_dis(node1,node2):
    return geodesic(node1,node2).km

def nearest(data, node, d):
    lon = data['longitude']
    lat = data['latitude']
    lat = lat.to_list()
    lon = lon.to_list()
    food_bank = data['Food Bank']
    food_bank = food_bank.to_list()
    loc1 = food_bank.index(node)
    lat1 = lat[loc1]
    lon1 = lon[loc1]
    node1 = [lat[loc1], lon[loc1]]
    distance_lst = []
    for i in food_bank:
        loc2 = food_bank.index(i)
        lat2 = lat[loc2]
        lon2 = lon[loc2]
        node2 = [lat[loc2], lon[loc2]]
        if cal_dis(node1, node2) >= d:
            distance_lst.append(cal_dis(node1, node2))

    return distance_lst



if __name__ == '__main__':

    df = pd.read_csv('lat_long.csv')
    # choose one food bank as an example
    ttl_ppl = df.loc[124, 'Total Population'] / 2
    insecure_percentage = df.loc[124, 'Revised Projections March 2021 Food Insecurity%']
    # assume 50% of food secured population might provide fresh food
    potential_supply = (1 - insecure_percentage) * 0.5
    ppl_insecure = math.ceil(ttl_ppl * insecure_percentage)
    ppl_potential_supply = math.ceil(ttl_ppl * potential_supply)
    # level of freshness: d3 means the food will spoil in 3 days
    shelf_life = ['d3', 'd2', 'd1', 'd0']

    # assume potential population provide supply once per ten days, the probability per day is 0.1
    supply_initial = np.random.binomial(ppl_potential_supply, 0.1, 4)
    food_balance = pd.DataFrame(supply_initial, index=shelf_life, columns=['Balance'])
    food_balance.index.name = 'Shelf_life'

    # initiate total waste and supply
    waste = 0
    total_supply = food_balance['Balance'].sum()

    # run 7 days
    for day in range(1, 8):

        print('================== Day {} Begin ================'.format(day))
        print('Original stock level:')
        print(food_balance)

        # an average of 1.6 shopping trips per week for each person, divide by 7 for the average per day
        # https://www.statista.com/statistics/251728/weekly-number-of-us-grocery-shopping-trips-per-household/
        demand = np.random.poisson(ppl_insecure * (1.6 / 7))
        supply = np.random.binomial(ppl_potential_supply, 0.1)
        total_supply += supply

        # suppose the fresh food sent to food bank are always in best freshness
        food_balance.loc['d3', 'Balance'] += supply
        print('------------------------------------------------')
        print('After supply in:')
        print(food_balance)

        # allocate the demand from d3 first to indicate people's preference to the most fresh food
        remain = demand
        for idx in food_balance.index:
            # if demand is more than current d3 numbers, the rest of them will go to d2
            if remain > food_balance.loc[idx, 'Balance']:
                food_balance.loc[idx, 'Daily_demand'] = food_balance.loc[idx, 'Balance']
                remain -= food_balance.loc[idx, 'Balance']
            # if current food level is higher than demand, allocate the remain proportion of demand
            else:
                food_balance.loc[idx, 'Daily_demand'] = remain
                break

        food_balance = food_balance.fillna(0)
        food_balance['New_balance'] = food_balance['Balance'] - food_balance['Daily_demand']
        print('------------------------------------------------')
        print('Current balance:')
        print(food_balance)

        waste += food_balance.loc['d0', 'New_balance']
        waste_percentage = (waste / total_supply) * 100
        print('------------------------------------------------')
        print('Current percentage of food waste: {:.2f}%'.format(waste_percentage))
        food_balance['Balance'] = [0]+food_balance['New_balance'].to_list()[0:3]
        food_balance[['New_balance', 'Daily_demand']] = 0

        print('------------------------------------------------')
        print('Reset the balance and demand:')
        print(food_balance)
        print('=================== Day {} End =================\n'.format(day))


