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
    
- HDF5 for DataFrame objects' storage for more efficient binary formats.
  - Pandas to wrap the functionality of the PyTables library

