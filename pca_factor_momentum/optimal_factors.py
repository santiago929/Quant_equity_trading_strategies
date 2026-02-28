# -*- coding: utf-8 -*-
"""
Created on Mon Jun  9 17:40:27 2025

@author: sgarcia
"""

import numpy as np
import pandas as pd
from scipy.sparse.linalg import eigs as sparse_eig
import optuna
from functools import partial


def get_pnl_of_mean_reversion(daily_rtns, lookback, num_pc, num_days_reversal):
    """
    Parameters
    ----------
    daily_rtns : np.array
        pct returns.
    lookback : int, optional
        The default is 252.
    num_pc : int, optional
        The default is 10.
    num_days_reversal : int, optional
        The default is 1.

    Returns
    -------
    rolling_pnl : np.array
    rolling_pnl_1d_lag : np.array
    weights_hist : np.array
    """
    
    rolling_pnl = np.zeros(
        shape = (daily_rtns.shape[0], num_pc),
        dtype=float
    )
    rolling_pnl_1d_lag = np.zeros(
        shape = (daily_rtns.shape[0], num_pc),
        dtype = float
    )
    
    weights_hist = {}
    for i in range(lookback, daily_rtns.shape[0] -1):
        backtest_returns = daily_rtns[(i-lookback):i, : ]
        cov_returns = np.cov(backtest_returns.T, ddof = 1)
        eig_vals, eig_vecs = sparse_eig(cov_returns, num_pc)
        
        eig_vals = np.real(eig_vals)
        
        sort_idx = eig_vals.argsort()[::-1]
        eig_vals = eig_vals[sort_idx]
        eig_vecs = np.real(eig_vecs[: , sort_idx])
        
        factor_loadings = np.dot(backtest_returns, eig_vecs)
        for j in range(num_pc):
            ret_explained_stocks = factor_loadings[:, :j].dot(eig_vecs[:, :j].T)
            residuals = backtest_returns - ret_explained_stocks
            
            w = -(residuals[-num_days_reversal:, :].sum(axis=0))
            w = np.sign(w - np.median(w))
            
            w[w>0] = w[w>0] / w[w>0].sum()
            w[w<0] = -w[w<0] / w[w<0].sum()
            weights_hist[i] = w
            
            rolling_pnl[i, j] = (w * daily_rtns[i, :]).sum()
            rolling_pnl_1d_lag[i+1, j] = (w * daily_rtns[i+1, :]).sum()
    
    rolling_pnl = rolling_pnl[lookback:, :]
    rolling_pnl_1d_lag = rolling_pnl_1d_lag[lookback:, :]
    
    return rolling_pnl, rolling_pnl_1d_lag, weights_hist


def standardize_results(df_ret, rolling_pnl, lookback = 252):
    
    pnl_df = pd.DataFrame(rolling_pnl, index = df_ret.iloc[lookback:, :].index)
    
    cum_pnl_standardized = (
        pnl_df.divide(pnl_df.std(axis=0) * np.sqrt(252)).cumsum(axis=0)
        )
    cum_pnl_standardized.columns.name = 'Number of factors'
    cum_pnl = pnl_df.cumsum(axis=0)
    
    return cum_pnl, cum_pnl_standardized


def strategy_wrapper(df_ret, lookback=252, num_days_reversal=1, num_pc = 5):
    
    results = {}
    
    rolling_pnl, rolling_pnl_1d_lag, _ = get_pnl_of_mean_reversion(
        daily_rtns= df_ret.values,
        lookback = lookback,
        num_pc = num_pc,
        num_days_reversal=num_days_reversal
    )
    cum_pnl, cum_pnl_standardized = standardize_results(
        df_ret,
        rolling_pnl,
        lookback
    )
    cum_pnl_1d_lag, cum_pnl_standardized_1d_lag = standardize_results(
        df_ret,
        rolling_pnl_1d_lag,
        lookback
    )
    
    results[f'cum_pnl_{num_days_reversal}'] = cum_pnl
    results[f'cum_pnl_standardized_{num_days_reversal}'] = cum_pnl_standardized
    results[f'cum_pnl_1d_lag_{num_days_reversal}'] = cum_pnl_1d_lag
    results[f'cum_pnl_standardized_1d_lag_{num_days_reversal}'] = cum_pnl_standardized_1d_lag
    results[f'rolling_pnl_{num_days_reversal}'] = rolling_pnl
    results[f'rolling_pnl_1d_lag_{num_days_reversal}'] = rolling_pnl_1d_lag
  
    return results


def get_sharpe_ratio(array, rf = 0):

    num_pc = array.shape[1]
    sharpe_ratios = np.zeros(
        shape = (1, num_pc),
        dtype = float
    )
    for i in range(0, num_pc):
        sharpe_ratios[0,i] = (array[:,i].mean() - rf) / array[:,i].std() * np.sqrt(252)
    
    return sharpe_ratios


def optimize_strategy(trial, returns_df, p1_range, p2_range, num_pc, rf=0):
    
    p1 = trial.suggest_int('lookback', p1_range[0], p1_range[1])
    p2 = trial.suggest_int('days_reversal', p2_range[0], p2_range[1])
    
    result = strategy_wrapper(returns_df, 
                              lookback=int(p1), 
                              num_days_reversal= int(p2),
                              num_pc = num_pc
    )
    
    arr = result[f'rolling_pnl_{p2}']
    
    sharpe = get_sharpe_ratio(arr).mean()
    
    return -sharpe
        
    
     
if __name__ == '__main__':
    
    #Define the pandas DataFrame containing the Index members' historical prices.
    df = pd.read_hdf(("dow_members_data.h5")).pct_change().fillna(0)
    
    study = optuna.create_study()
    study.optimize(
        partial(
            optimize_strategy, 
            returns_df = df, 
            p1_range = (126, 252), 
            p2_range = (1, 30),
            num_pc = 10
        ), 
        n_trials=5
    )
    
    optimal_params = study.best_params
    
    #TEST THE STRATEGY BASED ON THE optimal_params.
    #Note that num_pc can be adjusted once the first test is done,
    #so we can disregard the number of factors that provide the lower Sharpe Ratio. 
    
    results = {}
    day_reversals = [25]
    for d in day_reversals:
        results[f'{d}-days'] = strategy_wrapper(
            df_ret=df.copy(), 
            lookback=134, 
            num_pc = 10,
            num_days_reversal=d
        )
        
        plot = results[f'{d}-days'][f'cum_pnl_{d}'].plot(title = f'Cumulative P&L of {d}-day'
                                                         ).legend(bbox_to_anchor=(1.0, 1.0))
        plot = results[f'{d}-days'][f'cum_pnl_1d_lag_{d}'].plot(title = f'Cumulative P&L of {d}-day with lag'
                                                                ).legend(bbox_to_anchor=(1.0, 1.0))    




            
            
            
    