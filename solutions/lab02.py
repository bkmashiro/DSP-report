 # -*- coding: utf-8 -*-
"""
Brenda Mullally
07/01/2024



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



#step 2 replacing missing data
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


#step 3 data management missing values
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

#step 4, recoding values

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

nesarc_data['USFREQMO'].dtypes
nesarc_data.fillna(0)
nesarc_data.dropna(inplace=True)
nesarc_data['USFREQMO'].astype(int)


