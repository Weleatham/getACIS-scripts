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
from io import StringIO
import foldercreate
# Station identifiers via cwa or state and date of interest.
station_id = 'BTV'#',aly,okx,gyx,btv'
the_date = datetime(2011,10,30)
def fetch_weather_data(station_id, the_date):
    base_url = 'https://data.rcc-acis.org/MultiStnData?'
    params = {
        #'state': station_id,
        'cwa': station_id,
        'date': the_date.strftime("%Y-%m-%d"),
        'elems': 'snow',#'pcpn',
        'output':'csv'
        #pcpn
    }
    response = requests.post(base_url,json=params)
    response.raise_for_status()  # Raise an error for bad HTTP status codes
    return response.content
def main():
    # First checking if the folder directories are created or not.
    outdir = foldercreate.folder_check("DataRequests","ACIS","Snowtober")
    # Fetch data from the web
    weather_data = fetch_weather_data(station_id, the_date)
    # Parse the CSV data into a dataframe
    col_names = ['UID','CITYNAME','STATE','LON','LAT','Elev_ft','Val_in']
    df = pd.read_csv(StringIO(weather_data.decode('utf-8')),names=col_names,header=None)
    df['Date'] = the_date
    df['Val_in'] = df['Val_in'].replace('M',np.nan)
    df['Val_in'] = df['Val_in'].replace('T',0.001)
    df[['Val_in','LON','LAT']] = df[['Val_in','LON','LAT']].apply(pd.to_numeric)
    df['CWA'] = station_id
    # Save data to a CSV file
    output_file = f'{station_id}-{the_date.year}-{the_date.month}-{the_date.day}.csv'
    df.to_csv(outdir+output_file)
    print(f'Data saved to {outdir}{output_file}')
if __name__ == "__main__":
    main()