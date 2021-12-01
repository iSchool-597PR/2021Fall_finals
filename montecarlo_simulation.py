
import pandas as pd
import numpy as np
from geographiclib.geodesic import Geodesic

if __name__ == '__main__':

df = pd.read_csv('lat_long.csv')
ttl_ppl = df.loc[124 ,'Total Population' ] /2
insecure_percentage = df.loc[124 ,'Revised Projections March 2021 Food Insecurity%']
# assume 50% of food secured population might provide fresh food
potential_supply = (1 - insecure_percentage ) *0.5
ppl_insecure_per_day = int(ttl_ppl * insecure_percentage /7)
potential_supply_per_day = int(ttl_ppl * potential_supply /10)


food_bank = np.random.randint(1 ,potential_supply_per_day * 2, size=4)
food_balance = pd.DataFrame(food_bank, index=['d3', 'd2', 'd1', 'd0'], columns=['Balance'])
food_balance.index.name = 'Shelf_life'

waste = 0
total_supply = food_balance['Balance'].sum()

for n in range(1, 8):
    print('=============Day {} Begin============='.format(n))
    print('Original stock level:')
    print(food_balance)
    demand_a = np.random.randint(1, ppl_insecure_per_day)
    supply_a = np.random.randint(1, potential_supply_per_day)
    total_supply += supply_a

    # suppose the time limitation of fresh food A send to food bank can always keep 3 days
    food_balance.loc['d3', 'Balance'] += supply_a
    print('--------------------------------')
    print('Food in stock after supply in:')
    print(food_balance)

    # allocate the demand from d3
    remain = demand_a
    for idx in food_balance.index:
        if remain > food_balance.loc[idx, 'Balance']:
            food_balance.loc[idx, 'Daily_demand'] = food_balance.loc[idx, 'Balance']
            remain -= food_balance.loc[idx, 'Balance']
        else:
            food_balance.loc[idx, 'Daily_demand'] = remain
            break

    food_balance = food_balance.fillna(0)
    food_balance['New_balance'] = food_balance['Balance'] - food_balance['Daily_demand']
    print('--------------------------------')
    print('Current food balance:')
    print(food_balance)

    waste += food_balance.loc['d0', 'New_balance']
    print('Current percentage of food waste: {:.2f}%'.format((waste / total_supply) * 100))
    food_balance['Balance'] = food_balance['New_balance']
    food_balance[['New_balance', 'Daily_demand']] = 0

    print('--------------------------------')
    print('Reset the balance and demand:')
    print(food_balance)
    print('=============Day {} End=============\n'.format(n))
