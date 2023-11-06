#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
###############################################################################
# Script Created by William Leatham IV in October of 2023
# Description:
# This program created to gather multiple station precipitation and/or snowfall
# data. The data is returned to the user as a .csv file in the directory the
# user decides.
# See rcc-acis.org/docs_webservices.html for more detailed information. 
###############################################################################
# Edits:
# Added a folder check for where the data is downloaded to. 
# Nov 6, 2023
# Changed to area bounds for getting data vs CWA. Put the daily data into a
# dataframe that is summed up and returned to the user.
###############################################################################
"""
import requests
from datetime import datetime
import pandas as pd
import numpy as np
from io import StringIO
import foldercreate
import json
# Station identifiers via bounding box.
bounds = "-74.5,40.3,-68.0,43.2"
var = "snow" #pcpn
sumhead = "SNOWFALL"
sdate = datetime(2015,2,14)
edate = datetime(2015,2,16)
precision = 1
# First checking if the folder directories are created or not.
outdir = foldercreate.folder_check("DataRequests","ACIS","Feb-14-16-2015")
def fetch_weather_data(bound_box,start_date,end_date,variable):
    base_url = 'https://data.rcc-acis.org/MultiStnData?'
    params = {
        #'state': station_id,
        'bbox': bound_box,
        'sdate': start_date.strftime("%Y-%m-%d"),
        'edate': end_date.strftime("%Y-%m-%d"),
        'meta':'uid,name,ll,state',
        'elems': [{"name":variable,
                   "interval":[0,0,1]}],
        'output':'json'
    }
    response = requests.post(base_url,json=params)
    response.raise_for_status()  # Raise an error for bad HTTP status codes
    return response.text
def main():
    the_date_lst = [i.strftime("%Y-%m-%d") for i in pd.date_range(start=sdate,end=edate,freq='D')]
    json_parsed = []
    weather_data = json.loads(fetch_weather_data(bounds,sdate,edate,var))
    for item in weather_data.values():
        for x in item:
            json_parsed.append({
            'LON' : x['meta']['ll'][0],
            'LAT' : x['meta']['ll'][1],
            'STATE':x['meta']['state'],
            'UID': x['meta']['uid'],
            'NAME': x['meta']['name'],
            'Data': x['data'],
            })
    df = pd.DataFrame(json_parsed)
    # Adding the snow/precip/temp data to the dataframe a month at a time.
    df[the_date_lst] = pd.DataFrame(df['Data'].tolist()).map(lambda x: x[0])
    # Removing the extra data column we don't need.
    df = df.drop(columns='Data')
    # Converting the data into a numeric value.
    df[the_date_lst] = df[the_date_lst].replace('M',np.nan)
    df[the_date_lst] = df[the_date_lst].replace('T',0.0001)
    df[the_date_lst] = df[the_date_lst].apply(pd.to_numeric)
    # Summing up the columns of data. If one month is missing data then
    # the SUM is equal to NaN.
    df[sumhead] = df[the_date_lst].sum(axis=1, min_count=1)
    df[sumhead] = np.where((df[sumhead] > 0.0004),
                                    df[sumhead].round(precision),
                                    df[sumhead])
    df[sumhead] = np.where((df[sumhead] <= 0.0004),
                                    'T',
                                    df[sumhead])
    df.set_index('UID',inplace=True) 
    # Save data to a CSV file
    output_file = f'{sumhead}-{sdate.year}-{sdate.month}-{sdate.day}-to-{edate.year}-{edate.month}-{edate.day}.csv'
    df.to_csv(outdir+output_file)
    print(f'Data saved to {outdir}{output_file}')
if __name__ == "__main__":
   main()