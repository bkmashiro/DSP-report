# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas
import numpy

#load dataset from the csv file in the dataframe called nesarc_data
nesarc_data = pandas.read_csv('nesarc_pds.csv',low_memory=False)

#convert all columns names to uppercase
nesarc_data.columns = map(str.upper, nesarc_data.columns)
#nesarc_data.columns = map(str.lower, nesarc_data.columns)

#set PANDAS to show all columns in Data frame
pandas.set_option('display.max_columns', None)

#bug fix for display formats to avoid run time errors
pandas.set_option('display.float_format',lambda x:'%f'%x)

print (len(nesarc_data)) 
print (len(nesarc_data.columns))

#converting strings to numeric data for better output

nesarc_data['S3AQ3B1'] = pandas.to_numeric(nesarc_data['S3AQ3B1'], errors='ignore')
nesarc_data['S3AQ3C1'] = pandas.to_numeric(nesarc_data['S3AQ3C1'], errors='ignore')

#Count and percentage for each variable using value_counts function
print('counts for TAB12MDX - nicotine dependence in the past 12 months, yes=1')
print(nesarc_data["TAB12MDX"].value_counts(sort=True))
#percentage output for TAB12MDX
print('percentages for TAB12MDX - nicotine dependence in the past 12 months, yes=1')
print(nesarc_data["TAB12MDX"].value_counts(sort=True, normalize=True))


#same outcome using the groupby funciton
print('count of TAB12MDX nicotine dependence in the past 12 months, yes=1')
print (nesarc_data.groupby('TAB12MDX').size())
#percentage for TAB12MDX using the groupby function
print('percentage of TAB12MDX nicotine dependence in the past 12 months, yes=1')
print(nesarc_data.groupby('TAB12MDX').size() * 100 / len(nesarc_data))


#Count of CHECK321
print('counts for CHECK321 - smoked in the past year, yes=1')
print(nesarc_data["CHECK321"].value_counts(sort=True))

#Percentages of CHECK321
print('percentages for CHECK321 - smoked in the past year, yes=1')
print(nesarc_data["CHECK321"].value_counts(sort=True, normalize=True))

#count of S3AQ3B1
print('counts for S3AQ3B1 - usual frequency when smoked cigarettes')
print(nesarc_data["S3AQ3B1"].value_counts(sort=True))

#percentages of S3AQ3B1
print('percentages for S3AQ3B1 - usual frequency when smoked cigarettes')
print(nesarc_data["S3AQ3B1"].value_counts(sort=True, normalize=True))

#counts of S3AQ3C1
print('counts for S3AQ3C1 - usual quanitity when smoked cigarettes')
print(nesarc_data["S3AQ3C1"].value_counts(sort=True))

#percentages of S3AQ3C1
print('percentages for S3AQ3C1 - usual quanitity when smoked cigarettes')
print(nesarc_data["S3AQ3C1"].value_counts(sort=True, normalize=True))


