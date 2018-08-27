from Strategy_Folder.StrategyBaseModule import *

class Strategy35(StrategyBase):

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

    def __init__(self,stock,asset1,qtty1,asset2,qtty2,fee):

        StrategyBase.__init__(self,"long call spread",stock,asset1=asset1,qtty1=qtty1,asset2=asset2,qtty2=qtty2)

        #1. split self.priceatmaturity

        #split 1: elements <= asset1.strike
        split1 = self.priceatmaturity[self.priceatmaturity<=asset1.strike]
        #split 2: asset1.strike < elements <= asset2.strike
        split2 = self.priceatmaturity[(self.priceatmaturity>asset1.strike)&(self.priceatmaturity<=asset2.strike)]
        #split 3: elements > asset2.strike
        split3 = self.priceatmaturity[self.priceatmaturity>asset2.strike]


        #2. use split results to create cte valued arrays

        #out1 from split 1: output element values = asset2.price - asset1.price
        vout1 = asset2.price - asset1.price
        out1 = np.full(split1.shape,vout1)
        #out3 from split 3: output element values = asset2.strike + asset2.price - asset1.price - asset1.strike
        vout3 = asset2.strike + asset2.price - asset1.price - asset1.strike
        out3 = np.full(split3.shape,vout3)


        #3. use split results to create function valued arrays

        #out 2 from split 2: output elements func = asset2.price - asset1.price - asset1.strike + self.priceatmaturity[i]
        vout2 = asset2.price - asset1.price - asset1.strike
        out2 = [(vout2 + x) for x in split2]


        #4. join output arrays into one
        self.profit = np.concatenate((out1,out2,out3))


        #5. Calculating properties
        self.minprofitindex= np.argmin(self.profit)
        self.minprofit = np.amin(self.profit)
        self.maxprofitindex = np.argmax(self.profit)
        self.maxprofit = np.amax(self.profit)
        self.cost = vout1
        self.cost,self.profit = AccountForFee(fee,self.profit,self.cost,self.qtty1,self.qtty2,self.qtty3,self.qtty4)
        self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
        self.risk = 2


        pass


    pass
