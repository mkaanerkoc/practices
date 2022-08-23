import numpy as np
import matplotlib.pyplot as plt

first_price, last_price = 1400, 1800

strike_price = 1600
premium = 70

class PNL(object):
    def __init__(self, strike_price, premium, start, end):
        self._strike = strike_price
        self._premium = premium
        self._start = start
        self._end = end
        self._prices = np.arange(start, end, 1)
        self._constant_part = None
        self._linear_part = None
        self._profile = None
        self._multiplier = 0
            
    def plot(self):
        plt.plot(self._prices, self._profile)
        
    def __add__(self, other):
        if self._start != other._start or self._end != other._end:
            raise('start and end prices are not same')
        
        result = PNL(0, 0, self._start, self._end)
        result._profile = self._profile + other._profile
        return result

        
class CallPNL(PNL):
    def __init__(self, strike_price, premium, start, end):
        super().__init__(strike_price, premium, start, end)
        self._breakeven = strike_price + premium
        
    def calculate_pnl(self):
        self._constant_part = np.ones(self._strike - self._start) * self._premium * self._multiplier
        self._linear_part = np.linspace(-self._premium, self._end-self._breakeven, num=self._end-self._strike) 
        self._linear_part *=  self._multiplier * -1
        self._profile = np.concatenate((self._constant_part, self._linear_part))
    

class LongCallPNL(CallPNL):
    def __init__(self, strike_price, premium, start, end):
        super().__init__(strike_price, premium, start, end)
        self._multiplier = -1
    

class ShortCallPNL(CallPNL):
    def __init__(self, strike_price, premium, start, end):
        super().__init__(strike_price, premium, start, end)
        self._multiplier = 1

        
class PutPNL(PNL):
    def __init__(self, strike_price, premium, start, end):
        super().__init__(strike_price, premium, start, end)
        self._breakeven = strike_price - premium
        
    def calculate_pnl(self):
        self._constant_part = np.ones(self._end - self._strike) * self._premium * self._multiplier
        self._linear_part = np.linspace(self._breakeven - self._start, - self._premium, num=self._strike - self._start)
        self._linear_part *=  self._multiplier * -1
        self._profile = np.concatenate((self._linear_part, self._constant_part))

class LongPutPNL(PutPNL):
    def __init__(self, strike_price, premium, start, end):
        super().__init__(strike_price, premium, start, end)
        self._multiplier = -1       


class ShortPutPNL(PutPNL):
    def __init__(self, strike_price, premium, start, end):
        super().__init__(strike_price, premium, start, end)
        self._multiplier = 1
        
        
        
a = LongCallPNL(strike_price, premium, first_price, last_price)
a.calculate_pnl()
a.plot()
plt.grid()


## arbitrage payoff
first_price, last_price = 1650, 1750
long_call = LongCallPNL(1700, 24.65, first_price, last_price)
short_call = ShortCallPNL(1700, 32, first_price, last_price)

long_call.calculate_pnl()
short_call.calculate_pnl()

arbitrage_payoff = long_call + short_call

long_call.plot()

short_call.plot()
# arbitrage_payoff.plot()

plt.grid()
plt.plot(arbitrage_payoff._prices, arbitrage_payoff._profile)
