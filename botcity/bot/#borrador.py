#borrador

import config
from binance.client import Client
import pandas as pd
from datetime import datetime
from array import array

client = Client(config.apyKey, config.apySecurity)

#avbl = client.futures_position_information()
#print (avbl)
candles = client.futures_klines(symbol='BNBUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, limit=100)
df= pd.DataFrame(candles, columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])
dff = df['close'].astype(float)
#print(dff)
#n=0

#print (num)
#dfc = []
#for i in range(9):
#	dfc.append(float(df['close'][n]))
#	print(dfc)
#	n += 1






def rsi(df, periods = 14, ema = True):
    """
    Returns a pd.Series with the relative strength index.
    """

    close_delta = dff.diff()
    print(close_delta)
    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    print (up)
    if ema == True:
	    # Use exponential moving average
        ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window = periods, adjust=False).mean()
        ma_down = down.rolling(window = periods, adjust=False).mean()
        
    print(ma_up)    
    rsi = ma_up / ma_down
    print
    rsi = 100 - (100/(1 + rsi))
    print (rsi)
    return rsi

rsi(dff)
#a = rsi
#print(a)