#common.py

from datetime import datetime 
import pandas as pd
import json
import re
import requests
from bs4 import BeautifulSoup as bs 
import xlsxwriter
import time
from io import StringIO
from common import *
import xlwt


# dynamic file storage variables
today = datetime.today()
processdate = str(today.year) + "-" + str(today.month).zfill(2) + "-" + str(today.day).zfill(2)

def processcompanyprofile(url, ticker):

    # need to restructure to get description
    dfprofile=pd.DataFrame(columns=['profile_data'])
    profiledict = {}

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' } 
    r = requests.get(url.format(ticker, ticker), verify=False, headers=headers) 
    
    soup = bs(r.text, 'html.parser')
    pattern = re.compile(r'\s--\sData\s--\s')
    json_script = soup.find('script', text=pattern).contents[0]
    start = json_script.find('context')-2
    json_data = json.loads(json_script[start:-12])
    
    try: 
        # secFilings = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["secFilings"]
        # summaryDetail = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["summaryDetail"]
        assetProfile = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["assetProfile"]
    except:
        print('No stats found for: ', ticker)
        return 
    
    profiledict['profile_data'] = ticker
    dfprofile = dfprofile.append(profiledict, ignore_index=True)
    
    try:
        profiledict['profile_data'] = assetProfile['website']
        dfprofile = dfprofile.append(profiledict, ignore_index=True)
        profiledict['profile_data'] = assetProfile['address1']
        dfprofile = dfprofile.append(profiledict, ignore_index=True)
        profiledict['profile_data'] = assetProfile['city']
        dfprofile = dfprofile.append(profiledict, ignore_index=True)
        profiledict['profile_data'] = assetProfile['state']
        dfprofile = dfprofile.append(profiledict, ignore_index=True)
        profiledict['profile_data'] = assetProfile['zip']
        dfprofile = dfprofile.append(profiledict, ignore_index=True)
        profiledict['profile_data'] = assetProfile['country']
        dfprofile = dfprofile.append(profiledict, ignore_index=True)
    except:
        profiledict['profile_data'] = ' '
        dfprofile = dfprofile.append(profiledict, ignore_index=True)
        profiledict['profile_data'] = ' '
        dfprofile = dfprofile.append(profiledict, ignore_index=True)
        profiledict['profile_data'] = ' '
        dfprofile = dfprofile.append(profiledict, ignore_index=True)
        profiledict['profile_data'] = ' '
        dfprofile = dfprofile.append(profiledict, ignore_index=True)
        profiledict['profile_data'] = ' '
        dfprofile = dfprofile.append(profiledict, ignore_index=True)
        profiledict['profile_data'] = ' '
        dfprofile = dfprofile.append(profiledict, ignore_index=True)
    
    try:
        profiledict['profile_data'] = assetProfile['phone']
    except:
        profiledict['profile_data'] = ' '
    
    
    dfprofile = dfprofile.append(profiledict, ignore_index=True)
    try:
        profiledict['profile_data'] = assetProfile['fullTimeEmployees']
    except:
        profiledict['profile_data'] = 0
    
    dfprofile = dfprofile.append(profiledict, ignore_index=True)
    profiledict['profile_data'] = assetProfile['longBusinessSummary']
    dfprofile = dfprofile.append(profiledict, ignore_index=True)
    # print(dfprofile)
    return dfprofile

def processcompanykeystats(url, ticker):

    dfkeystats=pd.DataFrame()
    keystatsdict = {}

    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' } 
    r = requests.get(url.format(ticker, ticker), verify=False, headers=headers) 
    
    soup = bs(r.text, 'html.parser')
    pattern = re.compile(r'\s--\sData\s--\s')
    json_script = soup.find('script', text=pattern).contents[0]
    start = json_script.find('context')-2
    json_data = json.loads(json_script[start:-12])
    
    try: 
        keyStats = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["financialData"]
        # print(json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"])
        summaryDetail = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["summaryDetail"]
    except:
        print('No stats found for: ', ticker)
        return dfkeystats
    
    try:
        keystatsdict['debtToEquity'] = keyStats['debtToEquity']['raw']
    except:
        keystatsdict['debtToEquity'] = 0

    try: keystatsdict['returnOnEquity'] = keyStats['returnOnEquity']['raw']
    except: keystatsdict['returnOnEquity'] = 0

    try:
        keystatsdict['fiveYearAvgDividendYield'] = summaryDetail['fiveYearAvgDividendYield']['raw']
    except:
        keystatsdict['fiveYearAvgDividendYield'] = 0

    try:
        keystatsdict['lastYearDividendYield'] = summaryDetail['dividendYield']['raw']*100
    except: 
        keystatsdict['lastYearDividendYield'] = 0

    dfkeystats = dfkeystats.append(keystatsdict, ignore_index=True)
    
    return dfkeystats


def convert_date(date):
    return datetime.fromtimestamp(date).strftime("%m/%d/%Y")

def processpricehistory(url, ticker):

    dfpricehistory=pd.DataFrame(columns=['date','open','close','high','low','volume','adjclose'])

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' } 
#     headers = { 
#     'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36', 
#     'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 
#     'Accept-Language' : 'en-US,en;q=0.5',
#     'DNT'             : '1', # Do Not Track Request Header 
#     'Connection'      : 'close'
# }
    r = requests.get(url.format(ticker, ticker), verify=False, headers=headers) 
    
    soup = bs(r.text, 'html.parser')
    pattern = re.compile(r'\s--\sData\s--\s')
    json_script = soup.find('script', text=pattern).contents[0]
    start = json_script.find('context')-2
    json_data = json.loads(json_script[start:-12])
    
    try: 
        # create a loist
        pricehistory = json_data["context"]["dispatcher"]["stores"]["HistoricalPriceStore"]["prices"]
        
    except:
        print('No prices found for: ', ticker)
        return dfpricehistory
    
    # convert list into dataframe
    for record in pricehistory: 
        try:
            ### need to explicitly pull the open, close, high, low, volume - leave the others - avoid the dropna
            if record['open'] > 0:          # if this errors record['open'] does not exist = dividend
                dfpricehistory = dfpricehistory.append(record, ignore_index=True)
        except:
            pass            # dividend - skip record
    
    if len(dfpricehistory.index) > 0:
        dfpricehistory['date'] = dfpricehistory.apply(lambda x: convert_date(x['date']), axis=1)
    else:
        print("ticker found not records....")

    print(dfpricehistory)
    return dfpricehistory



def writevartofile(var, sendfile):
    v = open(sendfile,"w")
    v.write(str(var))
    print("contents written to file.... ")
    return True


def ask_which_espnid(title):

    espnid = '' 
    layout = [[sg.Text('Which ESPNID to Process?',font='Helvetica 14')],      
                 [sg.InputText(font='Helvetica 14')],      
                 [sg.Submit(font='Helvetica 14'), sg.Cancel(font='Helvetica 14')]]            
    window = sg.Window('Starting Pitcher Analysis', layout)            
    event, values = window.Read()    
    window.Close()        
    return values[0]    

def processcompanystatements(url, ticker):

    dfannincome = pd.DataFrame()
    dfannbalancesheet = pd.DataFrame()
    dfanncashflow = pd.DataFrame()
    err = False
    
    # in order to tell Yahoo finance that we are not a bot even though we are a bot
    headers = { 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36' } 

    for attempt in range(50):
    
        r = requests.get(url.format(ticker, ticker), verify=False, headers=headers) 
        
        soup = bs(r.text, 'html.parser')
        pattern = re.compile(r'\s--\sData\s--\s')
        try:
            json_script = soup.find('script', text=pattern).contents[0]
            start = json_script.find('context')-2
            json_data = json.loads(json_script[start:-12])
            break
        except:
            print('failed.... '+str(attempt))
            continue

    try: 
        ann_income_statement = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["incomeStatementHistory"]["incomeStatementHistory"]
        ann_balance_sheet = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["balanceSheetHistory"]["balanceSheetStatements"]
        ann_cash_flow = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["cashflowStatementHistory"]["cashflowStatements"]
    except:
        print('No stats found for: ', ticker)
        err = True
        return dfannincome, dfannbalancesheet, dfanncashflow, err
    
    dfannincome = getstatement(ann_income_statement)
    dfannbalancesheet = getstatement(ann_balance_sheet)
    dfanncashflow = getstatement(ann_cash_flow)
    
    return dfannincome, dfannbalancesheet, dfanncashflow, err

def getstatement(var):
    
    df = pd.DataFrame()

    # need to pick off end date for the year
    # need to get basic and doluted EPS

    for year in var:
        statedict = {}
        for key, val in year.items():
            try:
                statedict[key]=val['raw']/1000000
            except TypeError:
                continue
            except KeyError:
                continue
        # print(statedict)
        df = df.append(statedict, ignore_index=True)

        # need to reorder this according to a category mapping - go out and get all of these

    return df


def createreport(dfkeystats, dfannincome, dfannbalancesheet, dfanncashflow):

    dfcompanyreport = pd.read_csv('Corporate_Report_Template.csv')
    dfcompanyreport = dfcompanyreport.set_index('dimension')
    
    dfcompanyreport.at['Debt/Equity','value'] = dfkeystats['debtToEquity']  
    dfcompanyreport.at['ROE','value'] = dfkeystats['returnOnEquity']  
    dfcompanyreport.at['Earnings Consistency stdev/average','value'] = dfkeystats['stdoveravgEarnings']  
    dfcompanyreport.at['Cash to Debt','value'] = dfkeystats['cashtoLTDebt']  
    dfcompanyreport.at['perc of SGA expenses per gross profit','value'] = dfkeystats['SGAperofGP']  
    dfcompanyreport.at['R&D / Gross Profit','value'] = dfkeystats['RDperofGP']  
    dfcompanyreport.at['gross profit margin','value'] = dfkeystats['avgGrossMargin']  
    dfcompanyreport.at['net margin','value'] = dfkeystats['avgNetMargin']
    dfcompanyreport.at['Capital Expentiture / Net Earnings','value'] = dfkeystats['capExpPerNetIncome']
    dfcompanyreport.at['Years to pay off LT Debt','value'] = dfkeystats['yearstoPayOffDebt']
    dfcompanyreport.at['Earnings Growth','value'] = dfkeystats['netIncomeGrowth']
    dfcompanyreport.at['ROE Growth','value'] = dfkeystats['ROEGrowth']
    dfcompanyreport.at['Avg Dividend 5 Years','value'] = dfkeystats['fiveYearAvgDividendYield']
    dfcompanyreport.at['Dividend Rate','value'] = dfkeystats['lastYearDividendYield']
    dfcompanyreport.at['Cashflow Annual','value'] = dfkeystats['cashFlowAnnual']
    dfcompanyreport.at['Cashflow Average','value'] = dfkeystats['cashFlowAvg']
    dfcompanyreport.at['Cashflow LY over Average','value'] = dfkeystats['debtToEquity']
    dfcompanyreport.at['Earnings','value'] = dfannincome['netIncome'][0]
    
    print(dfcompanyreport)
    
    return dfcompanyreport


def computekeymeasurements(dfkeystats, dfannincome, dfannbalancesheet, dfanncashflow, ticker):
    # function which return the data frame with the computed key measurements
    
    try:
        dfkeystats['ticker'] = ticker
    except:
        dfkeystats['ticker'] = ' '

    try:
        dfkeystats['avgEarnings'] = dfannincome['netIncome'].mean()
    except:
        dfkeystats['avgEarnings'] = 0

    try:    
        dfkeystats['stdEarnings'] = round(dfannincome['netIncome'].std(),2) 
    except: 
        dfkeystats['stdEarnings'] = 0
    try:    
        dfkeystats['stdoveravgEarnings'] = dfkeystats['stdEarnings']/dfkeystats['avgEarnings'] 
    except: 
        dfkeystats['stdoveravgEarnings'] = 0
    try:    
        dfkeystats['cashtoLTDebt'] = dfannbalancesheet['cash']/dfannbalancesheet['longTermDebt'] 
    except: 
        dfkeystats['cashtoLTDebt'] = 0
    try:    
        dfkeystats['SGAperofGP'] = dfannincome['sellingGeneralAdministrative']/dfannincome['grossProfit'] 
    except: 
        dfkeystats['SGAperofGP'] = 0
    try:    
        dfkeystats['RDperofGP'] = dfannincome['researchDevelopment']/dfannincome['grossProfit'] 
    except: 
        dfkeystats['RDperofGP'] = 0
    try:    
        dfkeystats['avgGrossMargin'] = (dfannincome['grossProfit']/dfannincome['totalRevenue']).mean() 
    except: 
        dfkeystats['avgGrossMargin'] = 0
    try:    
        dfkeystats['avgNetMargin'] = (dfannincome['netIncome']/dfannincome['totalRevenue']).mean() 
    except: 
        dfkeystats['avgNetMargin'] = 0
    try:    
        dfkeystats['avgROE'] = dfannincome['netIncome'].mean()/dfannbalancesheet['totalStockholderEquity'].mean() 
    except: 
        dfkeystats['avgROE'] = 0
    try:    
        dfkeystats['lastYearROE'] = dfannincome['netIncome'][0]/dfannbalancesheet['totalStockholderEquity'][0] 
    except: 
        dfkeystats['lastYearROE'] = 0
    try:    
        dfkeystats['yearstoPayOffDebt'] = dfannincome['netIncome'][0]/dfannbalancesheet['longTermDebt'][0] 
    except: 
        dfkeystats['yearstoPayOffDebt'] = 0
    try:    
        dfkeystats['capExpPerNetIncome'] = dfanncashflow['capitalExpenditures'][0]/dfannincome['netIncome'][0] 
    except: 
        dfkeystats['capExpPerNetIncome'] = 0
    try:    
        dfkeystats['netIncomeGrowth'] = (dfannincome['netIncome'][0] - dfannincome['netIncome'][3]) / dfannincome['netIncome'][0] 
    except: 
        dfkeystats['netIncomeGrowth'] = 0

    try:    
        dfkeystats['netIncome'] = dfannincome['netIncome'][0] 
    except: 
        dfkeystats['netIncome'] = 0
    
    # * calculate ROE for year 3 (earliest)
    try:
        dfkeystats['yr3ROE'] = dfannincome['netIncome'][3]/dfannbalancesheet['totalStockholderEquity'][3]
        dfkeystats['yr0ROE'] = dfannincome['netIncome'][0]/dfannbalancesheet['totalStockholderEquity'][0]
        
        # determine growth of ROE from past to current
        dfkeystats['ROEGrowth'] = (dfkeystats['yr0ROE'] - dfkeystats['yr3ROE']) / dfkeystats['yr0ROE']
    except:
        dfkeystats['yr3ROE'] = 0
        dfkeystats['yr0ROE'] = 0
        dfkeystats['ROEGrowth'] = 0

    try:    
        dfkeystats['cashFlowAnnual'] = dfanncashflow['changeInCash'][0] 
    except: 
        dfkeystats['cashFlowAnnual'] = 0

    try:    
        dfkeystats['cashFlowAvg'] = dfanncashflow['changeInCash'].mean()
    except: 
        dfkeystats['cashFlowAvg'] = 0

    try:    
        dfkeystats['cashFlowAboveAvg'] = dfkeystats['cashFlowAnnual'] - dfkeystats['cashFlowAvg']
    except: 
        dfkeystats['cashFlowAboveAvg'] = 0
    
    return dfkeystats
