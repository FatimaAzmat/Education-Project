'''
This file is used for gathering data from two separate sources using API.
'''

#Please install the following before running below code:
#pip install CensusData --user

import csv
import pandas as pd
import censusdata
from sodapy import Socrata


#Setting 2010 Census data frame formatting option
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.precision', 2)


#Leveraging API provided by the NYC Department of Education
client = Socrata("data.cityofnewyork.us", None)
results = client.get("23z9-6uk9", limit=2000)
results_df = pd.DataFrame.from_records(results)


#Obtaining unique county codes for NYC to map data results
nyc_areacode_filename = 'nyc_census_tabulation.csv'
nyc_areacode = pd.read_csv(nyc_areacode_filename, delimiter=',', dtype=str)
nyc_county = nyc_areacode['2010 Census Bureau FIPS County Code'].unique()


#Creating dictionary mapping for census tract to zipcode
#to be able to map the census data to education data
census_zipcode_relation_filename = 'zcta_tract.csv'
census_zipcode_relation = pd.read_csv(census_zipcode_relation_filename, \
    delimiter=',', dtype=str)
ny_tract_to_zipcode = census_zipcode_relation[census_zipcode_relation\
['STATE'] == '36'][['TRACT', 'ZCTA5']]

tract_zipcode = {}
for row in ny_tract_to_zipcode.itertuples():
    tract_zipcode[row[1]] = row[2]


#Obtaining 2010 Census median income data for each borough in NYC
censusdata.search('acs5', 2015, 'label', 'median income')
censusdata.censustable('acs5', 2015, 'B06011')
median_income_bronx = censusdata.download('acs5', 2015, \
    censusdata.censusgeo([('state', '36'), ('county', '005'), \
        ('tract', '*')]), ['B06011_001E'])
median_income_kings = censusdata.download('acs5', 2015, \
    censusdata.censusgeo([('state', '36'), ('county', '047'), \
        ('tract', '*')]), ['B06011_001E'])
median_income_ny = censusdata.download('acs5', 2015, \
    censusdata.censusgeo([('state', '36'), ('county', '061'), \
        ('tract', '*')]), ['B06011_001E'])
median_income_queens = censusdata.download('acs5', 2015, \
    censusdata.censusgeo([('state', '36'), ('county', '081'), \
        ('tract', '*')]), ['B06011_001E'])
median_income_richmond = censusdata.download('acs5', 2015, \
    censusdata.censusgeo([('state', '36'), ('county', '085'), \
        ('tract', '*')]), ['B06011_001E'])


#Consolidating median income data for each borough in NYC
median_income = median_income_bronx.append(median_income_kings)
median_income = median_income.append(median_income_ny)
median_income = median_income.append(median_income_queens)
median_income = median_income.append(median_income_richmond)
median_income = median_income.fillna(0)


#Obtaining census tract identifiers from the data and adding the info as column
median_income_tract_lst = []
for row in median_income.index:
    median_income_tract_lst.append(row.geo[2][1])

median_income = median_income.reset_index()
median_income['census_tract'] = pd.Series(median_income_tract_lst)


#Cleaning data to remove invalid zipcodes
median_income = median_income[median_income['census_tract'] != '070203']
median_income = median_income[median_income['census_tract'] != '990100']
median_income = median_income[median_income['census_tract'] != '107202']


#Including zipcode column in census dataframe based on tract-zipcode mapping
median_income_zipcode = []
for tract in median_income['census_tract']:
    val = tract_zipcode[str(tract)]
    median_income_zipcode.append(val)
median_income['zipcode'] = pd.Series(median_income_zipcode)


##Obtaining 2010 Census poverty data for each borough in NYC
censusdata.search('acs5', 2015, 'label', 'poverty')
censusdata.censustable('acs5', 2015, 'B17017')
below_poverty_bronx = censusdata.download('acs5', 2015, \
    censusdata.censusgeo([('state', '36'), ('county', '005'), ('tract', '*')]),\
    ['B17017_002E'])
below_poverty_kings = censusdata.download('acs5', 2015, \
    censusdata.censusgeo([('state', '36'), ('county', '047'), ('tract', '*')]),\
    ['B17017_002E'])
below_poverty_ny = censusdata.download('acs5', 2015, \
    censusdata.censusgeo([('state', '36'), ('county', '061'), ('tract', '*')]),\
    ['B17017_002E'])
below_poverty_queens = censusdata.download('acs5', 2015, \
    censusdata.censusgeo([('state', '36'), ('county', '081'), ('tract', '*')]),\
    ['B17017_002E'])
below_poverty_richmond = censusdata.download('acs5', 2015, \
    censusdata.censusgeo([('state', '36'), ('county', '085'), ('tract', '*')]),\
    ['B17017_002E'])


#Consolidating poverty data for each borough in NYC
below_poverty = below_poverty_bronx.append(below_poverty_kings)
below_poverty = below_poverty.append(below_poverty_ny)
below_poverty = below_poverty.append(below_poverty_queens)
below_poverty = below_poverty.append(below_poverty_richmond)
below_poverty = below_poverty.fillna(0)


#Obtaining census tract identifiers from the data and adding the info as column
below_poverty_tract_lst = []
for row in below_poverty.index:
    below_poverty_tract_lst.append(row.geo[2][1])

below_poverty = below_poverty.reset_index()
below_poverty['census_tract'] = pd.Series(below_poverty_tract_lst)


#Cleaning data to remove invalid zipcodes
below_poverty = below_poverty[below_poverty['census_tract'] != '070203']
below_poverty = below_poverty[below_poverty['census_tract'] != '990100']
below_poverty = below_poverty[below_poverty['census_tract'] != '107202']


#Including zipcode column in census dataframe based on tract-zipcode mapping
below_poverty_zipcode = []
for tract in below_poverty['census_tract']:
    val = tract_zipcode[str(tract)]
    below_poverty_zipcode.append(val)
below_poverty['zipcode'] = pd.Series(below_poverty_zipcode)


#Obtaining 2010 Census SNAP data for each borough in NYC
censusdata.search('acs5', 2015, 'label', 'snap')
censusdata.censustable('acs5', 2015, 'B09010')
govt_assistance_bronx = censusdata.download('acs5', 2015, \
    censusdata.censusgeo([('state', '36'), ('county', '005'), ('tract', '*')]),\
    ['B09010_001E'])
govt_assistance_kings = censusdata.download('acs5', 2015, \
    censusdata.censusgeo([('state', '36'), ('county', '047'), ('tract', '*')]),\
    ['B09010_001E'])
govt_assistance_ny = censusdata.download('acs5', 2015, \
    censusdata.censusgeo([('state', '36'), ('county', '061'), ('tract', '*')]),\
    ['B09010_001E'])
govt_assistance_queens = censusdata.download('acs5', 2015, \
    censusdata.censusgeo([('state', '36'), ('county', '081'), ('tract', '*')]),\
    ['B09010_001E'])
govt_assistance_richmond = censusdata.download('acs5', 2015, \
    censusdata.censusgeo([('state', '36'), ('county', '085'), ('tract', '*')]),\
    ['B09010_001E'])


#Consolidating goverment assistance data for each borough in NYC
govt_assistance_received = govt_assistance_bronx.append(govt_assistance_kings)
govt_assistance_received = govt_assistance_received.append(govt_assistance_ny)
govt_assistance_received = govt_assistance_received.append(\
    govt_assistance_queens)
govt_assistance_received = govt_assistance_received.append(\
    govt_assistance_richmond)
govt_assistance_received = govt_assistance_received.fillna(0)


#Obtaining census tract identifiers from the data and adding the info as column
govt_assistance_received_tract_lst = []
for row in govt_assistance_received.index:
    govt_assistance_received_tract_lst.append(row.geo[2][1])

govt_assistance_received = govt_assistance_received.reset_index()
govt_assistance_received['census_tract'] = pd.Series(\
    govt_assistance_received_tract_lst)


#Cleaning data to remove invalid zipcodes
govt_assistance_received = govt_assistance_received[govt_assistance_received\
['census_tract'] != '070203']
govt_assistance_received = govt_assistance_received[govt_assistance_received\
['census_tract'] != '990100']
govt_assistance_received = govt_assistance_received[govt_assistance_received\
['census_tract'] != '107202']


#Including zipcode column in census dataframe based on tract-zipcode mapping
govt_assistance_zipcode = []
for tract in govt_assistance_received['census_tract']:
    val = tract_zipcode[str(tract)]
    govt_assistance_zipcode.append(val)
govt_assistance_received['zipcode'] = pd.Series(govt_assistance_zipcode)