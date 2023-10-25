#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
###############################################################################
# Script Created by William Leatham IV in October of 2023
# Description:
# This program created to gather single station normal temp data from RCC ACIS. 
# See rcc-acis.org/docs_webservices.html for more detailed information.Data
# output into a text file of json data.
###############################################################################
# Edits:
# 
###############################################################################
"""
import requests
from urllib.parse import urlencode, quote_plus
from datetime import datetime

def fetch_weather_data(station_id, start_date, end_date):
    base_url = 'https://data.rcc-acis.org/StnData?'
    if start_date =='por':
        sdate = 'por'
    else:
        sdate = start_date.strftime("%Y-%m-%d")
    params = {
        'sid': station_id,
        'sdate': sdate,
        'edate': end_date.strftime("%Y-%m-%d"),
        'elems': [{"name":"maxt","normal":"1"},
                  {"name":"mint","normal":"1"},
                  {"name":"avgt","normal":"1"}]
    }
    
    response = requests.post(base_url,json=params)
    response.raise_for_status()  # Raise an error for bad HTTP status codes
    return response.text

def main():
    # Station identifier and date range
    station_id = 'BOSthr'
    start_date = datetime(2020,1,1)
    end_date = datetime(2020, 12, 31)
    outdir = '/Users/triforce/DataRequests/ACIS/'
    # Fetch data from the web
    weather_data = fetch_weather_data(station_id, start_date, end_date)
    f = open(f'{station_id}-Temperature-Normals.txt',"w")
    f.write(weather_data)
    f.close()
    

    # Save data to a CSV file
   # output_file = 
    #df.to_csv(outdir+output_file)
    #print(f'Data saved to {outdir}{output_file}')

if __name__ == "__main__":
    main()