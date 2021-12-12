# Fresh Food Supply Network Simulation   
IS597PR Final Projects – Fall 2021 



### Team Members:


Candice Chen, Kinjal Shah   
(GitHub ID: candicechen016, kinjal-shah4)

## Introduction



>*The USDA estimates that approximately 7.3 billion pounds of produce is wasted in the U.S. each year. The Feeding America network of 200 food banks, in conjunction with 60,000 food pantries and meal programs, would like to see more of those fruits and vegetables go to neighbors in need. ([Feeding America](https://www.feedingamerica.org/hunger-blog/new-produce-matchmaker))*  

Feeding America, the largest food rescue organization, works with farms, retails, or restaurants to extend the lives of food and deliver it to hunger people. While keeping food fresh is important for grocery stores and farmers' market vendors, food banks also face similar challenges with the limitation of short freshness period.
So we are interested in how their network operates to lower the fresh food waste.

## Monte Carlo Simulation Scenarios


With the uncertain demand and supply of fresh produce in food bank's daily operation, we use Monte Carlo simulation to calculate the percentage of **fresh** food waste in the food banks network. The distance and the food-insecure population between food banks are two major weights in our design. 

First, here are some defined terms in the simulation:
- Demand: number of total food-insecure persons in each food banks
- Supply: number of total food-secure persons in each food banks
- Shared supply: units of supply send out by food banks themselves
- Extra supply: units of supply received from other food banks

### Hypothesis
The food waste is lower when the food banks share supply in the network.

In order to test the hypothesis, we focus on the following scenarios:   
1. The food banks operate independently.   
2. The food banks operate with extra supply through the network.

### Method
- We used a NetworkX Graph as our principal data structure to calculate the sharing supply between food banks. 
- Since the original data set we got from the organization lacked position, we also took some efforts on data pre-processing before creating the graph.
- There are 3 data sets in total. The original one includes total population and food-insecure population, which are the critical information to simulate the different scenarios. For the purpose of getting food banks' positions, we matched the zip codes with latitude and longitude so that distance between food banks could be calculated. So that's why we need the other data sets.   
- The second data set, which we also got from Feeding America, is to get the zip code from the address of each food bank. We parsed the information and merged it with the first data set then combined with latitude and longitude from the last data set.
- The graph of food banks network was created with most of the information stored in nodes attributes. On the other hand, edges are added only when food bank A is the nearest neighbor to food bank B, or food bank B is the nearest neighbor to food bank A. Accordingly, some nodes are connected more than once because the distance is also the shortest for others. Distance is the only attribute stored in the edges. 
- After generating random numbers of supply, we calculated the total supply and beginned the simulation of daily operations, which the percentage of food waste came to our conclusions.
- By doing these steps multiple times, the final statistic helps us justify the hypothesis.


### Assumptions and Variables of Uncertainty
We use two data sets to create our food banks network. The major data set with total population, food-insecure population, and food-secure population in each food  
#### Demand - number of total food-insecure persons in each food bank per day 
#### Supply - units of supply donated by food-secure persons per day 

- Use Modified PERT random distribution to both demand and supply.
- 50% of food secure population are potential donors.
- Each donor donates a unit of fresh food (e.g. a bag or a box of fruits and vegetables) at least once per ten days. 
- Each food-insecure person takes a unit of fresh food average 1.6 times per week. 


#### Extra Supply
- Potential percentage of sharing supply: demand_gap_rate = demand_gap / potential_supply_ppl

| demand_gap_rate |  share_supply_rate | 
| --------------- |:------------------:| 
|  > 0.2           | 0.1                | 
|  <= 0.2 or > 0.1 | demand_gap_rate/2  | 
|  <= 0.1.         | 0.01               | 

  
- Actual sharing supply: supply * share_supply_rate

#### Level of Freshness
- Use shelf life to present freshness of any kind of food. If the food will be spoiled  in 3 three days, we denote it as d5.
When the food is in d0 at the end of the day, it becomes a waste.

#### Daily Operation by LIFO approach  
- Supply from donors are always in the freshest condition, which means the number goes to the longest days of shelf life.
- People always have a preference for the freshest food, i.e. d3>d2>d1>d0, because these food are free for people in need. So we apply LIFO (Last-In, First-Out) approach in our daily simulations to match real-world situations.

#### Percentage of Food Waste   
- (total_waste / total_supply) * 100

## Conclusions

1. The simulation results showed that around 40% of food banks have lower waste by network support.
2. The two version of histograms showing the distribution of average waste. One presents distribution of all food banks. The other was filtered by edges in order to closely observe the difference. 
3. Based on the above results, the network between food banks regarding the sharing supply could lower the food waste to a certain degree.
![image](https://user-images.githubusercontent.com/89559531/145724707-410cc826-b34d-4129-87a0-ccf8f7c4ed8a.png "All_14days_50times_197nodes")
![image](https://user-images.githubusercontent.com/89559531/145724811-90e5af81-746a-4ad9-a077-4ed460a8548b.png "Nodes With Edges_14days_50times_197nodes")


## Discussions

1. More experiments to explore
In our simulation, we only use the FIFO approach to calculate daily transactions. If food banks have some promotions or encourage people to take some quantity of d0 or d1 produce home. The randomness could be designed in a different way. Similarly, the randomness of freshness (shelf life) is defined from the very beginning. Another way is defining in a daily scope.
2. The relation between food waste percentage and food freshness
Although we didn't focus on the the relationship between food waste percentage and food freshness, we still found some trends. The daily percentage of food waste has something to do with the shelf life. It's a simple topic to extend based on our current model.
3. Other scenarios expected to further studying
The network in our model is created mainly by distance. There are so many scenarios that could use this model to test. For example, with the sharing relation, what if one of the sharing partners couldn't work, how the network operates to support each other? Are they able to fulfill normal daily demands? Or, what if some unexpected events destroy certain regions, is the existing network capable to support such urgent demand?
4. Improve program efficiency
With our primary purpose of conducting MC simulation, the current version will be better if we make some efficiency improvements.



## Member Contributions

- The project topic, simulation scenarios are done by both team members together.
- The preprocess_dataset.py is completed by both members. Canice worked on scraping and processing the address information on the webpage then merged it to the food banks data set. Kinjal combined the food banks data sets with external zip code data set to get the latitude and longitude.
- Functions completed together: add_edges_with_attributes, add_edges_between_nearest_foodbanks
- Functions independently completed by Candice: create_shelflife_list, generate_random_variables, calculate_share_supply_rate, calculate_actual_share_supply, daily_simulation, mc_simulation
- Functions independently completed by Kinjal: calculate_distance, create_graph

## All Sources Used

### Data Source
- Food Insecurity in The United States   
[https://map.feedingamerica.org/county/2019/overall/](https://map.feedingamerica.org/county/2019/overall/)  
(Gundersen, C., M. Hake, A. Dewey, E. Engelhard (2021). The Impact of the Coronavirus on Food Insecurity in 2020 & 2021, Update March 2021. Available from Feeding America: research@feedingamerica.org. )
- Address of food banks in Feeding America   
[https://www.feedingamerica.org/find-your-local-foodbank](https://www.feedingamerica.org/find-your-local-foodbank)
- Zip code with latitude and longitude   
[https://www.listendata.com/2020/11/zip-code-to-latitude-and-longitude.html](https://www.listendata.com/2020/11/zip-code-to-latitude-and-longitude.html)

### Reference
- Consumers' weekly grocery shopping trips in the United States from 2006 to 2019
[https://www.statista.com/statistics/251728/weekly-number-of-us-grocery-shopping-trips-per-household/](https://www.statista.com/statistics/251728/weekly-number-of-us-grocery-shopping-trips-per-household/)
