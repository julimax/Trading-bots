import config
from binance.client import Client
import pandas as pd


client = Client(config.apyKey, config.apySecurity)

candles=client.futures_klines(symbol='BNBUSDT', interval=Client.KLINE_INTERVAL_15MINUTE,limit=15)



df = pd.DataFrame(candles, columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])
dfrsi = df['close'].astype(float)




def rsi(df, periods = 14, ema = True):
    """
    Returns a pd.Series with the relative strength index.
    """

    close_delta = df.diff()
    
    # Make two series: one for lower closes and one for higher closes
    up = close_delta.clip(lower=0)
    down = -1 * close_delta.clip(upper=0)
    
    if ema == True:
	    # Use exponential moving average
        ma_up = up.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
        ma_down = down.ewm(com = periods - 1, adjust=True, min_periods = periods).mean()
    else:
        # Use simple moving average
        ma_up = up.rolling(window = periods, adjust=False).mean()
        ma_down = down.rolling(window = periods, adjust=False).mean()
        
       
    rsi = ma_up / ma_down
    print
    rsi = 100 - (100/(1 + rsi))

    
    print(rsi)
    return rsi
    
    


rsi1 = rsi(dfrsi)
print(rsi1)