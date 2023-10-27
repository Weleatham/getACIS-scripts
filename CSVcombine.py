#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
###############################################################################
# Script Created by William Leatham IV in October of 2023
# Description:
# This program created to join together two panda dataframes from the 
# get-multistn-acis.py script. To generate a final dataframe/csv file 
# combining data. 
###############################################################################
# Edits:
#
###############################################################################
"""
import pandas as pd
import os
# Grabbing the directory where the data is located. This is also where the
# combined output file will be placed. The user must also enter the names of
# the files that they want to combine. 
data_dir = "/home/Shire/DataRequests/ACIS/Snowtober/"
cwa = "OKX"
f1 = cwa+"-2011-10-29.csv"
f2 = cwa+"-2011-10-30.csv"
# File naming convention.
fname, f_ext = f1.split('.')
fdate = f2.split('.')[0].split('-')[3]

def main():
    data_combine(f1,f2,data_dir)
    append_dfs(data_dir)

def data_combine(file1,file2,directory):
    # Opening the two pandas dataframes.
    df1 = pd.read_csv(directory+file1,index_col=0)
    df2 = pd.read_csv(directory+file2,index_col=0)
    # Changing the index to the CITYNAME.
    df1.set_index('CITYNAME',inplace=True)
    df2.set_index('CITYNAME',inplace=True)
    # Bringing together the two pandas dataframes.
    df_f = pd.concat([df1,df2],axis=1)
    df_f.index.rename('CITYNAME',inplace=True)
    # Summing up the columns of data we need. Then we remove the columns that we 
    # do not need.
    df_f['SNOWFALL'] = df_f['Val_in'].sum(axis=1)
    df_f = df_f.drop(columns=['UID','Elev_ft','Date','Val_in'])
    # Combining the areas where there is missing data based on the column index.
    # Then removing the columns we used to fill in the data.
    for i in range(4):
        df_f.iloc[:,i].fillna(df_f.iloc[:,i+4],inplace=True)
    # Removing the duplicate columns
    df_f = df_f.loc[:,~df_f.columns.duplicated()]
    # Creating the file name from the two files.
    output_file = fname+'-to-'+fdate+'.'+f_ext
    df_f.to_csv(directory+output_file)
    print(f'Data saved to {data_dir}{output_file}')

def append_dfs(filename,directory):
    for x in os.listdir(directory):
        if x.endswith("-to-"+fdate+'.'+f_ext):
            combined_df = pd.append([pd.read_csv(x)])
            combined_df.to_csv(directory+filename+f_ext)
            print(f'Data saved to {directory}{filename}{f_ext}')

if __name__ == "__main__":
    main()
    
