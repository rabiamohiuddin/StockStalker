# Dan Trinh
# Rabia Mohiuddin
# Arik Rakibullah
# Team Project: Stock Stalker
# GUI Component

import datetime
from decimal import Decimal
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import os
import platform
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tkmb
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar
from pandas.tseries.offsets import CustomBusinessDay
# Group's class
from dataRetriever import *


class StockGUI(tk.Tk):
    def __init__(self):
        '''
        Set up GUI window for Stock Stalker.
        '''
        super().__init__()
        
        # Title and resizable trait
        self.title('Stock "Stalker"')
        self.resizable(True, True)
        # Resolution
        w = 975
        h = 975
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        
        self.geometry('%dx%d+%d+%d' % (w, h, x, y-20))
        
        # Use Notebook to display three different options.
        self._nb = ttk.Notebook(self) # self to refer to this window 
        self._nb.grid(row=0,column=0, sticky='wens')

        # Notebook 
        # Tab 1: Closing prices for each day...
        option1 = ttk.Frame(self._nb)
        self._nb.add(option1, text='Compare Stocks')
        # Tab 2: Stock indices from today until the last year...
        option2 = ttk.Frame(self._nb)
        self._nb.add(option2, text='Stock Indices')
        # Tab 3: Technical Indicator Comparison
        option3 = ttk.Frame(self._nb)
        self._nb.add(option3, text='Market Trends')
        
        # Notebook should be expandable
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)        
        
        # Load the three choices, filling each tab with widgets.
        self._loadOption1(option1)
        self._loadOption2(option2)
        self._loadOption3(option3)
        
    def _loadOption1(self, option1):
        '''
        Creates option 1 GUI interface
        arg - option1, the tkinter frame which all the widgets are contained
              option1 is a frame that serves to fill tab 1 of the notebook
        return - none
        '''
        # Box of to display information about stocks.
        scrlBar = tk.Scrollbar(option1)
        boxLabel = tk.Label(option1, text="Stock Comparison",font = ('Comic Sans MS', 11))
        boxLabel.grid(row=0,column=0, columnspan=2, sticky = 'we')
        self._treebox = ttk.Treeview(option1, yscrollcommand=scrlBar.set)
        self._treebox.grid(row=2,column=0,columnspan=2, sticky = 'wens')
        # scrollbar configuration
        scrlBar.config(command=self._treebox.yview)
        scrlBar.grid(row=2,column=2, sticky='ens')
        # Filling in the treebox 
        # 1. Columns. A tuple
        #  - Should be of the stock names
        self._columns = ('date', 'close')
        self._treebox['columns'] = self._columns
        self._treebox.heading("#0", text='Symbol', anchor='center')
        self._treebox.column("#0", width=105, anchor='center')
        self._treebox.heading('date', text='Date')
        self._treebox.column('date',width=105, anchor='center')        
        self._treebox.heading('close', text='Close')
        self._treebox.column('close', anchor='center')         
        
        # Symbol Entry
        self._symbolInput1 = tk.StringVar()
        symLabel = tk.Label(option1, text='Symbols (Sym1,...,Sym4):')
        symLabel.grid(row=3, column=0, sticky = 'w')
        symEntry = tk.Entry(option1, textvariable = self._symbolInput1)
        symEntry.grid(row=3, column=1, sticky = 'we')
        symEntry.focus_set() # set focus to symbol.
        
        # Start Date
        self._startDateEntry = tk.StringVar()
        sDateLabel = tk.Label(option1, text='Start Date (YYYY-MM-DD): ')
        sDateLabel.grid(row=4, column=0, sticky = 'w')
        sDateEntry = tk.Entry(option1,textvariable=self._startDateEntry)
        sDateEntry.grid(row=4,column=1, sticky='we')
    
        # End Date
        self._endDateEntry = tk.StringVar()
        endDateLabel = tk.Label(option1, text='End Date (YYYY-MM-DD): ')
        endDateLabel.grid(row=5, column=0, sticky = 'w')
        endDateEntry = tk.Entry(option1,textvariable=self._endDateEntry)
        endDateEntry.grid(row=5,column=1, sticky='we')
    
        # Submit button
        submitButton = tk.Button(option1, text='Submit',
                                 command=self._submit)
        submitButton.grid(row=6, column=1,columnspan=2, sticky='wen')
        
        # Graph
        graphTitle = tk.Label(option1, text="Graph",font = ('Comic Sans MS', 20))
        graphTitle.grid(row=7,column=0,columnspan=2, sticky = 'we')    
        # Example graph
        self._figure1 = Figure(figsize=(5,5), dpi=100)
        # Argument is subplot grid parameters
        # 111 = makes a standard subplot
        self._graph1 = self._figure1.add_subplot(111)
        # to draw actual graph we need a canvas to display it.
        # f is figure holding graph, self is master
        canvas = FigureCanvasTkAgg(self._figure1, option1)
        canvas.show()
        # grid to put it on the GUI
        canvas.get_tk_widget().grid(row=8,column=0,columnspan=2, sticky='wens')
        # Toolbar for graph
        # - Have to use a frame because toolbars can only be used with pack
        tbFrame = ttk.Frame(option1)
        tbFrame.grid(row=9,column=0, columnspan=2, sticky='w')
        toolbar = NavigationToolbar2TkAgg(canvas, tbFrame)
        toolbar.update()
        # Arik's Analysis
        self._ch1Text = tk.StringVar()
        tk.Label(option1, textvar = self._ch1Text, bg = 'pink', font = ('Comic Sans MS', 15)).grid(row= 10, column= 0, columnspan = 2, sticky = 'we')
        
        option1.grid_columnconfigure(1, weight = 1)
        option1.grid_rowconfigure(7, weight = 1)
        
        
    def _loadOption2(self, option2):
        '''
        Create GUI interface for Option 2: Indices, 
        which shows graphs of the three stock indices,
        option2 - a frame that serves to fill tab 2 of the notebook
        '''
        # Graph (Placeholder) (Same as 1)
        graph = tk.Label(option2, text="Indices For the Last Year",font = ('Comic Sans MS', 11))
        graph.grid(row=0,column=0,columnspan=2, sticky = 'wens')    
        # Graph needs a figure to place it in
        self._figure2 = Figure(figsize=(5,5), dpi=100)
        # Argument is subplot grid parameters
        # 111 = 1x1 grid, first subplot
        self._graph2 = self._figure2.add_subplot(111)
        # Draw actual graph; need a canvas to display it. 
        canvas = FigureCanvasTkAgg(self._figure2, option2)
        canvas.show()
        # grid to put it on the GUI
        canvas.get_tk_widget().grid(row=1,column=0,columnspan=2, sticky='wens')
        # Toolbar for graph
        # - Have to use a frame because toolbars can only be used with pack
        tbFrame = ttk.Frame(option2)
        tbFrame.grid(row=2,column=0,sticky='e')
        toolbar = NavigationToolbar2TkAgg(canvas, tbFrame)
        toolbar.update() 
        
        # Load button
        submitButton = tk.Button(option2, text='Load Graph',
                                 command= self._createGraphOption2)
        submitButton.grid(row=3, column=0,columnspan=2, sticky='we') 
        
        # Arik's Analysis
        self._ch2Text = tk.StringVar()
        tk.Label(option2, textvar = self._ch2Text, bg = 'pink', font = ('Comic Sans MS', 15)).grid(row= 10, column= 0, columnspan = 2, sticky = 'we')        
        
        # Resizable trait
        option2.grid_columnconfigure(1, weight = 1)
        option2.grid_rowconfigure(1, weight = 1)           
    
    def _loadOption3(self, option3):
        '''
        Option 3: Relative Strength Index vs Average Directional Movement Index
        option3 - frame to contain widgets, serves as tab 3 of the notebook.
        '''   
        # Label
        title = tk.Label(option3, text="Technical Indicator Comparison", font = ('Comic Sans MS', 11))
        title.grid(row=0,column=0,columnspan=2, sticky = 'wen')    
        # Symbol Entry
        self._symbolInput3 = tk.StringVar()
        symLabel = tk.Label(option3, text='Symbol: ')
        symLabel.grid(row=1, column=0, sticky = 'wn')
        symEntry = tk.Entry(option3, textvariable = self._symbolInput3)
        symEntry.grid(row=1, column=1, sticky = 'wen')
        symEntry.focus_set() # set focus to symbol.             
        # Load button
        submitButton = tk.Button(option3, text='Compare',
                                     command=self._submit)
        submitButton.grid(row=2, column=1,columnspan=2, sticky='wen')        
        
        # Graph (Placeholder) (Same as Option 1 and 2)
        self._figure3 = Figure(figsize=(5,5), dpi=100)
        # Argument is subplot grid parameters
        # 111 = 1x1 grid, first subplot
        self._graph3 = self._figure3.add_subplot(1,1,1)
        # Draw actual graph; need a canvas to display it.
        # f is graph, self is master
        canvas = FigureCanvasTkAgg(self._figure3, option3)
        canvas.show()
        # grid to put it on the GUI
        canvas.get_tk_widget().grid(row=3,column=0,columnspan=2, sticky='wens')
        # Toolbar for graph
        tbFrame = ttk.Frame(option3)
        tbFrame.grid(row=4,column=0,columnspan=2, sticky='wens')
        toolbar = NavigationToolbar2TkAgg(canvas, tbFrame)
        toolbar.update()
        
        self._ch3Text = tk.StringVar()
        tk.Label(option3, textvar = self._ch3Text, bg = 'pink', font = ('Comic Sans MS', 15)).grid(row= 10, column= 0, columnspan = 2, sticky = 'we')
        
        # Resizable trait
        option3.grid_columnconfigure(1, weight = 1)
        option3.grid_rowconfigure(3, weight = 1) 
        
    def _submit(self, event=None):
        '''
        Submits user input for processing, depending on which tab is selected
        at the time.
        '''   
        #print("submit called")
        try:
            # On the first tab
            if self._nb.select() == self._nb.tabs()[0]:
                # Process option 1 input
                #print("On first tab") # Debug
                self._processOption1Input()
                self._createGraphOption1()
                self._createBoxOption1()
            # None for second tab; no entry box
            # On the third tab
            elif self._nb.select() == self._nb.tabs()[2]:
                #print("On last tab") # Debug
                self._processOption3Input()
                self._createGraphOption3()
        except ValueError as ValueE:
            tkmb.showerror(title="Input Error", message= str(ValueE) +
                           "\n\nFix input and try again.")
        except KeyError as KeyE:
            tkmb.showerror(title="Input Error!",
                           message = str(KeyE))
            
    def _processOption1Input(self):
        '''
        Validates input for option 1.
        '''
        #print("_procOp1") # debug
        self._symbols = self._symbolInput1.get().upper()
        self._startDate = self._startDateEntry.get()
        self._endDate = self._endDateEntry.get()
        
        endDateCheck = tuple(self._endDate.split('-'))
        startDateCheck = tuple(self._startDate.split('-'))
        
        if (self._symbols and self._startDate and self._endDate):
            # Convert symbols to tuple  
            self._symbolList = [symbol.strip() for symbol in self._symbols.split(',')]
            if "" in self._symbolList: self._symbolList.remove("")
            #print(self._symbolList)
            # No more than 4 symbols.
            limit = 4
            if len(self._symbolList) <= limit:
                for symbol in self._symbolList:
                    if not symbol.isalpha():
                        raise ValueError("Symbols must be alphabetical characters.")
            else:
                raise ValueError("There may be no more than "+ str(limit)+ " symbols.")
                # Must all be alphabetical chars.
                
            # date checks
            # 1. Correct format
            # 2. An date in the calendar
            # 3. The date ends before the start date
            if len(endDateCheck) is 3 and len(startDateCheck) is 3: # Correct format?
                # Are they all numbers? Check by converting to int
                #print(endDateCheck, startDateCheck)
                endDateList = [int(num) for num in endDateCheck]
                startDateList = [int(num) for num in startDateCheck]
                present = datetime.datetime.now()
                # Now check to see that the end date is later than the start date
                if not (datetime.datetime(*endDateList) <= datetime.datetime.now()):   
                    raise ValueError("The end date needs to either occur today or before today.")
                # and the endDate is no further than the current day.
                elif not (datetime.datetime(*endDateList) >= datetime.datetime(*startDateList)):
                    raise ValueError("The end date needs to occur after the start date.")
                else:
                    # So if those two errors aren't raised, modify the start date and end date
                    # to ensure that both are business days and not weekends nor holidays.
                    # If they are, then roll them to the nearest business day.
                    self._startDate = str(np.busday_offset(self._startDate, 0, roll='forward'))   
                    self._endDate = str(np.busday_offset(self._endDate, 0, roll='backward'))
                    us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
                    # also create a list of the dates in between the start and the end date to use in DataRetriever.
                    self._wantedDates = list(pd.DatetimeIndex(start=self._startDate,end=self._endDate, freq=us_bd).format())
                    self._startDate = self._wantedDates[0]
                    self._endDate = self._wantedDates[-1]
                    
            else:
                raise ValueError('Invalid date format!')
        else:
            #pass
            raise ValueError("All three fields need to be filled before a graph "+
                          "can be created.")
    
    def _processOption3Input(self):
        '''
        Validates input of option3
        '''
        symbol = self._symbolInput3.get()
        #print(symbol)
        if symbol:
            if not symbol.isalpha():
                raise ValueError("Invalid stock symbol.")
        else:
            #pass
            raise ValueError("The field need to be filled before a graph "+
                          "can be created.")       
        
    def _createBoxOption1(self):
        '''
        Create treeview for option 1 displaying the opening and closing price for
        that date.
        Note: Happens after graph for option 1 is created.
        '''
        # To round to two places
        twoplaces = Decimal(10) ** -2
        # Clear out tree
        self._treebox.delete(*self._treebox.get_children())
        
        for symbol in self._ch1:                                           # for each symbol that was input
            dayPrices = tuple((date, Decimal(symbol["Time Series (Daily)"][date]).quantize(twoplaces))  # get a tuple of the date and its price at that date.
                               for date in sorted(symbol["Time Series (Daily)"], # sort from oldest to most recent.
                               key =lambda x: datetime.datetime.strptime(x, '%Y-%m-%d')))
            for date in dayPrices:
                self._treebox.insert("", "end",text=symbol['Meta Data']['2. Symbol'],  # Insert the symbol name into the treeview widget
                                     values = date)                                    # and the tuple that was just retrieved.
        self._treebox.update()
            
    def _createGraphOption1(self):
        '''
        Creates graph for option 1.
        '''
        #print("Creating graph for option 1...")
        dr = DataRetriever()
        try:
            self._ch1 = dr.choiceOne(self._wantedDates, *self._symbolList)
            p = Plot()
            # Clear graph
            self._figure1.clear()
            # Add subplot onto figure
            self._graph1 = self._figure1.add_subplot(111)
            # Plot for the subplot
            ch1Analysis = p.ch1Graph(self._ch1, self._graph1, self._startDate, self._endDate)
            self._ch1Text.set(ch1Analysis)
            # Draw onto the established canvas
            self._figure1.canvas.draw()
        except IndexError:
            tkmb.showerror(title = "Input Error", message= "Dates are invalid!")
        except ValueError:
            tkmb.showerror(title = "Input Error", message= "Dates are invalid!")
        
    
    def _createGraphOption2(self):
        '''
        Loads the graph of 3 major stock indices for the previous 12 months.
        '''
        #print("load graph 2")
        dr= DataRetriever()
        ch2 = dr.choiceTwo()
        plot = Plot()
        # Clear graph
        self._figure2.clear()
        # Add subplot onto figure
        self._graph2 = self._figure2.add_subplot(111)
        # Plot for the subplot
        ch2Analysis = plot.ch2Graph(ch2, self._graph2)
        self._ch2Text.set(ch2Analysis)
        # Draw onto the established canvas
        self._figure2.canvas.draw()
   
    
    def _createGraphOption3(self, event=None):
        '''
        Loads the graph of the popular technical indicators Relative Strength
        Index vs Average Directional Movement Index based upon a symbol a user 
        put over the previous 12 months.
        '''     
        #print("load graph 3")
        dr= DataRetriever()
        ch3 = dr.choiceThree(self._symbolInput3.get().upper())
        plot = Plot()
        # Clear graph
        self._figure3.clear()
        # Add subplot onto figure
        self._graph3 = self._figure3.add_subplot(111)
        # Plot for the subplot
        ch3Analysis = plot.ch3Graph(ch3, self._graph3, self._symbolInput3.get().upper())
        self._ch3Text.set(ch3Analysis)
        # Draw onto the established canvas
        self._figure3.canvas.draw()            
    

              
        
def main(): 
    w = StockGUI()
    if platform.system() == 'Darwin': 
        tmpl = 'tell application "System Events" to set frontmost of every process whose unix id is %d to true'
        os.system("/usr/bin/osascript -e '%s'" % (tmpl % os.getpid())) 
    while True:
    # A result of a bug on Mac where using scrollwheel on the graph portion of the GUI crashes it.
        try:
            w.mainloop()
            break
        except UnicodeDecodeError: 
            pass        
    
main()

