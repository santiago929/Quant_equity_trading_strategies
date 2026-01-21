# -*- coding: utf-8 -*-
"""
Created on Thu Aug 11 17:27:30 2022

@author: Santiago

Strategy:
A signal to buy will be triggered when the absolute value of the (lag) day price change is greater than the (T) day standard deviation, 
the (lag) day average traded volume is less than the (lag) day average volume beginning 2*(lag) days prior, 
and the (lag) day price change is negative. 
We will assign a value of 1 to the column 'signal' when these conditions are met.

The sell signal is triggered when the opposite conditions happen in the price action. 
We will assign a value of -1 accordingly.

A closing signal is deployed when the model triggers an opposite signal to the open trade. 

"""

import numpy as np

def transform_df(df, lag, T):
    
    df.loc[:,'px_chg'] = df['px'].shift(1)-df['px'].shift(lag + 1)
    df.loc[:,'std'] = df['px_chg'].rolling(window= T).std()
    df.loc[:,'avg_vol'] = df['volume'].shift(1).rolling(window=lag).mean()
    df.loc[:,'past_avg_vol'] = df['avg_vol'].shift(lag)
    df.loc[:,'signal'] = 0
    
    return df


def strategy_implementation(df, lag, T, rf= 0):
    
    df = transform_df(df, lag, T)
    
    #Buy signal
    df.loc[((df['px_chg'].abs() > df['std']) & (df['avg_vol'] < df['past_avg_vol'])
              & (df['px_chg'] < 0)), 'signal'] = 1
    
    #Sell signal
    df.loc[((df['px_chg'].abs() > df['std'])
              & (df['avg_vol'] < df['past_avg_vol'])
              & (df['px_chg'] > 0)), 'signal'] = -1
    
    df['c_signal'] = np.nan
    df['exit'] = False
    
    for i in range(len(df)):
        df.loc[df.index[i], 'exit'] = False
        
        if (df.iloc[i]['signal'] != 0) & (df.iloc[i]['signal']!= df.iloc[i - 1]['c_signal']):
            df.iloc[i, df.columns.get_loc('c_signal')] = df.iloc[i,df.columns.get_loc('signal')]
            df.iloc[i, df.columns.get_loc('exit')] = True
      
        if (df['signal'].iloc[i] != 0) & (df['signal'].iloc[i] == df['c_signal'].iloc[i - 1]):
            df.iloc[i, df.columns.get_loc('c_signal')] = df['c_signal'].iloc[i - 1]
            if df['c_signal'].iloc[i - 1] == 1:
                df.iloc[i, df.columns.get_loc('exit')] = False
            else:
                df.iloc[i, df.columns.get_loc('exit')] = False
                
        if (df['signal'].iloc[i] == 0) & (df['exit'].iloc[i - 1] == False):
            df.iloc[i, df.columns.get_loc('c_signal')] = df['c_signal'].iloc[i - 1]
            df.iloc[i, df.columns.get_loc('exit')] = False
          
        if (df['signal'].iloc[i] == 0) & (df['exit'].iloc[i - 1] == True):
            df.iloc[i, df.columns.get_loc('c_signal')] = df['c_signal'].iloc[i - 1]
            df.iloc[i, df.columns.get_loc('exit')] = False

    return df
  

    


