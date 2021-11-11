#processpricehistory.py


from numpy.core.fromnumeric import mean
from pandas.io.parsers import read_csv
import requests
# from bs4 import BeautifulSoup as bs, MarkupResemblesLocatorWarning 
import pandas as pd
import xlsxwriter
import time
from io import StringIO
from common import *
import xlwt
import os
import talib as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
# import plotly.express as px
import PySimpleGUI as sg
from hurst import compute_Hc, random_walk


# price averages 
# 5 day
# 8 day
# 13 day
# 34 day

def fractal_up_test(high_price_test, dfprices, index):

    if index < 2 or index > len(dfprices.index)-2:
        return False
    else:
        if dfprices['High'].iloc[index-2] < dfprices['High'].iloc[index-1] and dfprices['High'].iloc[index-1] < high_price_test and high_price_test > dfprices['High'].iloc[index+1] and dfprices['High'].iloc[index+1] > dfprices['High'].iloc[index+2]:
            return True
        else:
            return False
    return False

def fractal_low_test(low_price_test):

    if index < 2 or index > len(dfprices.index)-2:
        return False
    else:
        if dfprices['Low'].iloc[index-2] > dfprices['Low'].iloc[index-1] and dfprices['Low'].iloc[index-1] > low_price_test and low_price_test < dfprices['Low'].iloc[index+1] and dfprices['Low'].iloc[index+1] < dfprices['Low'].iloc[index+2]:
            return True
        else:
            return False
    return False
# def assign_ticket_survival_rate(ticket, dfticketsurvival):
#     # for the test & train data - pull and assign the actual survival rate
#     try: 
#         rate = dfticketsurvival.loc[ticket,'survivalRate']
#     except:
#         rate = .35
#     return rate

def main():

    start_index = 860
    end_index = start_index+120
    config = dict({'scrollZoom': False})
    
    dfprices = read_csv('SSO_price.csv')
    # dfprices = dfprices[500:1000].reset_index()
    dfprices['sma5'] = ta.SMA(dfprices['Close'],5)
    dfprices['sma9'] = ta.SMA(dfprices['Close'],9)
    dfprices['sma13'] = ta.SMA(dfprices['Close'],13)
    dfprices['sma34'] = ta.SMA(dfprices['Close'],34)
    dfprices['po'] = dfprices['sma34'] - dfprices['sma5']
    dfprices['hurst'] = 0
    dfprices['c'] = 0
    # train_data['female_uc'] = train_data.apply(lambda x: female_upper_crust(x['Pclass'], x['Nsex']), axis=1)    
    # dfprices['up_test'] = dfprices.apply(lambda x: fractal_up_test(x['High'], dfprices, x.index), axis=1)
    # train_data['T_survivalRate'] = train_data.apply(lambda x: assign_ticket_survival_rate(x['Ticket'], dfticketsurvival), axis=1)

    # H, c, data = compute_Hc(series, kind='price', simplified=True)
    for counter, price in dfprices.iterrows():

        if counter > 199:
            series = dfprices['Close'][counter-200:counter]
            H, c, data = compute_Hc(series, kind='price', simplified=True)
            dfprices.loc[counter,'hurst'] = H
            dfprices.loc[counter,'c'] = c
    
    
    
    # print(dfprices)

    # .iloc[start_index:end_index],

    # data['120EMA'] = ta.EMA(data['close'], 120)
    # fig = go.Figure(data=[])
    start_index = 200
    while(start_index< 250):
    # (len(dfprices.index)-180)):

        # start_index = 200    # 500            # use 500 on full data set
        end_index = start_index+181

        # fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
        # ,specs=[[{"secondary_y": True}]])
            # # chart_data = go.Candlestick(x=dfprices['Date'].iloc[start_index+1:end_index],
            #                 open=dfprices['Open'].iloc[start_index+1:end_index],
            #                 high=dfprices['High'].iloc[start_index+1:end_index],
            #                 low=dfprices['Low'].iloc[start_index+1:end_index],
            #                 close=dfprices['Close'].iloc[start_index+1:end_index])
        fig.add_trace(go.Candlestick(x=dfprices['Date'].iloc[start_index+1:end_index],
                        open=dfprices['Open'].iloc[start_index+1:end_index],
                        high=dfprices['High'].iloc[start_index+1:end_index],
                        low=dfprices['Low'].iloc[start_index+1:end_index],
                        close=dfprices['Close'].iloc[start_index+1:end_index], name='Candlestick'), row=1, col=1)
        
        fig.update_layout(xaxis_rangeslider_visible=False)
        
        # fig = px.line(df, x="year", y="lifeExp", title='Life expectancy in Canada')
        # ema_trace = go.Scatter(x=dfprices['Date'].iloc[start_index+1:end_index], y=dfprices['sma34'].iloc[start_index+1:end_index], mode='lines', name='34SMA')
        # ema_trace2 = go.Scatter(x=dfprices['Date'].iloc[start_index+1:end_index], y=dfprices['sma5'].iloc[start_index+1:end_index], mode='lines', name='5SMA')
        fig.add_trace(go.Scatter(x=dfprices['Date'].iloc[start_index+1:end_index], y=dfprices['sma34'].iloc[start_index+1:end_index], mode='lines', name='34SMA'),row=1,col=1)
        fig.add_trace(go.Scatter(x=dfprices['Date'].iloc[start_index+1:end_index], y=dfprices['sma5'].iloc[start_index+1:end_index], mode='lines', name='5SMA'),row=1,col=1)
        
        # hurst=dfprices['hurst'].iloc[start_index+1:end_index]    
        fig.add_trace(go.Scatter(x=dfprices['Date'].iloc[start_index+1:end_index], y=dfprices['hurst'].iloc[start_index+1:end_index], name='hurst', mode='lines'),row=2,col=1)

        # Add figure title
        fig.update_layout(
            width=1300,
            height=800,
            title_text="SSO Prices",
            yaxis_tickformat='M'
        )

        # Add figure title
        # fig.update_layout(
        #     width=1300,
        #     height=100,
        #     yaxis_tickformat='M',
        #     row=2,
        #     col=1
        # )

        # Set x-axis title
        # fig.update_xaxes(title_text="Date")

        fig.update_layout(legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ))



        # Set y-axes titles
        fig.update_yaxes(title_text="<b>primary</b> Close", secondary_y=False, row=1)
        fig.update_yaxes(title_text="<b>secondary</b> Hurst", range=[0, 1], secondary_y=False,row=2)


        fig.show()
        start_index+=180
        
        # fig.write_image('sso_barchart.png')
        # response = int(input("(1) End or (2) Continue....."))
        # if response == 1: break

main()
