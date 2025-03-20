# -*- coding: utf-8 -*-
"""
Created on Tue Jan 29 14:02:12 2019

@author: BMULLALLY
"""

import numpy
import pandas
import statsmodels.formula.api as smf
import statsmodels.stats.multicomp as multi
import seaborn
import matplotlib.pyplot as plt


pandas.set_option('display.float_format',lambda x: '%f'%x)

nesarc_data = pandas.read_csv('nesarc_pds.csv', low_memory=False)


var_in_use = [ 
    'CHECK321',
    'S3AQ3B1',
    'S3AQ3C1',
    'AGE']

for i in var_in_use:
    nesarc_data[i] = nesarc_data[i].replace(" ", numpy.NaN)
    nesarc_data[i] = pandas.to_numeric(nesarc_data[i])
    print('Descriptive stats for ' + i)
    print(nesarc_data[i].describe())
  
"""


#SETTING MISSING SPACES in TEXT DATA
nesarc_data['CHECK321']=nesarc_data['CHECK321'].replace(' ', numpy.nan)
nesarc_data['S3AQ3B1'] = nesarc_data['S3AQ3B1'].replace(' ', numpy.nan)
nesarc_data['S3AQ3C1'] = nesarc_data['S3AQ3C1'].replace(' ', numpy.nan)

#setting variables you will be working with to numeric
nesarc_data['CHECK321'] = pandas.to_numeric(nesarc_data['CHECK321'])
nesarc_data['S3AQ3B1'] = pandas.to_numeric(nesarc_data['S3AQ3B1'])
nesarc_data['S3AQ3C1'] = pandas.to_numeric(nesarc_data['S3AQ3C1'])
nesarc_data['AGE'] = pandas.to_numeric(nesarc_data['AGE'])
"""

#subset data to young adults age 18 to 25 who have smoked in the past 12 months
nesarc_data = nesarc_data[(nesarc_data['AGE']>=18) & (nesarc_data['AGE']<=26) & (nesarc_data['CHECK321']==1)]


#SETTING MISSING NUMERICAL DATA
nesarc_data['S3AQ3B1']=nesarc_data['S3AQ3B1'].replace(9, numpy.nan)
nesarc_data['S3AQ3C1']=nesarc_data['S3AQ3C1'].replace(99, numpy.nan)

#recoding number of days smoked in the past month
recode1 = {1: 30, 2: 22, 3: 14, 4: 5, 5: 2.5, 6: 1}
nesarc_data['USFREQMO']= nesarc_data['S3AQ3B1'].map(recode1)

#test that the maping took place
print(nesarc_data[['S3AQ3B1','USFREQMO']])
nesarc_data['USFREQMO'].describe
nesarc_data['S3AQ3C1'].describe

# Create a secondary variable multiplying the days smoked/month and the number of cig/per day
nesarc_data['NUMCIGMO_EST']=nesarc_data['USFREQMO'] * nesarc_data['S3AQ3C1']

#print the number of people per value.
print('print the number of people per value in NUMCIGMO_EST')
print(nesarc_data.groupby('NUMCIGMO_EST').size())



#calculate the means and standard deviations for monthly smoking for each category of MAJORDEPLIFE
print('means for numcigmo_est by major depression status')

#Mean for NUMCIGMO_EST by each value in MAJORDEPLIFE
print('means for NUMCIGMO_EST by Major lIfe depression yes=1')
print(nesarc_data.groupby(['MAJORDEPLIFE']).agg({'NUMCIGMO_EST':['mean']}))

#Std deviation for NUMCIGMO_EST by each value in MAJORDEPLIFE
print('standard deviations for numcigmo_est by major depression status')
print(nesarc_data.groupby(['MAJORDEPLIFE']).agg({'NUMCIGMO_EST':['std']}))

# using OLS function for calculating the F-statistic and associated p value

model1 = smf.ols(formula='NUMCIGMO_EST ~ C(MAJORDEPLIFE)', data=nesarc_data)
results1 = model1.fit()
print(results1.summary())

#Step 3
#Explanatory variable with more than two values
#ethnicity & smoking - graph delveloped in lab 4 step 4

#only valid data allowed in the two variables
nesarc_data=nesarc_data[['NUMCIGMO_EST', 'ETHRACE2A']].dropna()

model2 = smf.ols(formula='NUMCIGMO_EST ~ C(ETHRACE2A)', data=nesarc_data)
results2 = model2.fit()
print(results2.summary())


#Recode variable type and categories instead of 1 to 5
nesarc_data['ETHRACE2A'] = nesarc_data['ETHRACE2A'].astype('category')

nesarc_data['ETHRACE2A'] = nesarc_data['ETHRACE2A'].cat.rename_categories(['White','Black','NatAm','Asian','Hispanic'])

#calculate the means and standard deviations for monthly smoking for each category of MAJORDEPLIFE
#Mean for NUMCIGMO_EST by each value in ETHRACE2A
print('means and std deviations for numcigmo_est by Ethnic race')
print(nesarc_data.groupby(['ETHRACE2A']).agg({'NUMCIGMO_EST':['mean']}))

#Std deviation for NUMCIGMO_EST by each value in MAJORDEPLIFE
print('standard deviations for numcigmo_est by Ethnicity')
print(nesarc_data.groupby(['ETHRACE2A']).agg({'NUMCIGMO_EST':['std']}))


#Step 3 post hoc test

mc1 = multi.MultiComparison(nesarc_data['NUMCIGMO_EST'], nesarc_data['ETHRACE2A'])
res1 = mc1.tukeyhsd()
print(res1.summary())

#Step 4
y = nesarc_data['NUMCIGMO_EST']
x = nesarc_data['USFREQMO']

x.corr(y)

seaborn.regplot(x="USFREQMO", y="NUMCIGMO_EST", fit_reg=True, data=nesarc_data)
plt.xlabel('Number of Cigs per month')
plt.ylabel('User frequency per month')
plt.title('Scatterplot for the Association between number of cigs and user frequency')

