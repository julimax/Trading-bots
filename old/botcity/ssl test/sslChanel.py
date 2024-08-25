
import config
from binance.client import Client
import pandas as pd



def ssl():
	client = Client(config.apyKey, config.apySecurity)
	candles=client.futures_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_15MINUTE,limit=1500)
	df= pd.DataFrame(candles, columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])
	price = df['close'].astype(float)

	low = df['low'].astype(float)
	high = df['high'].astype(float)

	smaLow = low.rolling(window = 10).mean()
	smaHigh = high.rolling(window = 10).mean()

	Hlv = 'none'
	sslH = []
	sslL = []
	it = 0
	for i in range(1500):
		if price[it] == smaHigh[it] or price[it] == smaLow[it]:
			print('adasd')
		
		if it < 9:
			sslH.append(price[it])
			sslL.append(price[it])
    
		if (price[it] > smaLow[it] or price[it] == smaLow[it]) and Hlv == 'none':
			sslH.append(smaHigh[it])
        	#sslH[it] = smaHigh[it]
        	#sslL[it] = smaLow[it]
			sslL.append(smaLow[it])
        
		if price[it] > smaHigh[it] and Hlv == 'inverted':
			sslH.append(smaHigh[it])
        	#sslH[it] = smaHigh[it]
        	#sslL[it] = smaLow[it]
			sslL.append(smaLow[it])
			Hlv = 'none'

        
		if (price[it] < smaHigh[it] or price[it] == smaHigh[it]) and Hlv == 'inverted':
			sslH.append(smaLow[it])
        	#sslH[it] = smaHigh[it]
        	#sslL[it] = smaLow[it] 
			sslL.append(smaHigh[it])
       
        
		if price[it] < smaLow[it] and Hlv == 'none':
			sslH.append(smaLow[it])
        	#sslH[it] = smaHigh[it]
        	#sslL[it] = smaLow[it]
			sslL.append(smaHigh[it])
			Hlv = 'inverted'
        
		it += 1
	print (len(sslH ))
	print ('  e')
	print ( len(sslL))
	return (sslH, sslL)
	

	
ssl()
