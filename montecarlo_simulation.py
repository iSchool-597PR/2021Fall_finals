"""
IS 597PR: Programming for Analytics & Data Processing
Final Project: Fresh Food Supply Network Simulation
Authors: Candice Chen, Kinjal Shah
"""
import pandas as pd
import networkx as nx
import numpy as np
from geopy.distance import geodesic
import matplotlib.pyplot as plt


def calculate_distance(node1: tuple, node2: tuple) -> float:
    """
    This function calculates distance between any two food banks.
    :param node1: dataframe with latitude and longitude values
    :param node1: food bank 1
    :param node2: food bank 2
    :return: distance in km
    """
    return geodesic(node1, node2).km


def create_graph(df: pd.DataFrame) -> nx.Graph:
    """
    Create graph from the dataframe with particular attributes, such as food-insecure population.
    :param df: dataframe from the data set
    :return: a graph with nodes and their attributes
    """
    g = nx.Graph()
    df = df.set_index('ID')
    attrs = df.to_dict('index')
    g.add_nodes_from(df.index)
    nx.set_node_attributes(g, attrs)
    return g

def create_shelflife_list() -> list:
    """
    Create a list to show level of freshness by randomly selecting 3 to 7 days.
    For example, d3 means the food will spoil in 3 days.
    :return: a list of labels for daily simulation

    >>> len(create_shelflife_list(5))
    5
    >>> shelf = create_shelflife_list(4)
    >>> shelf[-1]
    'd0'
    """
    day_list = [3, 4, 5, 6, 7]
    days = int(np.random.choice(day_list, 1))

    shelf_life = []
    for d in range(days, -1, -1):
        life = 'd' + str(d)
        shelf_life.append(life)

    return shelf_life


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
    :param samples:

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

def generate_random_variables(g: nx.Graph, node: int, variable_type: str, days=7) -> np.array:
    """
    To generate random supply or demand for a single food bank by Modified PERT distribution in particular days.
    For the supply side, we assume the lowest frequency of supply is once per 10 days.
    The highest frequency is once per 3 days. And the most likely is once per 7 days.
    For the demand side, according to the reference, an average of 1.6 shopping trips per week for each person.
    So we use 1.6/7 for the most likelihood. We assume the lowest frequency is once per week while the highest
    frequency is every day, which equal to 1.

    The reference of the fact that an average of 1.6 shopping trips per week for each person:
    https://www.statista.com/statistics/251728/weekly-number-of-us-grocery-shopping-trips-per-household/

    :param g: graph with attributes
    :param node: node in a graph
    :param variable_type: demand or supply
    :param days: to generate same number of random variables
    :return: an array random numbers

    >>> gh = nx.Graph
    >>> df_regional.to_dict('index')
    {1: {'Food Bank': 'High Plains Food Bank', 'ID': 2, 'Total Population': 475188.0, '2021 Food Insecurity %': 0.161,
    '2021 Food Insecurity #': 76360, 'state_y': 'Texas', 'statecode': 'TX', 'latitude': 35.1964, 'longitude': -101.8034},
    ... 'latitude': 31.6446, 'longitude': -106.2737}}

    >>> gh.add_nodes_from(adict)
    >>> gh[1]['2021 Food Insecurity #']
    TypeError
    >>> gh[0] is None
    True

    """
    node_ppl = g.nodes[node]['Total Population']
    insecure_ppl = g.nodes[node]['2021 Food Insecurity #']
    potential_supply_ppl = (node_ppl - insecure_ppl) * 0.5
    if variable_type == 'demand':
        demand = np.rint(mod_pert_random((1 / 7) * insecure_ppl, (1.6 / 7) * insecure_ppl, insecure_ppl, samples=days))
        return demand

    if variable_type == 'supply':
        supply = np.rint(mod_pert_random((1 / 10) * potential_supply_ppl, (1 / 7) * potential_supply_ppl,
                                         (1 / 3) * potential_supply_ppl, samples=days))
        return supply


def calculate_share_supply_rate(demand_gap_rate: float) -> float:
    """
    We design a method to decide the actual proportion of share supply to neighbors.
    use the percentage of demand_gap over potential_supply_ppl as the potential share supply to neighbor
    :param demand_gap_rate: a float number caculated from two food banks's demand and supply
    :return: a float number
    """

    if demand_gap_rate > 0.2:
        rate = 0.1
    elif 0.1 < demand_gap_rate <= 0.2:
        rate = demand_gap_rate / 2
    else:
        rate = 0.01
    return rate


def calculate_actual_share_supply(g: nx.Graph) -> None:
    """
    This function calculate the sharing supply between two food banks.
    The food bank with higher demand indicate extra supply needed,
    so the other would share a proportion of their supply based on the demand gap.
    :param g:
    :return:
    >>> for node1, node2 in list(g.edges):
    >>>     j, k  = node1, node2
    >>>     break
    >>> graph[j]['share_supply'] == graph[k]['extra_supply'] or graph[j]['extra_supply'] == graph[k]['share_supply']
    True

    """

    for node1, node2 in list(g.edges(data=False)):
        # calculate the gap of food insecure population between two food banks
        insecure_ppl_node = g.nodes[node1]['2021 Food Insecurity #']
        insecure_ppl_neighbor = g.nodes[node2]['2021 Food Insecurity #']
        demand_gap = insecure_ppl_node - insecure_ppl_neighbor
        # the neighbors with same population are in similar demand and supply so we ignore them
        if demand_gap == 0:
            continue
        elif demand_gap > 0:
            share_supply_node = node1
            receive_supply_node = node2
        else:
            share_supply_node = node2
            receive_supply_node = node1
            demand_gap = abs(demand_gap)

        node_ppl = g.nodes[share_supply_node]['Total Population']
        insecure_ppl_node = g.nodes[share_supply_node]['2021 Food Insecurity #']
        potential_supply_ppl = (node_ppl - insecure_ppl_node) * 0.5
        # use the percentage of demand_gap over potential_supply_ppl as the potential share supply to neighbor
        demand_gap_rate = demand_gap / potential_supply_ppl
        # we design a method to decide the actual proportion of share supply to neighbors
        share_supply_rate = calculate_share_supply_rate(demand_gap_rate)
        actual_share_supply = np.rint(g.nodes[share_supply_node]['supply'] * share_supply_rate)
        share_supply_update = g.nodes[share_supply_node]['share_supply'] + actual_share_supply
        extra_supply_update = g.nodes[receive_supply_node]['extra_supply'] + actual_share_supply
        # update node attribute after sharing
        nx.set_node_attributes(g, {share_supply_node: {'share_supply': share_supply_update},
                                   receive_supply_node: {'extra_supply': extra_supply_update}})


def add_edges_between_nearest_foodbanks(g: nx.Graph, distance_threshold=120) -> None:
    """
    The edges are added only when the distance between two nodes are the shortest.
    :param g: the graph
    :param distance_threshold: set a threshold of distance to create edges
    """

    list_of_nodes = list(g.nodes)
    for i in list_of_nodes:
        # initial distance and neighbor
        nearest = distance_threshold
        neighbor = 0
        node1 = g.nodes[i]['latitude'], g.nodes[i]['longitude']
        other_nodes = list_of_nodes.copy()
        other_nodes.remove(i)
        for fb in other_nodes:
            node2 = g.nodes[fb]['latitude'], g.nodes[fb]['longitude']
            distance = geodesic(node1, node2).km
            # find shortest distance
            if distance < nearest:
                nearest = distance
                neighbor = fb
        if neighbor != 0:
            g.add_edge(i, neighbor, distance=round(nearest, 3))


def initiate_random_supply(g: nx.Graph, days: int) -> None:
    """
    Initiate random supply for each food bank before daily operation or calculate sharing supply.
    This initial number will be stored in the graph as attributes of nodes.
    :param g:
    :param days:
    >>> initiate_random_supply(graph, 20)
    >>> len(graph[1]['supply']) == 20
    True
    """
    list_of_nodes = list(g.nodes)
    for node in list_of_nodes:
        supply = generate_random_variables(g, node, 'supply', days)
        nx.set_node_attributes(g, {node: {'supply': supply, 'share_supply': 0, 'extra_supply': 0}})


def daily_simulation(g: nx.Graph, node: int, supply: np.array, days=7) -> float:
    """
    This is our primary simulation module for single food bank with daily update outputs.
    :param g: the graph
    :param node: the food bank to simulate
    :param supply: total supply = supply - shared supply + add extra supply
    :param days: days to run for a cycle
    :return: percentage of food waste after operating many days
    """

    shelf_life = create_shelflife_list()

    supply_initial = generate_random_variables(g, node, 'supply', days=len(shelf_life))
    food_balance = pd.DataFrame(supply_initial, index=shelf_life, columns=['Balance'])
    food_balance.index.name = 'Shelf_life'

    demand = generate_random_variables(g, node, 'demand', days)

    # initiate total waste and supply
    waste = 0
    total_supply = food_balance['Balance'].sum()
    total_daily_demand = 0
    waste_percentage = 0

    for day in range(0, days):

        food_balance[['Daily_demand', 'Current_balance']] = 0
        total_supply += supply[day]

        # suppose the fresh food sent to food bank are always in best freshness
        food_balance.loc[shelf_life[0], 'Balance'] += supply[day]

        # allocate the demand from d3 first to indicate people's preference to the most fresh food
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

        waste += food_balance.loc['d0', 'Current_balance']
        waste_percentage = (waste / total_supply) * 100

        food_balance['Balance'] = [0] + food_balance['Current_balance'].to_list()[0:len(shelf_life) - 1]

    return waste_percentage

def mc_simulation(g: nx.Graph, times_to_run: int, network_supply: int, days=7) -> pd.DataFrame:
    """
    To simulate multiple times for two scenarios.
    :param g: the graph
    :param times_to_run: a number defined by user's input
    :param network_supply: 0: independent, 1: network
    :param days: days to run for a cycle
    :return: an overall results stored in a dataframe
    """

    count = 0
    list_of_nodes = list(g.nodes)

    # creat a dataframe to store the results
    result = pd.DataFrame(index=list_of_nodes)

    while count < times_to_run:
        nodes_results = []
        total_supply = None
        for node in list_of_nodes:
            if network_supply == 0:  # without network
                total_supply = g.nodes[node]['supply']
            if network_supply == 1:   # with network
                supply = g.nodes[node]['supply']
                extra_supply = g.nodes[node]['extra_supply']
                share_supply = g.nodes[node]['share_supply']
                total_supply = supply + extra_supply - share_supply

            waste_percentage = daily_simulation(g, node, total_supply, days)
            nodes_results.append(waste_percentage)

        result = pd.concat([result, pd.Series(nodes_results, name=count+1,index=result.index)], axis=1)
        count += 1
    # calculate mean percentage of food waste
    result_avg = result.mean(axis=1)
    result_avg.name = "Average"
    result = pd.concat([result, result_avg], axis=1)

    return result


if __name__ == '__main__':

    df_all = pd.read_csv('foodbank_with_latlon.csv',
                         usecols=['Food Bank', 'ID', 'Total Population', '2021 Food Insecurity %',
                                  '2021 Food Insecurity #', 'latitude', 'longitude', 'state_y', 'statecode'])
    # we select some states with more food banks or wth higher food_insecure percentage
    mask = ['TX', 'FL', 'GA', 'MO', 'AR', 'LA', 'TN', 'AL', 'OK', 'MS', 'OH', 'IN', 'PA', 'NY', 'CA']
    df_regional = df_all[df_all.statecode.isin(mask)]

    print("There are 197 food banks in our network. ")
    print("We selected some food banks by states with higher food-insecure percentage or more branches in one state.")

    # codes of input ideas from previous students project
    # https://github.com/saloneeshah/Final-Project/blob/master/GoalkeeperSuccessRateSimulation_Final.py
    input_check = 1
    while input_check == 1:
        try:
            # define the number of days as a period to calculate food waste
            run_all = int(input("Do you want to [1] run all [2] select fewer? "))

            if run_all in [1, 2]:
                input_check = 0
                break
            else:
                print('Please enter a valid integer.')
                continue

        except ValueError:
            print('Please enter a valid integer.')

    input_check = 1
    while input_check == 1:
        try:
            # define the number of days as a period to calculate food waste
            days_to_run = int(input("\nEnter the number of days as a cycle to calculate food waste: "))
            input_check = 0
        except ValueError:
            print('Please enter a valid integer.')

    input_check = 1
    while input_check == 1:
        try:
            test_times = int(input("Enter the number of times to repeat the entire program: "))
            input_check = 0
        except ValueError:
            print('Please enter a valid integer.')

    print('\nNow, the program is running for you...\n')

    if run_all == 1:
        df_to_run = df_all
    else:
        df_to_run = df_regional


    graph = create_graph(df_to_run)
    # assign each food bank with an array of random supply regarding their food-secure population
    initiate_random_supply(graph, days_to_run)
    # calculate distance between every pair of food banks
    add_edges_between_nearest_foodbanks(graph, distance_threshold=120)
    calculate_actual_share_supply(graph)

    # run simulations for the scenarios
    food_waste_without_network = mc_simulation(graph, times_to_run=test_times, network_supply=0, days=days_to_run)
    food_waste_with_network = mc_simulation(graph, times_to_run=test_times, network_supply=1, days=days_to_run)
    # create a dataframe to store overall results
    df_avg_results = pd.concat([food_waste_without_network["Average"], food_waste_with_network["Average"]],
                               axis=1, keys=['Independent', 'Network'])
    # check if the average food waste is lower by subtracting the number of Independent from Network
    gap = food_waste_with_network["Average"] - food_waste_without_network["Average"]
    number_of_decrease = food_waste_with_network.groupby(gap < 0).size()[1]
    decrease_rate = round(((number_of_decrease / len(df_avg_results)) * 100), 3)

    print('\n===== {} Days Summary by Running {} Times =====\n'.format(days_to_run, test_times ))
    print('The number of food banks with lower food waste after sharing: {} / {}'.format(number_of_decrease, len(df_avg_results)))
    print('The percentage of food banks in total with lower food waste: {}% \n'.format(decrease_rate))
    print(df_avg_results.reset_index(drop=True))

    # draw histogram
    # idea of plots is referred to https://www.dataindependent.com/pandas/pandas-histogram/

    # define for titles in figures and the output file name
    title = 'Histogram Of Food Waste'
    filename = '_{}days_{}times_{}nodes'.format(days_to_run, test_times, len(df_avg_results))
    plt.figure()
    ax1 = df_avg_results.reset_index(drop=True).plot(kind='hist', alpha=0.7, bins=30, rot=45, grid=True,
                                                     figsize=(16, 12), fontsize=20)

    ax1.set_xlabel('The Percentage of Fresh Food Waste (%)', fontdict={'fontsize': 20})
    ax1.set_ylabel('Number of Food Banks', fontdict={'fontsize': 20})
    ax1.legend(fontsize=20)
    ax1.set_title(title+'_All'+filename, pad=20, fontdict={'fontsize': 24})
    ax1.get_figure().savefig(fname=title+'_All'+filename)

    # to get the nodes with edges
    degree_dict = dict(graph.degree)
    nodes_with_edge=[]
    for k in degree_dict.keys():
        if degree_dict[k] >= 1:
            nodes_with_edge.append(k)


    print('\n===== {} Days Summary of Food Banks With Sharing Relation =====\n'.format(days_to_run))
    # to plot the result by filtering the nodes with edge
    df_edges = df_avg_results[df_avg_results.index.isin(nodes_with_edge)].reset_index(drop=True)
    print(df_edges)


    plt.figure()
    ax2 = df_edges.plot(kind='hist', alpha=0.7, bins=30, rot=45, grid=True, figsize=(16, 12),
                        color=['#A0E8AF', '#FFCF56'])

    ax2.set_xlabel('The Percentage of Fresh Food Waste (%)', fontdict={'fontsize': 20})
    ax2.set_ylabel('Number of Food Banks', fontdict={'fontsize': 20})
    ax2.legend(fontsize=20)
    ax2.set_title(title+'_Nodes With Edges'+filename, pad=20, fontdict={'fontsize': 24})
    ax2.get_figure().savefig(fname=title+'_Nodes With Edges'+filename)
