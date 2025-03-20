# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas
import numpy

# SETUP
#Columns that will be read from the CSV file and give them names that make sense
nesarc_dict =  {
  'TAB12MDX': 'NICOTINE_DEPENDENCE',
  'CHECK321' : 'SMOKING_STATUS',
   'S3AQ3B1' : 'FREQUENCY_OF_SMOKING',
   'S3AQ3C1' : 'QUANTITY_SMOKED',
   'S2AQ3': 'DRANK_ALCOHOL',
   'S2AQ8A' : 'ALCOHOL_FREQUENCY'
}

#LOAD DATA
nesarc_data = pandas.read_csv(
  'nesarc_pds.csv',
  low_memory=False
)
# RENAME COLUMNS
print('data read, performing rename operation')
nesarc_data.rename(columns=nesarc_dict, inplace=True)
print('data fetched')


#TEST THE RENAMING
print('counts for TAB12MDX - nicotine dependence in the past 12 months, yes=1')
print(nesarc_data["NICOTINE_DEPENDENCE"].value_counts(sort=True))


# PRINT details on dataframe
print('data details')
print('fetched ' + str(len(nesarc_data)) + ' rows')  # print length of data
print('fetched ' + str(len(nesarc_data.columns)) + ' columns')  # print number of columns
#
#Update the dataframe to only contain the columns you do want to use in your analysis.
nesarc_data = pandas.DataFrame(nesarc_data, columns = nesarc_dict.values())
print('new column amount: ' + str(len(nesarc_data.columns)))

print(nesarc_data.head())

print(nesarc_data.tail())

print(nesarc_data.dtypes)