#tryespnjson.py

import json
import re
from pandas.io.parsers import read_csv
import requests
from bs4 import BeautifulSoup as bs 
import pandas as pd
import xlsxwriter
import time
from io import StringIO
from common import *
import xlwt
import os
from hurst import compute_Hc, random_walk


def main():

    # longer: price_url = 'https://finance.yahoo.com/quote/{}/history?period1=1442880000&period2=1632268800&interval=1d&filter=history&frequency=1d&includeAdjustedClose=true'
    price_url = 'https://finance.yahoo.com/quote/{}/history?p={}'

    # ticker_code = 'KAR'         # later get a dialog box to ask for the code
    dfloader = pd.read_csv('comm_loadfile.csv')
    dfhursttracker = pd.DataFrame()
    dicthurst = {'ticker':'','hurst':.000,'c':.000, 'processdate':processdate}
    
    outputdir = '/Users/johncyclist22/Documents/Data/price_analysis/'+processdate+'/'
    CHECK_FOLDER = os.path.isdir(outputdir)
    if not CHECK_FOLDER:
        os.makedirs(outputdir)
    
    for counter, record in dfloader.iterrows():
    
        dfpricehistory = pd.DataFrame()
        print("downloading prices for....", record.ticker_code)
        dfpricehistory = processpricehistory(price_url, record.ticker_code)
        
        if len(dfpricehistory.index) > 0:
            outputfile = 'price_history-' + record.ticker_code + '-' + processdate + '.csv'
            dfpricehistory.to_csv(outputdir+outputfile)
            
            series = dfpricehistory['close'][len(dfpricehistory.index)-200:len(dfpricehistory.index)]
            # series = series.reset_index(inplace=True)
            H, c, data = compute_Hc(series, kind='price', simplified=True)
            dicthurst['ticker']=record.ticker_code
            dicthurst['hurst']=H
            dicthurst['c']=c
            dfhursttracker=dfhursttracker.append(dicthurst, ignore_index=True)
        else:
            dicthurst['ticker']=record.ticker_code
            dicthurst['hurst']=0
            dicthurst['c']=0
            dfhursttracker=dfhursttracker.append(dicthurst, ignore_index=True)

    dfhursttracker.to_csv(outputdir+'hurst-'+processdate+'.csv')
        

main()
