import datetime
from AssetModule import Asset
from StockModule import Stock
from collections import deque
import time

from Strategy_Folder.Strategy11 import Strategy11
from Strategy_Folder.Strategy12 import Strategy12
from Strategy_Folder.Strategy13 import Strategy13
from Strategy_Folder.Strategy14 import Strategy14
from Strategy_Folder.Strategy15 import Strategy15
from Strategy_Folder.Strategy21 import Strategy21
from Strategy_Folder.Strategy22 import Strategy22
from Strategy_Folder.Strategy23 import Strategy23
from Strategy_Folder.Strategy24 import Strategy24
from Strategy_Folder.Strategy31 import Strategy31
from Strategy_Folder.Strategy32 import Strategy32
from Strategy_Folder.Strategy33 import Strategy33
from Strategy_Folder.Strategy34 import Strategy34
from Strategy_Folder.Strategy35 import Strategy35
from Strategy_Folder.Strategy36 import Strategy36
from Strategy_Folder.Strategy37 import Strategy37
from Strategy_Folder.Strategy38 import Strategy38
from Strategy_Folder.Strategy41 import Strategy41
from Strategy_Folder.Strategy42 import Strategy42
from Strategy_Folder.Strategy43 import Strategy43
from Strategy_Folder.Strategy44 import Strategy44
from Strategy_Folder.Strategy45 import Strategy45

class StrategyListFactory:

    def __init__(self,stock_in,short_call_list_in,long_call_list_in,short_put_list_in,long_put_list_in,tolfil_short_call_list_in,tolfil_long_call_list_in,tolfil_short_put_list_in,tolfil_long_put_list_in,fee):

        self.stock = stock_in
        self.short_call_list = short_call_list_in
        self.long_call_list = long_call_list_in
        self.short_put_list = short_put_list_in
        self.long_put_list = long_put_list_in
        self.tolfil_short_call_list = tolfil_short_call_list_in
        self.tolfil_long_call_list = tolfil_long_call_list_in
        self.tolfil_short_put_list = tolfil_short_put_list_in
        self.tolfil_long_put_list = tolfil_long_put_list_in
        self.fee = fee
        pass


    #1.1. Long butterfly call
    def BuildLongButterflyCall(self): 

        strategy_list = []

        for short in self.tolfil_short_call_list:
            for longleft in self.long_call_list:
                if ((longleft.strike < short.strike) and (longleft.matmonth == short.matmonth)):
                    for longright in self.long_call_list:
                        if ((longright.strike > short.strike) and (longright.matmonth == longleft.matmonth)):
                            strategy_list.append(Strategy11(self.stock,asset1=longleft,qtty1=1,asset2=short,qtty2=2,asset3=longright,qtty3=1,fee = self.fee))

        return strategy_list


    #1.2. Long butterfly put
    def BuildLongButterflyPut(self):

        strategy_list = []

        for short in self.tolfil_short_put_list:
            for longleft in self.long_put_list:
                if ((longleft.strike < short.strike) and (longleft.matmonth == short.matmonth)):
                    for longright in self.long_put_list:
                        if ((longright.strike > short.strike) and (longright.matmonth == longleft.matmonth)):
                            strategy_list.append(Strategy12(self.stock,asset1=longleft,qtty1=1,asset2=short,qtty2=2,asset3=longright,qtty3=1,fee = self.fee))

        return strategy_list


    #1.3. Iron butterfly (PROCESSING TIME IS TOO LONG)
    def BuildIronButterflyPut(self):
    
        strategy_list = []
        #start_time2 = time.time()
    
        for shortput in self.tolfil_short_put_list:
            for shortcall in self.short_call_list:
                if ((shortcall.strike == shortput.strike)and(shortcall.matmonth == shortput.matmonth)):
                    for longput in self.long_put_list:
                        if ((longput.strike < shortput.strike)and(longput.matmonth == shortcall.matmonth)):
                            for longcall in self.long_call_list:
                                if ((longcall.strike>shortput.strike)and(longcall.matmonth==longput.matmonth)):
                                    strategy_list.append(Strategy13(self.stock,asset1 = longput,qtty1=1,asset2=shortput,qtty2=1,asset3=shortcall,qtty3=1,asset4=longcall,qtty4=1,fee = self.fee))
                                    #print("--- %s seconds ---" % (time.time() - start_time2))
    
        return strategy_list
    

    #1.4. Short straddle
    def BuildShortStraddle(self):

        strategy_list = []

        for call in self.tolfil_short_call_list:
            for put in self.short_put_list:
                if ((put.matmonth == call.matmonth) and (put.strike == call.strike)):
                    strategy_list.append(Strategy14(self.stock,asset1=call,qtty1=1,asset2=put,qtty2=1,fee = self.fee))

        return strategy_list


    #1.5. Short strangle
    def BuildShortStrangle(self):

        strategy_list = []

        for put in self.short_put_list:
            if put.strike < self.stock.price:
                for call in self.short_call_list:
                    if call.strike > self.stock.price:
                        strategy_list.append(Strategy15(self.stock,asset1=put,qtty1=1,asset2=call,qtty2=1,fee = self.fee))

        return strategy_list


    #2.1. Long straddle
    def BuildLongStraddle(self):

        strategy_list = []

        for call in self.tolfil_long_call_list:
            for put in self.long_put_list:
                if ((put.strike == call.strike)and(put.matmonth==call.matmonth)):
                    strategy_list.append(Strategy21(self.stock,asset1=call,qtty1=1,asset2=put,qtty2=1,fee = self.fee))
 
        return strategy_list
   

    #2.2. Long strangle
    def BuildLongStrangle(self):

        strategy_list = []

        for put in self.long_put_list:
            if put.strike < self.stock.price:
                for call in self.long_call_list:
                    if ((call.strike>self.stock.price) and (call.matmonth == put.matmonth)):
                        strategy_list.append(Strategy22(self.stock,asset1=put,qtty1=1,asset2=call,qtty2=1,fee = self.fee))

        return strategy_list


    #2.3. back spread call
    def BuildBackSpreadCall(self):

        strategy_list = []

        for short in self.tolfil_short_call_list:
            for long in self.long_call_list:
                if ((long.strike > short.strike) and (long.matmonth == short.matmonth) and (((-2) * long.price + short.price)>0)):
                    strategy_list.append(Strategy23(self.stock,asset1=short,qtty1=1,asset2=long,qtty2=2,fee = self.fee))

        return strategy_list


    #2.4. back spread put
    def BuildBackSpreadPut(self):

        strategy_list = []

        for short in self.tolfil_short_put_list:
            for long in self.long_put_list:
                if ((long.strike < short.strike) and (long.matmonth == short.matmonth) and (((-2) * long.price + short.price)>0)):
                    strategy_list.append(Strategy24(self.stock,asset1=long,qtty1=2,asset2=short,qtty2=1,fee = self.fee))

        return strategy_list


    #3.1. Covered call
    def BuildCoveredCall(self):

        strategy_list = []

        for option in self.short_call_list:
            if option.strike > self.stock.price:
                strategy_list.append(Strategy31(self.stock,stockqtty=1,asset1=option,qtty1=1,fee = self.fee))

        return strategy_list


    #3.2. Protective put
    def BuildProtectivePut(self):

        strategy_list = []

        for option in self.long_put_list:
            if option.strike < self.stock.price:
                strategy_list.append(Strategy32(self.stock,stockqtty=1,asset1=option,qtty1=1,fee = self.fee))

        return strategy_list


    #3.3. Collar
    def BuildCollar(self):

        strategy_list = []

        for put in self.long_put_list:
            if put.strike < self.stock.price:
                for call in self.short_call_list:
                    if ((call.strike > self.stock.price) and (put.matmonth == call.matmonth)):
                        strategy_list.append(Strategy33(self.stock,stockqtty=1,asset1=put,qtty1=1,asset2=call,qtty2=1,fee = self.fee))

        return strategy_list


    #3.4. Long call
    def BuildLongCall(self):

        strategy_list = []

        for call in self.long_call_list:
            if call.strike <= self.stock.price:
                strategy_list.append(Strategy34(self.stock,asset1 = call,qtty1 = 1,fee = self.fee))

        return strategy_list


    #3.5. Long call spread
    def BuildLongCallSpread(self):

        strategy_list = []

        for long in self.long_call_list:
            if long.strike <= self.stock.price:
                for short in self.short_call_list:
                    if ((short.strike > self.stock.price) and (long.matmonth == short.matmonth)):
                        strategy_list.append(Strategy35(self.stock,asset1 = long,qtty1 = 1,asset2 = short,qtty2=1,fee = self.fee))

        return strategy_list


    #3.6. Short put spread
    def BuildShortPutSpread(self):

        strategy_list = []

        for short in self.short_put_list:
            if short.strike > self.stock.price:
                for long in self.long_put_list:
                    if ((short.price > long.price) and (short.strike > long.strike)and (short.matmonth == long.matmonth)): 
                       strategy_list.append(Strategy36(self.stock,asset1=long,qtty1=1,asset2=short,qtty2=1,fee = self.fee)) 

        return strategy_list


    #3.7. Short put
    def BuildShortPut(self):

        strategy_list = []

        for put in self.short_put_list:
            if (put.strike < self.stock.price):
                strategy_list.append(Strategy37(self.stock,asset1=put,qtty1=1,fee = self.fee))

        return strategy_list

    
    #3.8. Long combination
    def BuildLongCombination(self):

        strategy_list = []

        for call in self.tolfil_long_call_list:
            for put in self.short_put_list:
                if ((put.matmonth == call.matmonth) and (put.strike == call.strike)):
                    strategy_list.append(Strategy38(self.stock,asset1=call,qtty1=1,asset2=put,qtty2=1,fee = self.fee))

        return strategy_list


    #4.1. Long put
    def BuildLongPut(self):

        strategy_list = []

        for put in self.long_put_list:
            if put.strike <= self.stock.price:
                strategy_list.append(Strategy41(self.stock,asset1 = put,qtty1 = 1,fee = self.fee))

        return strategy_list


    #4.2. Long put spread
    def BuildLongPutSpread(self):
    
        strategy_list = []

        for short in self.short_put_list:
            if short.strike < self.stock.price:
                for long in self.long_put_list:
                    if ((long.strike >= self.stock.price) and (short.matmonth == long.matmonth)):
                        strategy_list.append(Strategy42(self.stock,asset1=short,qtty1=1,asset2=long,qtty2=1,fee = self.fee))

        return strategy_list


    #4.3. Short call spread
    def BuildShortCallSpread(self):

        strategy_list = []

        for short in self.short_call_list:
            if short.strike > self.stock.price:
                for long in self.long_call_list:
                    if ((short.price > long.price) and (long.strike > short.strike) and (short.matmonth == long.matmonth)):
                        strategy_list.append(Strategy43(self.stock,asset1=short,qtty1=1,asset2=long,qtty2=1,fee = self.fee))

        return strategy_list


    #4.4. Short call
    def BuildShortCall(self):

        strategy_list = []

        for call in self.short_call_list:
            if (call.strike > self.stock.price):
                strategy_list.append(Strategy44(self.stock,asset1=call,qtty1=1,fee = self.fee))

        return strategy_list


    #4.5. Short combination
    def BuildShortCombination(self):

        strategy_list = []

        for call in self.tolfil_short_call_list:
            for put in self.long_put_list:
                if ((put.matmonth == call.matmonth) and (put.strike == call.strike)):
                    strategy_list.append(Strategy45(self.stock,asset1=call,qtty1=1,asset2=put,qtty2=1,fee = self.fee))

        return strategy_list

    pass

