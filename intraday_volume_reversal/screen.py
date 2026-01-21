# -*- coding: utf-8 -*-
"""
Created on Thu Jun 26 16:14:45 2025

@author: sgarcia
"""

import pandas as pd
import time
from datetime import datetime as dt
from Bloomberg_fetch.BB_utils_HFT import get_realtime_volume

#Working directory. 
path = 'C:/Users/sgarcia/OneDrive - LFS/SyncFiles/BACKTESTING/TTP/volume_reversal_strategy'
#Today's date
today = time.strftime('%Y%m%d')
#The code stops running at this local machine time. 
end_time = dt.strptime('21:30:00', '%H:%M:%S').time() #The code stops running at this local machine time. 


def screen_volume(df, threshold= 200_000):
    """
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing the current volume of the shares.
    threshold : integer, optional
        Just screen shares whose volume has reached x level during the session. 
        The default is 200_000.

    Returns
    -------
    pandas.Series
        Series of shares that meet the volume threshold.
    """
    
    return df[df["Volume"] > threshold]['Ticker']

def run_screen(tickers, t_minutes):
    """
    Parameters
    ----------
    tickers : list
    
    t_minutes : integer
        Refresh every t_minutes.

    Returns
    -------
    pandas.Series

    """
    
    global path, today, end_time
    filter_ = set()
    
    while dt.now().time() <= end_time:    
        df = get_realtime_volume(tickers, 'US', 'Equity')
        result = screen_volume(df)
        new_entries = [t for t in result if t not in filter_]
        if new_entries:
            filter_.update(new_entries)
            
            store_df = pd.DataFrame({'Time': time.strftime('%Y-%m-%d %H:%M:%S'), 
                                     'Ticker': list(filter_)})
            
            store_df.to_csv(path+f'/volume_filter_{today}.csv')
            print(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')} - {len(result)} tickers passed:\n", result)
        
        time.sleep(t_minutes * 60)

    
if __name__ == '__main__':
    stocks = pd.read_excel(path+'/market_screener.xlsx')
    stocks['EXPECTED_REPORT_DT'] = pd.to_datetime(stocks['EXPECTED_REPORT_DT'], dayfirst=True)
    stocks['DVD_EX_DT'] = pd.to_datetime(stocks['DVD_EX_DT'], dayfirst=True)
    stocks_ = stocks.loc[(stocks['EXPECTED_REPORT_DT'] - dt.today() > pd.Timedelta(5, 'D')) &  
                         (stocks['DVD_EX_DT'] - dt.today() > pd.Timedelta(5, 'D')) &
                         ((stocks['VOLATILITY_30D'] > 50) & (stocks['VOLATILITY_30D'] < 100)) &
                         (stocks['VOLUME_AVG_5D'] > 3000000) &
                         (stocks['yest_close'] > 2.0) &
                         (stocks['HALT'] == False)
                         ]
    run_screen(stocks_.ticker.values, t_minutes=5)
    
    