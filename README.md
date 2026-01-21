# Disclaimer
__________

The intraday volume reversal strategy provided in this repository is intended solely as an example of a basic quantitative signal-generation framework. You are encouraged to implement your own strategies and modify the code as needed.

Although variations of this strategy have been used in proprietary trading firm challenges, it is provided strictly for educational and research purposes and should not be considered financial advice.

____________
# Terms of Use
___________

- Personal and Academic Use
You are welcome to study, modify, and use this code for personal learning or academic research.

- No Guarantee
While reasonable efforts have been made to ensure the accuracy and reliability of the code, no guarantee is given that it is free of errors or suitable for any specific purpose.
You are strongly advised to test and validate all components before deploying them in a live or production environment.

____________
# Introduction
____________

This repository provides a systematic framework for trading on retail brokerage platforms that do not offer native API access.
The workflow assumes access to a market data provider capable of delivering intraday price data, such as Interactive Brokers or Bloomberg Terminal.
To balance usability and storage efficiency, the project integrates multiple data storage methods:

- Excel files (for inspection and lightweight analysis).
- PostgreSQL database hosted on Railway, which provides:
  - Free public access.
  - No VM or Docker setup.
  - Instant remote access via pgAdmin and Python.
  - Fully cloud-hosted database.

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












