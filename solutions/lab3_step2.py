# -*- coding: utf-8 -*-
"""
Created on Tue Jan 30 15:34:08 2018

@author: BMULLALLY
"""

import pandas
import numpy

addhealth_data = pandas.read_csv('addhealth_pds.csv', low_memory=False)

#convert all to number data type
addhealth_data['H1GI4'] = pandas.to_numeric(addhealth_data['H1GI4'])
addhealth_data['H1GI6A'] = pandas.to_numeric(addhealth_data['H1GI6A'])
addhealth_data['H1GI6B'] = pandas.to_numeric(addhealth_data['H1GI6B'])
addhealth_data['H1GI6C'] = pandas.to_numeric(addhealth_data['H1GI6C'])
addhealth_data['H1GI6D'] = pandas.to_numeric(addhealth_data['H1GI6D'])


#replace missing values for options 6 and 8
addhealth_data['H1GI4'] = addhealth_data['H1GI4'].replace([6,8], numpy.nan)
addhealth_data['H1GI6A'] = addhealth_data['H1GI6A'].replace([6,8], numpy.nan)
addhealth_data['H1GI6B'] = addhealth_data['H1GI6B'].replace([6,8], numpy.nan)
addhealth_data['H1GI6C'] = addhealth_data['H1GI6C'].replace([6,8], numpy.nan)
addhealth_data['H1GI6D'] = addhealth_data['H1GI6D'].replace([6,8], numpy.nan)

#create the new variable NUETHNIC, holding the count of ethnicity's
addhealth_data['NUMETHNIC'] = addhealth_data['H1GI4'] + addhealth_data['H1GI6A'] + addhealth_data['H1GI6B'] + addhealth_data['H1GI6C'] + addhealth_data['H1GI6D']

#show the counts for NUMETHNIC values showing how many respondents identify with 1, 2, 3 or 4 ethinicity's 
print('counts for new variable NUMETHNIC')
print(addhealth_data['NUMETHNIC'].value_counts(sort=True))

#This is how to define a function in python. The keyword def is used followed by the function name followed by parameters.
#A colon: signifies the end of the function header
def ETHNICITY (row):
    if row['NUMETHNIC']>1:
        return 1
    if row['H1GI4'] ==1:
        return 2
    if row['H1GI6A'] ==1:
        return 3
    if row['H1GI6B'] ==1:
        return 4
    if row['H1GI6C']==1:
        return 5
    if row['H1GI6D']==1:
        return 6

#next we apply the function along an axis of the dataframe, axis=1 means apply the function to each row
#in this case we use a lambda function call the syntax is lambda X: X where lambda x: is the bound variable and the second x is the body of the funciton
#here the body is a call to a predefined funciton.
#we could of just used a regular call to the function
addhealth_data['ETHNICITY'] = addhealth_data.apply(lambda row: ETHNICITY (row), axis=1)

addhealth_data = addhealth_data[['AID', 'H1GI4','H1GI6A','H1GI6B','H1GI6C','H1GI6D','NUMETHNIC','ETHNICITY']]
print(addhealth_data.head(n=25))

