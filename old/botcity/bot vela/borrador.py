

import config
from binance.client import Client
import pandas as pd

client = Client(config.apyKey, config.apySecurity)

candles=client.futures_klines(symbol='BNBUSDT', interval=Client.KLINE_INTERVAL_3MINUTE,limit=1000)

df = pd.DataFrame(candles, columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])
hora = df['date'] = pd.to_datetime(df['date'], unit= 'ms')

dfOpen = df['open'].astype(float)
dfHigh = df['high'].astype(float)
dfLow = df['low'].astype(float)
dfClose = df['close'].astype(float)

s = 0
trade = False
ganada = 0
perdida = 0 
stopLoss = 0.0
takeProfit = 0.0
for i in dfClose:
	cola = dfOpen[s] - dfLow[s]
	cuerpo = dfClose[s] - dfOpen[s]
	if dfClose[s] >= (dfHigh[s] - 0.95 ) and dfLow[s] < dfOpen[s] and trade == False and dfClose[s] > dfOpen [s] and cola > cuerpo *1.5:
		horario = hora[s]
		print('horario ' +str(horario))
		print('close ' +str(dfClose[s]) + ' open ' + str(dfOpen[s]) + ' low ' + str(dfLow[s]) + ' high ' + str(dfHigh[s]))
		trade = True
		stopLoss = dfLow[s]
		takeProfit = ((dfClose[s] - dfLow[s]) * 1.5) + dfClose[s]
		print('takeProfit ' + str(takeProfit) + ' stopLoss ' + str(stopLoss)) 
	if trade:
		if dfLow[s] < stopLoss:
			perdida +=1
			trade = False
			print ('cierre por stopLoss ' + str(dfLow[s]))
			print(' ')
		elif dfHigh[s] > takeProfit:
			ganada += 1
			trade = False
			print('cierre por takeProfit ' + str(takeProfit))
			print(' ')
	s += 1

print(ganada)
print(perdida)

print('-------short----------')
ganadaShort = 0
perdidaShort = 0
trade = False
s = 0

for i in dfClose:
	cola = dfHigh[s] - dfOpen[s]
	cuerpo = dfOpen[s] - dfClose[s]
	horario = hora[s]
	if dfClose[s] <= (dfLow[s] + 0.95 )  and dfHigh[s] > dfOpen[s] and trade == False and dfClose[s] < dfOpen [s] and cola > cuerpo *1.5:
		
		print('horario ' +str(horario))
		print('close ' +str(dfClose[s]) + ' open ' + str(dfOpen[s]) + ' low ' + str(dfLow[s]))
		trade = True
		stopLoss = dfHigh[s]
		takeProfit = ((dfHigh[s] - dfClose[s]) * -1.5) + dfClose[s]
		print('takeProfit ' + str(takeProfit) + ' stopLoss ' + str(stopLoss) + ' high ' + str(dfHigh[s])) 
	if trade:
		if dfHigh[s] > stopLoss:
			perdidaShort +=1
			trade = False
			print ('cierre por stopLoss ' + str(dfHigh[s]))
			print(horario)
			print(' ')
		elif dfLow[s] <= takeProfit:
			ganadaShort += 1
			trade = False
			print('cierre por takeProfit ' + str(takeProfit))
			print(' ')
	s += 1


print(ganada)
print(perdida)
print(' short')
print(ganadaShort)
print(perdidaShort)

