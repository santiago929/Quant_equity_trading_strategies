## screen.py

Update the path and end_time variables as needed, then run the following function:

run_screen(tickers, t_minutes):
    
    Parameters
    ----------
    tickers : list
        List of tickers to screen.

    t_minutes : int
        Refresh interval in minutes.

    Returns
    -------
    pandas.Series

## main.py

Run this file from a separate command prompt.
This script calls both screen.py and the volume_reversal_strategy.py module included in this repository.
Although Bloomberg and IBKR are used for data retrieval in the example implementation, the code can be easily adapted to other data providers.
The included Excel files are provided for demonstration purposes only. While optional, they help maintain a granular overview of ticker selection.
If you choose to remove them, ensure that you define:

open_tickers (to prevent duplicate trades and manage exit signals), and
tickers (the universe of tradable assets).

## market_screener.xlsx
Prompts related to equities can be retrieve with the following Bloomberg Query Language line:

=BQL(CONCAT(ticker," US"," Equity"),"expected_report_dt")

=BQL(CONCAT(ticker," US"," Equity"), "volatility(calc_interval=range(-30D, TODAY(), frq=D), mode=REALTIME)")
















