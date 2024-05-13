# John Parrish
# parrishj
# sp0587115

"""
INSTRUCTIONS

Available: May 2nd

Due: May 12th at 11:59PM

Gentle reminder that, among other things, you

(a) Must answer your questions in the homework3.py file
(b) Must homework3.py commit to your clone of the GitHub homework repo
(c) Must link your GitHub repo to GradeScope
(d) Must NOT repeatedly use a hard-coded path for the working directory
(e) Must NOT modify the original data in any way

Failure to do any of these will result in the loss of points
"""
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

##base path for working on project
base_path = r"C:\Users\Jay\OneDrive\Desktop\Snake 1\Homework 3\submission"

##preset variables for existing csv files
stock_path = os.path.join(base_path, "capitalstock.csv")
pop_path = os.path.join(base_path, "population(1).csv")
europe_path = os.path.join(base_path, "europe.csv")

stock = pd.read_csv(stock_path)
population = pd.read_csv(pop_path)
europe = pd.read_csv(europe_path)
"""
QUESTION 1

In this question, you'll be replicating the graph from Lecture 14, slide 5
which shows the population of Europe from 0 AD to the present day in both
the linear and the log scale. You can find the data in population.csv, and the
variable names are self-explanatory.

Open this data and replicate the graph. 

Clarification: You are not required to replicate the y-axis of the right hand
side graph; leaving it as log values is fine!

Clarification: You are not required to save the figure

Hints: Note that...

- The numpy function .log() can be used to convert a column into logs
- It is a single figure with two subplots, one on the left and the other on
the right
- The graph only covers the period after 0 AD
- The graph only covers Europe
- The figure in the slides is 11 inches by 6 inches
"""
##renames "time" column with country name
population.rename(columns = {"Entity": "country"}, inplace = True)
europe.rename(columns = {"Countries": "country"}, inplace = True)

##creates list of only European countries
europe_countries = population.merge(europe, 
                      on = "country",
                      how = "inner")

##creates cutoff year to filter date range by
cutoff_year = 0

##creates new df that contains only entires after cutoff year
filtered_europe = europe_countries[europe_countries["Year"] >= cutoff_year]

##groupby object with total population per year
total_pop_per_year = filtered_europe.groupby("Year")["Population (historical estimates)"].sum().reset_index()

##resets population to count in millions
total_pop_per_year["Population (historical estimates)"] = total_pop_per_year["Population (historical estimates)"]/1000000


##creates log population for later graph
total_pop_per_year["log pop"] = np.log(total_pop_per_year["Population (historical estimates)"])

##all graphable values
year = total_pop_per_year["Year"]
pop = total_pop_per_year["Population (historical estimates)"]
log_pop = total_pop_per_year["log pop"]


##creates figures IAW specified guide
fig, axs = plt.subplots(1, 2, figsize = (11, 6))
axs[0].plot(year, pop)
axs[0].set_title("Populaition of Europe from 0 BCE in millions")
axs[1].plot(year, log_pop)
axs[1].set_title("Populaition of Europe from 0 BCE in millions (log scale)")

"""
QUESTION 2

A country's "capital stock" is the value of its' physical capital, which includes the 
stock of equipment, buildings, and other durable goods used in the production 
of goods and services. Macroeconomists seem to conisder it important to have 
public policies that encourage the growth of capital stock. Why is that?

In this exercise we will look at the relationship between capital stock and 
GDP. You can find data from the IMF in "capitalstock.csv" and documentation in
"capitalstock documentation.txt".

In this exercise we will only be using the variables that are demarcated in
thousands of 2017 international dollars to adjust for variation in the value 
of nominal national currency. Hint: These are the the variables that 
end in _rppp.

1. Open the dataset capitalstock.csv and limit the dataframe to only 
observations from 2018
"""

##creates filter year
filter_year = 2018

##creates new df that contains only 2018 entries
filtered_stock = stock[stock["year"] == filter_year]

"""
2. Construct a variable called "capital_stock" that is the sum of the general
government capital stock and private capital stock. Drop 
observations where the value of capital stock is 0 or missing. (We will be 
ignoring public-private partnership capital stock for the purpose of t
his exercise.)
"""
##creates new sum variable
filtered_stock["capital_stock"] = filtered_stock["kgov_rppp"] + filtered_stock["kpriv_rppp"]

##removes any na values
filtered_stock.dropna(subset=["capital_stock"], inplace = True)

##removes any 0 values
filtered_stock = filtered_stock[filtered_stock["capital_stock"] != 0]

"""
3. Create a scatterplot showing the relationship between log GDP and log
capital stock. Put capital stock on the y-axis. Add the line of best 
fit. Add labels where appropriate and make any cosmetic adjustments you want.

(Note: Does this graph suggest that macroeconomists are correct to consider 
 capital stock important? You don't have to answer this question - it's 
 merely for your own edification.)
"""
## creates log gdp and log capstock variables for comparison
filtered_stock["log GDP"] = np.log(filtered_stock["GDP_rppp"])
filtered_stock["log capstock"] = np.log(filtered_stock["capital_stock"])

##Creates initial scatterplot between gdp and capstock
fig2, ax2 = plt.subplots()
ax2.scatter(filtered_stock["GDP_rppp"], filtered_stock["capital_stock"])
ax2.set_title(" Relationship between Log GDP and Log Capital Stock")
ax2.set_xlabel("Log GDP")
ax2.set_ylabel("Log Capital Stock")

##creates line of best fit
slope, intercept = np.polyfit(filtered_stock["GDP_rppp"], filtered_stock["capital_stock"], 1)
y_fit = slope * filtered_stock["GDP_rppp"] + intercept

##adds line of best fit to graph
ax2.plot(filtered_stock["GDP_rppp"], y_fit, color = "green", linestyle = "--", label = "Line of Best Fit")
"""
4. Estimate a model of the relationship between the log of GDP 
and the log of capital stock using OLS. GDP is the dependent 
variable. Print a table showing the details of your model and, using comments, 
interpret the coefficient on capital stock. 

Hint: when using the scatter() method that belongs to axes objects, the alpha
option can be used to make the markers transparent. s is the option that
controls size
"""
import statsmodels.api as sm

## adds constant to model for intercept and setting up OLS model
cap_stock = sm.add_constant(filtered_stock["capital_stock"])
gdp = filtered_stock["GDP_rppp"]
model = sm.OLS(gdp, cap_stock).fit()

##prints model summary
print(model.summary())
##The coefficient on captial stock is ".3509" and it is statisitically significant at a .0001 level. This means that for every increase in 1 units of 
##"capital_stock" gdp will increase by .3509 units

