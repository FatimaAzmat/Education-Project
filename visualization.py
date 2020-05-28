'''
This file is used for generating visualization graphs based on data analysis.
'''

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#Setting the seaborn graph style
sns.set(style="darkgrid")


#Reading csv output file from regression.py to create visualizations
#and perform analysis
census_education_data = pd.read_csv("export_dataframe.csv")
census_education_data = census_education_data[census_education_data\
["B06011_001E"] > 0]
census_education_data = census_education_data.rename(columns=\
    {"B06011_001E": "median_income", "B17017_002E": "population_below_poverty",\
    "B09010_001E": "population_on_government_assistance", \
    "total_score": "sat_total_score"})


#Plotting regression on the impact of median household income on sat scores
sns.regplot(x="median_income", y="sat_total_score", data=census_education_data)
plt.show()


#Plotting regression on the impact of population below poverty on sat scores
sns.regplot(x="population_below_poverty", y="sat_total_score", \
    data=census_education_data)
plt.show()


#Plotting regression on the impact of being on food stamp on sat scores
sns.regplot(x="population_on_government_assistance", y="sat_total_score", \
    data=census_education_data)
plt.show()