#info trade actual

import config
from binance.client import Client
import pandas as pd
from datetime import datetime
client = Client(config.apyKey, config.apySecurity)
global count
count = 0

a = client.futures_position_information()
#b= a["entryPrice"]
#print (a[139])
#print (str(a['entryPrice']))
#count =0
#for i in a:
#	print(count)
#	print (i)
#	count +=1
#print(a[59])
infoTrade = client.futures_position_information()
for i in infoTrade:
	if infoTrade[count]['symbol'] == 'CTSIUSDT':
		print ('aaaaa')
	print (count)
	print(infoTrade[count])

	count += 1
#candles=client.futures_klines(symbol='GMTUSDT', interval=Client.KLINE_INTERVAL_1MINUTE,limit=30)
#df= pd.DataFrame(candles, columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])
#print(df)