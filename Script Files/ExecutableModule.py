#Importing standard libs
from tkinter import *
from datetime import date
import numpy as np
import matplotlib.pyplot as plt
import math
import time

#Importing custom libs
from AssetModule import Asset
from StockModule import Stock
from StrategyListFactoryModule import *
from Strategy_Folder.StrategyBaseModule import *


def LoadTable():

    #This function loads the table with the option quotes
    #input: .dat comma delimited table saved on the main application folder.
    #Standard download format from CBOE exchange quotes:
    #http://www.cboe.com/delayedquote/quote-table
    #output: unordered table containing all options data.  underlying stock as
    #an object (and respective attributes name, price, date)

    print('Reading quote table...')
    rawassetattributes = np.genfromtxt('quotedata.dat',delimiter=',',max_rows=1,dtype=str)
    stockname = rawassetattributes[0]
    stockprice = rawassetattributes[-3]
    currentdate = str(datetime.datetime.now())
    rootstock = Stock(stockname,stockprice,currentdate)
    rawquotetable = np.genfromtxt('quotedata.dat',delimiter=',',skip_header=4,dtype=str)
    
    print('Quote table loaded successfuly')
    print(" ")

    return rawquotetable, rootstock

def CleanTable(rawtable,assetname):
    
    #This functions takes the unordered data outputed by the LoadTable()
    #function and transforms it into structured numpy arrays
    #inputs: unordered data table, underlying asset
    #outputs: call options table, respective list of call tags, put options
    #table, respective list of put tags

    maxrows, maxcols = rawtable.shape
    
    #CALL TABLE

    #info needed per call option vs position in raw table:
    #option type | strike price | bid | ask | maturity day | maturity month |
    #maturity year | vol | interest
    #call | col 3 | col 7 | col 8 | col 4 char 3 & 4 after room name | col 2 |
    #col 1 | col 9 | col 10

    calltable = np.empty([maxrows,8])
    tag_call = []
    tag_put = []

    i = 0
    while i < maxrows:
        calltable[i,0] = float(rawtable[i,2]) #strikeprice
        calltable[i,1] = float(rawtable[i,6]) #bid
        calltable[i,2] = float(rawtable[i,7]) #ask
        calltable[i,3] = CutDay(rawtable[i,3],assetname) #maturity day
        calltable[i,4] = MonthFloatConversion(rawtable[i,1]) #maturity month
        calltable[i,5] = (float(rawtable[i,0]) + 2000) #maturity year
        calltable[i,6] = float(rawtable[i,8]) #volume
        calltable[i,7] = float(rawtable[i,9]) #open interest
        tag_call.append(rawtable[i,3])
        i = i + 1

    
    #PUTS

    #info needed per put option vs position in raw table:
    #option type | strike price | bid | ask | maturity day | maturity month |
    #maturity year | vol | interest
    #put | col 3 | col 7 | col 8 | col 4 char 3 & 4 after room name | col 2 |
    #col 1 | col 9 | col 10

    puttable = np.empty([maxrows,8])

    i = 0
    while i < maxrows:
        puttable[i,0] = float(rawtable[i,2]) #strikeprice
        puttable[i,1] = float(rawtable[i,-5]) #bid**
        puttable[i,2] = float(rawtable[i,-4]) #ask**
        puttable[i,3] = CutDay(rawtable[i,3],assetname) #maturity day
        puttable[i,4] = MonthFloatConversion(rawtable[i,1]) #maturity month
        puttable[i,5] = (float(rawtable[i,0])) + 2000 #maturity year
        puttable[i,6] = rawtable[i,-3] #volume**
        puttable[i,7] = rawtable[i,-2] #open interest**
        tag_put.append(rawtable[i,13])
        i = i + 1

    return calltable, puttable, tag_call, tag_put

def CutDay(rawstring,assetname):

    #This function cuts the day out of the string from the raw data
    #inputs: raw data string, name of the underlying asset
    #output: maturity day
    
    char1 = len(assetname) + 3
    char2 = char1 + 1
    dayno = rawstring[char1] + rawstring[char2]
    dayreturn = float(dayno)

    return dayreturn

def MonthFloatConversion(monthstring):
    
    #This function converts a month name string into a month number
    #input: month name string (Jan, Feb, ...)
    #output: month number (1, 2, ...) 
    monthno = 0

    if monthstring == 'Jan':
        monthno = 1
    if monthstring == 'Feb':
        monthno = 2
    if monthstring == 'Mar':
        monthno = 3
    if monthstring == 'Apr':
        monthno = 4
    if monthstring == 'May':
        monthno = 5
    if monthstring == 'Jun':
        monthno = 6
    if monthstring == 'Jul':
        monthno = 7
    if monthstring == 'Aug':
        monthno = 8
    if monthstring == 'Sep':
        monthno = 9
    if monthstring == "Oct":
        monthno = 10
    if monthstring == 'Nov':
        monthno = 11
    if monthstring == 'Dec':
        monthno = 12
    if monthno == 0:
        print("Error converting month string into from raw table into float for option table")

    monthreturn = float(monthno)

    return monthreturn

def CreateOptionList(type,cleantable,taglist):
    
    #This function converts the numpy option array into a list of option objects
    #input: option contract type (long call, short call, long put, short put), numpy array of options, respective option tags
    #output:

    #creating list of available derivative assets
    rows,cols = cleantable.shape
    option_list = []
    i = 0    

    while i < rows:
        option = Asset(type,cleantable[i,0],cleantable[i,1],cleantable[i,2],cleantable[i,3],cleantable[i,4],cleantable[i,5],cleantable[i,6],cleantable[i,7],taglist[i])
        option_list.append(option)
        i = i + 1
    
    return option_list

def BuildListOptmizedStrategies(strategytype,breakeven,stock,short_call_list,long_call_list,short_put_list,long_put_list,tolfil_short_call_list,tolfil_long_call_list,tolfil_short_put_list,tolfil_long_put_list,fee):
    
    #https://www.optionsplaybook.com/option-strategies/
    #This function builds a list of strategies with a specific profit profile and return a list of optimized strategy lists
    #inputs: profit profile (strategy type), break even points, underlying stock, short call list, long call list, short put list, long put list, filtered option lists, transaction fee 
    #outputs: ordered list of optimized strategy lists

    listfactory = StrategyListFactory(stock,short_call_list,long_call_list,short_put_list,long_put_list,tolfil_short_call_list,tolfil_long_call_list,tolfil_short_put_list,tolfil_long_put_list,fee)

    print("--- %s seconds ---" % (time.time() - start_time))

    if strategytype == 1: #profit inside price delta interval
        
        print("--- %s seconds ---" % (time.time() - start_time))
        
        #1.1.  Long butterfly call
        print("Optimizing long butterfly with calls")
        print(" ")
        long_butterfly_call_list = listfactory.BuildLongButterflyCall()
        optbe_long_butterfly_call_list = OptimizeTwoBreakEven(long_butterfly_call_list,breakeven)
        OptimizeCostMaxminratio(optbe_long_butterfly_call_list)
        
        print("--- %s seconds ---" % (time.time() - start_time))
        
        #1.2.  Long butterfly put
        print("Optimizing long butterfly with puts")
        print(" ")
        long_butterfly_put_list = listfactory.BuildLongButterflyPut()
        optbe_long_butterfly_put_list = OptimizeTwoBreakEven(long_butterfly_put_list,breakeven)
        OptimizeCostMaxminratio(optbe_long_butterfly_put_list)
        
        print("--- %s seconds ---" % (time.time() - start_time))
        
        #1.3.  Iron butterfly (PROCESSING TIME TOO LONG)
        #print("Optimizing iron butterfly")
        #print(" ")
        #iron_butterfly_list = listfactory.BuildIronButterflyPut()
        #optbe_butterfly_list =
        #OptimizeTwoBreakEven(iron_butterfly_list,breakeven)
        #OptimizeCostMaxminratio(optbe_butterfly_list)
        #
        #print("--- %s seconds ---" % (time.time() - start_time))

        #1.4.  Short straddle
        print("Optimizing short straddle")
        print(" ")
        short_straddle_list = listfactory.BuildShortStraddle()
        optbe_short_straddle_list = OptimizeTwoBreakEven(short_straddle_list,breakeven)
        OptimizeCostMaxprofit(optbe_short_straddle_list)

        print("--- %s seconds ---" % (time.time() - start_time))

        #1.5.  Short strangle
        print("Optimizing short strangle")
        print(" ")
        short_strangle_list = listfactory.BuildShortStrangle()
        optbe_short_strangle_list = OptimizeTwoBreakEven(short_strangle_list,breakeven)
        OptimizeCostMaxprofit(optbe_short_strangle_list)

        print("--- %s seconds ---" % (time.time() - start_time))
        
        #strategylist =
        #[optbe_long_butterfly_call_list,optbe_long_butterfly_put_list,optbe_short_straddle_list,optbe_short_strangle_list]
        strategylist = [optbe_long_butterfly_call_list,optbe_long_butterfly_put_list,optbe_butterfly_list,optbe_short_straddle_list,optbe_short_strangle_list]


        #TODO:
        #Figure out how to reduce processing time for strategies with 4+ assets
        #(long condor spread with calls, long condor spread with puts, iron
        #condor)
        #Long calendar spread with calls
        #Long calendar spread with puts
        #Diagonal spread with calls
        #Diagonal spread with puts
        #Christmas tree butterfly with calls
        #Christmas tree butterfly with puts
        #Double diagonal
        #OTM butterflies


    elif strategytype == 2: #profit outside price delta interval

        #2.1.  Long straddle
        print("Optimizing long straddle")
        print(" ")
        long_straddle_list = listfactory.BuildLongStraddle()
        optbe_long_straddle_list = OptimizeTwoBreakEven(long_straddle_list,breakeven)
        OptimizeCostMinprofit(optbe_long_straddle_list)

        print("--- %s seconds ---" % (time.time() - start_time))

        #2.2.  Long strangle
        print("Optimizing long strangle")
        print(" ")
        long_strangle_list = listfactory.BuildLongStrangle()
        optbe_long_strangle_list = OptimizeTwoBreakEven(long_strangle_list,breakeven)
        OptimizeCostMinprofit(optbe_long_strangle_list)

        print("--- %s seconds ---" % (time.time() - start_time))

        #2.3.  Back spread with calls
        print("Optimizing back spread with calls")
        print(" ")
        back_spread_call_list = listfactory.BuildBackSpreadCall()
        optbe_back_spread_call_list = OptimizeTwoBreakEven(back_spread_call_list,breakeven)
        OptimizeCostMaxminratio(optbe_back_spread_call_list)

        print("--- %s seconds ---" % (time.time() - start_time))

        #2.4.  Back spread with puts
        print("Optimizing back spread with puts")
        print(" ")
        back_spread_puts_list = listfactory.BuildBackSpreadPut()
        optbe_back_spread_puts_list = OptimizeTwoBreakEven(back_spread_puts_list,breakeven)
        OptimizeCostMaxminratio(optbe_back_spread_puts_list)

        print("--- %s seconds ---" % (time.time() - start_time))

        strategylist = [optbe_long_straddle_list,optbe_long_strangle_list,optbe_back_spread_call_list,optbe_back_spread_puts_list]


        #TODO:
        #Inverse skip strike butterfly with calls
        #Inverse skip strike butterfly with puts
        
      
    if strategytype == 3: #profit above price delta point

        #3.1.  Covered call
        print("Optimizing covered call")
        print(" ")
        covered_call_list = listfactory.BuildCoveredCall()
        optbe_covered_call_list = OptimizeOneBreakEven(covered_call_list,breakeven)
        OptimizeCostMaxprofit(optbe_covered_call_list)

        print("--- %s seconds ---" % (time.time() - start_time))

        #3.2.  Protective put
        print("Optimizing protective put")
        print(" ")
        protective_put_list = listfactory.BuildProtectivePut()
        optbe_protective_put_list = OptimizeOneBreakEven(protective_put_list,breakeven)
        OptimizeCostMinprofit(optbe_protective_put_list)
        
        print("--- %s seconds ---" % (time.time() - start_time))

        #3.3.  Collar
        print("Optimizing collar")
        print(" ")
        collar_list = listfactory.BuildCollar()
        optbe_collar_list = OptimizeOneBreakEven(collar_list,breakeven)
        OptimizeCostMaxminratio(optbe_collar_list)
        
        print("--- %s seconds ---" % (time.time() - start_time))

        #3.4.  Long call
        print("Optimizing long call")
        print(" ")
        long_call_strategy_list = listfactory.BuildLongCall()
        optbe_long_call_strategy_list = OptimizeOneBreakEven(long_call_strategy_list,breakeven)
        OptimizeCostMinprofit(optbe_long_call_strategy_list)
        
        print("--- %s seconds ---" % (time.time() - start_time))

        #3.5.  Long call spread
        print("Optimizing long call spread")
        print(" ")
        long_call_spread_list = listfactory.BuildLongCallSpread()
        optbe_long_call_spread_list = OptimizeOneBreakEven(long_call_spread_list,breakeven)
        OptimizeCostMaxminratio(optbe_long_call_spread_list)
        
        print("--- %s seconds ---" % (time.time() - start_time))

        #3.6.  Short put spread
        print("Optimizing short put spread")
        print(" ")
        short_put_spread_list = listfactory.BuildShortPutSpread()
        optbe_short_put_spread_list = OptimizeOneBreakEven(short_put_spread_list,breakeven)
        OptimizeCostMaxminratio(short_put_spread_list)
        
        print("--- %s seconds ---" % (time.time() - start_time))

        #3.7.  Short put
        print("Optimizing short put")
        print(" ")
        short_put_strategy_list = listfactory.BuildShortPut()
        optbe_short_put_strategy_list = OptimizeOneBreakEven(short_put_strategy_list,breakeven) 
        OptimizeCostMaxprofit(optbe_short_put_strategy_list)
        
        print("--- %s seconds ---" % (time.time() - start_time))

        #3.8.  Long combination
        print("Optimizing long combination")
        print(" ")
        long_combination_list = listfactory.BuildLongCombination()
        optbe_long_combination_list = OptimizeOneBreakEven(long_combination_list ,breakeven) 
        OptimizeCost(optbe_long_combination_list)

        print("--- %s seconds ---" % (time.time() - start_time))

        strategylist = [optbe_covered_call_list,optbe_protective_put_list,optbe_collar_list,optbe_long_call_strategy_list,optbe_long_call_spread_list,optbe_short_put_spread_list,optbe_short_put_strategy_list,optbe_long_combination_list]


        #TODO:
        #Cash-secured put
        #Fig leag
        #Skip strike
        #Butterfly with puts
        #Front spread with puts

        
    if strategytype == 4: #profit below price delta point
        
        #4.1.  Long put
        print("Optimizing long put")
        print(" ")
        long_put_strategy_list = listfactory.BuildLongPut()
        optbe_long_put_strategy_list = OptimizeOneBreakEven(long_put_strategy_list ,breakeven)
        OptimizeCostMinprofit(optbe_long_put_strategy_list)

        print("--- %s seconds ---" % (time.time() - start_time))

        #4.2.  Long put spread
        print("Optimizing long put spread")
        print(" ")
        long_put_spread_list = listfactory.BuildLongPutSpread()
        optbe_long_put_spread_list = OptimizeOneBreakEven(long_put_spread_list ,breakeven)
        OptimizeCostMaxminratio(optbe_long_put_spread_list)
        
        print("--- %s seconds ---" % (time.time() - start_time))

        #4.3.  Short call spread
        print("Optimizing short call spread")
        print(" ")
        short_call_spread_list = listfactory.BuildShortCallSpread()
        optbe_short_call_spread_list = OptimizeOneBreakEven(short_call_spread_list,breakeven)
        OptimizeCostMaxminratio(optbe_short_call_spread_list)
        
        print("--- %s seconds ---" % (time.time() - start_time))

        #4.4.  Short call
        print("Optimizing short call")
        print(" ")
        short_call_strategy_list = listfactory.BuildShortCall()
        optbe_short_call_strategy_list = OptimizeOneBreakEven(short_call_strategy_list ,breakeven)
        OptimizeCostMaxprofit(optbe_short_call_strategy_list)
        
        print("--- %s seconds ---" % (time.time() - start_time))

        #4.5.  Short combination
        print("Optimizing short combination")
        print(" ")
        short_combination_list = listfactory.BuildShortCombination()
        optbe_short_combination_list = OptimizeOneBreakEven(short_combination_list ,breakeven)
        OptimizeCost(optbe_short_combination_list)

        print("--- %s seconds ---" % (time.time() - start_time))

        strategylist = [optbe_long_put_strategy_list,optbe_long_put_spread_list,optbe_short_call_spread_list,optbe_short_call_strategy_list,optbe_short_combination_list]


        #TODO:
        #Skip strike butterfly with calls
        #Front spread with calls

       
    return strategylist

def FilterStrikeNearStock(inputlist,stock,tolerance):

    #This function filters out options with strike too far from current stock price
    #inputs: list of options, underlying stock, tolerance level
    #outputs: filtered list
     
    lowbound = (1 - tolerance) * stock.price
    upbound = (1 + tolerance) * stock.price

    lowfilter = [x for x in inputlist if  x.strike >= lowbound]
    highfilter = [x for x in lowfilter if x.strike <= upbound]

    return highfilter

def OptimizeOneBreakEven(strategylist,desiredbreakeven):

    #This function filters strategies that have a single break even too far from the desired level
    #inputs: list of strategies, break even point
    #output: filtered list of strategies

    mindelta = 1000

    for strategy in strategylist:
        delta1 = math.fabs(desiredbreakeven - strategy.breakeven)
        if delta1 < mindelta:
            mindelta = delta1

    if mindelta < 0.01:
        precision = 60
    elif mindelta <= 0.02:
        precision = 20
    elif mindelta <= 0.05:
        precision = 6
    elif mindelta <= 0.2:
        precision = 3
    elif mindelta <= 0.5:
        precision = 2
    elif mindelta <= 1:
        precision = 1.3
    elif mindelta <= 2:
        precision = 0.2
    else:
        precision = 0.01

    optimized_list = []

    for strategy in strategylist:
        if ((strategy.breakeven <= (desiredbreakeven + mindelta + (precision * mindelta))) and (strategy.breakeven >= (desiredbreakeven - mindelta - (precision * mindelta)))):
            optimized_list.append(strategy)

    return optimized_list

def OptimizeTwoBreakEven(strategylist,desiredbreakeven):
    
    #This function filters strategies that have both break even points too far from the desired level
    #inputs: list of strategies, break even point
    #output: filtered list of strategies

    opt_coeff = 1000

    for strategy in strategylist:
        delta_l = math.fabs(desiredbreakeven[0] - float(strategy.breakeven[0]))
        delta_r = math.fabs(desiredbreakeven[1] - float(strategy.breakeven[1]))
        coeff = delta_l ** 2 + delta_r ** 2
        if coeff < opt_coeff:
            opt_coeff = coeff

    if opt_coeff < 0.01:
        precision = 60
    elif opt_coeff <= 0.02:
        precision = 20
    elif opt_coeff <= 0.05:
        precision = 6
    elif opt_coeff <= 0.2:
        precision = 3
    elif opt_coeff <= 0.5:
        precision = 2
    elif opt_coeff <= 1:
        precision = 1
    elif opt_coeff <= 2:
        precision = 0.1
    else:
        precision = 0.01
  
    optimized_list = []
    
    for strategy in strategylist:
        delta_l = strategy.breakeven[0] - desiredbreakeven[0]
        delta_r = strategy.breakeven[1] - desiredbreakeven[1]
        coeff = delta_l ** 2 + delta_r ** 2
        if (coeff <= (opt_coeff + (precision * opt_coeff))):
            optimized_list.append(strategy)

    return optimized_list

def OptimizeCostMaxprofit(strategy_list):

    #This function orders strategies by their max profit and cost
    #input: list of strategies
    #output: None (input list is affected)

    strategy_list.sort(key=lambda x: x.cost, reverse = True)
    strategy_list.sort(key=lambda x: x.maxprofit, reverse = True)

    pass

def OptimizeCostMinprofit(strategy_list):

    #This function orders strategies by their min profit and cost
    #input: list of strategies
    #output: None (input list is affected)

    strategy_list.sort(key=lambda x: x.cost, reverse = True)
    strategy_list.sort(key=lambda x: x.minprofit)

    pass

def OptimizeCostMaxminratio(strategy_list):

    #This function orders strategies by their min max profit ration and cost
    #input: list of strategies
    #output: None (input list is affected)

    strategy_list.sort(key=lambda x: x.cost, reverse = True)
    strategy_list.sort(key=lambda x: math.fabs(x.maxprofit / x.minprofit), reverse = True)

    pass

def OptimizeCost(strategy_list):

    #This function orders strategies by their cost
    #input: list of strategies
    #output: None (input list is affected)

    strategy_list.sort(key=lambda x: x.cost, reverse = True)

    pass

def CreateGraph(n,strategy,stock):

    #This function graphs the returns of a given strategy
    #inputs: figure number counter, strategy, underlying stock
    #outputs: None (creates plt.plot of the strategy)

    yrange = 12
    if strategy.maxprofit > 12:
        yrange = strategy.maxprofit + 5
    if (((math.fabs(strategy.minprofit)) > yrange) and (strategy.minprofit != -999)):
        yrange = (math.fabs(strategy.minprofit)) + 5


    plt.figure(n)
    plt.title(strategy.name + " profit curve")
    plt.xlabel("Stock price delta at maturity (%)")
    plt.ylabel("Profit ($)")
    plt.ylim([-yrange,yrange])
    plt.grid(True)
    plt.axhline(0, color='blue', linewidth = 0.3)
    plt.axvline(0, color='blue', linewidth = 0.3)
    

    plt.plot(100 * ((strategy.priceatmaturity - stock.price) / stock.price),strategy.profit,color = 'red')

    return

def PrintData2(strategy):

    #This function prints the text details of a given strategy
    #inputs: strategy
    #outputs: None (prints the details on the text box)

    display_frame.insert(END,"Strategy: " + str(strategy.name) + "\n",'BLUE')
    display_frame.insert(END,"Cost: $%.2f \n" % (strategy.cost))
    if strategy.maxprofit != -999:
        display_frame.insert(END,"Max cte profit: $%.2f \n" % (strategy.maxprofit))
    if strategy.minprofit != -999:
        display_frame.insert(END,"Max cte loss: $%.2f \n" % (strategy.minprofit))

    if isinstance(strategy.breakeven,float):
        display_frame.insert(END,"Breakeven: %.2f%% \n" % (strategy.breakeven))
    else:
        display_frame.insert(END,"Low breakeven: %.2f%% \n" % (strategy.breakeven[0]))
        display_frame.insert(END,"High breakeven: %.2f%% \n" % (strategy.breakeven[1]))

    display_frame.insert(END,"Risk profile: " + str(strategy.risk) + "/4 \n")
    display_frame.insert(END,"Options: \n")
    currentasset = strategy.asset1
    if currentasset.tag != "dummy":
        display_frame.insert(END,str(strategy.qtty1) + "x " + str(currentasset.positiontype) + str(currentasset.tag) + " | Maturity: " + str(int(currentasset.matyear)) + "-" + str(int(currentasset.matmonth)) + "-" + str(int(currentasset.matday)) + "\n")
    currentasset = strategy.asset2
    if currentasset.tag != "dummy":
        display_frame.insert(END,str(strategy.qtty2) + "x " + str(currentasset.positiontype) + str(currentasset.tag) + " | Maturity: " + str(int(currentasset.matyear)) + "-" + str(int(currentasset.matmonth)) + "-" + str(int(currentasset.matday)) + "\n")
    currentasset = strategy.asset3
    if currentasset.tag != "dummy":
        display_frame.insert(END,str(strategy.qtty3) + "x " + str(currentasset.positiontype) + str(currentasset.tag) + " | Maturity: " + str(int(currentasset.matyear)) + "-" + str(int(currentasset.matmonth)) + "-" + str(int(currentasset.matday)) + "\n")
    currentasset = strategy.asset4
    if currentasset.tag != "dummy":
        display_frame.insert(END,str(strategy.qtty4) + "x " + str(currentasset.positiontype) + str(currentasset.tag) + " | Maturity: " + str(int(currentasset.matyear)) + "-" + str(int(currentasset.matmonth)) + "-" + str(int(currentasset.matday)) + "\n")

    display_frame.insert(END,"\n")

    pass

def FilterVolume(rawtable):

    #This function filters out options with zero volume
    #inputs: unordered options data
    #outputs: filtered unordered options data

    row,col = rawtable.shape
    idx = []


    i = 0
    while i < row:
        if ((rawtable[i,6] == 0) and (rawtable[i,7] == 0)):
            idx.append(i)
        i = i + 1
    
    rawtable = np.delete(rawtable, idx,axis = 0)
    

    return rawtable

def FilterMaturity(rawtable,maxmat,minmat):

    #This function filters out options with maturity below the minimum desired maturity or with maturity above the desired maximum maturity
    #inputs: unordered options data, maximum maturity (in days), minimum maturity (in days)
    #outputs: filtered unordered data

    row,col = rawtable.shape
    idxm = []

    i = 0

    while i < row:
        maturitydate = date(int(rawtable[i,5]),int(rawtable[i,4]),int(rawtable[i,3]))
        currentdate = date.today()
        delta = maturitydate - currentdate
        timetomat = float(delta.days)
        if ((timetomat > maxmat) or (timetomat < minmat)):
            idxm.append(i)
        i = i + 1

    rawtable = np.delete(rawtable, idxm,axis = 0)

    return rawtable

def FilterStrike(rawtable,tolstrike,stock):

    #This function filters out options with strike below the low treshold or above the high treshold
    #inputs: unordered opitons data, tolerance, underlying stock
    #outputs: filtered unordered options data

    filterlow = stock.price - (stock.price * tolstrike)
    filterhigh = stock.price + (stock.price * tolstrike)

    filter_result = rawtable[(rawtable[:,0] <= filterhigh) & (rawtable[:,0] >= filterlow)]

    return filter_result

def ConvertStrategyInput(dropdown):

    #This function converts the dropdown choice on the GUI for the profit profile into an integer 
    #input: dropodown user choice
    #output: corresponding strategy integer

    if dropdown == '1. Profit inside price delta interval':
        type = 1
    elif dropdown == '2. Profit outside price delta interval':
        type = 2
    elif dropdown == '3. Profit above price delta point':
        type = 3
    else:
        type = 4

    return type

def ReadBEGUI(strategy):
    
    #This function correlates the coice of profit profile to the field on the GUI for the break even points
    #input: profit profile type integer
    #output: corresponding break even get

    if ((strategy == 1) or (strategy == 2)):
        breakeven = np.empty(2)
        breakeven[0] = float(be_entry1.get())
        breakeven[1] = float(be_entry2.get())
    else:
        breakeven = float(be_entry3.get())

    return breakeven

def SetTolParams(tolerance):

    #This function maps the level of tolerance chosen on the GUI to the tolerance constants used in other functions
    #input: GUI tolerance level choice
    #outptu: respective tolerance constants

    if tolerance == 1:
        tolfil = 0.015
        tolstrike = 0.15
    elif tolerance == 2:
        tolfil = 0.03
        tolstrike = 0.25
    else:
        tolfil = 0.05
        tolstrike = 0.35

    return tolfil,tolstrike

def InterfaceStart():

    #USER INTERFACE

    root = Tk()
    root.title("Option Strategy Optimization")
    root.wm_iconbitmap('icon.ico')
    root.configure(background='white')

    #Frames
    param_frame = Frame(root,bg = 'white')
    param_frame.grid(row = 0, column = 0)

    button_frame = Frame(root,bg = 'white')
    button_frame.grid(row = 1, column = 0)

    global display_frame
    display_frame = Text(root,bg = 'white',height = 30,width = 55)
    display_frame.grid(row = 0,column = 1,rowspan = 2)
    display_frame.tag_config('RED', foreground='red')
    display_frame.tag_config('BLUE', foreground='blue')

    #Parameter Frame:

    #Title
    Label(param_frame, text = "Select desired parameters:", fg = "blue",bg = 'white', font = 'Bold').grid(row=0,columnspan=10,pady=20) 

    #Param column 1 - Strategy

    #Title
    Label(param_frame, text = "Strategy Parameters", fg = "red",bg = 'white').grid(row=1,columnspan=3,pady=20)

    #Strategy Type
    global profitprofile_input 
    profitprofile_input = StringVar(root)  #TEST WHAT IS THIS?  NEEDED TO TAKE INPUT
    Label(param_frame, text = "Profit Profile: ",bg = 'white').grid(row=2,column=0,sticky=E,pady=5)
    type_menu = OptionMenu(param_frame,profitprofile_input,"1. Profit inside price delta interval","2. Profit outside price delta interval","3. Profit above price delta point","4. Profit below price delta point")
    type_menu.grid(row = 2,column=1,columnspan = 2,sticky=W,padx=10,pady=5)
    
    #Minimum Maturity
    global minmat_entry
    Label(param_frame, text = "Min Maturity: ",bg = 'white').grid(row=3,column=0,sticky=E,pady=5)
    minmat_entry = Entry(param_frame,width=6)
    minmat_entry.grid(row=3,column=1)
    minmat_entry.insert(INSERT,-1000)
    Label(param_frame, text = "(days)",fg = 'gray',bg = 'white').grid(row=3,column=2,sticky=W,padx=10,pady=5)

    #Maximum Maturity
    global maxmat_entry
    Label(param_frame, text = "Max Maturity: ",bg = 'white').grid(row=4,column=0,sticky=E,pady=5)
    maxmat_entry = Entry(param_frame,width=6)
    maxmat_entry.grid(row=4,column=1)
    maxmat_entry.insert(INSERT,1000)
    Label(param_frame, text = "(days)",fg = 'gray',bg = 'white').grid(row=4,column=2,sticky=W,padx=10,pady=5)



    #Param column 2 - Break Even

    #Title
    Label(param_frame, text = "Profit Break Even",fg = "red",bg = 'white').grid(row=1,column=3,columnspan = 4,pady=20)

    #Type 1,2:
    global be_entry1
    global be_entry2
    Label(param_frame, text = 'Profiles 1 & 2: ',bg = 'white').grid(row=2,column=3, pady=5)
    Label(param_frame, text = "Low: ",bg = 'white').grid(row=2,column = 4,sticky=E,pady=5)
    be_entry1 = Entry(param_frame,width=6)
    be_entry1.grid(row=2,column=5,sticky=W)
    be_entry1.insert(INSERT,-2)
    Label(param_frame, text = "(%)",fg = 'gray',bg = 'white').grid(row=2,column=6,sticky=W,padx=10,pady=5)
    Label(param_frame, text = "High: ",bg = 'white').grid(row=3,column = 4,sticky=E,pady=5)
    be_entry2 = Entry(param_frame,width=6)
    be_entry2.grid(row=3,column=5,sticky=W)
    be_entry2.insert(INSERT,3)
    Label(param_frame, text = "(%)",fg = 'gray',bg = 'white').grid(row=3,column=6,sticky=W,padx=10,pady=5)

    #Type 3,4:
    global be_entry3
    Label(param_frame, text = 'Profiles 3 & 4: ',bg = 'white').grid(row=4,column=3,pady=5)
    Label(param_frame, text = "Point: ",bg = 'white').grid(row=4,column = 4,sticky=E, pady=5)
    be_entry3 = Entry(param_frame,width=6)
    be_entry3.grid(row=4,column=5,sticky=W)
    be_entry3.insert(INSERT,-1)
    Label(param_frame, text = "(%)",fg = 'gray',bg = 'white').grid(row=4,column=6,sticky=W,padx=10,pady=5)



    #Param column 2 - Settings

    #Title
    Label(param_frame, text = "Algorithm Settings",fg = "red",bg = 'white').grid(row=1,column=7,columnspan = 3,pady=20)

    #Transaction Fee
    global tfee_entry
    Label(param_frame, text = "Per contract fee: ",bg = 'white').grid(row=2,column=7,sticky=E,pady=5)
    tfee_entry = Entry(param_frame,width=6)
    tfee_entry.grid(row=2,column=8)
    tfee_entry.insert(INSERT,0.00)
    Label(param_frame, text = "($)",fg = 'gray',bg = 'white').grid(row=2,column=9,sticky=W,padx=10,pady=5)

    #Graph Precision
    global precision_entry
    Label(param_frame, text = "Graph Precision: ",bg = 'white').grid(row=3,column=7,sticky=E,pady=5)
    precision_entry = Entry(param_frame,width=6)
    precision_entry.grid(row=3,column=8)
    precision_entry.insert(INSERT,200)
    Label(param_frame, text = "(100-1000)",fg = 'gray',bg = 'white').grid(row=3,column=9,sticky=W,padx=10,pady=5)

    #Tolerance
    global tolerance_entry
    Label(param_frame, text = "Optimization Tolerance: ",bg = 'white').grid(row=4,column=7,sticky=E,pady=5)
    tolerance_entry = Entry(param_frame,width=6)
    tolerance_entry.grid(row=4,column=8)
    tolerance_entry.insert(INSERT,2)
    Label(param_frame, text = "(1-3)",fg = 'gray',bg = 'white').grid(row=4,column=9,sticky=W,padx=10,pady=5)

    #Xaxisrange
    global xaxisrange_entry
    Label(param_frame, text = "x-axis Range: ",bg = 'white').grid(row=5,column=7,sticky=E,pady=5)
    xaxisrange_entry = Entry(param_frame,width=6)
    xaxisrange_entry.grid(row=5,column=8)
    xaxisrange_entry.insert(INSERT,0.20)
    Label(param_frame, text = "(0.05-1.0)",fg = 'gray',bg = 'white').grid(row=5,column=9,sticky=W,padx=10,pady=5)

    #Button Frame:

    #Run Button
    run_button = Button(button_frame, text = "Generate Strategies", bg = "blue", fg = "white", font = 'Bold',cursor = 'hand2')
    run_button.grid(row=1,columnspan = 10,pady=20)
    run_button.bind("<Button-1>",main)

    root.mainloop()

    pass

def main(event):

    #MAIN EXECUTABLE

    global start_time
    start_time = time.time()                                                                          #Setting base time for software performace measurement

    currentdate = str(datetime.datetime.now())
    rawquotetable, rootstock = LoadTable()                                                            #Loading raw table
                                                                                                     
                                                                                                     
    #1.  Reading GUI inputs
    strategyinput = ConvertStrategyInput(profitprofile_input.get())                                   #Receiving desired strategy
    minmaturity = float(minmat_entry.get())                                                          
    maxmaturity = float(maxmat_entry.get())                                                          
                                                                                                     
    breakeven = ReadBEGUI(strategyinput)                                                              #Receiving
                                                                                                      #desired break
                                                                                                      #even point(s)
                                                                                                     
    fee = float(tfee_entry.get())                                                                     #Receiving
                                                                                                      #transaction
                                                                                                      #fee
    graphprecision = int(precision_entry.get())                                                       #Receiving desired graph
                                                                                                      #precision
    StrategyBase.SetGraphPrecision(graphprecision)                                                    #Setting graph precision
    tolerance = int(tolerance_entry.get())                                                            #Receiving desired
                                                                                                      #strike price
                                                                                                      #tolerance
    tolfil,tolstrike = SetTolParams(tolerance)                                                       
    xaxisrange = float(xaxisrange_entry.get())                                                        #Receiving desired
                                                                                                      #x-axis range
    StrategyBase.SetXaxisrange(xaxisrange)                                                            #Setting graph
                                                                                                      #x-axis range
    
    #2.  Printing input parameters:

    display_frame.insert(END,"----------------------------- \n",'RED')
    display_frame.insert(END,"Strategy Generator Parameters \n \n",'RED')
    display_frame.insert(END,"Underlying asset: " + str(rootstock.assetname) + "\n")
    display_frame.insert(END,"Current price: " + str(rootstock.price) + "\n")
    display_frame.insert(END,"Date and time: " + str(currentdate) + "\n")
    display_frame.insert(END,"Strategy type: " + str(strategyinput) + "\n")
    display_frame.insert(END,"Maturity range: " + str(int(minmaturity)) + " - " + str(int(maxmaturity)) + "\n")
    if isinstance(breakeven,float):
        display_frame.insert(END,"Desired breakeven: %.2f%% \n" % (breakeven))
    else:
        display_frame.insert(END,"Desired low breakeven: %.2f%% \n" % (breakeven[0]))
        display_frame.insert(END,"Desired high breakeven: %.2f%% \n" % (breakeven[1]))
    display_frame.insert(END,"Transaction fee: " + str(fee) + "\n")
    display_frame.insert(END,"Tolerance: " + str(tolerance) + "\n")
    display_frame.insert(END,"Graph precision: " + str(graphprecision) + "\n")
    display_frame.insert(END,"----------------------------- \n",'RED')
    display_frame.insert(END, "\n")


    #3.  Processing raw table
                                                                                                     
    print("Processing raw table")                                                                    
    print(" ")                                                                                       
                                                                                                     
    calltable,puttable,tag_call,tag_put = CleanTable(rawquotetable,rootstock.assetname)               #Cleaning and splitting loaded raw table
                                                                                                     
    calltable = FilterVolume(calltable)                                                               #Filtering
                                                                                                      #non-tradable
                                                                                                      #options
    puttable = FilterVolume(puttable)                                                                 #Filtering
                                                                                                      #non-tradable
                                                                                                      #options
                                                                                                     
    calltable = FilterMaturity(calltable,maxmaturity,minmaturity)                                    #Filtering by desired maturity range
    puttable = FilterMaturity(puttable,maxmaturity,minmaturity)                                       #Filtering by desired maturity range
                                                                                                     
    calltable = FilterStrike(calltable,tolstrike,rootstock)                                           #Filtering by strike price
    puttable = FilterStrike(puttable,tolstrike,rootstock)                                             #Filtering by strike price
                                                                                                     
                                                                                                     
    #4.  Creating options
                                                                                                     
    print("Creating list of options")                                                                
    print(" ")                                                                                       
                                                                                                     
    short_call_list = CreateOptionList("short_call",calltable,tag_call)                               #Creating list of available short call positions
    long_call_list = CreateOptionList("long_call",calltable,tag_call)                                 #Creating list of available long call
                                                                                                      #positions
    short_put_list = CreateOptionList("short_put",puttable,tag_put)                                   #Creating list of available short put
                                                                                                      #positions
    long_put_list = CreateOptionList("long_put",puttable,tag_put)                                     #Creating list of available long put
                                                                                                      #positions
                                                                                                     
    tolfil_short_call_list = FilterStrikeNearStock(short_call_list,rootstock,tolfil)                  #Filtering by tolerance
    tolfil_long_call_list = FilterStrikeNearStock(long_call_list,rootstock,tolfil)                    #Filtering by tolerance
    tolfil_short_put_list = FilterStrikeNearStock(short_put_list,rootstock,tolfil)                    #Filtering by tolerance
    tolfil_long_put_list = FilterStrikeNearStock(long_put_list,rootstock,tolfil)                      #Filtering by tolerance
                                                                                                     

    #5.  Creating and optimizing Strategies

    print("Optimizing strategies")
    print(" ")

    #Building list of optimized strategies
    strategy_matrix = BuildListOptmizedStrategies(strategyinput,breakeven,rootstock,short_call_list,long_call_list,short_put_list,long_put_list,tolfil_short_call_list,tolfil_long_call_list,tolfil_short_put_list,tolfil_long_put_list,fee) 
    

    #6.  Printing results

    no_strategies = len(strategy_matrix)
    
    i = 0

    while i < no_strategies:
        PrintData2(strategy_matrix[i][0])                                                              #Printing
                                                                                                       #information
                                                                                                       #about optimal
                                                                                                       #strategies
        CreateGraph(i + 1,strategy_matrix[i][0],rootstock)                                              #Printing graphs
        i = i + 1
    display_frame.see(END)
    print("--- %s seconds ---" % (time.time() - start_time))

    plt.show()


    pass

if __name__ == '__main__': 

    InterfaceStart()
