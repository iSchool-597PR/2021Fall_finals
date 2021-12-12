# ANALYSIS OF MOTOR VEHICLE CRASHES IN THE UNITED STATES OF AMERICA

Authors: Prayag Patel, Rohit Doraiswamy, Priyanka Dewani

### Overview: 

It is important to analyze how, where and, when vehicle crashes occur for our personal safety and information. And it also helps the law enforcements to understand the nature and injury outcomes of crashes. Our project aims at analyzing these questions. We have referred the NHTSA official report to recreate and check if what they have plotted and analyzed makes sense and can be useful. This has also allowed us to expand on what they have done and what they could have done better in their analysis and plots. Our research has led us to study some hypothesis as follows:

Here are few things NHTSA could have done better in order to incorporate a much more precise way of analysing the data

1. They plotted only the number of fatalities in each state of the USA 

![Screenshot](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/Map_NHTSA.png)

This is a perfect graph if we want to analyze just the fatalities but it would make much more sense to Normalize this data with the number of vehicles that are owned by people in a particular state to get a better relative understanding of the severity of crashes beyond the evident data infront of us

![Screenshot](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/Normalized_NHTSA.png)

This is a Normalized Chloropleth plot of the fatalities which takes into consideration the number of vehicles in each state.


2. They have plotted data for the year of 2019 but if we want to do a year by year analysis, it's not possible tounderstand that using their analysis. Even in their previous editions they have different graphs, hence it becomes difficult to analyze the changes and trends from the previous years which could allow decision makers to take reasonable and proper action. We have allowed the user to have the liberty to enter the year they want which allows them to do a comparitive analysis via the graph which will provide a uniformity in comparison.


3. Since the report did not provide any insight on why there is an upward and downward trend in the number of fatalities per 100million VMT, we have analyzed a few factors and have certain assumptions on what the reason can be.

    1. There is a steep decrease in the fatality rate per 100 Million VMT from 1980 till around 2015.
      
      ![Screenshot](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/fatality_line.png)

      Our assumption is that this is possible because the States became more strict in enforcing restraints in vehicles and hence there were less number of fatalities during this period.
      
    2. There is an increase in this rate from 2015
    
        ![](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/scatterplot.PNG)
        
        Our assumption in this case is that since the gasoline prices saw a decrease in 2016 due to which there is an upward trend in the fatalities, this can be analyzed using the scatter plot as shown
        



### Hypothesis 1: There are more fatal crashes on weekends (Friday, Saturday, Sunday)

Step 1:

We create a new dataframe to sum the number of fatalities occured from 2010-2019 for each day of the week.

Step 2:
The final graph for fatalities on weekdays vs weekends is as shown.
We divide the total number of fatalities by the number of days considered. (3 for weekends and 4 for weekdays)

![](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/hypothesis_1.PNG)
 
Here, we can see that our hypothesis is proved correct since over the years the mean of the fatalities on weekends is higher than the mean of the fatalities on the weekdays.

### Hypothesis 2: Older models of car leads to more fatalities

Step 1 :

We create a new column in the DataFrame to identify vehicle model as "old", "new" or "Not Available" depending on the year of the model
![](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/model_crash.PNG)

Step 2 : 

Let us observe the plots for 2019, 2016, and 2011

![](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/hypothesis_2_3.PNG)
Plot for 2019

![](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/hypothesis_2_2.PNG)
Plot for 2016

![](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/hypothesis_2_1.PNG)
Plot for 2011

We can see that there are lot of cases of fatalities in the newer model of the car as compared to the older one, we can hence reject our initial hypothesis since the evidence is strongly suggesting against it. The possibility of this can be that there are more number of people who own newer model of cars 

### Hypothesis 3: Fatalities due to drunk driving is independent of time

Step 1:

We first slice the DataFrame into two categories
1. Deaths which involves drunk driving
2. Deaths which does not involve drunk driving
INJ_SEV == 4 or 2 means that the fatalities are cases of drunk driving

![](https://github.com/prayagpatel99/2021Fall_finals/blob/main/code_drunk.PNG)

Step 2:

Let us observe the plots for 2019, 2016, and 2011

![](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/hypothesis_3_3.PNG)
Plot for 2019

![Screenshot](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/hypothesis_3_2.jpeg)
Plot for 2016

![Screenshot](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/hypothesis_3_1.jpeg)
Plot for 2011

From this graph we can see that there has been higher number of deaths associated with drunk driving during the time of 9am-11am. We could see that from all these graphs that morning and afternoon times have higher deaths associated with drunk driving. Hence we cannot accept the hypothesis that Fatalities due to drunk driving is independent of time but we also cannot reject this hypothesis since we do not have other conclusive evidence against this hypothesis.


### Hypothesis 4: As the day begins to get shorter due to daylight savings, more accidents occur between 4pm-7pm, since it gets dark earlier.

Step 1:

We first create a dictionary of dataframes from 2010-2019 and plot the total number of fatalities for each hour of the day over the years

![](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/hypothesis_4_1.png)
Plot for 2019

From this graph, we see that most fatalities occur from 3pm - 9pm and not 4pm - 7pm.

![](http://localhost:8888/view/2021Fall_finals/Plotly%20graphs/hypothesis_4_1_2016.PNG)
Plot for 2016

![](http://localhost:8888/view/2021Fall_finals/Plotly%20graphs/hypothesis_4_1_2011.PNG)
Plot for 2011

Step 2:

We plot the total number of fatalities based on the daylight savings months (November to March) and months with no daylight saving hours (April to October), for a particular year, from 3pm to 9pm.

![](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/hypothesis_4_2.png)
Plot for months with daylight saving hours for 2019

![](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/hypothesis_4_3.png)
Plot for months with no daylight saving hours for 2019

![](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/hypothesis_4_2_2016.png)
Plot for months with daylight saving hours for 2016

![](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/hypothesis_4_3_2016.png)
Plot for months with no daylight saving hours for 2016

![](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/hypothesis_4_2_2011.png)
Plot for months with daylight saving hours for 2011

![](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/hypothesis_4_3_2011.png)
Plot for months with no daylight saving hours for 2011


The garphs prove our hypothesis to be correct, since for almost all the hours from 3pm-9pm (except 6pm which is almost close to the count for the non daylight months) we observe that the count of fatalities are more for daylight months, whereas for non daylight months.

### Hypothesis 5: Fatalities are less in vehicles where airbags are deployed

Step 1:

We extract a dataframe from the airbags dictionary based on the desired year and filter it by the person type, the severity of the injury, the seat position, and if the airbags were deployed incase of a crash.

Step 2:

![](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/hypothesis_5.png)
Plot for fatalities when airbags were deployed vs when airbags were not deployed for the year 2019

![](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/hypothesis_5_2016.png)
Plot for fatalities when airbags were deployed vs when airbags were not deployed for the year 2016

![](https://github.com/prayagpatel99/2021Fall_finals/blob/main/Plotly%20graphs/hypothesis_5_2011.png)
Plot for fatalities when airbags were deployed vs when airbags were not deployed for the year 2011

Here, we see that except for the year 2019 vehicles, most of the years where airbags have been deployed has seen more number of fatalities as compared to the vehicles where airbags have not been deployed, hence we reject our initial hypothesis. This result helps us understand that there are lot more factors involved when there is a crash apart from the deployment of airbag which could lead to fatal injuries.
