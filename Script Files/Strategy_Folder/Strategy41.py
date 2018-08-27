from Strategy_Folder.StrategyBaseModule import *

class Strategy41(StrategyBase):

    #4.1. Long put

    #Properties:
    #minprofit (float)
    #minrofitindex (int)
    #breakeven (float)
    #breakevenindex (int)
    #asset1 = long put
    #qtty1 = 1

    def __init__(self,stock,asset1,qtty1,fee):
           
        StrategyBase.__init__(self,"long put",stock,asset1=asset1,qtty1=qtty1)

        #1. split self.priceatmaturity

        #split 1: elements <= asset1.strike
        split1 = self.priceatmaturity[self.priceatmaturity<=asset1.strike]
        #split 2: elements > asset1.strike
        split2 = self.priceatmaturity[self.priceatmaturity>asset1.strike]


        #2. use split results to create cte valued arrays

        #out2 from split 2: output element values = -asset1.price
        vout2 = -asset1.price
        out2 = np.full(split2.shape,vout2)


        #3. use split results to create function valued arrays

        #out 1 from split 1: output elements func = asset1.strike - self.priceatmaturity[i] - asset1.price
        vout1 = asset1.strike - asset1.price
        out1 = [(vout1 - x) for x in split1]


        #4. join output arrays into one
        self.profit = np.concatenate((out1,out2))


        #5. Calculating properties
        self.minprofitindex = np.argmin(self.profit)
        self.minprofit = np.amin(self.profit)
        self.cost = vout2
        self.cost,self.profit = AccountForFee(fee,self.profit,self.cost,self.qtty1,self.qtty2,self.qtty3,self.qtty4)
        self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,1,self.graphprecision,self.xaxisrange)
        self.risk = 2



        pass

    pass

