# Rabia Mohiuddin
# Dan Trinh
# Arik Rakibullah

import time
import numpy as np

class Analyzer:
    
    def compareOne(self, stockList, startDate, endDate):
        ''' Takes in a list of dictionaries representing stock closing prices and returns the strock with the greatest percentage increase. '''
        deltaList = [(((stock['Time Series (Daily)'][endDate] - stock['Time Series (Daily)'][startDate]) / (stock['Time Series (Daily)'][startDate])) * 100, stock['Meta Data']['2. Symbol']) for stock in stockList]
        
        (change, sname) = max(deltaList)
        return sname + ' has done best, with a percentage change of ' + str(round(change, 4)) + '%'   
    
    def compareTwo(self, indexList):
        ''' Takes in a list of dictionaries representing index values over a year and returns the best performing index. '''        
        deltaList = [(sum([date[1] for date in indexList[index]]), index) for index in indexList]
        
        (change, indexName) = max(deltaList)
        return indexName + ' has done best, with a percentage change of ' + str(round(change, 4)) + '%'
    
    def compareThree(self, indicatorDictionary, symbol):
        ''' Takes in a dictionary containing the values of RSI and ADX for a particular stock and returns the average values for each. '''
        adx = [value[1] for value in indicatorDictionary["ADX"]]
        rsi = [value[1] for value in indicatorDictionary["RSI"]]
        
        (direction, strength) = (np.mean(adx),np.mean(rsi))
        
        # Based on the strength value, set string to definition of value of strength
        if strength >= 70: analysis = symbol + " is overvalued with an average RSI value of " + str(round(strength, 4))
        elif strength <= 30: analysis = symbol +" is undervalued with an average RSI value of " + str(round(strength, 4))
        else: analysis = symbol + " has a fair value with an average RSI value of " + str(round(strength, 4))
        
        # Based on the direction value, set string to defintion of value of direction
        if (0 <= direction <= 25): analysis += ", and has a weak trend with an average ADX value of " + str(round(direction, 4))
        elif (25 <= direction <= 50): analysis += ", and has a strong trend with an average ADX value of " + str(round(direction, 4))
        elif (50 <= direction <= 75): analysis += ", and has a very strong trend with an average ADX value of " + str(round(direction, 4))
        else: analysis += ", and has an extremely strong trend with an average ADX value of " + str(round(direction, 4))
    
        # Return completed analysis string to Plot
        return analysis        