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
usrdir = os.path.expanduser('~')+"/"
data_dir = usrdir+"DataRequests/ACIS/Snowtober/"
offices = ('BOX','ALY','OKX','GYX','BTV')
datval = "SNOWFALL"

def merge_col(x):
        return ','.join(x[x.notnull()].astype(str))
def main():
    for cwa in offices:
        data_combine(cwa,data_dir,datval)
    append_dfs("Snowtober",data_dir)

def data_combine(header,directory,val_str):
    # Combine data via CWA first. 
    # Finding all the files that start with the CWA name.
    files = [x for x in os.listdir(directory) if x.startswith(header)]
    lst = []
    # Appending each of the files to a list.
    for f in files:
        dfi = pd.read_csv(directory+f,index_col=0)
    # Removing where any of the data is missing.
        dfi = dfi.dropna(subset=['Val_in'])
    # Removing duplicate information when the data is missing/blank.
        dfi = dfi.sort_values(['UID','Val_in'],ascending=['True','False']).drop_duplicates(['UID'])
        dfi.set_index('UID',inplace=True)
        lst.append(dfi)
    # Concatenate the list of the dataframes.
    df_f = pd.concat(lst,axis=1)
    df_f.index.rename('UID',inplace=True)
    # Summing totals from the Val_in columns. 
    df_f[val_str] = df_f.filter(like='Val_in').sum(axis=1)
    # Filling in where there is NaN in columns outside of Snowfall
    for i in lst:
        df_f.update(i)
    # Removing some of the columns that we no longer need.
    df_f = df_f.drop(columns=['Elev_ft','Date','Val_in',])
    # Removing the duplicate columns.
    df_f = df_f.T.drop_duplicates().T
    # Creating the file name from the two files.
    output_file = "Merged-"+val_str+"-"+header+".csv"
    df_f.to_csv(directory+output_file)
    print(f'Data saved to {data_dir}{output_file}')

def append_dfs(filename,directory):
   #Listing only the files in the directory that start with the name merged.
   # Comes from the data_combine section above.
   files = [x for x in os.listdir(directory) if x.startswith("Merged")]
   # Bringing together all of the Merged csv files in the directory.
   combined_df = pd.concat((pd.read_csv(directory+f) for f in files),ignore_index=True)
   combined_df.set_index('UID',inplace=True)
   # Setting values that are equal to 0.001 back to a trace. May need to revisit here
   # for longer term data.
   combined_df ['SNOWFALL'] = combined_df['SNOWFALL'].replace(0.001,'T')
   combined_df.to_csv(directory+filename+".csv")
   print(f'Data saved: {directory}{filename}.csv')

if __name__ == "__main__":
    main()
    
