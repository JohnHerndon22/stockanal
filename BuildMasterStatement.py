# BuildMasterStatement.py
# Used to comb through a series of company and grab every possible income, cashflow, and balance sheet item - and park in a template

import pandas as pd
from common import *
import json
import re
import requests

def getelements(var):
    
    # df = pd.DataFrame(columns=['elements'])
    allElements = []

    for year in var:
        for element in list(year):
            allElements.append(element)
        
        df = pd.DataFrame(allElements, columns=['element'])
        return df
        
    return False

def getcompanyelements(ticker):

    url = 'https://finance.yahoo.com/quote/{}/financials?p={}'
    
    print('Processing Ticker: ' + ticker)

    dfannincome = pd.DataFrame()
    dfannbalancesheet = pd.DataFrame()
    dfanncashflow = pd.DataFrame()
    
    r = requests.get(url.format(ticker, ticker), verify=False) 

    try: 
        
        # r = requests.get(url.format(ticker, ticker), verify=False) 
    
        soup = bs(r.text, 'html.parser')
        # writevartofile(soup, 'soup.txt')
        pattern = re.compile(r'\s--\sData\s--\s')
        json_script = soup.find('script', text=pattern).contents[0]
        start = json_script.find('context')-2
        json_data = json.loads(json_script[start:-12])
        
        ann_income_statement = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["incomeStatementHistory"]["incomeStatementHistory"]
        ann_balance_sheet = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["balanceSheetHistory"]["balanceSheetStatements"]
        ann_cash_flow = json_data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["cashflowStatementHistory"]["cashflowStatements"]
        
    except:
        print('No elements found.....')
        return dfannincome, dfannbalancesheet, dfanncashflow
    
    dfannincome = getelements(ann_income_statement)
    print(str(len(dfannincome.index)) + ' elements found...')
    dfannbalancesheet = getelements(ann_balance_sheet)
    dfanncashflow = getelements(ann_cash_flow)
    
    return dfannincome, dfannbalancesheet, dfanncashflow

def main():

    # export PYTHONWARNINGS="ignore:Unverified HTTPS request"

    companyList = ['F','GM','JPM','KAR','IAA','AMZN','T','DIS','NFLX','BA','FB','KO','JNJ','VZ','PG','PSB','MA','AOS']
    dfnewMasterIncome = pd.DataFrame(columns=['element','subtype'])
    dfnewMasterCashFlow = pd.DataFrame(columns=['element','subtype'])
    dfnewMasterBalanceSheet = pd.DataFrame(columns=['element','subtype'])

    # eventually we will open from the saved sheets - to include the subtype - revenue, cost, profit (for income) but first
    dfMasterIncome = pd.DataFrame(columns=['element','subtype'])
    dfMasterIncome = dfMasterIncome.set_index('element', drop=False)
    dfMasterCashFlow = pd.DataFrame(columns=['element','subtype'])
    dfMasterBalanceSheet = pd.DataFrame(columns=['element','subtype'])

    # incomeSubTypes = ['Revenue','Costs','Profit']
    # cashflowSubTypes = ['Operating','Financing','Investing','End']
    # balanceSubTypes = ['Assets','Liabilities','Equity']

    incomeFoundElementCounter = 0
    cashflowFoundElementCounter = 0
    balanceFoundElementCounter = 0

    # loop through company list 
    for company in companyList:
        # for each company - download income, cashflow, and balance sheet
        dfnewMasterIncome, dfnewMasterBalanceSheet, dfnewMasterCashFlow = getcompanyelements(company)
        dfMasterIncome = dfMasterIncome.append(dfnewMasterIncome, sort=False)
        dfMasterCashFlow = dfMasterCashFlow.append(dfnewMasterCashFlow, sort=False)
        dfMasterBalanceSheet = dfMasterBalanceSheet.append(dfnewMasterBalanceSheet, sort=False)
        
    dfMasterIncome = dfMasterIncome.drop_duplicates(subset=['element'])
    dfMasterCashFlow = dfMasterCashFlow.drop_duplicates(subset=['element'])
    dfMasterBalanceSheet = dfMasterBalanceSheet.drop_duplicates(subset=['element'])
    
    with pd.ExcelWriter('FinancialStatementsMaster-'+processdate+'.xls') as writer:
        dfMasterIncome.to_excel(writer, sheet_name='Annual Income')
        dfMasterBalanceSheet.to_excel(writer, sheet_name='Balance Sheet')
        dfMasterCashFlow.to_excel(writer, sheet_name='Cash Flow')
    
    print ('end.....')
        # income statement - loop through each element - find the element on the existing master
        # dfnewMasterIncome = dfnewMasterIncome.set_index('elements', drop=False)
        # for index_number, element_value in dfnewMasterIncome.iterrows():
        #     try:
        #         finder = dfnewMasterIncome.loc[element_value]
        #     except:
        #         dfMasterIncome['elements'] = element_value
        #         print(dfMasterIncome)
        #     # if not found - add the element - leave the subtype as 'TBD'

        # balance sheet - loop through each element - find the element on the existing master
        # if not found - add the element - leave the subtype as 'TBD'

        # cashflow statement - loop through each element - find the element on the existing master
        # if not found - add the element - leave the subtype as 'TBD' - increase count for new element found

        # save the new master data frames to a new file

main()

    # grab all of the elements

