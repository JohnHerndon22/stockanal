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


def main():

    base_url = 'https://finance.yahoo.com/quote/{}/financials?p={}'
    base_url_profile = 'https://finance.yahoo.com/quote/{}/profile?p={}'
    base_url_keystats = 'https://finance.yahoo.com/quote/{}/key-statistics?p={}'

    # ticker_code = 'IAA'         # later get a dialog box to ask for the code
    # ticker_code = 'GM'         # later get a dialog box to ask for the code
    loadfile = 'loadfile.csv'
    outputdir = '/Users/johncyclist22/Documents/Data/stock_analysis/'+processdate+'/'
    CHECK_FOLDER = os.path.isdir(outputdir)
    if not CHECK_FOLDER:
        os.makedirs(outputdir)
    
    # load input file into dfprocess
    dfprocess = read_csv(loadfile)
    dfkeymeasures = pd.DataFrame()

    # loop here thru each record in dfprocess
    for index, stock in dfprocess.iterrows():

        dfannincome = pd.DataFrame()
        dfannbalancesheet = pd.DataFrame()
        dfanncashflow = pd.DataFrame()
        dfkeystats = pd.DataFrame()
        dfannincome, dfannbalancesheet, dfanncashflow, err = processcompanystatements(base_url,stock.ticker_code)
        if err: continue
        dfprofile = processcompanyprofile(base_url_profile, stock.ticker_code)
        dfkeystats = processcompanykeystats(base_url_keystats, stock.ticker_code)
        dfkeystats = computekeymeasurements(dfkeystats, dfannincome, dfannbalancesheet, dfanncashflow, stock.ticker_code)
        print('Company Report for -> ', stock.ticker_code)
        dfcompanyreport = createreport(dfkeystats, dfannincome, dfannbalancesheet, dfanncashflow)

        outputfile = 'fin_statements-' + stock.ticker_code + '-' + processdate + '.xls'

        with pd.ExcelWriter(outputdir+outputfile) as writer:
            dfcompanyreport.to_excel(writer, sheet_name='Company Report')
            dfannincome.to_excel(writer, sheet_name='Annual Income')
            dfannbalancesheet.to_excel(writer, sheet_name='Balance Sheet')
            dfanncashflow.to_excel(writer, sheet_name='Cash Flow')
            dfprofile.to_excel(writer, sheet_name='Profile')
            dfkeystats.to_excel(writer, sheet_name='Key Statistics')

        dfkeymeasures = dfkeymeasures.append(dfkeystats)
    
    outputdbf = 'fin_statements-All-Tickers-' + processdate + '.xls'
    with pd.ExcelWriter(outputdir+outputdbf) as writer:
        dfkeymeasures.to_excel(writer, sheet_name='Company Database')
    
main()
