# Algo_Trading

Welcome to the Algo_Trading repository! This repository contains code related to the setup of an Automated High-Frequency Trading system. Whether you're a beginner looking to learn about algorithmic trading or an experienced trader seeking to automate your strategies, you'll find valuable resources here.  

**Note:** In this repository ***FyersAPI*** has been used. To integrate with any other broker's API, change the required parts with the code given by the broker in their API Documentation.  

**Warning:** The codes **should not** be directly deployed into markets with real money. The purpose of this Repository is to provide a ready-to-use template that can be used to set up a very advanced HFT system.  

## How it works

- The Historical Data takes the range of dates you need the data for as input and breaks them into chunks, which can be queried using fyersapi cause of limitations on the number of rows that fyers sends at once. 

- Then the modules, like Consolidation Breakout, test how well the strategy has performed on the historical data just downloaded. Replace the module's core logic with any other strategy you want to test.

- Live_Trading Modules contains modules that handle the websocket connection provided by Fyers to handle your order smoothly. Add a custom function in the module to trade your desired strategy. Or you can just tweak the entry points to get entry whenever that particular price point hits.

- Derivatives_Trading module serves the purpose of giving an entry when the particular price point is hit on the spot, a functionality not provided by brokers generally, due to which the trader has to set the limit order on the contract instead of spot, leading to sometimes undesired entry and exit.

## Pip Modules Used

Before diving into the code, make sure you have the following pip modules installed:

- [pandas](https://pandas.pydata.org/): Powerful data manipulation and analysis library.
  ```
  pip install pandas
  ```

- [numpy](https://numpy.org/): Fundamental package for scientific computing with Python.
  ```
  pip install numpy
  ```

- [fyers-apiv3](https://github.com/fyers-api/fyers_api_v3): Fyers API v3 library for accessing Fyers trading APIs.
  ```
  pip install fyers-apiv3
  ```

- [matplotlib](https://matplotlib.org/): Comprehensive library for creating static, animated, and interactive visualizations in Python.
  ```
  pip install matplotlib
  ```

- [datetime](https://docs.python.org/3/library/datetime.html): Library for handling date and time.
  ```
  pip install datetime
  ```

- [dateutil](https://dateutil.readthedocs.io/en/stable/): Library providing powerful extensions to the standard datetime module.
  ```
  pip install python-dateutil
  ```

- [xlsxwriter](https://xlsxwriter.readthedocs.io/): Library for creating Excel XLSX files.
  ```
  pip install XlsxWriter
  ```

## Getting Started

To get started with the Algo_Trading repository, simply clone the repository to your local machine and install the required pip modules as mentioned above. Then, you can explore the code, add functions for implementing your own trading system and build up your Automated High-Frequency Trading system!

## Contribution

Contributions to this project are welcome! If you have any ideas, suggestions, or improvements, feel free to open an issue or submit a pull request. Let's collaborate and make algorithmic trading more accessible to everyone.

Hope you find this repository helpful.
