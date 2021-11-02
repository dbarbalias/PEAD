import yfinance as yf
import pandas as pd

class StockObj():

    def __init__(self, tic, end=None, delta=None):

        self.tic = tic
        self.full_obj = yf.Ticker(tic)
        self.get_info()
        self.spike = 0

        if (self.market_cap >= 1000000000 or self.market_cap == 0 or self.market_cap == None) and self.current_price > 35 and self.year_return > 0: #mid cap stock or no data and above 35 dollars a share  CHECK FOR VALUE GROWTH
            if self.financial_check():
                self.count_spike()

    def get_info(self):
        x = self.full_obj.info
        self.sector = x['sector']
        self.summary = x['longBusinessSummary']
        self.industry = x['industry']
        self.market_cap = x['marketCap']
        self.book_ratio = x['bookValue']
        self.trailing_pe = x['trailingPE']
        self.institution_percent = x['heldPercentInstitutions']
        self.current_price = x['previousClose']
        self.year_return = x['52WeekChange']

    def count_spike(self):
        x = self.full_obj.history(period='2mo')
        x = x[['Close', 'Volume']]
        x['Vol 15 Day'] = x['Volume'].rolling(window=15).mean() #15 day rolling average on the volume
        x['Price 15'] = x['Close'].rolling(window=15).mean() #15 day rolling average on the price
        x['Spike'] = ((x['Volume'] - x['Vol 15 Day']) / x['Vol 15 Day'] > 1)  #BRING THIS TO 1.3 from 2 and maybe low; simply looking for volume
        x = x[x['Spike']] #filtering out all volume spikes
        x = x[((x.Close - x['Price 15'])/ x['Price 15']) > 0.02] # BRING THIS DOWN from 0.03; positive price actions on these days

        self.spike = x.Spike.count()

    def financial_check(self):
        x = self.full_obj.quarterly_earnings.pct_change()
        self.max_revenue = x.Revenue.max()
        self.average_revenue = x.Revenue.mean()

        self.max_earnings = x.Earnings.max()
        self.average_earnings = x.Earnings.mean()

        if self.average_earnings > 0.01 and self.average_revenue > 0.01 and (self.max_earnings > 0.5 or self.max_revenue > 0.5): #no negative values and unique
            return True
        else:
            return False

    def __str__(self):
        return self.tic
    

if __name__ == '__main__':
    x = StockDaddy('SRC')
    print(f'max revenue: {x.max_revenue}')
    print(f'max earnings: {x.max_earnings}')
    print(f'av revenue: {x.average_earnings}')
    print(f'av earnings: {x.average_revenue}')
    print(x.spike)
    
