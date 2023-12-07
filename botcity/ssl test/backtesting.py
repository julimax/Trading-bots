import config
from binance.client import Client
import pandas as pd
from sslChanel import ssl

client = Client(config.apyKey, config.apySecurity)

candles=client.futures_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_15MINUTE,limit=1500)

df = pd.DataFrame(candles, columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])
hora = df['date'] = pd.to_datetime(df['date'], unit= 'ms')

ema200 = df["close"].ewm(span=200, adjust=False).mean()
ema25 = df["close"].ewm(span=25, adjust=False).mean()

dfOpen = df['open'].astype(float)
dfHigh = df['high'].astype(float)
dfLow = df['low'].astype(float)
dfClose = df['close'].astype(float)

sslH = ssl()[0]
sslL = ssl()[1]
#print (len(sslH))
global tradeLong
global tradeShort

tendenciaL = 'none'
tendenciaS = 'none'
tradeLong = 'none'
tradeShort = 'none'
perdidasLong = 0
perdidasshort = 0
ganadasLong = 0
ganadasShort = 0
tendencia = 'none'
def long():
	global tendenciaL
	global tradeLong
	global perdidasLong
	global ganadasLong
	count = 0

	for i in range(1498):
		print (count + 1)
		if sslH[count] > sslL[count]:
			tendenciaL = 'long'
		if sslH[count] < sslL[count]:
			tendenciaL = 'short'


# and dfClose[count + 1] > ema200 [count + 1]
		if tendenciaL == 'short' and tradeLong == 'none':
			if sslH[count + 1] > sslL[count +1]  and dfClose[count + 1] < ema25[count + 1]:
				entry = dfClose[count + 1]
				print ('open long en ' + str(dfClose[count + 1]) + ' hora ' + str(hora[count + 1]) )
				print (str(sslH[count + 1]) + '   ' + str(sslL[count + 1]) + ' ema200 ' + str(ema200[count + 1]))
				tradeLong = 'on'
				stopLoss = sslL[count + 1] 
				taketProfit = entry + ((entry - stopLoss) * 1)
				print('stopLoss ' + str(stopLoss) + ' taketProfit ' + str(taketProfit))

		if tradeLong == 'on':
			if stopLoss > dfLow[count + 2]:
				print('stopLoss long')
				perdidasLong += 1
				tradeLong = 'none'

			if taketProfit < dfHigh[count + 2]:
				print('taketProfit long')
				ganadasLong += 1
				tradeLong = 'none'

		count += 1

def short():
	global tradeShort
	global ganadasShort
	global perdidasshort
	global tendenciaS
	count = 0

	for i in range(1498):
		print (count + 1)
		if sslH[count] > sslL[count]:
			tendenciaS = 'long'
		if sslH[count] < sslL[count]:
			tendenciaS = 'short'
#and dfClose[count + 1] < ema200 [count + 1]
		if tendenciaS == 'long' and tradeShort == 'none':
			if sslH[count + 1] < sslL[count +1]  and dfClose[count + 1] > ema25[count + 1]:
				entryShort = dfClose[count + 1]
				print ('open short en ' + str(dfClose[count + 1]) + ' hora ' + str(hora[count + 1]) )
				print (str(sslH[count + 1]) + '   ' + str(sslL[count + 1]) + ' ema200 ' + str(ema200[count + 1]))
				tradeShort = 'on'
				stopLossShort = sslL[count + 1]
				taketProfitShort = entryShort - ((stopLossShort - entryShort) * 1)
				print ('stopLoss ' + str(stopLossShort) + ' taketProfit ' + str(taketProfitShort))

		if tradeShort == 'on':
			if stopLossShort < dfHigh[count + 2]:
				print('stopLoss short ' + str(hora[count + 2]))
				perdidasshort += 1
				tradeShort = 'none'

			if taketProfitShort > dfLow[count + 2]:
				print('taketProfit short' + str(hora[count + 2]))
				ganadasShort += 1
				tradeShort = 'none'


		count += 1
long()
print('---------------------------------------')
short()

print('ganadasLong ' + str(ganadasLong) )
print('ganadasShort ' + str(ganadasShort) )
print('perdidasLong ' + str(perdidasLong) )
print('perdidasshort ' + str(perdidasshort) )