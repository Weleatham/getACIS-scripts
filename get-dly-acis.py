#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
###############################################################################
# Script Created by William Leatham IV in September and October of 2023
# Description:
# This program created to gather single station daily data from RCC ACIS. 
# See rcc-acis.org/docs_webservices.html for more detailed information.
###############################################################################
# Edits:
# 
###############################################################################
"""
import requests
import pandas as pd
import numpy as np
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
        'meta': [],
        'elems': 'maxt,mint,pcpn,snow,snwd,cdd,hdd,gdd',
        'output': 'json',
    }

    response = requests.get(base_url, params=params)
    response.raise_for_status()  # Raise an error for bad HTTP status codes
    return response.json()

def main():
    # Station identifier and date range
    station_id = 'ORHthr'
    start_date = 'por'
    end_date = datetime(2023, 10, 20)
    outdir = '/Users/triforce/DataRequests/ACIS/'
    # Fetch data from the web
    weather_data = fetch_weather_data(station_id, start_date, end_date)
    #print(weather_data)
    # Parse CSV data into a DataFrame
    col_names = ['Date', 'Max Temp (F)', 'Min Temp (F)', 'Precipitation (in)',
                 'Snowfall (in)', 'Snow Depth (in)', 'CDD', 'HDD', 'GDD']
    metadata = weather_data['meta']
    # This dataframe has the data in it.
    df = pd.DataFrame(weather_data['data'], columns=col_names)
    df['Location'] = metadata['name']
    df.set_index('Location', inplace=True)
    coords = metadata.get('ll',[np.nan,np.nan])
    df['Lon'] = coords[0]
    df['Lat'] = coords[1]
    
    # Save data to a CSV file
    output_file = f'{station_id}-Ending-{end_date.year}-{end_date.month}-{end_date.day}.csv'
    df.to_csv(outdir+output_file)
    print(f'Data saved to {outdir}{output_file}')

if __name__ == "__main__":
    main()