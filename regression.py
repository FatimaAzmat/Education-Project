'''
This file is used for obtaining regression analysis based on multiple datasets.
'''

from sklearn.model_selection import KFold
from sklearn.linear_model import LinearRegression
import csv
import pandas as pd
import data


#NYC school dataset
NY_data = data.results_df[['dbn', 'school_name', 'postcode', 'graduation_rate']]


#drop 0 values of income in median_income dataframe
median_income = data.median_income[data.median_income['B06011_001E'] != 0]


#groupby zipcode and average the income. Then merge with new york school data
new_income = median_income.groupby('zipcode', \
    as_index=False)['B06011_001E'].mean()
merged_data = NY_data.join(new_income.set_index('zipcode'), on='postcode')


#same steps as median_income for below_poverty
new_poverty_count = data.below_poverty.groupby\
('zipcode', as_index=False)['B17017_002E'].mean()
merged_data = merged_data.join(new_poverty_count.set_index\
    ('zipcode'), on='postcode')


#same steps for govt_assistance_received
new_govt_info = data.govt_assistance_received.groupby\
('zipcode', as_index=False)['B09010_001E'].mean()
merged_data = merged_data.join(new_govt_info.set_index\
    ('zipcode'), on='postcode')


#read in SAT scores data and merge
sat_scores = pd.read_csv("sat.csv")
merged_data = merged_data.join(sat_scores.set_index('DBN'), on='dbn')


#clean data for regression
merged_data = merged_data.dropna()
merged_data = merged_data[merged_data.total_score != '#VALUE!']
merged_data = merged_data[merged_data["B06011_001E"] > 0]


class Model:
    '''
    Class for representing a model of linear regression based on scikit tools.
    '''

    def __init__(self, dataset, pred_var, dep_vars, k):
        '''
        Construct a data structure to hold the model.

        Inputs:
            dataset: an pandas dataframe
            pred_var: (string) a column name in the dataset
            dep_vars: a single column name or list of column
                      names in the dataset
            k: (integer) number of samples to divide model
               into for computing multiple R squared
        '''

        self.dataset = dataset
        self.dep_vars = dep_vars
        self.pred_var = pred_var
        self.R2 = self.regression()[0]
        self.slope = self.regression()[1]
        self.intercept = self.regression()[2]
        self.R2_list = self.multiple_samples_R2(k)


    def regression(self):
        '''
        Conducts a regression of the specified dependent and independent
        variables.

        Output:
            tuple of th R squared, slope coefficient and intercept
            of the regression.
        '''


        X = pd.DataFrame(self.dataset[self.dep_vars]).to_numpy()
        y = pd.DataFrame(self.dataset[self.pred_var]).to_numpy()
        reg = LinearRegression()
        reg.fit(X, y)
        r_sq = reg.score(X, y)
        return (r_sq, reg.coef_, reg.intercept_)


    def multiple_samples_R2(self, k):
        '''
        Computes multiple R squared by dividing data into
        k training samples to get a more robust idea of the
        model's explanatory power.
        '''

        X = pd.DataFrame(self.dataset[self.dep_vars]) 
        y = pd.DataFrame(self.dataset[self.pred_var])
        reg = LinearRegression()
        R2_list = []
        kfold = KFold(n_splits=k, shuffle=True, random_state=42)
        for i, (train, test) in enumerate(kfold.split(X, y)):
            reg.fit(X.iloc[train, :], y.iloc[train, :])
            R2 = reg.score(X.iloc[test, :], y.iloc[test, :])
            R2_list.append(R2)
        return R2_list


#Applying Model class to New York dataset
#Bivariate regression with dependent variable as total SAT score and independent variable as:

#1) median income:
median_income_model = Model(merged_data, 'total_score', 'B06011_001E', 5)

#2) count below poverty level 
below_poverty_model = Model(merged_data, 'total_score', 'B17017_002E', 5)

#3) level of government assistance received
govt_assistance_model = Model(merged_data, 'total_score', 'B09010_001E', 5)

#Multivariate regression with all 3 variables as the independent variables
multivariate_regression_model = Model(merged_data, 'total_score', \
    ['B06011_001E', 'B17017_002E', 'B09010_001E'], 5)

#Exporting merged_data for further analysis in GIS tool
merged_data.to_csv('export_dataframe.csv', index = False, header=True)
