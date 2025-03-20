# -*- coding: utf-8 -*-
"""
Created on Tue Mar  6 14:47:13 2018

@author: Brenda
"""

import pandas
import numpy
import seaborn
import matplotlib.pyplot as plt

#load dataset from the csv file in the dataframe called nesarc_data
gapminder_data = pandas.read_csv('gapminder.csv',low_memory=False)

#set PANDAS to show all columns in Data frame
pandas.set_option('display.max_columns', None)

#set PANDAS to show all rows in Data frame
pandas.set_option('display.max_rows', None)


#following code is commented out as we used a for loop instead to reduce the lines of code.
#replace blanks with Nan
#gapminder_data['internetuserate']=gapminder_data['internetuserate'].replace(" ", numpy.NaN)
#gapminder_data['urbanrate']=gapminder_data['urbanrate'].replace(" ", numpy.NaN)
#gapminder_data['incomeperperson']=gapminder_data['incomeperperson'].replace(" ", numpy.NaN)
#gapminder_data['hivrate']=gapminder_data['hivrate'].replace(" ", numpy.NaN)


#converting strings to numeric data for better output
#apminder_data['internetuserate'] = pandas.to_numeric(gapminder_data['internetuserate'])
#gapminder_data['urbanrate'] = pandas.to_numeric(gapminder_data['urbanrate'])
#gapminder_data['incomeperperson'] = pandas.to_numeric(gapminder_data['incomeperperson'])
#gapminder_data['hivrate'] = pandas.to_numeric(gapminder_data['hivrate'])

#print('Descriptive stats for internet use rate')
#print(gapminder_data['internetuserate'].describe())

#print('Descriptive stats for urban rate')
#print(gapminder_data['urbanrate'].describe())

#print('Descriptive stats for hiv rate')
#print(gapminder_data['hivrate'].describe())

#print(gapminder_data.groupby('hivrate').size())

#descriptive stats
#create a variable to hold an array of the variables you are using
var_in_use = [ 
    'internetuserate',
    'urbanrate',
    'incomeperperson',
    'hivrate']

#now loop through the variables and for each one remove spaces, change datatype and output the descriptive stats
for i in var_in_use:
    gapminder_data[i] = gapminder_data[i].replace(" ", numpy.NaN)
    gapminder_data[i] = pandas.to_numeric(gapminder_data[i])
    print('Descriptive stats for ' + i)
    print(gapminder_data[i].describe())
    


#scatter charts for quantitative response and explanatory variables
#urbanrate and internetuserate
seaborn.regplot(x="urbanrate", y="internetuserate", data=gapminder_data)
plt.xlabel('Urban Rate')
plt.ylabel('Internet Use Rate')
plt.title('Scatterplot for the Association between Urban Rate and Internet Use Rate')

#run pearsons correlation for these variables.
y = gapminder_data['internetuserate']
x = gapminder_data['urbanrate']
x.corr(y)

#Step 2 Exercises for incomeperperson and internetuserate
seaborn.regplot(x="incomeperperson", y="internetuserate", data=gapminder_data)
plt.xlabel('Income Per Person')
plt.ylabel('Internet Use Rate')
plt.title('Scatterplot for the Association between Income Per Person and Internet Use Rate')

#run pearsons correlation for these variables.
y = gapminder_data['internetuserate']
x = gapminder_data['incomeperperson']
x.corr(y)

#Step 3 hivrate and incomeperperson
#incomperperson and hivrate
seaborn.regplot(x="incomeperperson", y="hivrate", data=gapminder_data)
plt.xlabel('Income Rate')
plt.ylabel('HIV Rate')
plt.title('Scatterplot for the Association between Income Rate and HIV Rate')

#run pearsons correlation for these variables.
y = gapminder_data['hivrate']
x = gapminder_data['incomeperperson']
x.corr(y)

#quartile split (use qcut function for 4 groups giving the quartiles for incomeperperson)
print('Income per person - 4 categories - quartiles')
gapminder_data['incomegrp4']=pandas.qcut(gapminder_data.incomeperperson,4,labels=['1=25%tile','2=50%tile','3=75%tile','4=100%tile'])
c1 = gapminder_data['incomegrp4'].value_counts(sort=False,dropna=True)
print(c1)

#bivariate bar graph C->Q
seaborn.catplot(x='incomegrp4',y='hivrate',data=gapminder_data,kind='bar',errorbar=None)
plt.xlabel('income group')
plt.ylabel('mean HIV rate')
