Disclaimer.

The intraday volume reversal strategy is just intended to suggest a basic strategy that could be applied to feed the signals in main.py. Feel free to use
your own quantitative strategies and modify the code as you wish. While the strategy suggested here has been applied in some prop trading firms challenges, 
it is important to acknowledge that it is intended for educational and reference purposes only. 

Personal Use: You are welcome to study, modify, and utilize this code for personal learning or academic purposes. 
No Guarantee: While efforts have been made to ensure the accuracy and reliability of the code provided, there is no guarantee that it will be error-free or 
suitable for your specific requirements. You are encouraged to test and validate any code before using it in a production environment or for critical tasks.

Introduction.

We provide a set of codes that deliver a systematic approach to trade on retail brokerage platforms
that do not offer an API scheme. Ideally, we need a data provider where we can pull intraday data,
namely Interactive Brokers or Bloomberg Terminal. We also combine different methods to store data, and the preferences
are more directed to ease of use and storage capacity. Therefore, we make us of Excel files and a PostgreSQL database on Railway, wich is a DB
host that offers:

-Free public access.
-No VM or Docker setup.
-Instant remote access with pgAdmin and Python.
-Fully cloud-hosted DB. 


screen.py

Modify the path and end_time variables as you which, then run the following function:

run_screen(tickers, t_minutes):
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


main.py

Run from a different command prompt. 

This code calls both screen.py and the volume_reversal_strategy which are provided in this repository.

Although I'm ussing both Bloomberg and IBKR to retrieve data for demonstration, you can change the code and use your preffered data provider. 

I'm providing the Excel files for demonstration only. Despite being optional, they can help to have a granular overview of the process. If you opt 
to comment them out, just make sure to provide a structure for open_tickers (To avoid duplicated trades and help with the closing signal), 
and tickers. 

market_screener.xlsx
Prompts related to equities can be retrieve with the following formula as an example:
=BQL(CONCAT(ticker," US"," Equity"),"expected_report_dt")

=BQL(CONCAT(ticker," US"," Equity"), "volatility(calc_interval=range(-30D, TODAY(), frq=D), mode=REALTIME)")


TIME_DATE_LST_TRAD_SUSPENSION -> date	
HALT -> bool (As one of the conditions of the prop trading challenge is not to trade stocks halted in the previous x minutes)









