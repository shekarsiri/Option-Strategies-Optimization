import math
import numpy as np
from AssetModule import Asset
from StockModule import Stock


def GetBreakEvenPoint(profitcurve,noofpoints,graphprecision,xaxisrange):
    
    storage = np.empty(graphprecision)

    if noofpoints == 1:
        
        #detecting absolute min value
        np.absolute(profitcurve,out = storage) 
        breakevenindex = np.argmin(storage)
    
        breakevendelta = 100*(xaxisrange*(((2*breakevenindex)/graphprecision)-1))

    else:

        #detecting signal change
        np.sign(profitcurve, out=storage)
        signchange = ((np.roll(storage, 1) - storage) != 0).astype(int)
        breakevenindex = np.argwhere(signchange == 1).flatten()

        if breakevenindex.size !=2:
            breakevenindex = np.array([0,1])

        breakevendelta=(100*(xaxisrange*(((2*breakevenindex[0])/graphprecision)-1)),100*(xaxisrange*(((2*breakevenindex[1])/graphprecision)-1)))

    return breakevendelta,breakevenindex    


class Strategy:
    
    dummyasset = Asset("short_call",0,0,0,1,1,2050,0,0,"dummy")
    graphprecision = 300
    xaxisrange = 0.12

    def __init__(self,strategyname, type, stock,stockqtty=0, asset1=dummyasset,qtty1=0,asset2=dummyasset,qtty2=0,asset3=dummyasset,qtty3=0,asset4=dummyasset,qtty4=0,fee=0):
        
        #Properties common across all strategies:
        #profit[i] (float numpy array) (size = graph precision): profit curve
        #priceatmaturitylin (float numpy array) (size = graph precision): linear distribution of stock price variation delimited by xaxisrange
        #maturity (float): number of days until maturity
        #risk (int): risk profile respective to te strategy scale goes from 1 to 4, 1 = least risky | 4 = most risky
        #cost: credit or debit necessary to open the position (transaction fee not included)

        self.profit = np.empty(Strategy.graphprecision)
        priceatmaturity= np.linspace(stock.price-(stock.price*Strategy.xaxisrange),stock.price+(stock.price*Strategy.xaxisrange),Strategy.graphprecision)
        self.maturity = min(asset1.timetomat,asset2.timetomat,asset3.timetomat,asset4.timetomat)
        
        self.priceatmaturitylin = priceatmaturity

        self.asset1 = asset1
        self.asset2 = asset2
        self.asset3 = asset3
        self.asset4 = asset4

        self.qtty1=qtty1
        self.qtty2=qtty2
        self.qtty3=qtty3
        self.qtty4=qtty4

        self.name = strategyname

        self.maxprofit = -1
        self.minprofit = -1

        if type == 1:
            
            #1.1. Long butterfly call

            #Properties:
            #minprofit (float)
            #minrofitindex (int)
            #maxprofit (float)
            #maxprofitindex (int)
            #breakeven ([float, float])
            #breakevenindex ([int, int])
            #asset1 = long call
            #asset2 = short call
            #asset3 = long call
            #qtty1 = 1
            #qtty2 = 2
            #qtty3 = 1

            if strategyname == "long butterfly call":
                i=0
                graphbreakflaglow1 = -1
                graphbreakflaglow2 = -1
                graphbreakflaghigh = -1
                while i<self.graphprecision:
                    if priceatmaturity[i] <= asset1.strike:
                        self.profit[i] = -asset1.price-asset3.price+(2*asset2.price)
                    elif ((priceatmaturity[i] > asset1.strike) and (priceatmaturity[i] <= asset2.strike)):
                        if graphbreakflaglow1 == -1:
                             graphbreakflaglow1 = i
                        self.profit[i] = -asset1.price-asset3.price+(2*asset2.price) - asset1.strike + priceatmaturity[i]
                    elif ((priceatmaturity[i]>asset2.strike)and(priceatmaturity[i]<=asset3.strike)):
                        if graphbreakflaghigh == -1:
                             graphbreakflaghigh = i
                        self.profit[i] = -asset1.price-asset3.price+(2*asset2.price) -asset1.strike + (2*asset2.strike) - priceatmaturity[i]
                    else:
                        if graphbreakflaglow2 == -1:
                             graphbreakflaglow2 = i
                        self.profit[i] = -asset1.price-asset3.price+(2*asset2.price) - asset3.strike -asset1.strike + (2*asset2.strike) 
                    i=i+1
                self.minprofitindex1 = graphbreakflaglow1
                self.minprofitindex2 = graphbreakflaglow2
                self.minprofit = min(self.profit[graphbreakflaglow1],self.profit[graphbreakflaglow2])
                self.maxprofitindex = graphbreakflaghigh
                self.maxprofit = self.profit[graphbreakflaghigh]
                self.cost = -asset1.price-asset3.price+(2*asset2.price)
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
                self.risk = 3



            #1.2. Long butterfly put
            
            #Properties:
            #minprofit (float)
            #minrofitindex (int)
            #maxprofit (float)
            #maxprofitindex (int)
            #breakeven ([float, float])
            #breakevenindex ([int, int])
            #asset1 = long put
            #asset2 = short put
            #asset3 = long put
            #qtty1 = 1
            #qtty2 = 2
            #qtty3 = 1

            elif strategyname == "long butterfly put":
                i=0
                graphbreakflaglow1 = -1
                graphbreakflaglow2 = -1
                graphbreakflaghigh = -1
                while i<self.graphprecision:
                    if priceatmaturity[i] <= asset1.strike:
                        self.profit[i] = -asset1.price-asset3.price+(2*asset2.price)+asset3.strike-(2*asset2.strike)+asset1.strike
                    elif ((priceatmaturity[i] > asset1.strike) and (priceatmaturity[i] <= asset2.strike)):
                        if graphbreakflaglow1 == -1:
                             graphbreakflaglow1 = i
                        self.profit[i] = -asset1.price-asset3.price+(2*asset2.price) +asset3.strike - (2* asset2.strike) + priceatmaturity[i]
                    elif ((priceatmaturity[i]>asset2.strike)and(priceatmaturity[i]<=asset3.strike)):
                        if graphbreakflaghigh == -1:
                             graphbreakflaghigh = i
                        self.profit[i] = -asset1.price-asset3.price+(2*asset2.price) +asset3.strike - priceatmaturity[i]
                    else:
                        if graphbreakflaglow2 == -1:
                             graphbreakflaglow2 = i
                        self.profit[i] = -asset1.price-asset3.price+(2*asset2.price) 
                    i=i+1
                self.minprofitindex1 = graphbreakflaglow1
                self.minprofitindex2 = graphbreakflaglow2
                self.minprofit = min(self.profit[graphbreakflaglow1],self.profit[graphbreakflaglow2])
                self.maxprofitindex = graphbreakflaghigh
                self.maxprofit = self.profit[graphbreakflaghigh]
                self.cost = -asset1.price-asset3.price+(2*asset2.price)
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
                self.risk = 3



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

            elif strategyname == "iron butterfly":
                i=0
                graphbreakflaglow1 = -1
                graphbreakflaglow2 = -1
                graphbreakflaghigh = -1
                while i<self.graphprecision:
                    if priceatmaturity[i] <= asset1.strike:
                        self.profit[i] = -asset1.price-asset4.price+asset2.price+asset3.price-asset2.strike+asset1.strike
                    elif ((priceatmaturity[i] > asset1.strike) and (priceatmaturity[i] <= asset2.strike)):
                        if graphbreakflaglow1 == -1:
                             graphbreakflaglow1 = i
                        self.profit[i] = -asset1.price-asset4.price+asset2.price+asset3.price-asset2.strike+priceatmaturity[i]
                    elif ((priceatmaturity[i]>asset2.strike)and(priceatmaturity[i]<=asset4.strike)):
                        if graphbreakflaghigh == -1:
                             graphbreakflaghigh = i
                        self.profit[i] = -asset1.price-asset4.price+asset2.price+asset3.price+asset3.strike - priceatmaturity[i]
                    else:
                        if graphbreakflaglow2 == -1:
                             graphbreakflaglow2 = i
                        self.profit[i] = -asset1.price-asset4.price+asset2.price+asset3.price-asset4.strike+asset3.strike
                    i=i+1
                self.minprofitindex1 = graphbreakflaglow1
                self.minprofitindex2 = graphbreakflaglow2
                self.minprofit = min(self.profit[graphbreakflaglow1],self.profit[graphbreakflaglow2])
                self.maxprofitindex = graphbreakflaghigh
                self.maxprofit = self.profit[graphbreakflaghigh]
                self.cost = -asset1.price-asset4.price+asset2.price+asset3.price
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
                self.risk = 3



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

            elif strategyname == "short straddle":
                i=0
                graphbreakflag = -1
                while i<self.graphprecision:
                    if priceatmaturity[i] < asset1.strike:
                       self.profit[i] = asset1.price + asset2.price - asset2.strike + priceatmaturity[i]
                    else:
                       if graphbreakflag == -1:
                            graphbreakflag = i
                       self.profit[i] = asset1.price + asset2.price -priceatmaturity[i] + asset1.strike 
                    i=i+1
                self.maxprofitindex = graphbreakflag
                self.maxprofit = self.profit[graphbreakflag]
                self.cost = asset1.price + asset2.price
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
                self.risk = 4



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

            elif strategyname == "short strangle":
                i=0
                graphbreakflaglow = -1
                graphbreakflaghigh = -1
                while i<self.graphprecision:
                    if priceatmaturity[i] < asset1.strike:
                       self.profit[i] = asset1.price + asset2.price - asset1.strike + priceatmaturity[i]
                    elif ((priceatmaturity[i] >=asset1.strike) and (priceatmaturity[i] <= asset2.strike)):
                       if graphbreakflaglow == -1:
                            graphbreakflaglow = i
                       self.profit[i] = asset1.price + asset2.price
                    else:
                       if graphbreakflaghigh == -1:
                            graphbreakflaghigh = i
                       self.profit[i] = asset1.price + asset2.price - priceatmaturity[i] + asset2.strike 
                    i=i+1
                self.minprofitindex = graphbreakflaglow
                self.maxprofitindex = graphbreakflaghigh
                self.maxprofit = asset1.price + asset2.price
                self.cost = asset1.price + asset2.price
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
                self.risk = 4




        elif type == 2:

            #2.1. Long straddle

            #Properties:
            #minprofit (float)
            #minrofitindex (int)
            #breakeven ([float, float])
            #breakevenindex ([int, int])
            #asset1 = long call
            #asset2 = long put
            #qtty1 = 1
            #qtty2 = 1

            if strategyname == "long straddle":
                i=0
                graphbreakflag = -1
                while i<self.graphprecision:
                    if priceatmaturity[i] > asset1.strike:
                       if graphbreakflag == -1:
                            graphbreakflag = i
                       self.profit[i] = -asset1.price -asset2.price -asset1.strike +priceatmaturity[i]
                    else:
                       self.profit[i] = -asset1.price -asset2.price -priceatmaturity[i] +asset2.strike 
                    i=i+1
                self.minprofitindex = graphbreakflag
                self.minprofit = self.profit[graphbreakflag]
                self.cost = -asset1.price -asset2.price
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
                self.risk = 3



            #2.2. Long strangle

            #Properties:
            #minprofit (float)
            #minrofitindex (int)
            #maxprofitindex (int)
            #breakeven ([float, float])
            #breakevenindex ([int, int])
            #asset1 = long put
            #asset2 = long call
            #qtty1 = 1
            #qtty2 = 1

            elif strategyname == "long strangle":
                i=0
                graphbreakflaglow = -1
                graphbreakflaghigh = -1
                while i<self.graphprecision:
                    if priceatmaturity[i] < asset1.strike:
                       self.profit[i] = -asset1.price - asset2.price + asset1.strike - priceatmaturity[i]
                    elif priceatmaturity[i] > asset2.strike:
                       if graphbreakflaghigh == -1:
                            graphbreakflaghigh = i
                       self.profit[i] = -asset1.price -asset2.price - asset2.strike + priceatmaturity[i]
                    else:
                       if graphbreakflaglow == -1:
                            graphbreakflaglow = i
                       self.profit[i] = -asset1.price -asset2.price 
                    i=i+1
                self.minprofitindex = graphbreakflaglow
                self.minprofit = -asset1.price -asset2.price
                self.maxprofitindex = graphbreakflaghigh
                self.cost = -asset1.price -asset2.price
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
                self.risk = 3



            #2.3. back spread call
            
            #Properties:
            #minprofit (float)
            #minrofitindex (int)
            #maxprofit (float)
            #maxprofitindex (int)
            #breakeven ([float, float])
            #breakevenindex ([int, int])
            #asset1 = short call
            #asset2 = long call
            #qtty1 = 1
            #qtty2 = 2

            elif strategyname == "back spread call":
                i=0
                graphbreakflaglow = -1
                graphbreakflaghigh = -1
                while i<self.graphprecision:
                    if priceatmaturity[i] < asset1.strike:
                       self.profit[i] = (-2) * asset2.price + asset1.price
                    elif priceatmaturity[i] > asset2.strike:
                       if graphbreakflaglow == -1:
                            graphbreakflaglow = i
                       self.profit[i] = (-2) * asset2.price + asset1.price + asset1.strike - (2 * asset2.strike) + priceatmaturity[i]
                    else:
                       if graphbreakflaghigh == -1:
                            graphbreakflaghigh = i
                       self.profit[i] = (-2) * asset2.price + asset1.price + asset1.strike - priceatmaturity[i] 
                    i=i+1
                self.minprofitindex = graphbreakflaglow
                self.minprofit = self.profit[graphbreakflaglow]
                self.maxprofitindex = graphbreakflaghigh
                self.maxprofit = self.profit[graphbreakflaghigh]
                self.cost = (-2) * asset2.price + asset1.price
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
                self.risk = 3



            #2.4. back spread put
            
            #Properties:
            #minprofit (float)
            #minrofitindex (int)
            #maxprofit (float)
            #maxprofitindex (int)
            #breakeven ([float, float])
            #breakevenindex ([int, int])
            #asset1 = long put
            #asset2 = short put
            #qtty1 = 2
            #qtty2 = 1

            elif strategyname == "back spread put":
                i=0
                graphbreakflaglow = -1
                graphbreakflaghigh = -1
                while i<self.graphprecision:
                    if priceatmaturity[i] < asset1.strike:
                       self.profit[i] = (-2) * asset1.price + asset2.price - asset2.strike + (2*asset1.strike) - priceatmaturity[i]
                    elif priceatmaturity[i] > asset2.strike:
                       if graphbreakflaghigh == -1:
                            graphbreakflaghigh = i
                       self.profit[i] = (-2) * asset1.price + asset2.price
                    else:
                       if graphbreakflaglow == -1:
                            graphbreakflaglow = i
                       self.profit[i] = (-2) * asset1.price + asset2.price - asset2.strike + priceatmaturity[i] 
                    i=i+1
                self.minprofitindex = graphbreakflaglow
                self.minprofit = self.profit[graphbreakflaglow]
                self.maxprofitindex = graphbreakflaghigh
                self.maxprofit = self.profit[graphbreakflaghigh]
                self.cost = (-2) * asset1.price + asset2.price
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
                self.risk = 3



        elif type == 3:
            
            #3.1. Covered call
            
            #Properties:
            #maxprofit (float)
            #maxprofitindex (int)
            #breakeven (float)
            #breakevenindex (int)
            #asset1 = short call
            #qtty1 = 1

            if strategyname == "covered call":
                i=0
                graphbreakflag = -1
                while i<self.graphprecision:
                    if priceatmaturity[i] > asset1.strike:
                       self.profit[i] = asset1.price + asset1.strike - stock.price
                    else:
                       if graphbreakflag == -1:
                            graphbreakflag = i
                       self.profit[i] = asset1.price + priceatmaturity[i] - stock.price 
                    i=i+1
                self.maxprofitindex = graphbreakflag
                self.maxprofit = asset1.price + asset1.strike - stock.price
                self.cost = -stock.price+asset1.price
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
                self.risk = 1



            #3.2. Protective put

            #Properties:
            #minprofit (float)
            #minrofitindex (int)
            #breakeven (float)
            #breakevenindex (int)
            #asset1 = long put
            #qtty1 = 1

            elif strategyname == "protective put":
                i = 0
                graphbreakflag = -1
                while i<self.graphprecision:
                    if priceatmaturity[i] > asset1.strike:
                        self.profit[i] = priceatmaturity[i] - asset1.price - stock.price
                        if graphbreakflag == -1:
                            graphbreakflag = i
                    else:
                        self.profit[i] = asset1.strike - asset1.price - stock.price
                    i=i+1
                self.minprofitindex = graphbreakflag
                self.minprofit = asset1.strike - asset1.price - stock.price
                self.cost = -stock.price - asset1.price
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
                self.risk = 1
   
                

            #3.3. Collar

            #Properties:
            #minprofit (float)
            #minrofitindex (int)
            #maxprofit (float)
            #maxprofitindex (int)
            #breakeven (float)
            #breakevenindex (int)
            #asset1 = long put
            #asset2 = short call
            #qtty1 = 1
            #qtty2 = 1

            elif strategyname == "collar":
                i=0
                graphbreakflaglow = -1
                graphbreakflaghigh = -1
                while i<self.graphprecision:
                    if priceatmaturity[i] > asset2.strike: #max profit
                        if graphbreakflaghigh == -1:
                            graphbreakflaghigh = i
                        self.profit[i] = asset2.price + asset2.strike - stock.price - asset1.price
                    elif priceatmaturity[i] < asset1.strike: #min profit
                        self.profit[i] = asset1.strike - asset1.price - stock.price + asset2.price
                    else:# in between no option exercised
                        if graphbreakflaglow == -1:
                            graphbreakflaglow = i
                        self.profit[i] = priceatmaturity[i] + asset2.price - asset1.price - stock.price
                    i=i+1
                self.minprofit = asset1.strike - asset1.price - stock.price + asset2.price
                self.maxprofit = asset2.price + asset2.strike - stock.price - asset1.price
                self.minprofitindex = graphbreakflaglow
                self.maxprofitindex = graphbreakflaghigh
                self.cost = -stock.price - asset1.price + asset2.price
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
                self.risk = 1



            #3.4. Long call

            #Properties:
            #minprofit (float)
            #minrofitindex (int)
            #breakeven (float)
            #breakevenindex (int)
            #asset1 = long call
            #qtty1 = 1

            elif strategyname == "long call":
                i = 0
                graphbreakflag = -1
                while i < self.graphprecision:
                    if priceatmaturity[i] > asset1.strike:
                        if graphbreakflag == -1:
                            graphbreakflag = i
                        self.profit[i] = priceatmaturity[i] - asset1.strike - asset1.price
                    else:
                        self.profit[i] = -asset1.price
                    i=i+1
                self.minprofit = -asset1.price
                self.minprofitindex = graphbreakflag
                self.cost = -asset1.price
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
                self.risk = 2



            #3.5. Long call spread

            #Properties:
            #minprofit (float)
            #minrofitindex (int)
            #maxprofit (float)
            #maxprofitindex (int)
            #breakeven (float)
            #breakevenindex (int)
            #asset1 = long call
            #asset2 = short call
            #qtty1 = 1
            #qtty2 = 1

            elif strategyname == "long call spread":
                i=0
                graphbreakflaghigh = -1
                graphbreakflaglow = -1
                while i<self.graphprecision:
                    if priceatmaturity[i]>asset2.strike:
                        if graphbreakflaghigh == -1:
                            graphbreakflaghigh = i
                        self.profit[i] = asset2.strike + asset2.price - asset1.price - asset1.strike
                    elif priceatmaturity[i]<asset1.strike:
                        self.profit[i] = asset2.price - asset1.price
                    else:
                        if graphbreakflaglow == -1:
                            graphbreakflaglow = i
                        self.profit[i] = asset2.price - asset1.price - asset1.strike + priceatmaturity[i]
                    i=i+1
                self.maxprofit = asset2.strike + asset2.price - asset1.price - asset1.strike
                self.maxprofitindex = graphbreakflaghigh
                self.minprofit = asset2.price - asset1.price
                self.minprofitindex = graphbreakflaglow
                self.cost = asset2.price - asset1.price
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
                self.risk = 2
            


            #3.6. Short put spread

            #Properties:
            #minprofit (float)
            #minrofitindex (int)
            #maxprofit (float)
            #maxprofitindex (int)
            #breakeven (float)
            #breakevenindex (int)
            #asset1 = long put
            #asset2 = short put
            #qtty1 = 1
            #qtty2 = 1

            elif strategyname == "short put spread":
                i=0
                graphbreakflaghigh = -1
                graphbreakflaglow = -1
                while i<self.graphprecision:
                    if priceatmaturity[i]>asset2.strike:
                        if graphbreakflaghigh == -1:
                            graphbreakflaghigh = i
                        self.profit[i] = asset2.price-asset1.price
                    elif priceatmaturity[i]<asset1.strike:
                        self.profit[i] = asset2.price-asset1.price-asset2.strike+asset1.strike
                    else:
                        if graphbreakflaglow == -1:
                            graphbreakflaglow = i
                        self.profit[i] = asset2.price-asset1.price-asset2.strike+priceatmaturity[i]
                    i=i+1
                self.maxprofit = asset2.price-asset1.price
                self.maxprofitindex = graphbreakflaghigh
                self.minprofit = asset2.price-asset1.price-asset2.strike+asset1.strike
                self.minprofitindex = graphbreakflaglow
                self.cost = asset2.price - asset1.price
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
                self.risk = 3



            #3.7. Short put

            #Properties:
            #maxprofit (float)
            #maxprofitindex (int)
            #breakeven (float)
            #breakevenindex (int)
            #asset1 = short put
            #qtty1 = 1

            elif strategyname == "short put":
                i=0
                graphbreakflag = -1
                while i < self.graphprecision:
                    if priceatmaturity[i] < asset1.strike:
                        self.profit[i] = asset1.price + priceatmaturity[i] - asset1.strike
                    else: 
                        if graphbreakflag == -1:
                                graphbreakflag = i
                        self.profit[i] = asset1.price
                    i=i+1

                    self.maxprofit = asset1.price
                    self.cost = asset1.price
                    self.maxprofitindex = graphbreakflag
                    self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
                    self.risk = 4



            #3.8. Long combination

            #Properties:
            #minprofit (float)
            #minrofitindex (int)
            #maxprofit (float)
            #maxprofitindex (int)
            #breakeven (float)
            #breakevenindex (int)
            #asset1 = long call
            #asset2 = long put
            #qtty1 = 1
            #qtty2 = 1

            elif strategyname == "long combination":
                i=0
                while i < self.graphprecision:
                    if priceatmaturity[i] < asset1.strike:
                        self.profit[i] = -asset1.price + asset2.price -asset2.strike + priceatmaturity[i]
                    else: 
                        self.profit[i] = -asset1.price + asset2.price - asset1.strike + priceatmaturity[i]
                    i=i+1

                    self.cost = asset1.price
                    self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
                    self.risk = 4



        elif type == 4:
            
            #4.1. Long put

            #Properties:
            #minprofit (float)
            #minrofitindex (int)
            #breakeven (float)
            #breakevenindex (int)
            #asset1 = long put
            #qtty1 = 1

            if strategyname == "long put":
                i = 0
                graphbreakflag = -1
                while i < self.graphprecision:
                    if priceatmaturity[i] < asset1.strike:
                        self.profit[i] = asset1.strike - priceatmaturity[i] - asset1.price
                    else:
                        if graphbreakflag == -1:
                            graphbreakflag = i
                        self.profit[i] = -asset1.price
                    i=i+1
                self.minprofit = -asset1.price
                self.minprofitindex = graphbreakflag
                self.cost = -asset1.price
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
                self.risk = 2
            


            #4.2. Long put spread

            #Properties:
            #minprofit (float)
            #minrofitindex (int)
            #maxprofit (float)
            #maxprofitindex (int)
            #breakeven (float)
            #breakevenindex (int)
            #asset1 = short put
            #asset2 = long put
            #qtty1 = 1
            #qtty2 = 1

            elif strategyname == "long put spread":
                i=0
                graphbreakflaghigh = -1
                graphbreakflaglow = -1
                while i<self.graphprecision:
                    if priceatmaturity[i] < asset1.strike:
                        self.profit[i] = asset2.strike + asset1.price - asset2.price - asset1.strike
                    elif priceatmaturity[i] >asset2.strike:
                        if graphbreakflaglow == -1:
                            graphbreakflaglow = i
                        self.profit[i] = asset1.price - asset2.price
                    else:
                        if graphbreakflaghigh == -1:
                            graphbreakflaghigh = i
                        self.profit[i] = -asset2.price + asset1.price - priceatmaturity[i] + asset2.strike
                    i=i+1

                self.maxprofit = asset2.strike + asset1.price - asset2.price - asset1.strike
                self.maxprofitindex = graphbreakflaghigh
                self.minprofitindex = graphbreakflaglow
                self.minprofit = asset1.price - asset2.price
                self.cost = asset1.price - asset2.price
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
                self.risk = 2



            #4.3. Short call spread

            #Properties:
            #minprofit (float)
            #minrofitindex (int)
            #maxprofit (float)
            #maxprofitindex (int)
            #breakeven (float)
            #breakevenindex (int)
            #asset1 = short call
            #asset2 = long call
            #qtty1 = 1
            #qtty2 = 1

            elif strategyname == "short call spread":
                i=0
                graphbreakflaghigh = -1
                graphbreakflaglow = -1
                while i<self.graphprecision:
                    if priceatmaturity[i] < asset1.strike:
                        self.profit[i] = asset1.price - asset2.price
                    elif priceatmaturity[i] > asset2.strike:
                        if graphbreakflaglow == -1:
                                graphbreakflaglow = i
                        self.profit[i] = asset1.price - asset2.price + asset1.strike - asset2.strike
                    else:
                        if graphbreakflaghigh == -1:
                            graphbreakflaghigh = i
                        self.profit[i] = asset1.price-asset2.price+asset1.strike-priceatmaturity[i]
                    i=i+1
                self.maxprofit = asset1.price - asset2.price
                self.maxprofitindex = graphbreakflaghigh
                self.minprofit = asset1.price - asset2.price + asset1.strike - asset2.strike
                self.minprofitindex = graphbreakflaglow
                self.cost = asset1.price - asset2.price
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
                self.risk = 3



            #4.4. Short call

            #Properties:
            #maxprofit (float)
            #maxprofitindex (int)
            #breakeven (float)
            #breakevenindex (int)
            #asset1 = short call
            #qtty1 = 1

            elif strategyname == "short call":
                i=0
                graphbreakflag = -1
                while i < self.graphprecision:
                    if priceatmaturity[i] < asset1.strike:
                        self.profit[i] = asset1.price
                    else: 
                        if graphbreakflag == -1:
                                graphbreakflag = i
                        self.profit[i] = asset1.price - priceatmaturity[i] + asset1.strike
                    i=i+1

                self.maxprofit = asset1.price
                self.cost = asset1.price
                self.maxprofitindex = graphbreakflag
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
                self.risk = 4



            #4.5. Short combination

            #Properties:
            #breakeven (float)
            #breakevenindex (int)
            #asset1 = short call
            #asset2 = long put
            #qtty1 = 1
            #qtty2 = 1

            elif strategyname == "short combination":
                i=0
                while i < self.graphprecision:
                    if priceatmaturity[i] < asset1.strike:
                        self.profit[i] = asset1.price - asset2.price +asset2.strike - priceatmaturity[i]
                    else: 
                        self.profit[i] = asset1.price - asset2.price + asset1.strike - priceatmaturity[i]
                    i=i+1

                self.cost = asset1.price - asset2.price
                self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
                self.risk = 4


        pass
    

