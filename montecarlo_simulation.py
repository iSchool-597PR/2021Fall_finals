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


def calculate_distance(node1: tuple, node2: tuple):
    """
    This function calculates distance between any two food banks
    :param node1: dataframe with latitude and longitude values
    :param node1: food bank 1
    :param node2: food bank 2
    :return: distance in km
    """
    return geodesic(node1, node2).km


def create_graph(df: pd.DataFrame, g: nx.DiGraph) -> None:
    """
    Creat graph from the dataframe.
    :param df:
    :param g:
    :return:
    """

    df = df.set_index('ID')
    attrs = df.to_dict('index')
    g.add_nodes_from(df.index)
    nx.set_node_attributes(g, attrs)

def create_shelflife_list(days: int) -> list:
    """
    Create a list to show level of freshness.
    For example, d3 means the food will spoil in 3 days.
     labels of shelf_life in daily simulation.
    :param days:
    :return: a list of labels for daily simulation
    """

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

def generate_random_variables(g: nx.DiGraph, node: int, variable_type: str, days=7) -> np.array:
    """
    To generate random supply or demand for a single food bank by Modified PERT distribution in particular days.
    For the supply side, we assume the lowest frequency of supply is once per 10 days.
    The highest frequency is once per 3 days. And the most likely is once per 7 days.
    For the demand side, according to the reference, an average of 1.6 shopping trips per week for each person.
    So we use 1.6/7 for the most likelihood. We assume the lowest frequency is once per week while the highest
    frequency is every day, which equal to 1.

    The reference of the fact that an average of 1.6 shopping trips per week for each person:
    https://www.statista.com/statistics/251728/weekly-number-of-us-grocery-shopping-trips-per-household/

    :param g:
    :param node:
    :param variable_type: demand or supply
    :param days:
    :return:
    """
    node_ppl = g.nodes[node]['Total Population']
    insecure_ppl = g.nodes[node]['2021 Food Insecurity #']
    potential_supply_ppl = (node_ppl - insecure_ppl) * 0.5

    demand = np.rint(mod_pert_random((1 / 7) * insecure_ppl, (1.6 / 7) * insecure_ppl, insecure_ppl,
                                     samples=days))
    supply = np.rint(mod_pert_random((1 / 10) * potential_supply_ppl, (1 / 7) * potential_supply_ppl,
                                     (1 / 3) * potential_supply_ppl, samples=days))

    if variable_type == 'demand':
        return demand
    else:
        return supply

def calculate_share_supply_rate(demand_gap_rate: float) -> float:
    """
    We design a method to decide the actual proportion of share supply to neighbors.
    :param demand_gap_rate:
    :return:
    """
    #
    if demand_gap_rate > 0.2:
        rate = 0.1
    elif 0.1 < demand_gap_rate < 0.2:
        rate = demand_gap_rate / 2
    else:
        rate = 0.01
    return rate

def determine_direction(demand_gap: int, node1: int, node2: int) -> tuple:
    """
    To determine the direction of edge that is going to added.
    The food bank with higher demand indicate extra supply needed,
    so the other would share a proportion of their supply based on the demand gap.
    :param demand_gap:
    :param node1:
    :param node2:
    :return:
    """

    if demand_gap > 0:
        share_supply = node1
        receive_supply = node2
    else:
        share_supply = node2
        receive_supply = node1
        demand_gap = abs(demand_gap)
    return share_supply, receive_supply, demand_gap


def add_edges_with_attributes(g: nx.DiGraph, node_out: int, node_in: int, demand_gap: int, distance: float) -> None:
    """
    If edges don't exist, add the current neighbor with the share proportion of supply as attribute.
    :param g:
    :param node_out:
    :param node_in:
    :param demand_gap:
    :param distance:
    :return:
    """

    # calculate the gap of food insecure population between two food banks as an edge attribute
    node_ppl = g.nodes[node_out]['Total Population']
    insecure_ppl_node = g.nodes[node_out]['2021 Food Insecurity #']
    potential_supply_ppl = (node_ppl - insecure_ppl_node) * 0.5

    # use the percentage of demand_gap over potential_supply_ppl as the potential share supply to neighbor
    demand_gap_rate = demand_gap / potential_supply_ppl
    # we design a method to decide the actual proportion of share supply to neighbors
    share_supply_rate = calculate_share_supply_rate(demand_gap_rate)

    supply = generate_random_variables(g, node_out, 'supply')
    actual_share_supply = np.rint(supply * share_supply_rate)
    supply -= actual_share_supply
    # set one more node attribute for the supply after sharing
    nx.set_node_attributes(g, {node_out: {'supply': supply}})
    g.add_edge(node_out, node_in, distance=round(distance, 3), share_supply=actual_share_supply)


def add_edges_between_nearest_foodbanks(g: nx.DiGraph, list_of_nodes: list, distance_threshold=120) -> None:
    """
    The edges are added only when the distance between two nodes are the shortest.
    :param g:
    :param list_of_nodes:
    :param distance_threshold:
    :return:
    """
    for i in range(len(list_of_nodes)):
        # initial distance and neighbor
        nearest = distance_threshold
        neighbor = 0
        node1 = g.nodes[list_of_nodes[i]]['latitude'], g.nodes[list_of_nodes[i]]['longitude']
        for fb in list_of_nodes[i + 1:]:
            node2 = g.nodes[fb]['latitude'], g.nodes[fb]['longitude']
            distance = geodesic(node1, node2).km
            # find shortest distance
            if distance < nearest:
                nearest = distance
                neighbor = fb

        if neighbor != 0:
            # determine the direction: the food bank with higher demand indicate extra supply needed
            # so the other would share a proportion of their supply based on the demand gap
            insecure_ppl_node = g.nodes[list_of_nodes[i]]['2021 Food Insecurity #']
            insecure_ppl_neighbor = g.nodes[neighbor]['2021 Food Insecurity #']
            demand_gap = insecure_ppl_node - insecure_ppl_neighbor
            # the neighbors with same population since they are in similar demand and supply so we ignore them
            if demand_gap == 0:
                continue
            share_supply, receive_supply, demand_gap = determine_direction(demand_gap, list_of_nodes[i], neighbor)

            # check if edges exists because we only keep the nearest one for out_edge
            if len(g.edges(share_supply)) > 0:
                # compare the distance
                for adj in list(g.adj[share_supply]):
                    if g.edges[share_supply, adj]['distance'] > nearest:
                        g.remove_edge(share_supply, adj)
                    else:
                        continue
            # if edges don't exist, add the current neighbor with the share proportion of supply as attribute
            add_edges_with_attributes(g, share_supply, receive_supply, demand_gap, nearest)


def daily_simulation(g: nx.DiGraph, node: int, supply: np.array, days=7) -> float:
    """
    This is our primary simulation module for single food bank with daily update outputs.
    :param g:
    :param node:
    :param supply:
    :param days:
    :return:
    """

    shelf_life = create_shelflife_list(3)

    supply_initial = generate_random_variables(g, node, 'supply', days=len(shelf_life))
    food_balance = pd.DataFrame(supply_initial, index=shelf_life, columns=['Balance'])
    food_balance.index.name = 'Shelf_life'

    demand = generate_random_variables(g, node, 'demand')

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

def mc_simulation(g: nx.DiGraph, times_to_run: int, network_supply: int) -> pd.DataFrame:
    """
    To simulate multiple times for two scenarios.
    :param g:
    :param times_to_run:
    :param network_supply:
    :return:
    """

    count = 0
    result = pd.DataFrame(nodes)

    while count < times_to_run:
        nodes_results = []
        supply = None
        for node in nodes:
            if network_supply == 0:
                supply = generate_random_variables(g, node, 'supply')
            if network_supply == 1:
                all_neighbors = list(nx.all_neighbors(g, node))
                # single nodes without neighbors
                if len(all_neighbors) == 0:
                    supply = generate_random_variables(g, node, 'supply')
                # nodes with neighbors
                else:
                    extra_supply = 0
                    for neighbor in all_neighbors:
                        if g.has_predecessor(node, neighbor):
                            extra_supply += g.edges[neighbor, node]['share_supply']
                        else:
                            supply = g.nodes[node]['supply']

                    if supply is None:
                        supply = generate_random_variables(g, node, 'supply')
                    # sum up supply
                    supply += extra_supply

            waste_percentage = daily_simulation(g, node, supply, days=7)
            nodes_results.append(waste_percentage)

        result[count+1] = nodes_results
        count += 1

    result = result.set_index([0])

    return result.T


if __name__ == '__main__':

    df_all = pd.read_csv('foodbank_with_latlon.csv',
                         usecols=['Food Bank', 'ID', 'Total Population', '2021 Food Insecurity %',
                                  '2021 Food Insecurity #', 'latitude', 'longitude', 'state_y', 'statecode'])

    mask = ['TX', 'FL', 'GA', 'MO', 'AR', 'LA', 'TN', 'AL', 'OK', 'MS', 'CA', 'OH', 'NY', 'IN', 'PA']
    df_regional = df_all[df_all.statecode.isin(mask)]

    graph = nx.DiGraph()
    create_graph(df_regional, graph)
    # create_graph(df_all, graph)
    days_to_run = 7

    nodes = list(graph.nodes)
    add_edges_between_nearest_foodbanks(graph, nodes, distance_threshold=120)

    food_waste_without_network = mc_simulation(graph, times_to_run=15, network_supply=0)
    food_waste_with_network = mc_simulation(graph, times_to_run=15, network_supply=1)

    print(food_waste_without_network)
    print(food_waste_with_network)

    # TODO: plots

    # fig, (ax0, ax1) = plt.subplots(2, 1, figsize=(20, 16))
    # plt.subplots_adjust(hspace=.5)

    plt.figure(figsize=(20, 12))
    plt.title('food_waste_without_network')
    plt.hist(food_waste_without_network.iloc[:, 0:2], bins=20)
    plt.xlabel('Food Waste %')
    plt.ylabel('Number of Times')
    plt.legend()
    # plt.show()

    plt.figure(figsize=(20, 12))
    # plt.title('food_waste_with_network')
    plt.hist(food_waste_with_network.iloc[:, 0:2], bins=20)
    # plt.xlabel('Number of simulations')
    # plt.ylabel('Food Waste %')
    plt.legend()
    # plt.show()
