from Strategy_Folder.StrategyBaseModule import *

class Strategy14(StrategyBase):

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

    def __init__(self,stock,asset1,qtty1,asset2,qtty2,fee):

        StrategyBase.__init__(self,"short straddle",stock,asset1=asset1,qtty1=qtty1,asset2=asset2,qtty2=qtty2)

        #1. split self.priceatmaturity

        #split 1: elements <= asset1.strike
        split1 = self.priceatmaturity[self.priceatmaturity<=asset1.strike]
        #split 2: elements > asset1.strike
        split2 = self.priceatmaturity[self.priceatmaturity>asset1.strike]


        #2. use split results to create function valued arrays

        #out 1 from split 1: output elements func = asset1.price + asset2.price - asset2.strike + self.priceatmaturity[i]
        vout1 = asset1.price + asset2.price - asset2.strike
        out1 = [(vout1 + x) for x in split1]
        #out 2 from split 2: output elements func = asset1.price + asset2.price + asset1.strike - self.priceatmaturity[i]
        vout2 = asset1.price + asset2.price + asset1.strike
        out2 = [(vout2 - x) for x in split2]


        #3. join output arrays into one
        self.profit = np.concatenate((out1,out2))


        #4. Calculating properties
        self.maxprofitindex = np.argmax(self.profit)
        self.maxprofit = np.amax(self.profit)
        self.cost = asset1.price + asset2.price
        self.cost,self.profit = AccountForFee(fee,self.profit,self.cost,self.qtty1,self.qtty2,self.qtty3,self.qtty4)
        self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
        self.risk = 4


        pass
    pass


