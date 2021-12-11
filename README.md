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


With the uncertain demand and supply of fresh produce in food bank's daily operation, we use Monte Carlo simulation to calculate the percentage of **fresh** food waste in the food bank network. 

So we test these two scenarios:   
**1. The food banks operates independently.**  
**2. The food banks operates with extra supply through the network.**

Here are the major terms in the scenarios:
- Demand: number of total food-insecure persons in each food banks
- Supply: number of total food-secure persons in each food banks
- Extra supply: 


We use two data sets to create our food banks network. The major data set with total population, food-insecure population, and food-secure population in each food banks is from Feeding America. Considering the network
After combining out data sets with zip codes,  


### Hypothesis
The food waste is lower when the food banks share supply in the network.

### Assumptions and Variables of Uncertainty
We use two data sets to create our food banks network. The major data set with total population, food-insecure population, and food-secure population in each food banks is from Feeding America. Considering the network
After combining out data sets with zip codes,  
#### Demand -  number of total food-insecure persons in each food banks   


#### Supply - 50% of food secure population in each food banks are potential donors   


#### Extra Supply
- Potential percentage of sharing supply: 
- Actual sharing supply: 

#### Percentage of Food Waste   

#### Daily Operation by LIFO approach  

#### Level of freshness

## Conclusions




## Discussions

1. Daily Operation by LIFO or FIFO approach
2. Simulate different food freshness
3. The relation between food waste percentage and food freshness
4. Further research: shout down scenario

## Instructions on how to use the program



## Member Contributions

- The project topic, simulation scenarios are done by both team members together.
- The preprocess_dataset.py is completed by both members. Canice worked on scraping and processing the adress information on the webpage then merged to the food banks data set. Kinjal combined the food banks data sets with external zip code data set to get the latitude and longitude.
- Functions completed together: add_edges_with_attributes, add_edges_between_nearest_foodbanks
- Functions independently completed by Candice: create_shelflife_list, generate_random_variables, calculate_share_supply_rate, determine_direction, daily_simulation, mc_simulation
- Functions independently completed by Kinjal: calculate_distance, create_graph

## All Sources Used

### Data Source
- Food Insecurity in The United States   
[https://map.feedingamerica.org/county/2019/overall/](https://map.feedingamerica.org/county/2019/overall/)  
(Gundersen, C., M. Hake, A. Dewey, E. Engelhard (2021). The Impact of the Coronavirus on Food Insecurity in 2020 & 2021, Update March 2021. Available from Feeding America: research@feedingamerica.org. )
- Address of food banks in Feeding America   
[https://www.feedingamerica.org/find-your-local-foodbank](https://www.feedingamerica.org/find-your-local-foodbank)
- Zip code with latitude and logitude
[https://www.listendata.com/2020/11/zip-code-to-latitude-and-longitude.html](https://www.listendata.com/2020/11/zip-code-to-latitude-and-longitude.html)

### Reference
- Consumers' weekly grocery shopping trips in the United States from 2006 to 2019
[https://www.statista.com/statistics/251728/weekly-number-of-us-grocery-shopping-trips-per-household/](https://www.statista.com/statistics/251728/weekly-number-of-us-grocery-shopping-trips-per-household/)
