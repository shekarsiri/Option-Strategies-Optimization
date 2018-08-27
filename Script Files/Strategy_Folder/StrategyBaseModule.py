import math
import numpy as np
from AssetModule import Asset
from StockModule import Stock
from ExecutableModule import *

def AccountForFee(fee,profitcurve,cost,qtty1,qtty2,qtty3,qtty4):

    cost = cost - ((qtty1 + qtty2 + qtty3 + qtty4)*fee)
    profitcurve = profitcurve - ((qtty1 + qtty2 + qtty3 + qtty4)*fee)

    return cost, profitcurve

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


#self.profit = self.profit + ((qtty1 + qtty2 + qtty3 + qtty4)*fee)

class StrategyBase:
    
    dummyasset = Asset("short_call",0,0,0,1,1,2050,0,0,"dummy")

    #REMOVI type (depois de strategy name)
    def __init__(self,strategyname,stock,stockqtty=0, asset1=dummyasset,qtty1=0,asset2=dummyasset,qtty2=0,asset3=dummyasset,qtty3=0,asset4=dummyasset,qtty4=0):
        
        #Properties common across all strategies:
        #profit[i] (float numpy array) (size = graph precision): profit curve
        #priceatmaturitylin (float numpy array) (size = graph precision): linear distribution of stock price variation delimited by xaxisrange
        #maturity (float): number of days until maturity
        #risk (int): risk profile respective to te strategy scale goes from 1 to 4, 1 = least risky | 4 = most risky
        #cost: credit or debit necessary to open the position (transaction fee not included)

        self.profit = np.empty(StrategyBase.graphprecision)
        self.priceatmaturity= np.linspace(stock.price-(stock.price*StrategyBase.xaxisrange),stock.price+(stock.price*StrategyBase.xaxisrange),StrategyBase.graphprecision)
        self.maturity = min(asset1.timetomat,asset2.timetomat,asset3.timetomat,asset4.timetomat)

        self.asset1 = asset1
        self.asset2 = asset2
        self.asset3 = asset3
        self.asset4 = asset4

        self.qtty1=qtty1
        self.qtty2=qtty2
        self.qtty3=qtty3
        self.qtty4=qtty4

        self.name = strategyname

        self.maxprofit = -999
        self.minprofit = -999

        pass
    
    def SetGraphPrecision(input):
        
        StrategyBase.graphprecision = input

        pass

    def SetXaxisrange(input):
        
        StrategyBase.xaxisrange = input

        pass

    pass

