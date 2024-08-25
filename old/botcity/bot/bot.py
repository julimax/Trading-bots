#balance account
import config
from binance.client import Client
import pandas as pd
from datetime import datetime
client = Client(config.apyKey, config.apySecurity)

avbl = client.futures_account_balance()

#df=pd.DataFrame(avbl, columns=['a','b','c','d','s'])
a=  (avbl)
p=float(a[6]['balance'])

print (p)
l=type(p)
print(l)


quantity= int(p/) 





#print(int(p))


#print (int(p))



b=type(a)

#b=int
#print (b)
#print (a["balance"])
#for i in avbl:
#	print (i)



#candles = client.get_klines(symbol='BNBUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, limit=10)
#df= pd.DataFrame(candles[:-1], columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])
#df['date'] = pd.to_datetime(df['date'], unit= 'ms')
#print (str(df['date'][:]),str(df['open']))
#print (candles)





#accounts = client.get_sub_account_list()
#print(accounts)
#balance = client.get_asset_balance(asset='USDT')
#print (balance)
#info = client.get_account()
#prices = client.get_all_tickers()
#print(info)
#print (prices)
#for i in prices:
#	print(i[5:])
#	print(i)

#print(info)
#print(info['symbols'])
