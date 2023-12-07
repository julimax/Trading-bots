
import config
from binance.client import Client
import pandas as pd



def ssl():
	client = Client(config.apyKey, config.apySecurity)
	candles=client.futures_klines(symbol='BNBUSDT', interval=Client.KLINE_INTERVAL_5MINUTE,limit=50)
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
	for i in range(50):
		
		if it < 9:
			sslH.append(price[it])
			sslL.append(price[it])
    
		if price[it] > smaLow[it] and Hlv == 'none':
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

        
		if price[it] < smaHigh[it] and Hlv == 'inverted':
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

	return (sslH[48], sslL[48], sslH[49], sslL[49])
	


ssl()
