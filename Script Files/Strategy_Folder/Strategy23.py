from Strategy_Folder.StrategyBaseModule import *

class Strategy23(StrategyBase):

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

    def __init__(self,stock,asset1,qtty1,asset2,qtty2,fee):

        StrategyBase.__init__(self,"back spread call",stock,asset1=asset1,qtty1=qtty1,asset2=asset2,qtty2=qtty2)

        #1. split self.priceatmaturity

        #split 1: elements <= asset1.strike
        split1 = self.priceatmaturity[self.priceatmaturity<=asset1.strike]
        #split 2: asset1.strike < elements <= asset2.strike
        split2 = self.priceatmaturity[(self.priceatmaturity>asset1.strike)&(self.priceatmaturity<=asset2.strike)]
        #split 3: elements > asset2.strike
        split3 = self.priceatmaturity[self.priceatmaturity>asset2.strike]


        #2. use split results to create cte valued arrays

        #ou1 from split 1: (-2) * asset2.price + asset1.price
        vout1 = (-2) * asset2.price + asset1.price
        out1 = np.full(split1.shape,vout1)


        #3. use split results to create function valued arrays
        
        #out 2 from split 2: output elements func = (-2) * asset2.price + asset1.price + asset1.strike - self.priceatmaturity[i]
        vout2 = (-2) * asset2.price + asset1.price + asset1.strike
        out2 = [(vout2 - x) for x in split2]
        #out 3 from split 3:output elements func = (-2) * asset2.price + asset1.price + asset1.strike - (2 * asset2.strike) + self.priceatmaturity[i]
        vout3 = (-2) * asset2.price + asset1.price + asset1.strike - (2 * asset2.strike)
        out3 = [(vout3 + x) for x in split3]


        #4. join output arrays into one
        self.profit = np.concatenate((out1,out2,out3))


        #5. Calculating properties
        self.minprofitindex= np.argmin(self.profit)
        self.minprofit = np.amin(self.profit)
        self.maxprofitindex = np.argmax(self.profit)
        self.maxprofit = np.amax(self.profit)
        self.cost = vout1
        self.cost,self.profit = AccountForFee(fee,self.profit,self.cost,self.qtty1,self.qtty2,self.qtty3,self.qtty4)
        self.breakeven,self.breakevenindex = GetBreakEvenPoint(self.profit,2,self.graphprecision,self.xaxisrange)
        self.risk = 3



        pass
    pass