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
###############################################################################
"""
import requests
from datetime import datetime
import pandas as pd
import numpy as np
import foldercreate
import json
# Station identifiers via cwa or state and date of interest.
bounds = "-74.5,40.3,-68.0,43.2"
sdate = datetime(2020,12,1)
edate = datetime(2021,2,28)
var = "snow"
sumhead = "SNOWFALL"
precision = 1
msdays = 3
# First checking if the folder directories are created or not.
outdir = foldercreate.folder_check("DataRequests","ACIS","StrongElNino")
def fetch_weather_data(bound_box, start_date, end_date, variable,maxmissdays):
    base_url = 'https://data.rcc-acis.org/MultiStnData?'
    params = {
        #'state': station_id,
        'bbox': bound_box,
        'sdate':start_date.strftime("%Y-%m"),
        'edate': end_date.strftime("%Y-%m"),
        'meta':'uid,name,ll,state',
        'elems': [{"name":variable,
                   "interval":[0,1],
                   "duration":1,
                   "reduce":"sum",
                   "normal":1}],
                  # "maxmissing":maxmissdays}],
        'output':'json'
        #pcpn
    }
    response = requests.post(base_url,json=params)
    response.raise_for_status()  # Raise an error for bad HTTP status codes
    return response.text
def main():
    month_list = [i.strftime("%b-%y") for i in pd.date_range(start=sdate,end=edate,freq='MS')]
    json_parsed = []
    weather_data = json.loads(fetch_weather_data(bounds,sdate,edate,var,msdays))
# print(weather_data)
 #print(weather_data)
 # Parsing through json so it can easily be loaded into a dataframe.
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
    df[month_list] = pd.DataFrame(df['Data'].tolist()).map(lambda x: x[0])
    # Removing the extra data column we don't need.
    df = df.drop(columns='Data')
    # Converting the data into a numeric value.
    df[month_list] = df[month_list].replace('M',np.nan)
    df[month_list] = df[month_list].replace('T',0.0001)
    df[month_list] = df[month_list].apply(pd.to_numeric)
    # Summing up the columns of data. If one month is missing data then
    # the SUM is equal to NaN.
    df[sumhead] = df[month_list].sum(axis=1, min_count=1)
    df[sumhead] = np.where((df[sumhead] > 0.0004),
                                    df[sumhead].round(precision),
                                     df[sumhead])
    # Save data to a CSV file
    output_file = f'{sumhead}-{sdate.year}-{edate.year}.csv'
    df.to_csv(outdir+output_file)
    print(f'Data saved to {outdir}{output_file}')
if __name__ == "__main__":
   main()