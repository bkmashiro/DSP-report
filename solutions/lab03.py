 # -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas
import numpy


#load dataset from the csv file in the dataframe called nesarc_data
nesarc_data = pandas.read_csv('nesarc_pds.csv',low_memory=False)

#convert spaces to NAN
nesarc_data['CHECK321']=nesarc_data['CHECK321'].replace(' ', numpy.nan)

#converting strings to numeric data for better output

nesarc_data['TAB12MDX'] = pandas.to_numeric(nesarc_data['TAB12MDX'],errors='ignore')
nesarc_data['CHECK321'] = pandas.to_numeric(nesarc_data['CHECK321'],errors='ignore')

nesarc_data['S3AQ3C1'] = pandas.to_numeric(nesarc_data['S3AQ3C1'], errors='ignore')

# restrict to those observations that are between 18 and 25 and smoke now
nesarc_data = nesarc_data[(nesarc_data['AGE']>=18) & (nesarc_data['AGE']<=25) & (nesarc_data['CHECK321']==1)]
print(len(nesarc_data))

print('counts for AGE ')
print(nesarc_data['AGE'].value_counts(sort=True))

print('percentages for AGE ')
print(nesarc_data["AGE"].value_counts(sort=True, normalize=True))


print('The count of those who have smoked in the past 12 months')
print(nesarc_data['CHECK321'].value_counts(sort='TRUE'))


subset2 = nesarc_data.copy()

print('Number of observations in subset 2')
print(len(subset2))

print(subset2.dtypes)
print(len(subset2.columns))


#Lab 2 step 2 replacing missing data
#counts for S3AQ3B1
print('counts for S3AQ3B1 - usual frequency when smoked cigarettes')
print(nesarc_data['S3AQ3B1'].value_counts(sort=True))
nesarc_data['S3AQ3B1'] = pandas.to_numeric(nesarc_data['S3AQ3B1'])
print(nesarc_data['S3AQ3B1'].dtypes)

#replace the value 9 in S3AQ3B1 with Nan to signify missing data
nesarc_data['S3AQ3B1'].replace(to_replace =9, value=numpy.NaN, inplace=True)

#check 
print((nesarc_data['S3AQ3B1']==9).sum())
print(nesarc_data['S3AQ3B1'].isnull().sum())

#counts for S3AQ3B1 after set to Nan
print(nesarc_data.describe())
print('counts for S3AQ3B1 - usual frequency when smoked cigarettes')
print(nesarc_data['S3AQ3B1'].value_counts(sort=True, dropna=False))


#Lab 2 step 3 data management missing values
#first make sure the variable is a number
nesarc_data['S2AQ3']=pandas.to_numeric(nesarc_data['S2AQ3'])

#next look at the counts for the variables
#180 answered "no" for did you dringk in the past 12 months
print(nesarc_data['S2AQ3'].value_counts(sort=True, dropna=False))

#180 answered " " blank for how often they drank in the past 12 months
print(nesarc_data['S2AQ8A'].value_counts(sort=True, dropna=False))


#first see if there are any nulls
print('count of nulls')
print((nesarc_data['S2AQ8A'].isnull()).sum())

#next see if there are any empty values
print('count of empty')
print((nesarc_data['S2AQ8A']=="").sum())

#next see if there are any that contain a space
print('count of " " spaces')
print((nesarc_data['S2AQ8A']==" ").sum())

#replace the blank data with a NaN
nesarc_data['S2AQ8A']=nesarc_data['S2AQ8A'].replace(' ', numpy.NaN)

#Print the counts for the S2AQ8A variable and then sum the number of nulls
print('counts of nulls')
print(nesarc_data['S2AQ8A'].isna().sum())


#using loc to apply logic and replace with a new value of 11
nesarc_data.loc[(nesarc_data['S2AQ3']!=9) & (nesarc_data['S2AQ8A'].isnull()),'S2AQ8A']=11


print((nesarc_data['S2AQ8A']==11).sum())

#Lab2 step 4, recoding values

#first create the dictionary to recode
recode1= {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1}

#next use the map funciton to replace values using the recode dictionary
nesarc_data['USFREQ'] = nesarc_data['S3AQ3B1'].map(recode1)

#Now recode to a quantitative value based on an estimate of how many times per month each person smokes

recode2 = {1: 30, 2: 22, 3: 14, 4: 5, 5: 2.5, 6: 1}

nesarc_data['USFREQMO'] = nesarc_data['S3AQ3B1'].map(recode2)

print('counts for S3AQ3B1')
print(nesarc_data['S3AQ3B1'].value_counts(sort=True, dropna=False))


print('counts for USFREQ')
print(nesarc_data['USFREQ'].value_counts(sort=True, dropna=False))


print('counts for USFREQMO')
print(nesarc_data['USFREQMO'].value_counts(sort=True, dropna=False))


print('percentages for USFREQMO')
print(nesarc_data['USFREQMO'].value_counts(sort=True, normalize=True))



#lab3 step 1 add a variable


#make sure S2AQ3C1 is a number
nesarc_data['S3AQ3C1']=pandas.to_numeric(nesarc_data['S3AQ3C1'])


#create new secondary variable to hold number of cigarettes per month
nesarc_data['NUMCIGMO_EST'] = nesarc_data['USFREQMO'] * nesarc_data['S3AQ3C1']

#make a new subset with only certain varialbes are included
subset1=nesarc_data[['IDNUM','S3AQ3C1','USFREQMO', 'NUMCIGMO_EST','AGE']]

#display only the first 25 rows of data in the new subset
subset1.head(25)


#Lab 3 Step 4 regroup values


#quartile split qcut function into 4 groups
print('AGE - 4 Categories - quartiles')
nesarc_data['AGEGROUP'] = pandas.qcut(nesarc_data.AGE, 4, labels=['1=25%tile','2=50%tile','3=75%tile','4=100%tile'])
print(nesarc_data['AGEGROUP'].value_counts(sort=False, dropna=True))

#we can also groupby agegroup and see the mean for number of smoked
print('count values in categories using groupby')
print(nesarc_data.groupby(['AGEGROUP']).agg({'NUMCIGMO_EST':['mean']}))

#we can groupby agegroup and see the mean for number smoked and the count of cigarettes per month for each agegroup
print('customise splits of agegroup')
print(nesarc_data.groupby(['AGEGROUP']).agg({'NUMCIGMO_EST':'mean','USFREQMO':'count'}))


#categorise variable based on customised splits using the cut() functions
# splits into three groups, 18-20, 21-22, and 23-25
nesarc_data['AGEGROUP2']= pandas.cut(nesarc_data.AGE, [17, 20, 22, 25], labels=['18-20','21-22','23-25'])
print(nesarc_data['AGEGROUP2'].value_counts(sort=False, dropna=True))
print(nesarc_data['AGEGROUP'].dtypes)

#print out a crosstab of AGEGROUP and AGE
print('Crosstab showing the distribution of Age\'s for each AGEGROUP')
print(pandas.crosstab(nesarc_data['AGEGROUP2'],nesarc_data['AGE']))

#print out the value counts as percentages for AGEGROUP2
print('Counts for each category in AGEGROUP2')
print(round(nesarc_data['AGEGROUP2'].value_counts(sort=False, dropna=False, normalize=True),2))
