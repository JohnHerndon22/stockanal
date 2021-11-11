#Batter_Analysis.py

#backup to analplayerdf.py
#analyze a batter's performance thru time - evaluate current value
#v23 - account for dates already inthe YYYY-MM-DD date format
#v24
#v25 - abandon v24 convert to object oriented
#v26 - get the sorting right - still not doing string YYYY-MM-DD correctly
#v27 - prep for movement into web function
#v28 bring back for 2021 season
#determnine max for each date and use for percentile
#break down performce by catagory 
#modules new modules
import sqlite3
import os
from os import path
import sys
from datetime import *
from datetime import datetime
import csv
import codecs
from decimal import *
from shutil import copyfile
from statistics import *
from common import *
import pandas
import PySimpleGUI as sg

def get_team(espnid):

    dfdemos = pd.DataFrame(columns=['espnid','lastname','team'])
    b_c.execute("SELECT espnid, lastname, mlb_short_team FROM espn_rosters WHERE espnid = ?", (espnid,))
    demos = b_c.fetchall()
    if len(demos) == 0:
        print("Player: " + espnid + " not recognized....program ending.....")
        quit()
    else:
        # dfdemos = dfdemos.append(demos)
        dfdemos.loc[len(dfdemos)] = demos[0]
        # dfdemos['espnid'] = demos[0][0]
        # dfdemos['lastname'] = demos[0][1]
        # dfdemos['team'] = demos[0][2] 
        
    print("Analyzing: ")
    print(dfdemos.to_string(index=False))
    # print("Records to process for: " + lastname.strip() + "    " + team.strip()) 
                    
    return dfdemos

def get_performance_records(espnid):
    b_c.execute("SELECT espnid, processdate, avg, onBasePct, overall_order, totals_order, eff_order, homeRuns, RBIs FROM espn_batter_season_to_date WHERE espnid = ? ORDER BY processdate ASC", (espnid,))
    perf = b_c.fetchall()
    dfperf = pd.DataFrame(columns=['espnid','processdate','avg','OBS','overall_order', 'totals_order', 'eff_order' ,'homeRuns','RBIs'])

    for record in perf:
        record=list(record)
        dfperf.loc[len(dfperf)] = record

    return dfperf

#Main module
#clear the screen
os.system("clear")

batterconn = sqlite3.connect(dbf_directory+playerdbf)
b_c = batterconn.cursor()

while True:      

    # get the arguments
    # espnid = str(sys.argv[1])
    espnid = ask_which_espnid('Batter Analysis')
    # espnid = "31265"          # testing
    # espnid = '36185'
    dfdemos = get_team(espnid) 
    dfperf = get_performance_records(espnid)
    dfperf = dfperf.sort_values(by=['processdate'],ascending=False)
    dfperf = dfperf.round(decimals=3)
    header_list = dfperf.columns.tolist()
    data = dfperf.values.tolist()
    
    # yes its procedural - determine average scores
    b_c.execute("SELECT espnid, overall_order, eff_order, totals_order,onBasePct,RBIs,WARBR,atBats,avg,doubles,hits,homeRuns,onBasePct,runs,slugAvg,stolenBases,strikeouts, triples FROM espn_batter_season_to_date WHERE espnid = ? ORDER BY date(processdate) DESC", (espnid,))
    records = b_c.fetchall()

    dfplayerstats = pd.DataFrame()
    dictplayerstats = {'espnid':'', 'overall_order':0, 'eff_order':0, 'totals_order':0, 'OBS':.000, 'RBIs':0, 'WARBR':.000, 'atBats':0, 'avg':.000, 'doubles':0, 'hits':0, 'homeRuns':0, 'onBasePct':.000, 'runs':0, 'slugAvg':.000, 'stolenBases':0, 'strikeouts':0, 'triples':0, 'totals_order':0, 'eff_order':0,'overall_order':0}

    for record in records:
        dictplayerstats['atBats']=record[7]
        dictplayerstats['runs']=record[13]
        dictplayerstats['hits']=record[10]
        dictplayerstats['doubles']=record[9]
        dictplayerstats['triples']=record[17]
        dictplayerstats['homeRuns']=record[11]
        dictplayerstats['RBIs']=record[5]
        dictplayerstats['stolenBases']=record[15]     
        dictplayerstats['avg']=record[8]
        dictplayerstats['OBS']=record[12]
        dictplayerstats['totals_order']=record[3]     
        dictplayerstats['eff_order']=record[2]
        dictplayerstats['overall_order']=record[1]
        dfplayerstats = dfplayerstats.append(dictplayerstats, ignore_index=True)    
        
    std_dev = dfplayerstats.std()
    mean = dfplayerstats.mean()
    lastname = dfdemos.lastname[0]
    team = dfdemos.team[0]
    espnid = str(dfdemos.espnid[0])

    sg.theme('BrightColors')

    layout = [      
        [sg.Text('ESPNID: ' + espnid + '  Player: ' + lastname + '   MLB Team: ' + team, size=(80, 2),font='Helvetica 18')],      
        [sg.Table(values=data,
                    headings=header_list,
                    display_row_numbers=False,
                    font='Helvetica 14',
                    auto_size_columns=False,
                    num_rows=min(10, len(data)))],
        [sg.Text('Avg of Overall Order->  '+ str(round(mean['overall_order'],2)),size=(40, 1),font='Helvetica 14')],
        [sg.Text('Std_Dev of Overall order-> ' + str(round(std_dev['overall_order'],2)),size=(40, 1),font='Helvetica 14')],
        [sg.Text('Avg of Totals Order->  '+ str(round(mean['totals_order'],2)),size=(40, 1),font='Helvetica 14')],
        [sg.Text('Std_Dev of Totals Order-> ' + str(round(std_dev['totals_order'],2)),size=(40, 1),font='Helvetica 14')],
        [sg.Text('Avg of Eff Order->  '+ str(round(mean['eff_order'],2)),size=(40, 1),font='Helvetica 14')],
        [sg.Text('Std_Dev of Eff Order-> ' + str(round(std_dev['eff_order'],2)),size=(40, 1),font='Helvetica 14')],
        [sg.Text('Avg of Avg->  '+ str(round(mean['avg'],3)),size=(40, 1),font='Helvetica 14')],
        [sg.Text('Std_Dev of Avg-> ' + str(round(std_dev['avg'],2)),size=(40, 1),font='Helvetica 14')],
        [sg.Text('Avg of OBS-> ' + str(round(mean['OBS'],3)),size=(40, 1),font='Helvetica 14')],
        [sg.Text('Std_Dev of OBS-> '+ str(round(std_dev['OBS'],2)),size=(40, 1),font='Helvetica 14')],
        [sg.Button('New ID',font='Helvetica 14'), sg.Button('QUIT',font='Helvetica 14')]]      


    window = sg.Window('Batter Analysis', layout)   

    (event, value) = window.Read()   
    
    if event == 'QUIT'  or event is None:      
        break # exit button clicked
    elif event == 'New ID':
        continue   # will be continue later      
    else:
        break    # exit X hit


print('\n'+'Analysis Concluded.....')

