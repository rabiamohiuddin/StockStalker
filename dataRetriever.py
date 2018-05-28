# Team Project: Stock Stalker
# DataRetriever and Plot Classes
# Rabia Mohiuddin
# Dan Trinh
# Arik Rakibullah
# CIS 41B
# Winter 2018

import requests
import datetime
from Analyzer import Analyzer
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay

class DataRetriever:
    def choiceOne(self, wantedDates, *symbols):
        ''' Returns list of dictionaries for multiple symbols' closing price'''
        
        linkOne = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=%s&outputsize=full&apikey=6T24ORZWIQDOWPXS"
        # List of JSON dict for each symbol
        dictList = [requests.get(linkOne % oneSymbol).json() for oneSymbol in symbols]    
        
        # For each dictionary in list of dictionaries
        for dictionary in dictList:
            # Error checking - if so, raise exception to be printed in error box in GUI
            if 'Error Message' in dictionary: raise KeyError("One or more of the symbols does not exist.")
            if wantedDates[0] not in dictionary['Time Series (Daily)'] : raise KeyError("Stock does not exist for start date. ")
            if wantedDates[-1] not in dictionary['Time Series (Daily)'] : raise KeyError("Stock does not exist for end date. ")
            
            # Find dates from dictionary that are not in wantedDates
            remove = [key for key in dictionary["Time Series (Daily)"] if key not in wantedDates]
            # Delete all dates that are in remove 
            for key in remove: del dictionary["Time Series (Daily)"][key]
            
            # For all dates (keys) in the dictionary
            for key in dictionary["Time Series (Daily)"]:
                # Only keep closing price   
                dictionary["Time Series (Daily)"][key] = float(dictionary["Time Series (Daily)"][key]["4. close"])
        
        # What resulting dictionary may look like
        ''' {'Meta Data': 
                {'1. Information': 'Daily Prices (open, high, low, close) and Volumes',
                '2. Symbol': 'MSFT', 
                '3. Last Refreshed': '2018-03-19', 
                '4. Output Size': 'Full size', 
                '5. Time Zone': 'US/Eastern' }, 
            
            'Time Series (Daily)': 
                {'2016-11-10': '58.7000', 
                '2003-03-21': '26.5700', 
                '2017-06-02': '71.7600', 
                '2004-03-17': '25.1300', 
                '2001-03-14': '54.0000', 
                '2006-06-23': '22.5000', ... 
        '''        
        
        # Return list of dictionaries
        return dictList       
        
    def choiceTwo(self):
        ''' Returns dict of list of Monthly prices for 3 stock indices (NASDAQ, S&P 500, Dow Jones) for last 12 months '''
        
        link = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=%s&apikey=6T24ORZWIQDOWPXS"
        # Symbols of Indices NASDAQ, S&P 500, Dow Jones
        indices = ["IXIC", "SPX", "DJI"]
        
        # List of JSON dict for each index
        indexDicts = [requests.get(link % symbol).json() for symbol in indices]     
        
        # Last business day of last 12 months
        dates = sorted(indexDicts[0]["Monthly Time Series"], key =lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'), reverse=True)[:13]     
        
        # Create dictionary where (key: value) = (indicator: [(date1, val1)...])
        monthlyPrices = {}
        
        # For each index in indices
        for index in indexDicts:           
            # Create ist of closing price for each day
            vals = [float(index["Monthly Time Series"][day]["4. close"]) for day in dates]
            # Dict of Symbol: [(date1, val1)...]
            monthlyPrices[index["Meta Data"]["2. Symbol"]] =  [*zip(dates, vals)]
        
        # What resulting dictionary may look like
        ''' 
        {Index1: [(date1, val1), (dat2, val2), ...], 
        Index2: [(date1, val1), ...], 
        … }
        '''
        
        # Return dictionary of lists
        return monthlyPrices   
    
    
    def choiceThree(self, symbol):
        ''' Return dict of lists of Relative Strength Index vs Average Directional Movement Index for a symbol over last year '''
        
        link  = "https://www.alphavantage.co/query?function=%s&symbol=%s&interval=monthly&time_period=10&series_type=close&apikey=6T24ORZWIQDOWPXS"
        
        # RSI dictionary
        RSIdict = requests.get(link % ("RSI", symbol)).json()    
        # ADX dictionary
        ADXdict = requests.get(link % ("ADX", symbol)).json()  
        
        # Raise exception to be printed in GUI error message if dictionary empty
        if RSIdict == {}: raise KeyError("One or more of the symbols does not exist.")
        if ADXdict == {}: raise KeyError("One or more of the symbols does not exist.")
        
        # Last business day of last 12 months
        # We create two separate lists of dates because it is possible that the two values are not
        # updated at the same time while the stock market is open.
        rsiDates = sorted(RSIdict["Technical Analysis: RSI"], key =lambda x: datetime.datetime.strptime(x.split()[0], '%Y-%m-%d'), reverse=True)[:12]
        adxDates = sorted(ADXdict["Technical Analysis: ADX"], key =lambda x: datetime.datetime.strptime(x.split()[0], '%Y-%m-%d'), reverse=True)[:12]
        
        # tuple of (date, val) for RSI
        RSIvalues = [*zip(rsiDates, [float(RSIdict["Technical Analysis: RSI"][day]["RSI"]) for day in rsiDates])]
        # tuple of (date, val) for ADX
        ADXvalues = [*zip(adxDates, [float(ADXdict["Technical Analysis: ADX"][day]["ADX"]) for day in adxDates])]
        
        # Create dictionary where key: value = indicator: [(date1, val1)...]
        techIndicators = {}
        # Insert list for each technical indicator
        techIndicators["RSI"] =  RSIvalues
        techIndicators["ADX"] =  ADXvalues
        
        # What resulting dictionary may look like
        '''
        {RSI: [(date1, val1), (dat2, val2), ...], 
        ADX: [(date1, val1), ...] }
        '''
        
        # Return dictionary of lists
        return techIndicators    
    
class Plot:
    def _placeValues(self, resultDict, graph):
        ''' Private - Plots date vs closing price using dictionary. Returns nothing. '''
        
        # Colors for graph
        colors = ["Blue", "Red", "Green", "Purple"]
        
        # For every stock/index in resultDict (list of dictionaries)
        for n, index in enumerate(resultDict):         
            # unzip to get list of dates and prices
            dates, prices = zip(*resultDict[index])
            dates = list(reversed(dates))
            prices = list(reversed(prices))
            # used to plot on x-axis : 12 values for 12 months
            nums = np.arange(0,12)                          
            # plot dates vs prices
            graph.plot(nums, prices, nums, prices, 'ob', label="%s" % index, color="%s" % colors[n])    
            
            # plot x-axis numbers
            graph.set_xticks(nums)              
            # plot x-axis labels
            graph.set_xticklabels([date[:10] for date in dates])       
        
        # set legend in best location    
        graph.legend(loc="best")    
    
    
    def ch1Graph(self, resultDict, graph, startDate, endDate):
        ''' Sets title and labels for choice one, and graphs values. Returns analysis string.'''
        
        # Graph setup
        graph.set_title("Stock Price vs Time")      # Set graph title
        graph.set_xlabel("Date")                    # Set x-axis label
        graph.set_ylabel("Stock Price")             # Set y-axis label
        
        # for each stock dictionary in the resultDict (list of dictionaries)
        for stock in resultDict:            
            # Create list of dates from dictionary
            dateList = [date for date in sorted(stock['Time Series (Daily)'], key = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))]           
            # Create list of prices for corresponding dates
            prices = [stock['Time Series (Daily)'][date] for date in sorted(stock['Time Series (Daily)'], key = lambda x: datetime.datetime.strptime(x, '%Y-%m-%d'))]       
            # Plot the prices
            graph.plot(prices, label= stock['Meta Data']['2. Symbol'])          
        
        # Set legend in the best location
        graph.legend(loc = 'best')      
        # Set 3 x-axis points
        graph.set_xticks([0,len(dateList) // 2,len(dateList) - 1])
        # Set corresponding dates on x-axis
        graph.set_xticklabels([dateList[0], dateList[(len(dateList) - 1) // 2], dateList[-1]])  
        
        # Analysis
        a = Analyzer()     
        # Get change and stock name from analysis of dictionary values
        analysis = a.compareOne(resultDict, startDate, endDate)      
        
        # Return analysis string to GUI 
        return analysis  
    
         
    def ch2Graph(self, resultDict, graph):
        ''' Sets title and labels for choice two. Calls _placeValues to plot values. Returns analysis string. '''
        
        # Graph setup
        graph.set_title("Monthly Price Percent Change for Stock Indices NASDAQ, S&P 500, Dow Jones during last 12 Months")  # Set title
        graph.set_xlabel("Date")        # Set x-axis label
        graph.set_ylabel("Percentage Change in Closing Price")      # Set y-axis label
        
        
        # For each index in resultDict (dictionary of list)
        for index in resultDict: 
            # Unzip dates and prices for each index - original dictionary has dates in most recent order
            dates, prices = zip(*reversed(resultDict[index])) 
            # Create a numpy array and convert each price to float
            prices = np.array(prices).astype(float)
            # Compute percent change betwen each data point
            prices = [0] + ((np.diff(prices)/ prices[:-1]) * 100)
            # Replace dictionary value with list of dates and price percent change
            resultDict[index] = [*zip(reversed(dates), reversed(prices))]
        
        # Graph dictionary values
        self._placeValues(resultDict, graph)
        
        # Analysis
        a = Analyzer()
        # Get percent change and index name from analysis of dictionary values
        analysis = a.compareTwo(resultDict)   
        
        # Return analysis string with best performing index and its percent change to GUI
        return analysis       
    
    
    def ch3Graph(self, resultDict, graph, symbol):
        ''' Sets title and labels for choice three. Calls _placeValues to plot values. Returns analysis. '''
        
        # Graph setup
        graph.set_title("Relative Strength Index vs Average Directional Movement Index for " + symbol + " over last year")   # Set title 
        graph.set_xlabel("Date")            # Set x-axis label
        graph.set_ylabel("Index Value")     # Set y-axis label
        graph.axhline(y=30, color = 'black', linestyle = 'dashed')
        graph.axhline(y=70, color = 'black', linestyle = 'dashed')        
        
        # Graph dictionary values
        self._placeValues(resultDict, graph)
        
        # Analysis
        a = Analyzer()
        # Get direction and strength from analysis of dictionary values
        analysis = a.compareThree(resultDict, symbol)
        
        # Return completed analysis string to GUI
        return analysis

