import datetime

class Stock:

    #Constructor for stocks
    def __init__(self, stockname, stockprice, currentdate):
        self.assetname = stockname
        self.price = float(stockprice)
        self.currentdate = currentdate #TODO: split date into year, month day
        self.timetomat = 1000
        return
