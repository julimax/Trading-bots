import config
from binance.client import Client
import pandas as pd

global limit

client = Client(config.apyKey, config.apySecurity)
limit = 500
candles=client.futures_klines(symbol='MATICUSDT', interval=Client.KLINE_INTERVAL_15MINUTE,limit=limit)

df = pd.DataFrame(candles, columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])

velas = 100
cubos = 5

def maxMin(df, velas, cubos):
	global position
	global pl
	global ph

	pl = 0
	ph = 0

	low = []
	high = []

	dfMin = df['low'].astype(float)
	dfMax = df['high'].astype(float)

	velasTotal = velas * cubos

	position = limit - velas 

	de = 0
	hasta = (velas / cubos)

	hasta = int(hasta)

	for i in range(cubos):
		low.append(min(dfMin , position, hasta))
		high.append(max(dfMax , position, hasta))
		
		position += hasta
		
	print (low)
	print (high)

	return (low, high)




def min(dfMin, position, hasta):
	global pl

	numMin = 100000
	low = []
	
	
	for i in range(hasta):
		
		if dfMin[position] < numMin:
			
			numMin = dfMin[position]
			
			low = [dfMin[pl],pl]
		position += 1
		pl += 1	

	
	return (low)

def max(dfMin, position, hasta):
	global ph

	numMax = 0
	high = []
	
	
	for i in range(hasta):
		
		if dfMax[position] > numMax:
			
			numMax = dfMax[position]
			
			high = [dfMax[ph],ph]
		position += 1
		ph += 1	

	return (high)


#print (df['low'][10])

dfMin = df['low'].astype(float)
dfMax = df['high'].astype(float)

#print(str(min(dfMin, position))+ ' aaaaaaaaaaaaaa')
#print(str(max(dfMax)) + '  aaaaaaaaaaaaaaaa')
#print (dfMin)
maxMin(df , velas, cubos)

def estructura():
	estructura = []
	low = maxMin(df , velas, cubos)[0]
	high = maxMin(df , velas, cubos)[1]

	L = low[0]
	H = high[0]

	if L[1] < H[1]:
		for i in range(len(low) - 1):
			
			if low[1][1] < high[1][1]:
				estructura = []
				if low[1][0] < L[0]:

	else:
		print ('else')


	print (L)
	print (H)

	

estructura()