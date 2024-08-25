#info exchange


import config
from binance.client import Client
import pandas as pd
from datetime import datetime
client = Client(config.apyKey, config.apySecurity)
 
#a=client.futures_coin_klines(symbol='BNBBTC', interval=Client.KLINE_INTERVAL_1MINUTE, limit=10)
a=client.futures_klines(symbol='BNBUSDT', interval=Client.KLINE_INTERVAL_1MINUTE,limit=10)

df= pd.DataFrame(a[:-1], columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])
                            
df['date'] = pd.to_datetime(df['date'], unit= 'ms')

print(a)
"""for i in (a):
	print (i)

a=client.futures_coin_exchange_info()
#print (a)

for i in a:
	print(i)"""