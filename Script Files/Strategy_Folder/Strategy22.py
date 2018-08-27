from Strategy_Folder.StrategyBaseModule import *

class Strategy22(StrategyBase):
    
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

    def __init__(self,stock,asset1,qtty1,asset2,qtty2,fee):

        StrategyBase.__init__(self,"long strangle",stock,asset1=asset1,qtty1=qtty1,asset2=asset2,qtty2=qtty2)


        #1. split self.priceatmaturity

        #split 1: elements <= asset1.strike
        split1 = self.priceatmaturity[self.priceatmaturity<=asset1.strike]
        #split 2: asset1.strike < elements <= asset2.strike
        split2 = self.priceatmaturity[(self.priceatmaturity>asset1.strike)&(self.priceatmaturity<=asset2.strike)]
        #split 3: elements > asset2.strike
        split3 = self.priceatmaturity[self.priceatmaturity>asset2.strike]


        #2. use split results to create cte valued arrays

        #out2 from split 2: output element values = asset1.price + asset2.price
        vout2 = -asset1.price -asset2.price
        out2 = np.full(split2.shape,vout2)


        #3. use split results to create function valued arrays
        
        #out 1 from split 1: output elements func = -asset1.price - asset2.price + asset1.strike - self.priceatmaturity[i]
        vout1 = -asset1.price - asset2.price + asset1.strike
        out1 = [(vout1 - x) for x in split1]
        #out 3 from split 3:output elements func = -asset1.price -asset2.price - asset2.strike + self.priceatmaturity[i]
        vout3 = -asset1.price -asset2.price - asset2.strike 
        out3 = [(vout3 + x) for x in split3]


        #4. join output arrays into one
        self.profit = np.concatenate((out1,out2,out3))


        #5. Calculating properties
        self.minprofitindex = np.argmin(self.profit)
        self.minprofit = np.amin(self.profit)
        self.cost = vout2
        self.cost,self.profit = AccountForFee(fee,self.profit,self.cost,self.qtty1,self.qtty2,self.qtty3,self.qtty4)
        self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
        self.risk = 3


        pass
    pass