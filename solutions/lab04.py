# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 10:06:18 2018

@author: BMULLALLY
"""

import pandas
import numpy
import seaborn
import matplotlib.pyplot as plt
import math

#load dataset from the csv file in the dataframe called nesarc_data
nesarc_data = pandas.read_csv('nesarc_pds.csv',low_memory=False)

#set PANDAS to show all columns in Data frame
pandas.set_option('display.max_columns', None)

# restrict to those observations that are between 18 and 25 and smoke now
nesarc_data = nesarc_data[(nesarc_data['AGE']>=18) & (nesarc_data['AGE']<=25) & (nesarc_data['CHECK321']=='1')]
nesarc_data.head()

#subset2 = subset1.copy()

#ensure the variable is number data type first
nesarc_data['S3AQ3B1'] = pandas.to_numeric(nesarc_data['S3AQ3B1'], errors='ignore')

#replace the value 9 in S3AQ3B1 with Nan to signify missing data
nesarc_data['S3AQ3B1'].replace(to_replace =9, value=numpy.NaN, inplace=True)

#double check did it work
print((nesarc_data['S3AQ3B1']==9).sum())

#first create the dictionary to recode
recode1= {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}

#next create the new USFREQ variable and use the map funciton to replace values using the recode dictionary
nesarc_data['USFREQ'] = nesarc_data['S3AQ3B1'].map(recode1)

#Now recode to a quantitative value based on an estimate of how many times per month each person smokes
recode2 = {1: 30, 2: 22, 3: 14, 4: 5, 5: 2.5, 6: 1}

#create a new variable USFREQMO how many days a person smokes in a month
nesarc_data['USFREQMO'] = nesarc_data['S3AQ3B1'].map(recode2)

#make sure S2AQ3C1 is a number and any 99's are changed to NaN
nesarc_data['S3AQ3C1'] = pandas.to_numeric(nesarc_data['S3AQ3C1'], errors='ignore')
nesarc_data['S3AQ3C1'].replace(99, numpy.NaN, inplace=True)

#create new secondary variable to hold number of cigarettes per month
nesarc_data['NUMCIGMO_EST'] = nesarc_data['USFREQMO'] * nesarc_data['S3AQ3C1']

#make a new subset with only certain varialbes are included
subset1=nesarc_data[['IDNUM','S3AQ3C1','USFREQMO', 'NUMCIGMO_EST']]

#display only the first 25 rows of data in the new subset
subset1.head(25)


#LAB 04
#step 1 Exercise


#counts for TAB12MDX
print('count of TAB12MDX')
print (nesarc_data.groupby('TAB12MDX').size())

print('same count different function used')
print( nesarc_data['TAB12MDX'].value_counts(sort=False, dropna=True))


#percentages for TAB12MDX
print('percentages of counts')
print(nesarc_data.groupby('TAB12MDX').size() * 100 /len(nesarc_data))

#counts for NUMCIGMO_EST
print('count of NUMCIGMO_EST')
print(nesarc_data.groupby('NUMCIGMO_EST').size())

print('same count different function used')
print(nesarc_data['NUMCIGMO_EST'].value_counts(sort=False, dropna=True))

#percentages for NUMCIGMO_EST
print('percentages of counts')
p2 = nesarc_data.groupby('NUMCIGMO_EST').size() * 100 /len(nesarc_data)
print(p2)

#Description of NUMCIGMO_EST and mean, mode, median, std, min and max
print('describe number of cigarettes smoked per month')
print(nesarc_data['NUMCIGMO_EST'].describe())

#mean only for NUMCIGMO_EST
print('mean')
print(nesarc_data['NUMCIGMO_EST'].mean())

#std dev only for NUMCIGMO_EST
print('std deviation')
print(nesarc_data['NUMCIGMO_EST'].std())

#minimum only for NUMCIGMO_EST
print('min')
print(nesarc_data['NUMCIGMO_EST'].min())

#maximum only for NUMCIGMO_EST
print('max')
print(nesarc_data['NUMCIGMO_EST'].max())

#median only for NUMCIGMO_EST
print('median')
print(nesarc_data['NUMCIGMO_EST'].median())

#mode only for NUMCIGMO_EST
print('mode')
print(nesarc_data['NUMCIGMO_EST'].mode())



#lab 4 step 2 univariate graphing

#categorical bar chart
seaborn.countplot(x='TAB12MDX',data=nesarc_data)
plt.xlabel('Nicotine Dependence past 12 months 1=yes')
plt.ylabel('The number of respondents')
plt.title('Nicotine Dependence in the past 12 months among young adult smokers in the Nesarc study')

#Step 2 Exercise
print('describe categorical variable TAB12MDX')
print(nesarc_data['TAB12MDX'].describe())

#Step 3
#numerical histogram
seaborn.histplot(nesarc_data.NUMCIGMO_EST.dropna())
plt.xlabel('Number of cigarettes per month')
plt.title('Estimated number of cigarettes per month among young adult smokers in the Nesarc study')



#step 3 exercise
#categorise variable based on customised splits using the cut() function
# splits into 6 groups, 1-200, 200-400, 400-600, 600-800, 800-1000, 1000-4000
print('Group the variable NUMCIGMO_EST into bins')
nesarc_data['NUMCIGMO_EST_BINS'] = pandas.cut(nesarc_data.NUMCIGMO_EST, [0,199,399,599,799,999,4000], labels=['1-199','200-399','400-599','600-799','800-999','1000-3999'])
print(nesarc_data['NUMCIGMO_EST_BINS'].value_counts(sort=False,dropna=True))

#Step 3 exercise bar chart of number of cigs 6 bins
seaborn.countplot(x='NUMCIGMO_EST_BINS', data=nesarc_data)
plt.xlabel('Nicotine Dependence past 12 months by number of cigarettes')
plt.title('Nicotine Dependnce among young adults')

#step 4 
#create a new variable packspermonth 
nesarc_data['PACKSPERMONTH'] = nesarc_data['NUMCIGMO_EST'] / 20

#output the counts for packs per month
print('describe packs per month')
print(nesarc_data.groupby('PACKSPERMONTH').size())

#create a variable to hold a packspermonth category
nesarc_data['PACKCATEGORY'] = pandas.cut(nesarc_data.PACKSPERMONTH, [0,5,10,20,30,147], labels=['1-5','6-10','11-20','21-30','31-147'])

#change format of variable from numerical to categorical
#convert to numerical so the proportion is calculated without errors
nesarc_data['PACKCATEGORY'] = nesarc_data['PACKCATEGORY'].astype('category')

#output the counts per category
print('describe pack category')
print(nesarc_data['PACKCATEGORY'].groupby(nesarc_data['PACKCATEGORY']).size())


#now chart using a categorical to categorical chart
#bivariate bar chart, here tab12mdx is in fact a numer so a proportion
#is shown on the y axis, i.e. 50% of those smoking 5 to 10 packs a month are nicotine dependent

seaborn.catplot(x='PACKCATEGORY',y='TAB12MDX',data=nesarc_data,kind='bar', errorbar=None)
plt.xlabel('Packs per month')
plt.ylabel('Proportion Nicotine dependence')



#Step 5 smokegrp holds 1 if nicotine dependent, 2 for daily smoker, 3 all others
#define a function called SMOKEGRP, it takes a row as its parameters
#if  that row has a 1 for TAB12MDX then the the function returns a 1
#if  that row has a 30 for USFREQMO then the the function returns a 2
#otherwise it returns a 3.
def SMOKEGRP (row):
  if row['TAB12MDX'] == 1:
    return 1
  elif row['USFREQMO'] == 30:
    return 2
  else:
    return 3

#create the new variable SMOKEGRP by applying the function to each row in the nesarc_data
nesarc_data['SMOKEGRP'] = nesarc_data.apply(lambda row: SMOKEGRP (row), axis=1)

#counts for each smoke group
print('counts 1 = nicotine dependent 2 = daily smoker 3 = other')
print(nesarc_data['SMOKEGRP'].value_counts(normalize=True))


#univariate chart for smokegrp
seaborn.countplot(x='SMOKEGRP',data=nesarc_data)
plt.xlabel('Nicotine Dependence past 12 months')
plt.title('Nicotine Dependence (1), daily smokers(2) and all other(3) young adult smokers in the Nesarc study')


#to conduct analysis with another variable we must collapse the groups into two.
#DAILY function returns 1 if usfreqmo is 30 and 0 otherwise
def DAILY(row):
    if row['USFREQMO'] == 30:
        return 1
    elif row['USFREQMO'] != 30:
        return 0

#apply the function to each row in the nesarc dataset
nesarc_data['DAILY'] = nesarc_data.apply(lambda row: DAILY(row), axis=1)

#counts for daily(1) smokers and others(0)
print(nesarc_data.groupby('DAILY').size())

#Next work on bringing in ETHRACE2A to see the relationship between daily smokers
#and ethinicity
nesarc_data['ETHRACE2A'] = nesarc_data['ETHRACE2A'].astype('category')

#show the counts for each ethnic category 1 through 5
print(nesarc_data.groupby('ETHRACE2A').size())

#rename the categories in ETHRACE2A so they are more meaningfull
nesarc_data['ETHRACE2A'] = nesarc_data['ETHRACE2A'].cat.rename_categories(['White','Black','NatAm','Asian','Hispanic'])


#graph the relationship between categorical ETHRACE2A and new categorical DAILY
seaborn.catplot(x='ETHRACE2A', y='DAILY', data=nesarc_data, kind='bar', errorbar=None)
plt.xlabel('Ethnic Group')
plt.ylabel('Proportion Daily Smokers')
plt.title('Proportion of Daily Smokers for each Ethnic group')

#output the counts for ethnic groups for daily and non daily smokers.
print(nesarc_data.groupby(['DAILY','ETHRACE2A']).size())

#lab4 step 5
#multiple graph output

#this creates a figure that holds two charts, a histogram and a box plot
#matplotlib library allows us to create a subplot which in this case is 1 row and 2 coloumns
#it returns a figure and an ax or axes, in this cases the axes is a single dimension array
#with two positions, ax[0] and ax[1] each for a chart.
fig, ax = plt.subplots(1,2)

#we can set the main title using fig.suptitle
fig.suptitle('Estimated number of cigarettes per month')
#set the title of the chart in position 0
ax[0].title.set_text('Distribution')

#create the histogram of NUMCIGMO_EST data for ax[0]
seaborn.histplot(nesarc_data['NUMCIGMO_EST'].dropna(),kde=False, ax=ax[0])


#set the title for the second chart in ax[1]
ax[1].title.set_text('Outliers')
#create a temporary dataframe to hold the NUMCIGMO_EST data
#tmp_dtf = pandas.DataFrame(nesarc_data['NUMCIGMO_EST'])
#tmp_dtf['NUMCIGMO_EST'] = numpy.log(tmp_dtf['NUMCIGMO_EST'])
#create the boxplot for ax[1]
nesarc_data.boxplot(column='NUMCIGMO_EST', ax=ax[1])
#tmp_dtf.boxplot(column='NUMCIGMO_EST', ax=ax[1])
plt.show
