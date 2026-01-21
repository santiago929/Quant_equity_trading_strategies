# -*- coding: utf-8 -*-
"""
Created on Fri Jun 27 15:19:36 2025

@author: sgarcia
"""

import pandas as pd
import time
from screen import path, today, end_time
from volume_reversal_strategy import strategy_implementation
from datetime import datetime, date, timedelta
from Bloomberg_fetch.BB_utils_HFT import req_underlying_data
from IBKR_fetch.IB_request_historical_data import websocket_con, usTechStk, histData
from tabulate import tabulate

from Railway.railway_connect import conn_low_vol_vol_reversal, engine_low_vol_vol_reversal


def get_next_minute():
    now = datetime.now()
    return (now + timedelta(minutes=5)).replace(second=0, microsecond=0)


def main(lag = 10, T = 40):

    close = []  
    invalid_tickers = [] 
    data_ = {} 
    prices = {}
    #Connect to the Interactive Brokers' server.
    app = websocket_con()
    
    ID_COUNT = 0
    
    next_run = datetime.now()
    
    while datetime.now().time() <= end_time: 
        
        now = datetime.now() 
        
        if now >= next_run: 
            
            next_run = get_next_minute()
            #Optional codes. Freel free to comment out the next five lines, just make sure to provide a list of tickers. 
            #volume_filter_.csv file is obtained from the screen.py code. 
            _filter_df = pd.read_csv(path+f'/volume_filter_{today}.csv')
            #Optional positions.xlsx file to track positions and calculate PnL. 
            _book_df = pd.read_excel(path+'/positions.xlsx')
            #Optional open_tickers to avoid duplicate trades on the same ticker. 
            open_tickers = (_book_df.loc[_book_df['status'] == 'open',['ticker']].values)[:,0].tolist()
            filter_tickers = (_filter_df['Ticker'].values).tolist()
            tickers = list(set(dict.fromkeys(open_tickers+ filter_tickers)))
            
            #Connect to Railway(PostgreSQL) database
            cur = conn_low_vol_vol_reversal.cursor()
            
            cur.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_type = 'BASE TABLE';
            """)
            
            buys = []
            sells = []
            tables = [row[0] for row in cur.fetchall()]
           
            for t in tickers:
                #We provide two ways to obtain historical data, depending on the data provider of preference.
                #Both IBKR and Bloomberg should provide the same results, although the later is faster.
                if t in tables:
                    prices[t] = histData(app, ID_COUNT, usTechStk(t),'1 D','5 mins')
                else:
                    print(f"{t} is a new ticker. Adding new data_ into the Database" )
                    prices[t] = req_underlying_data([t], 'US', 'Equity', start_date = '20250822', 
                                                    end_date = (date.today() + timedelta(days=1)).strftime('%Y%m%d'), 
                                                    interval = 5)[t]  
                    prices[t].to_sql(f"{t}", engine_low_vol_vol_reversal, index=True)
                    
                data_[t] = pd.read_sql(f'SELECT * FROM "{t}"', con = engine_low_vol_vol_reversal, 
                                    parse_dates = True, index_col= 'date')
                data_[t] = pd.concat([data_[t], prices[t].loc[prices[t].volume > 0]])
                data_[t] = (data_[t][~data_[t].index.duplicated(keep='last')]).sort_index()
                ID_COUNT += 1
                
            for t in tickers: 
                if len(data_[t]) > 0:
                    data_[t] = strategy_implementation(data_[t], lag, T)
                        
                    _df = data_[t].loc[data_[t].index.date == date.today()]
                    
                    if t not in open_tickers:
                
                        if any(_df['signal'] > 0) and t not in buys:
                            buys.append(t)
                             
                        elif any(_df['signal'] < 0) and t not in sells:
                            sells.append(t)
                           
                        else:
                            continue
                    else:
                        
                        if _df.loc[_df.index[-1], 'exit'] == True and t not in close:
                            close.append(t) 
                            
                        else: 
                            continue
                else:
                    invalid_tickers.append(t)
                    
            print(tabulate([[f'Buys ({len(buys)})', buys], 
                            [f'Sell ({len(sells)})', sells], 
                            ['Close', close]]))
            #Optional txt file to track signals when offsite.
            #For instance, I can check the file from my smarthphone should the txt file is saved in the clud. 
            file1 = open('CLOSE_POSITIONS.txt', 'w')
            file1.writelines(close)
            file1.close()
            
            print(f"Code executed at {time.strftime('%Y-%m-%d %H:%M:%S')}")
            
    
        time.sleep(0.1) 
    
    else:
        #At the end of the day, store today's data in the Database.
        for t in set(dict.fromkeys(open_tickers + filter_tickers)): 
            try:
                data_[t].loc[data_[t].index.date == date.today()].to_sql(f"{t}", engine_low_vol_vol_reversal, 
                                                                     if_exists = 'append', index=True)
            except:
                print(f"{t} is a new ticker. Replacing new data_ into the Database" )
            finally:
                data_[t].to_sql(f"{t}", engine_low_vol_vol_reversal, if_exists = 'replace', index=True)
    
    
 
if __name__ == "__main__":
    main()
    
        
        
        
