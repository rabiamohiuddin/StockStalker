# StockStalker
Stock “Stalker”
By: Dan Trinh, Rabia Mohiuddin, Arik Rakibullah

Functionality
	-> Stock “Stalker” is an application that lets a user do three main functions for stock data over the last 20 years.


1. Compare Stocks
   a. The user can enter up to four stock symbols as well as a start and end date and the closing prices for each stock for each day within the range of start and end dates will be displayed.
      * All stocks must be valid (have closing prices) through the start and end date or else error message will be displayed.
   b. Below the closing price, a graph will show the requested symbols and their closing price over the time indicated.
   c. Underneath the graph, an analysis is given as to which stock is performing the best based on the highest percent increase from the start date.


2. Compare 3 major stock indices (NASDAQ, S&P 500, and Dow Jones)
   a. A set graph in the window has a “load” button located under it which the user can click to show the percent change in closing prices of NASDAQ, S&P 500, and Dow Jones over the last 12 months.
   b. Underneath, analysis is given as to which index is performing the best based on the highest percent change


3. Look at market trends for a particular stock
   a. For a user entered symbol, a graph will display two technical indicator values over the last 12 months. 
   b. The first being the Relative Strength Index (RSI) which based on its value, tells whether the stock is undervalued, overvalued, or has a fair price. 
   c. The second being the Average Directional Movement Index (ADX) which based on its value, tells whether the stock has a weak, strong, very strong, or extremely strong trend.
   d. Below, analysis is given based on the average value of RSI and ADX over the last 12 months


Files

Analyzer.py (Arik)
- Class Analyzer
   * Helps the plotting class analyze stock/index data.
   * Compares stock/index percentage increase to determine the best performer.
   * Returns analysis string as to what numbers mean to Plot class

Stockstalker.py (Dan)
- Class StockGUI
   * Creates a GUI window for the user to interact with.
   * The GUI window uses a Tkinter notebook widget to split each feature of the program’s functions into tabs.
   * Accepts and validates user input depending on the selected feature.
   * Utilizes DataRetriever and Plot to display graphs of stock data, and a brief analysis as to what the data means.
   * Graphs are embed in the GUI window using TkAgg to render to Tk canvas.

DataRetriever.py (Rabia)
- Class DataRetriever 
   * Sends a request to the API and downloads the JSON dictionary. Goes through the data and only keeps whats necessary. 
- Class Plot 
   * Takes returned dictionary or list of dictionaries from DataRetriever, sets up the graph, and plots it on matplotlib figure object passed by Class StockGUI.
   * Then calls Class Analyzer with resulting dictionary and gets analysis string which is returned to the GUI.
