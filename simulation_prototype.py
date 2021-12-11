"""
This is our primary simulation module for single food bank with daily update outputs.
We keep it here only for testing and validation.
"""
import pandas as pd
import numpy as np

def mod_pert_random(low, likely, high, confidence=4, samples=1):
    """ (Refer to Mr. Weible's in-class materials.)
    Produce random numbers according to the 'Modified PERT' distribution.

    :param low: The lowest value expected as possible.
    :param likely: The 'most likely' value, statistically, the mode.
    :param high: The highest value expected as possible.
    :param confidence: This is typically called 'lambda' in literature
                        about the Modified PERT distribution. The value
                        4 here matches the standard PERT curve. Higher
                        values indicate higher confidence in the mode.
                        Currently allows values 1-18

    Formulas to convert beta to PERT are adapted from a whitepaper
    "Modified Pert Simulation" by Paulo Buchsbaum.
    """
    # Check for reasonable confidence levels to allow:
    if confidence < 1 or confidence > 18:
        raise ValueError('confidence value must be in range 1-18.')

    mean = (low + confidence * likely + high) / (confidence + 2)

    a = (mean - low) / (high - low) * (confidence + 2)
    b = ((confidence + 1) * high - low - confidence * likely) / (high - low)

    beta = np.random.beta(a, b, samples)
    beta = beta * (high - low) + low
    return beta

if __name__ == '__main__':

    df = pd.read_csv('foodbank_with_latlon.csv',
                     usecols=['Food Bank', 'ID', 'Total Population', '2021 Food Insecurity %',
                              '2021 Food Insecurity #', 'latitude', 'longitude'])
    df = df.set_index('ID')

    # calculate food waste of each food bank for 14-days basis
    days = 14
    # level of freshness: d5 means the food will spoil in 5 days
    shelf_life = ['d5', 'd4', 'd3', 'd2', 'd1', 'd0']
    # shelf_life = ['d3', 'd2', 'd1', 'd0']

    # choose one food bank as an example
    ttl_ppl = df.loc[124, 'Total Population']
    insecure_percentage = df.loc[124, '2021 Food Insecurity %']

    # assume 50% of food secured population might provide fresh food
    potential_supply = (1 - insecure_percentage) * 0.5
    ppl_insecure = round(ttl_ppl * insecure_percentage, 0)
    ppl_potential_supply = round(ttl_ppl * potential_supply, 0)

    supply_initial = mod_pert_random((1/10)*ppl_potential_supply, (1/7)*ppl_potential_supply,
                                     (1/3)*ppl_potential_supply, samples=len(shelf_life)).astype(int)
    food_balance = pd.DataFrame(supply_initial, index=shelf_life, columns=['Balance'])
    food_balance.index.name = 'Shelf_life'

    # generate random variables for simulation
    demand = np.rint(mod_pert_random((1/7)*ppl_insecure, (1.6/7)*ppl_insecure, ppl_insecure, samples=days))
    # demand = np.random.poisson(ppl_insecure * (1.6 / 7))
    # supply = np.random.binomial(ppl_potential_supply, 0.1)
    supply = np.rint(mod_pert_random((1/10)*ppl_potential_supply, (1/7)*ppl_potential_supply,
                                     (1/3)*ppl_potential_supply, samples=days))

    # initiate total waste and supply
    waste = 0
    total_daily_demand = 0
    total_supply = food_balance['Balance'].sum()

    # run 14 days
    for day in range(0, days):
        food_balance[['Daily_demand', 'Current_balance']] = 0
        print('================== Day {} Begin =================='.format(day+1))
        print('Original stock level:')
        print(food_balance)
        total_supply += supply[day]

        # suppose the fresh food sent to food bank are always in best freshness
        food_balance.loc[shelf_life[0], 'Balance'] += supply[day]
        print('--------------------------------------------------')
        print('After supply in:')
        print(food_balance)

        # allocate the demand from the freshest food (d5/d3) to indicate people's preference
        remain = demand[day]
        for idx in food_balance.index:
            # if demand is more than current d5/d3 numbers, the rest of them will go to next
            if remain > food_balance.loc[idx, 'Balance']:
                food_balance.loc[idx, 'Daily_demand'] = food_balance.loc[idx, 'Balance']
                remain -= food_balance.loc[idx, 'Balance']
            # if current food level is higher than demand, allocate the remain proportion of demand
            else:
                food_balance.loc[idx, 'Daily_demand'] = remain
                break

        food_balance = food_balance.fillna(0)
        food_balance['Current_balance'] = food_balance['Balance'] - food_balance['Daily_demand']
        total_daily_demand += food_balance['Daily_demand']
        print('--------------------------------------------------')
        print('Current balance:')
        print(food_balance)

        waste += food_balance.loc['d0', 'Current_balance']
        waste_percentage = (waste / total_supply) * 100
        print('--------------------------------------------------')
        print('Current percentage of food waste: {:.2f}%'.format(waste_percentage))
        food_balance['Balance'] = [0]+food_balance['Current_balance'].to_list()[0:len(shelf_life)-1]
        # food_balance[['Current_balance', 'Daily_demand']] = 0

        # print('------------------------------------------------')
        # print('Reset the balance and demand:')
        # print(food_balance)
        print('=================== Day {} End ===================\n'.format(day+1))

    # def print_summary_of_daily_balance(days, food_balance, total_daily_demand,waste_percentage):
    #
    #     summary = pd.concat([total_daily_demand, food_balance['Current_balance']], axis =1)
    #     print('================== {} Days Summary ============='.format(days))
    #     print(summary)
    #     print('------------------------------------------------')
    #     print('Accumulated percentage of food waste: {:.2f}%'.format(waste_percentage))
    #     print('================================================\n')
