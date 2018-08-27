#Module name: StrategyLib
#Has to be imported as follows: from StrategyLib import "Class"

#Importing SciPy libraries
import numpy as np
import matplotlib.pyplot as plt
import math


   #    i=0
   #    graphbreakflag = -1
   #    while i < self.graphprecision:
   #        if self.priceatmaturity[i] < asset1.strike:
   #            self.profit[i] = asset1.price
   #        else: 
   #            if graphbreakflag == -1:
   #                    graphbreakflag = i
   #            self.profit[i] = asset1.price - self.priceatmaturity[i] + asset1.strike
   #        i=i+1
   #
   #    self.maxprofit = asset1.price
   #    self.cost = asset1.price
   #    self.maxprofitindex = graphbreakflag
   #    self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
   #    self.risk = 4


   #     i=0
   #     while i < self.graphprecision:
   #         if self.priceatmaturity[i] < asset1.strike:
   #             self.profit[i] = -asset1.price + asset2.price -asset2.strike + self.priceatmaturity[i]
   #         else: 
   #             self.profit[i] = -asset1.price + asset2.price - asset1.strike + self.priceatmaturity[i]
   #         i=i+1
   #
   #         self.cost = asset2.price - asset1.price
   #         self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
   #         self.risk = 4



   #     i=0
   #     graphbreakflag = -1
   #     while i < self.graphprecision:
   #         if self.priceatmaturity[i] < asset1.strike:
   #             self.profit[i] = asset1.price + self.priceatmaturity[i] - asset1.strike
   #         else: 
   #             if graphbreakflag == -1:
   #                     graphbreakflag = i
   #             self.profit[i] = asset1.price
   #         i=i+1
   #
   #         self.maxprofit = asset1.price
   #         self.cost = asset1.price
   #         self.maxprofitindex = graphbreakflag
   #         self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
   #         self.risk = 4



   #     i=0
   #     graphbreakflaghigh = -1
   #     graphbreakflaglow = -1
   #     while i<self.graphprecision:
   #         if self.priceatmaturity[i]>asset2.strike:
   #             if graphbreakflaghigh == -1:
   #                 graphbreakflaghigh = i
   #             self.profit[i] = asset2.price-asset1.price
   #         elif self.priceatmaturity[i]<asset1.strike:
   #             self.profit[i] = asset2.price-asset1.price-asset2.strike+asset1.strike
   #         else:
   #             if graphbreakflaglow == -1:
   #                 graphbreakflaglow = i
   #             self.profit[i] = asset2.price-asset1.price-asset2.strike+self.priceatmaturity[i]
   #         i=i+1
   #     self.maxprofit = asset2.price-asset1.price
   #     self.maxprofitindex = graphbreakflaghigh
   #     self.minprofit = asset2.price-asset1.price-asset2.strike+asset1.strike
   #     self.minprofitindex = graphbreakflaglow
   #     self.cost = asset2.price - asset1.price
   #     self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
   #     self.risk = 3


   #     i=0
   #     graphbreakflaghigh = -1
   #     graphbreakflaglow = -1
   #     while i<self.graphprecision:
   #         if self.priceatmaturity[i]>asset2.strike:
   #             if graphbreakflaghigh == -1:
   #                 graphbreakflaghigh = i
   #             self.profit[i] = asset2.strike + asset2.price - asset1.price - asset1.strike
   #         elif self.priceatmaturity[i]<asset1.strike:
   #             self.profit[i] = asset2.price - asset1.price
   #         else:
   #             if graphbreakflaglow == -1:
   #                 graphbreakflaglow = i
   #             self.profit[i] = asset2.price - asset1.price - asset1.strike + self.priceatmaturity[i]
   #         i=i+1
   #     self.maxprofit = asset2.strike + asset2.price - asset1.price - asset1.strike
   #     self.maxprofitindex = graphbreakflaghigh
   #     self.minprofit = asset2.price - asset1.price
   #     self.minprofitindex = graphbreakflaglow
   #     self.cost = asset2.price - asset1.price
   #     self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
   #     self.risk = 2


   #     i=0
   #     graphbreakflaglow = -1
   #     graphbreakflaghigh = -1
   #     while i<self.graphprecision:
   #         if self.priceatmaturity[i] > asset2.strike: #max profit
   #             if graphbreakflaghigh == -1:
   #                 graphbreakflaghigh = i
   #             self.profit[i] = asset2.price + asset2.strike - stock.price - asset1.price
   #         elif self.priceatmaturity[i] < asset1.strike: #min profit
   #             self.profit[i] = asset1.strike - asset1.price - stock.price + asset2.price
   #         else:# in between no option exercised
   #             if graphbreakflaglow == -1:
   #                 graphbreakflaglow = i
   #             self.profit[i] = self.priceatmaturity[i] + asset2.price - asset1.price - stock.price
   #         i=i+1
   #     self.minprofit = asset1.strike - asset1.price - stock.price + asset2.price
   #     self.maxprofit = asset2.price + asset2.strike - stock.price - asset1.price
   #     self.minprofitindex = graphbreakflaglow
   #     self.maxprofitindex = graphbreakflaghigh
   #     self.cost = -stock.price - asset1.price + asset2.price
   #     self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
   #     self.risk = 1



   #     i = 0
   #     graphbreakflag = -1
   #     while i<self.graphprecision:
   #         if self.priceatmaturity[i] > asset1.strike:
   #             self.profit[i] = self.priceatmaturity[i] - asset1.price - stock.price
   #             if graphbreakflag == -1:
   #                 graphbreakflag = i
   #         else:
   #             self.profit[i] = asset1.strike - asset1.price - stock.price
   #         i=i+1
   #     self.minprofitindex = graphbreakflag
   #     self.minprofit = asset1.strike - asset1.price - stock.price
   #     self.cost = -stock.price - asset1.price
   #     self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
   #     self.risk = 1


   #     i=0
   #     graphbreakflag = -1
   #     while i<self.graphprecision:
   #         if self.priceatmaturity[i] > asset1.strike:
   #            self.profit[i] = asset1.price + asset1.strike - stock.price
   #         else:
   #            if graphbreakflag == -1:
   #                 graphbreakflag = i
   #            self.profit[i] = asset1.price + self.priceatmaturity[i] - stock.price 
   #         i=i+1
   #     self.maxprofitindex = graphbreakflag
   #     self.maxprofit = asset1.price + asset1.strike - stock.price
   #     self.cost = -stock.price+asset1.price
   #     self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
   #     self.risk = 1




   #     i = 0
   #     graphbreakflag = -1
   #     while i < self.graphprecision:
   #         if self.priceatmaturity[i] > asset1.strike:
   #             if graphbreakflag == -1:
   #                 graphbreakflag = i
   #             self.profit[i] = self.priceatmaturity[i] - asset1.strike - asset1.price
   #         else:
   #             self.profit[i] = -asset1.price
   #         i=i+1
   #     self.minprofit = -asset1.price
   #     self.minprofitindex = graphbreakflag
   #     self.cost = -asset1.price
   #     self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
   #     self.risk = 2




   #    i=0
   #    while i < self.graphprecision:
   #        if self.priceatmaturity[i] < asset1.strike:
   #            self.profit[i] = asset1.price - asset2.price +asset2.strike - self.priceatmaturity[i]
   #        else: 
   #            self.profit[i] = asset1.price - asset2.price + asset1.strike - self.priceatmaturity[i]
   #        i=i+1



    #    i=0
    #    graphbreakflaghigh = -1
    #    graphbreakflaglow = -1
    #    while i<self.graphprecision:
    #        if self.priceatmaturity[i] < asset1.strike:
    #            self.profit[i] = asset1.price - asset2.price
    #        elif self.priceatmaturity[i] > asset2.strike:
    #            if graphbreakflaglow == -1:
    #                    graphbreakflaglow = i
    #            self.profit[i] = asset1.price - asset2.price + asset1.strike - asset2.strike
    #        else:
    #            if graphbreakflaghigh == -1:
    #                graphbreakflaghigh = i
    #            self.profit[i] = asset1.price-asset2.price+asset1.strike-self.priceatmaturity[i]
    #        i=i+1
    #    self.maxprofit = asset1.price - asset2.price
    #    self.maxprofitindex = graphbreakflaghigh
    #    self.minprofit = asset1.price - asset2.price + asset1.strike - asset2.strike
    #    self.minprofitindex = graphbreakflaglow
    #    self.cost = asset1.price - asset2.price
    #    self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
    #    self.risk = 3




    #    i=0
    #    graphbreakflaghigh = -1
    #    graphbreakflaglow = -1
    #
    #    while i<self.graphprecision:
    #        if self.priceatmaturity[i] < asset1.strike:
    #            self.profit[i] = asset2.strike + asset1.price - asset2.price - asset1.strike
    #        elif self.priceatmaturity[i] >asset2.strike:
    #            if graphbreakflaglow == -1:
    #                graphbreakflaglow = i
    #            self.profit[i] = asset1.price - asset2.price
    #        else:
    #            if graphbreakflaghigh == -1:
    #                graphbreakflaghigh = i
    #            self.profit[i] = -asset2.price + asset1.price - self.priceatmaturity[i] + asset2.strike
    #        i=i+1
    #
    #    self.maxprofit = asset2.strike + asset1.price - asset2.price - asset1.strike
    #    self.maxprofitindex = graphbreakflaghigh
    #    self.minprofitindex = graphbreakflaglow
    #    self.minprofit = asset1.price - asset2.price
    #    self.cost = asset1.price - asset2.price
    #    self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
    #    self.risk = 2



  #     i = 0
  #     graphbreakflag = -1
  #     while i < self.graphprecision:
  #         if self.priceatmaturity[i] < asset1.strike:
  #             self.profit[i] = asset1.strike - self.priceatmaturity[i] - asset1.price
  #         else:
  #             if graphbreakflag == -1:
  #                 graphbreakflag = i
  #             self.profit[i] = -asset1.price
  #         i=i+1
  #     self.minprofit = -asset1.price
  #     self.minprofitindex = graphbreakflag
  #     self.cost = -asset1.price
  #     self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
  #     self.risk = 2




  #     i=0
  #     graphbreakflaglow = -1
  #     graphbreakflaghigh = -1
  #     while i<self.graphprecision:
  #         if self.priceatmaturity[i] < asset1.strike:
  #            self.profit[i] = (-2) * asset1.price + asset2.price - asset2.strike + (2*asset1.strike) - self.priceatmaturity[i]
  #         elif self.priceatmaturity[i] > asset2.strike:
  #            if graphbreakflaghigh == -1:
  #                 graphbreakflaghigh = i
  #            self.profit[i] = (-2) * asset1.price + asset2.price
  #         else:
  #            if graphbreakflaglow == -1:
  #                 graphbreakflaglow = i
  #            self.profit[i] = (-2) * asset1.price + asset2.price - asset2.strike + self.priceatmaturity[i] 
  #         i=i+1
  #     self.minprofitindex = graphbreakflaglow
  #     self.minprofit = self.profit[graphbreakflaglow]
  #     self.maxprofitindex = graphbreakflaghigh
  #     self.maxprofit = self.profit[graphbreakflaghigh]
  #     self.cost = (-2) * asset1.price + asset2.price
  #     self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
  #     self.risk = 3



 #       i=0
 #       graphbreakflaglow = -1
 #       graphbreakflaghigh = -1
 #       while i<self.graphprecision:
 #           if self.priceatmaturity[i] < asset1.strike:
 #              self.profit[i] = (-2) * asset2.price + asset1.price
 #           elif self.priceatmaturity[i] > asset2.strike:
 #              if graphbreakflaglow == -1:
 #                   graphbreakflaglow = i
 #              self.profit[i] = (-2) * asset2.price + asset1.price + asset1.strike - (2 * asset2.strike) + self.priceatmaturity[i]
 #           else:
 #              if graphbreakflaghigh == -1:
 #                   graphbreakflaghigh = i
 #              self.profit[i] = (-2) * asset2.price + asset1.price + asset1.strike - self.priceatmaturity[i] 
 #           i=i+1
 #       self.minprofitindex = graphbreakflaglow
 #       self.minprofit = self.profit[graphbreakflaglow]
 #       self.maxprofitindex = graphbreakflaghigh
 #       self.maxprofit = self.profit[graphbreakflaghigh]
 #       self.cost = (-2) * asset2.price + asset1.price
 #       self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
 #       self.risk = 3


     #   i=0
     #   graphbreakflaglow = -1
     #   graphbreakflaghigh = -1
     #   while i<self.graphprecision:
     #       if self.priceatmaturity[i] < asset1.strike:
     #          self.profit[i] = -asset1.price - asset2.price + asset1.strike - self.priceatmaturity[i]
     #       elif self.priceatmaturity[i] > asset2.strike:
     #          if graphbreakflaghigh == -1:
     #               graphbreakflaghigh = i
     #          self.profit[i] = -asset1.price -asset2.price - asset2.strike + self.priceatmaturity[i]
     #       else:
     #          if graphbreakflaglow == -1:
     #               graphbreakflaglow = i
     #          self.profit[i] = -asset1.price -asset2.price 
     #       i=i+1
     #   self.minprofitindex = graphbreakflaglow
     #   self.minprofit = -asset1.price -asset2.price
     #   self.maxprofitindex = graphbreakflaghigh
     #   self.cost = -asset1.price -asset2.price
     #   self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
     #   self.risk = 3







    #    i=0
    #    graphbreakflag = -1
    #    while i<self.graphprecision:
    #        if self.priceatmaturity[i] > asset1.strike:
    #           if graphbreakflag == -1:
    #                graphbreakflag = i
    #           self.profit[i] = -asset1.price -asset2.price -asset1.strike +self.priceatmaturity[i]
    #        else:
    #           self.profit[i] = -asset1.price -asset2.price -self.priceatmaturity[i] +asset2.strike 
    #        i=i+1
    #    self.minprofitindex = graphbreakflag
    #    self.minprofit = self.profit[graphbreakflag]
    #    self.cost = -asset1.price -asset2.price
    #    self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
    #    self.risk = 3
    #
    #
    #    pass



    #1.3. Iron butterfly put

    #Properties:
    #minprofit (float)
    #minrofitindex (int)
    #maxprofit (float)
    #maxprofitindex (int)
    #breakeven ([float, float])
    #breakevenindex ([int, int])
    #asset1 = long put
    #asset2 = short put
    #asset3 = short call 
    #asset4 = long call
    #qtty1 = 1
    #qtty2 = 1
    #qtty3 = 1
    #qtty4 = 1

    #def __init__(self,stock,asset1,qtty1,asset2,qtty2,asset3,qtty3,asset4,qtty4):
    #
    #    StrategyBase.__init__(self,"iron butterfly",stock,asset1=asset1,qtty1=qtty1,asset2=asset2,qtty2=qtty2,asset3=asset3,qtty3=qtty3,asset4=asset4,qtty4=qtty4)
    #
    #    i=0
    #    graphbreakflaglow1 = -1
    #    graphbreakflaglow2 = -1
    #    graphbreakflaghigh = -1
    #    while i<self.graphprecision:
    #        if self.priceatmaturity[i] <= asset1.strike:
    #            self.profit[i] = -asset1.price-asset4.price+asset2.price+asset3.price-asset2.strike+asset1.strike
    #        elif ((self.priceatmaturity[i] > asset1.strike) and (self.priceatmaturity[i] <= asset2.strike)):
    #            if graphbreakflaglow1 == -1:
    #                 graphbreakflaglow1 = i
    #            self.profit[i] = -asset1.price-asset4.price+asset2.price+asset3.price-asset2.strike+self.priceatmaturity[i]
    #        elif ((self.priceatmaturity[i]>asset2.strike)and(self.priceatmaturity[i]<=asset4.strike)):
    #            if graphbreakflaghigh == -1:
    #                 graphbreakflaghigh = i
    #            self.profit[i] = -asset1.price-asset4.price+asset2.price+asset3.price+asset3.strike - self.priceatmaturity[i]
    #        else:
    #            if graphbreakflaglow2 == -1:
    #                 graphbreakflaglow2 = i
    #            self.profit[i] = -asset1.price-asset4.price+asset2.price+asset3.price-asset4.strike+asset3.strike
    #        i=i+1
    #    self.minprofitindex1 = graphbreakflaglow1
    #    self.minprofitindex2 = graphbreakflaglow2
    #    self.minprofit = min(self.profit[graphbreakflaglow1],self.profit[graphbreakflaglow2])
    #    self.maxprofitindex = graphbreakflaghigh
    #    self.maxprofit = self.profit[graphbreakflaghigh]
    #    self.cost = -asset1.price-asset4.price+asset2.price+asset3.price
    #    self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
    #    self.risk = 3
    #
    #    pass


    #1.5. Short strangle

    #Properties:
    #minrofitindex (int)
    #maxprofit (float)
    #maxprofitindex (int)
    #breakeven ([float, float])
    #breakevenindex ([int, int])
    #asset1 = short put
    #asset2 = short call
    #qtty1 = 1
    #qtty2 = 1

    #def __init__(self,stock,asset1,qtty1,asset2,qtty2):
    #
    #    StrategyBase.__init__(self,"short strangle",stock,asset1=asset1,qtty1=qtty1,asset2=asset2,qtty2=qtty2)
    #
    #    i=0
    #    graphbreakflaglow = -1
    #    graphbreakflaghigh = -1
    #    while i<self.graphprecision:
    #        if self.priceatmaturity[i] < asset1.strike:
    #           self.profit[i] = asset1.price + asset2.price - asset1.strike + self.priceatmaturity[i]
    #        elif ((self.priceatmaturity[i] >=asset1.strike) and (self.priceatmaturity[i] <= asset2.strike)):
    #           if graphbreakflaglow == -1:
    #                graphbreakflaglow = i
    #           self.profit[i] = asset1.price + asset2.price
    #        else:
    #           if graphbreakflaghigh == -1:
    #                graphbreakflaghigh = i
    #           self.profit[i] = asset1.price + asset2.price - self.priceatmaturity[i] + asset2.strike 
    #        i=i+1
    #    self.minprofitindex = graphbreakflaglow
    #    self.maxprofitindex = graphbreakflaghigh
    #    self.maxprofit = asset1.price + asset2.price
    #    self.cost = asset1.price + asset2.price
    #    self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
    #    self.risk = 4
    #
    #    pass



    #1.4. Short straddle

    #Properties:
    #maxprofit (float)
    #maxprofitindex (int)
    #breakeven ([float, float])
    #breakevenindex ([int, int])
    #asset1 = short call
    #asset2 = short put
    #qtty1 = 1
    #qtty2 = 1

    #def __init__(self,stock,asset1,qtty1,asset2,qtty2):
    #
    #    StrategyBase.__init__(self,"short straddle",stock,asset1=asset1,qtty1=qtty1,asset2=asset2,qtty2=qtty2)
    #
    #    i=0
    #    graphbreakflag = -1
    #    while i<self.graphprecision:
    #        if self.priceatmaturity[i] < asset1.strike:
    #           self.profit[i] = asset1.price + asset2.price - asset2.strike + self.priceatmaturity[i]
    #        else:
    #           if graphbreakflag == -1:
    #                graphbreakflag = i
    #           self.profit[i] = asset1.price + asset2.price -self.priceatmaturity[i] + asset1.strike 
    #        i=i+1
    #    self.maxprofitindex = graphbreakflag
    #    self.maxprofit = self.profit[graphbreakflag]
    #    self.cost = asset1.price + asset2.price
    #    self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
    #    self.risk = 4
    #
    #    pass
    




#def __init__(self,stock,asset1,qtty1,asset2,qtty2,asset3,qtty3):
#
#        StrategyBase.__init__(self,"long butterfly put",stock,asset1=asset1,qtty1=qtty1,asset2=asset2,qtty2=qtty2,asset3=asset3,qtty3=qtty3)
#
#        i=0
#        graphbreakflaglow1 = -1
#        graphbreakflaglow2 = -1
#        graphbreakflaghigh = -1
#        while i<self.graphprecision:
#            if self.priceatmaturity[i] <= asset1.strike:
#                self.profit[i] = -asset1.price-asset3.price+(2*asset2.price)+asset3.strike-(2*asset2.strike)+asset1.strike
#            elif ((self.priceatmaturity[i] > asset1.strike) and (self.priceatmaturity[i] <= asset2.strike)):
#                if graphbreakflaglow1 == -1:
#                     graphbreakflaglow1 = i
#                self.profit[i] = -asset1.price-asset3.price+(2*asset2.price) +asset3.strike - (2* asset2.strike) + self.priceatmaturity[i]
#            elif ((self.priceatmaturity[i]>asset2.strike)and(self.priceatmaturity[i]<=asset3.strike)):
#                if graphbreakflaghigh == -1:
#                     graphbreakflaghigh = i
#                self.profit[i] = -asset1.price-asset3.price+(2*asset2.price) +asset3.strike - self.priceatmaturity[i]
#            else:
#                if graphbreakflaglow2 == -1:
#                     graphbreakflaglow2 = i
#                self.profit[i] = -asset1.price-asset3.price+(2*asset2.price) 
#            i=i+1
#        self.minprofitindex1 = graphbreakflaglow1
#        self.minprofitindex2 = graphbreakflaglow2
#        self.minprofit = min(self.profit[graphbreakflaglow1],self.profit[graphbreakflaglow2])
#        self.maxprofitindex = graphbreakflaghigh
#        self.maxprofit = self.profit[graphbreakflaghigh]
#        self.cost = -asset1.price-asset3.price+(2*asset2.price)
#        self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
#        self.risk = 3
#
#
#        pass
#


#     def __init__(self,stock,asset1,qtty1,asset2,qtty2,asset3,qtty3):
#            
#            StrategyBase.__init__(self,"long butterfly call",stock,asset1=asset1,qtty1=qtty1,asset2=asset2,qtty2=qtty2,asset3=asset3,qtty3=qtty3)
#
#            i=0
#            graphbreakflaglow1 = -1
#            graphbreakflaglow2 = -1
#            graphbreakflaghigh = -1
#            while i<self.graphprecision:
#                if self.priceatmaturity[i] <= asset1.strike:
#                    self.profit[i] = -asset1.price-asset3.price+(2*asset2.price)
#                elif ((self.priceatmaturity[i] > asset1.strike) and (self.priceatmaturity[i] <= asset2.strike)):
#                    if graphbreakflaglow1 == -1:
#                         graphbreakflaglow1 = i
#                    self.profit[i] = -asset1.price-asset3.price+(2*asset2.price) - asset1.strike + self.priceatmaturity[i]
#                elif ((self.priceatmaturity[i]>asset2.strike)and(self.priceatmaturity[i]<=asset3.strike)):
#                    if graphbreakflaghigh == -1:
#                         graphbreakflaghigh = i
#                    self.profit[i] = -asset1.price-asset3.price+(2*asset2.price) -asset1.strike + (2*asset2.strike) - self.priceatmaturity[i]
#                else:
#                    if graphbreakflaglow2 == -1:
#                         graphbreakflaglow2 = i
#                    self.profit[i] = -asset1.price-asset3.price+(2*asset2.price) - asset3.strike -asset1.strike + (2*asset2.strike) 
#                i=i+1
#            self.minprofitindex1 = graphbreakflaglow1
#            self.minprofitindex2 = graphbreakflaglow2
#            self.minprofit = min(self.profit[graphbreakflaglow1],self.profit[graphbreakflaglow2])
#            self.maxprofitindex = graphbreakflaghigh
#            self.maxprofit = self.profit[graphbreakflaghigh]
#            self.cost = -asset1.price-asset3.price+(2*asset2.price)
#            self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
#            self.risk = 3
#
#            pass





#outdated print
#def PrintData(strategy):
#    
#    print("Strategy: "+str(strategy.name))
#    print("Cost: $%.2f"%(strategy.cost))
#    if strategy.maxprofit != -1:
#        print("Max cte profit: $%.2f"%(strategy.maxprofit))
#    if strategy.minprofit != -1:
#        print("Max cte loss: $%.2f"%(strategy.minprofit))
#
#    if isinstance(strategy.breakeven,float):
#        print("Breakeven: %.2f%%"%(strategy.breakeven))
#    else:
#        print("Low breakeven: %.2f%%"%(strategy.breakeven[0]))
#        print("High breakeven: %.2f%%"%(strategy.breakeven[1]))
#
#    print("Risk profile: "+str(strategy.risk)+"/4")
#    print("Options:")
#    currentasset = strategy.asset1
#    if currentasset.tag != "dummy":
#        print(str(strategy.qtty1)+"x "+str(currentasset.positiontype)+str(currentasset.tag)+" | Maturity: "+str(int(currentasset.matyear))+"-"+str(int(currentasset.matmonth))+"-"+str(int(currentasset.matday)))
#    currentasset = strategy.asset2
#    if currentasset.tag != "dummy":
#        print(str(strategy.qtty2)+"x "+str(currentasset.positiontype)+str(currentasset.tag)+" | Maturity: "+str(int(currentasset.matyear))+"-"+str(int(currentasset.matmonth))+"-"+str(int(currentasset.matday)))
#    currentasset = strategy.asset3
#    if currentasset.tag != "dummy":
#        print(str(strategy.qtty3)+"x "+str(currentasset.positiontype)+str(currentasset.tag)+" | Maturity: "+str(int(currentasset.matyear))+"-"+str(int(currentasset.matmonth))+"-"+str(int(currentasset.matday)))
#    currentasset = strategy.asset4
#    if currentasset.tag != "dummy":
#        print(str(strategy.qtty4)+"x "+str(currentasset.positiontype)+str(currentasset.tag)+" | Maturity: "+str(int(currentasset.matyear))+"-"+str(int(currentasset.matmonth))+"-"+str(int(currentasset.matday)))
#
#    print(" ")
#
#    pass


#Outdated user input get
#1. Getting user inputs

#strategyinput = GetStrategy() #Receiving desired strategy from user
#breakeven = GetBreakEven(strategyinput) #Receiving desired break even point(s)
#maxmaturity = GetMaxMaturity() #Receiving desired maximum maturity
#minmaturity = GetMinMaturity() #Receiving desired minimum maturity
#fee = GetFee() #Receiving transaction fee from user

#def GetStrategy():
#    
#    #Definining strategytype
#    print("Select strategy type:")
#    print(" ");
#    print("1. Profit inside price delta interval")
#    print("2. Profit outside price delta interval")
#    print("3. Profit above price delta point")
#    print("4. Profit below price delta point")
#    print(" ")
#    strategyinput = int(input('Enter your input:'))
#    print(" ")
#
#    #Handling invalid user input:
#    if (strategyinput == 1) or (strategyinput == 2) or (strategyinput == 3) or (strategyinput == 4):
#        return strategyinput        
#    else:
#        print('Invalid input please try again')
#        print(" ")
#        strategyinput = GetStrategy()
#
#    return strategyinput


#def GetBreakEven(strategy):
#
#    if strategy >=3:
#        print("Select desired break even point")
#        breakeven = float(input('Enter your input:'))
#        print("")
#    else:
#        print("Select desired lower break even point")
#        breakeven1 = float(input('Enter your input:'))
#        print("")
#        print("Select desired upper break even point")
#        breakeven2 = float(input('Enter your input:'))
#        print("")
#
#        breakeven = (breakeven1,breakeven2)
#
#    return breakeven
#
#
#def GetMaxMaturity():
#
#    print("Select desired maximum maturity (in number of days)")
#    maxmat = float(input('Enter your input:'))
#    print("")
#
#    return maxmat
#
#def GetMinMaturity():
#
#    print("Select desired minimum maturity (in number of days)")
#    maxmat = float(input('Enter your input:'))
#    print("")
#
#    return minmat
#
#def GetFee():
#
#    #Receiving user inputs
#    print("Input transaction fee");
#    fee = float(input('Enter your input:'))
#    print(" ")
#
#    return fee


#OUTDATED Strategy List factory
#
#
#def BuildStrategyListofType(type,stock,short_call_list,long_call_list,short_put_list,long_put_list,tolfil_short_call_list,tolfil_long_call_list,tolfil_short_put_list,tolfil_long_put_list):
#
#    strategy_list = []
#    tolerance = 0.03
#    lowbound = 1 - tolerance
#    upbound = 1 + tolerance
#    prevmat = 999.0
#
#
#    #1.1. Long butterfly call
#
#    if type == "long butterfly call":
#        for short in tolfil_short_call_list:
#            for longleft in long_call_list:
#                if ((longleft.strike < short.strike) and (longleft.matmonth == short.matmonth)):
#                    for longright in long_call_list:
#                        if ((longright.strike > short.strike) and (longright.matmonth == longleft.matmonth)):
#                            strategy_list.append(Strategy11("long butterfly call",stock,asset1=longleft,qtty1=1,asset2=short,qtty2=2,asset3=longright,qtty3=1))
#
#
#    #1.2. Long butterfly put
#
#    if type == "long butterfly put":
#        for short in tolfil_short_put_list:
#            for longleft in long_put_list:
#                if ((longleft.strike < short.strike) and (longleft.matmonth == short.matmonth)):
#                    for longright in long_put_list:
#                        if ((longright.strike > short.strike) and (longright.matmonth == longleft.matmonth)):
#                            strategy_list.append(Strategy12("long butterfly put",stock,asset1=longleft,qtty1=1,asset2=short,qtty2=2,asset3=longright,qtty3=1))
#
#
#    #1.3. Iron butterfly put (PROCESSING TIME IS TOO LONG)
#
#    #if type == "iron butterfly":
#    #    for shortput in short_put_list:
#    #        if ((shortput.strike >= (lowbound*stock.price))and(shortput.strike <= (upbound*stock.price))):
#    #            for shortcall in short_call_list:
#    #                if ((shortcall.strike == shortput.strike)and(shortcall.matmonth == shortput.matmonth)):
#    #                    for longput in long_put_list:
#    #                        if ((longput.strike < shortput.strike)and(longput.matmonth == shortcall.matmonth)):
#    #                            for longcall in long_call_list:
#    #                                if ((longcall.strike>shortput.strike)and(longcall.matmonth==longput.matmonth)):
#    #                                    strategy_list.append(Strategy13("iron butterfly",stock,asset1 = longput,qtty1=1,asset2=shortput,qtty2=1,asset3=shortcall,qtty3=1,asset4=longcall,qtty4=1))
#    
#    #1.4. Short straddle
#
#    if type == "short straddle":
#        for call in tolfil_short_call_list:
#            for put in short_put_list:
#                if ((put.matmonth == call.matmonth) and (put.strike == call.strike)):
#                    strategy_list.append(Strategy14("short straddle",stock,asset1=call,qtty1=1,asset2=put,qtty2=1))
#
#
#    #1.5. Short strangle
#
#    if type == "short strangle":
#        for put in short_put_list:
#            if put.strike < stock.price:
#                for call in short_call_list:
#                    if call.strike > stock.price:
#                        strategy_list.append(Strategy15("short strangle",stock,asset1=put,qtty1=1,asset2=call,qtty2=1))
#
#
#    #2.1. Long straddle
#
#    if type == "long straddle":
#        for call in tolfil_long_call_list:
#            for put in long_put_list:
#                if ((put.strike == call.strike)and(put.matmonth==call.matmonth)):
#                    strategy_list.append(Strategy21("long straddle",stock,asset1=call,qtty1=1,asset2=put,qtty2=1))
#    
#
#    #2.2. Long strangle
#
#    if type == "long strangle":
#        for put in long_put_list:
#            if put.strike < stock.price:
#                for call in long_call_list:
#                    if ((call.strike>stock.price) and (call.matmonth == put.matmonth)):
#                        strategy_list.append(Strategy22("long strangle",stock,asset1=put,qtty1=1,asset2=call,qtty2=1))
#
#
#    #2.3. back spread call
#
#    if type == "back spread call":
#        for short in tolfil_short_call_list:
#            for long in long_call_list:
#                if ((long.strike > short.strike) and (long.matmonth == short.matmonth) and (((-2) * long.price + short.price)>0)):
#                    strategy_list.append(Strategy23("back spread call",stock,asset1=short,qtty1=1,asset2=long,qtty2=2))
#
#
#    #2.4. back spread put
#
#    if type == "back spread put":
#        for short in tolfil_short_put_list:
#            for long in long_put_list:
#                if ((long.strike < short.strike) and (long.matmonth == short.matmonth) and (((-2) * long.price + short.price)>0)):
#                    strategy_list.append(Strategy24("back spread put",stock,asset1=long,qtty1=2,asset2=short,qtty2=1))
#
#
#    #3.1. Covered call
#
#    if type == "covered call":
#        for option in short_call_list:
#            if option.strike > stock.price:
#                strategy_list.append(Strategy31("covered call",stock,stockqtty=1,asset1=option,qtty1=1))
#
#
#    #3.2. Protective put
#
#    if type == "protective put":
#        for option in long_put_list:
#            if option.strike < stock.price:
#                strategy_list.append(Strategy32("protective put",stock,stockqtty=1,asset1=option,qtty1=1))
#
#
#    #3.3. Collar
#
#    if type == "collar":
#        for put in long_put_list:
#            if put.strike < stock.price:
#                for call in short_call_list:
#                    if ((call.strike > stock.price) and (put.matmonth == call.matmonth)):
#                        strategy_list.append(Strategy33("collar",stock,stockqtty=1,asset1=put,qtty1=1,asset2=call,qtty2=1))
#
#
#    #3.4. Long call
#
#    if type == "long call":
#        for call in long_call_list:
#            if call.strike <= stock.price:
#                strategy_list.append(Strategy34("long call",stock,asset1 = call,qtty1 = 1))
#
#
#    #3.5. Long call spread
#
#    if type == "long call spread":
#        for long in long_call_list:
#            if long.strike <= stock.price:
#                for short in short_call_list:
#                    if ((short.strike > stock.price) and (long.matmonth == short.matmonth)):
#                        strategy_list.append(Strategy35("long call spread",stock,asset1 = long,qtty1 = 1,asset2 = short,qtty2=1))
#
#
#    #3.6. Short put spread
#
#    if type == "short put spread":
#        for short in short_put_list:
#            if short.strike > stock.price:
#                for long in long_put_list:
#                    if ((short.price > long.price) and (short.strike > long.strike)and (short.matmonth == long.matmonth)): 
#                       strategy_list.append(Strategy36("short put spread",stock,asset1=long,qtty1=1,asset2=short,qtty2=1)) 
#
#
#    #3.7. Short put
#
#    if type == "short put":
#        for put in short_put_list:
#            if (put.strike < stock.price):
#                strategy_list.append(Strategy37("short put",stock,asset1=put,qtty1=1))
#
#    
#    #3.8. Long combination
#
#    if type == "long combination":
#        for call in tolfil_long_call_list:
#            for put in short_put_list:
#                if ((put.matmonth == call.matmonth) and (put.strike == call.strike)):
#                    strategy_list.append(Strategy38("long combination",stock,asset1=call,qtty1=1,asset2=put,qtty2=1))
#
#
#    #4.1. Long put
#
#    if type == "long put":
#        for put in long_put_list:
#            if put.strike <= stock.price:
#                strategy_list.append(Strategy41("long put",stock,asset1 = put,qtty1 = 1))
#
#
#    #4.2. Long put spread
#
#    if type == "long put spread":
#        for short in short_put_list:
#            if short.strike < stock.price:
#                for long in long_put_list:
#                    if ((long.strike >= stock.price) and (short.matmonth == long.matmonth)):
#                        strategy_list.append(Strategy42("long put spread",stock,asset1=short,qtty1=1,asset2=long,qtty2=1))
#
#
#    #4.3. Short call spread
#
#    if type == "short call spread":
#        for short in short_call_list:
#            if short.strike > stock.price:
#                for long in long_call_list:
#                    if ((short.price > long.price) and (long.strike > short.strike) and (short.matmonth == long.matmonth)):
#                        strategy_list.append(Strategy43("short call spread",stock,asset1=short,qtty1=1,asset2=long,qtty2=1))
#
#
#    #4.4. Short call
#
#    if type == "short call":
#        for call in short_call_list:
#            if (call.strike > stock.price):
#                strategy_list.append(Strategy44("short call",stock,asset1=call,qtty1=1))
#
#
#    #4.5. Short combination
#
#    if type == "short combination":
#        for call in tolfil_short_call_list:
#            for put in long_put_list:
#                if ((put.matmonth == call.matmonth) and (put.strike == call.strike)):
#                    strategy_list.append(Strategy45("short combination",stock,asset1=call,qtty1=1,asset2=put,qtty2=1))
#
#    return strategy_list



#Outdated list build method

    #1.1. Long butterfly call

#    if type == "long butterfly call":
#        for short in short_call_list:
#            if ((short.strike >= (lowbound*stock.price))and(short.strike <= (upbound*stock.price))):
#                for longleft in long_call_list:
#                    if ((longleft.strike < short.strike) and (longleft.matmonth == short.matmonth)):
#                        for longright in long_call_list:
#                            if ((longright.strike > short.strike) and (longright.matmonth == longleft.matmonth)):
#                                strategy_list.append(Strategy("long butterfly call",1,stock,asset1=longleft,qtty1=1,asset2=short,qtty2=2,asset3=longright,qtty3=1))

#    if type == "long butterfly put":
#        for short in short_put_list:
#            if ((short.strike >= (lowbound*stock.price))and(short.strike <= (upbound*stock.price))):
#                for longleft in long_put_list:
#                    if ((longleft.strike < short.strike) and (longleft.matmonth == short.matmonth)):
#                        for longright in long_put_list:
#                            if ((longright.strike > short.strike) and (longright.matmonth == longleft.matmonth)):
#                                strategy_list.append(Strategy("long butterfly put",1,stock,asset1=longleft,qtty1=1,asset2=short,qtty2=2,asset3=longright,qtty3=1))
#

 #   if type == "long butterfly put":
 #       for short in tolfil_short_put_list:
 #           if prevmat != short.matmonth:
 #               longfilt_list = [x for x in long_put_list if x.matmonth == short.matmonth]
 #               prevmat = short.matmonth
 #           longleft_list = [x for x in longfilt_list if x.strike < short.strike]
 #           longright_list = [x for x in longfilt_list if x.strike > short.strike]      
 #           for longleft in longleft_list:
 #               for longright in longright_list:
 #                   strategy_list.append(Strategy("long butterfly put",1,stock,asset1=longleft,qtty1=1,asset2=short,qtty2=2,asset3=longright,qtty3=1))

 #    if type == "long butterfly call":
#        for short in tolfil_short_call_list:
#            if prevmat != short.matmonth:
#                longfilt_list = [x for x in long_call_list if x.matmonth == short.matmonth]
#                prevmat = short.matmonth
#            longleft_list = [x for x in longfilt_list if x.strike < short.strike]
#            longright_list = [x for x in longfilt_list if x.strike > short.strike] 
#            for longleft in longleft_list:
#                for longright in longright_list:
#                    strategy_list.append(Strategy("long butterfly call",1,stock,asset1=longleft,qtty1=1,asset2=short,qtty2=2,asset3=longright,qtty3=1))


#CURRENT ASSET PRICE AND NAME
stockprice = 157.11
root= "AAPL"

#DEFINING LABELS AND RANGE FOR X AXIS ON THE GRAPH
#xlabelsplit=np.linspace(-15,15,11)
#xlabelname = ["-15%","-12%","-9%","-6%","-3%","0%","+3%","+6%","+9%","+12%","+15%"]
priceatmaturity= np.linspace(stockprice-(stockprice*0.9),stockprice+(stockprice*0.9),1000)

#CALL SPECS
c_strike = 160
c_lastprice = 4.03
c_bid = 4.00
c_askprice = 4.05
c_timetomaturity = 52

#PUT SPECS

p_strike = 150
p_lastprice = 7.15	
p_bid = 7.15
p_askprice = 7.25
p_timetomaturity = 52


#TEST AREA
#cost = stockprice
#
profit = np.empty(1000)
#i=0
#while i<1000:
#    if c_strike < priceatmaturity[i]:
#       profit[i] = c_bid + c_strike - stockprice
#    else:
#       profit[i] = c_bid + priceatmaturity[i] - stockprice 
#    i=i+1

i=0
graphbreakflaglow = -1
graphbreakflaghigh = -1
while i<1000:
    if priceatmaturity[i] > c_strike: #max profit
        profit[i] = c_bid + c_strike - stockprice - p_askprice
        print("hit")
        print(profit[i])
        print(c_bid + c_strike - stockprice - p_askprice)
    elif priceatmaturity[i] < p_strike: #min profit
        profit[i] = p_strike - p_askprice - stockprice + c_bid
    else:# in between no option exercised
        if graphbreakflaglow == -1:
            graphbreakflaglow = i
        profit[i] = priceatmaturity[i] + c_bid - p_askprice - stockprice
    i=i+1

print(graphbreakflaghigh)

plt.figure(1)
plt.plot(100*((priceatmaturity-stockprice)/stockprice),profit)
plt.title(root+" TEST CHART")
plt.xlabel("Stock price delta at maturity")
plt.ylabel("Profit ($)")
plt.ylim([-100,100])
#plt.xticks(xlabelsplit,xlabelname)
plt.grid(True)
plt.axhline(0, color='red')
plt.show()

print(np.mean(priceatmaturity))
#print put profit graph

#p_profit = p_strike-(p_askprice+priceatmaturity)
#
#i=0
#while i<1000:
#    if p_profit[i]<(-p_askprice):
#        p_profit[i]=(-p_askprice)
#    i=i+1
#
#
#plt.figure(1)
#plt.plot(100*((priceatmaturity-stockprice)/stockprice),p_profit)
#plt.title(root+" put option profit chart")
#plt.xlabel("Stock price delta at maturity")
#plt.ylabel("Profit ($)")
#plt.ylim([-8,8])
#plt.xticks(xlabelsplit,xlabelname)
#plt.grid(True)
#plt.axhline(0, color='red')
#plt.show()


#print call profit graph
#c_profit = priceatmaturity-(c_strike+c_askprice)
#
#
#c_minprofit=10
#
#i=0
#while i<1000:
#    if c_profit[i]<(-c_askprice):
#        c_profit[i]=(-c_askprice)
#    i=i+1
#
#i=0	
#while i <1000:
#	c_absmin=abs(c_profit[i])
#	if c_absmin<c_minprofit:
#		c_minprofit=c_absmin
#		a=i
#	i=i+1
#	
#c_breakevendelta=100*((priceatmaturity[a]-stockprice)/stockprice)	
#
#plt.figure(2)
#plt.plot(100*((priceatmaturity-stockprice)/stockprice),c_profit)
#plt.title(root+" call option profit chart")
#plt.xlabel("Stock price delta at maturity")
#plt.ylabel("Profit ($)")
#plt.text((c_breakevendelta-15), 2, 'break even at delta = '+str(round(c_breakevendelta,2))+'%')
#plt.ylim([-8,8])
#plt.xticks(xlabelsplit,xlabelname)
#plt.grid(True)
#plt.axhline(0, color='red')
#plt.show()



#test

#plt.figure(3)
#plt.plot(100*((priceatmaturity-stockprice)/stockprice),3*c_profit+p_profit)
#plt.title(root+" mixed strategy profit chart")
#plt.xlabel("Stock price delta at maturity")
#plt.ylabel("Profit ($)")
#plt.ylim([-20,20])
#plt.xticks(xlabelsplit,xlabelname)
#plt.grid(True)
#plt.axhline(0, color='red')
#plt.show()


