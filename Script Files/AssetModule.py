from datetime import date

class Asset:
        
    def __init__(self, type, strike, bid, ask, matday, matmonth, matyear, vol, interest,tagname ):

        self.strike = strike
        self.vol = vol
        self.interest = interest
        self.matday = matday
        self.matmonth = matmonth
        self.matyear = matyear
        self.timetomat = self.TimeToMaturity(matday,matmonth,matyear)
        self.tag = tagname

        if type == "short_call":
            self.assetname = "call"
            self.positiontype = "short"
            self.price = bid

        if type == "long_call":
            self.assetname = "call"
            self.positiontype = "long"
            self.price = ask

        if type == "short_put":
            self.assetname = "put"
            self.positiontype = "short"
            self.price = bid

        if type == "long_put":
            self.assetname = "put"
            self.positiontype = "long"
            self.price = ask

        return

    def TimeToMaturity(self,matday,matmonth,matyear):

        maturitydate = date(int(matyear),int(matmonth),int(matday))
        currentdate = date.today()
        delta = maturitydate - currentdate
        timetomat = float(delta.days)
        
        return timetomat




