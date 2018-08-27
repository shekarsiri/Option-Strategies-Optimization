from Strategy_Folder.StrategyBaseModule import *

class Strategy34(StrategyBase):

    #3.4. Long call
    
    #Properties:
    #minprofit (float)
    #minrofitindex (int)
    #breakeven (float)
    #breakevenindex (int)
    #asset1 = long call
    #qtty1 = 1

    def __init__(self,stock,asset1,qtty1,fee):

        StrategyBase.__init__(self,"long call",stock,asset1=asset1,qtty1=qtty1)

        #1. split self.priceatmaturity

        #split 1: elements <= asset1.strike
        split1 = self.priceatmaturity[self.priceatmaturity<=asset1.strike]
        #split 2: elements > asset1.strike
        split2 = self.priceatmaturity[self.priceatmaturity>asset1.strike]


        #2. use split results to create cte valued arrays

        #out1 from split 1: output element values = -asset1.price
        vout1 = -asset1.price
        out1 = np.full(split1.shape,vout1)


        #3. use split results to create function valued arrays

        #out 2 from split 2: output elements func = self.priceatmaturity[i] - asset1.strike - asset1.price
        vout2 = - asset1.strike - asset1.price
        out2 = [(vout2 + x) for x in split2]


        #4. join output arrays into one
        self.profit = np.concatenate((out1,out2))


        #5. Calculating properties
        self.minprofitindex = np.argmin(self.profit)
        self.minprofit = np.amin(self.profit)
        self.cost = vout1
        self.cost,self.profit = AccountForFee(fee,self.profit,self.cost,self.qtty1,self.qtty2,self.qtty3,self.qtty4)
        self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
        self.risk = 2


        pass


    pass
