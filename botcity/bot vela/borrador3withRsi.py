import config
from binance.client import Client
import pandas as pd
from rsi import rsi

client = Client(config.apyKey, config.apySecurity)

candles=client.futures_klines(symbol='BNBUSDT', interval=Client.KLINE_INTERVAL_15MINUTE,limit=1500)

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

prsi = df['close'].astype(float)
rsiLast = rsi(prsi)
print(rsiLast[14])

for i in range(999):
	velaAnterior = dfClose[s + 13] - dfOpen[s + 13]
	cola = dfClose[s + 14] - dfLow[s + 14]
	cuerpo = dfOpen[s + 14] - dfClose[s + 14]
	if dfClose[s] >= (dfHigh[s + 1] - 5.9 ) and dfLow[s + 14] < dfOpen[s + 14] and trade == False and dfClose[s + 14] < dfOpen [s + 14] and cola  > cuerpo * 5 and velaAnterior < 0 and rsiLast[s + 14] < 50:
		horario = hora[s+1]
		print('horario ' +str(horario))
		print('close ' +str(dfClose[s + 14]) + ' open ' + str(dfOpen[s + 14]) + ' low ' + str(dfLow[s + 14]) + ' high ' + str(dfHigh[s + 14]))
		trade = True
		
		takeProfit = ((dfClose[s + 14] - dfLow[s + 14]) * 1) + dfClose[s + 14]
		stopLoss = dfLow[s + 14] 

		print('takeProfit ' + str(takeProfit) + ' stopLoss ' + str(stopLoss))
		s +=1  
	if trade:
		if dfLow[s + 14] < stopLoss:
			perdida +=1
			trade = False
			print ('cierre por stopLoss ' + str(dfLow[s + 14]))
			print(' ')
		elif dfHigh[s + 14] > takeProfit:
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

for i in range(999):
	velaAnterior = dfClose[s + 13] - dfOpen[s + 13]
	cola = dfHigh[s + 14] - dfClose[s + 14]
	cuerpo = dfClose[s + 14] - dfOpen[s + 14]
	horario = hora[s + 14]
	if dfClose[s + 14] <= (dfLow[s + 14] + 5.9 )  and dfHigh[s + 14] > dfOpen[s + 14] and trade == False and dfClose[s + 14] > dfOpen [s + 14] and cola > cuerpo * 5 and velaAnterior > 0 and rsiLast[s + 14] > 70:
		
		print('horario ' +str(horario))
		print('close ' +str(dfClose[s + 14]) + ' open ' + str(dfOpen[s + 14]) + ' low ' + str(dfLow[s + 14]) + ' high ' + str(dfHigh[s + 14]))
		trade = True
		stopLoss = dfHigh [s + 14] 
		takeProfit = ((dfHigh[s + 14] - dfClose[s + 14]) * -1) + dfClose[s + 14]
		print('takeProfit ' + str(takeProfit) + ' stopLoss ' + str(stopLoss) ) 
		s += 1
	if trade:
		if dfHigh[s + 14] > stopLoss:
			perdidaShort +=1
			trade = False
			print ('cierre por stopLoss ' + str(dfHigh[s + 14]))
			print(horario)
			print(' ')
		elif dfLow[s + 14] <= takeProfit:
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

