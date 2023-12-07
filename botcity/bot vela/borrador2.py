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
'''for i in range(999):
	velaAnterior = dfClose[s] - dfOpen[s]
	cola = dfOpen[s + 1] - dfLow[s + 1]
	cuerpo = dfClose[s + 1] - dfOpen[s + 1]
	if dfClose[s] >= (dfHigh[s + 1] - 0.9 ) and dfLow[s + 1] < dfOpen[s + 1] and trade == False and dfClose[s + 1] > dfOpen [s + 1] and cola > cuerpo *1.5 and velaAnterior < 0:
		horario = hora[s+1]
		print('horario ' +str(horario))
		print('close ' +str(dfClose[s + 1]) + ' open ' + str(dfOpen[s + 1]) + ' low ' + str(dfLow[s + 1]) + ' high ' + str(dfHigh[s + 1]))
		trade = True
		
		takeProfit = ((dfClose[s + 1] - dfLow[s + 1]) * 2) + dfClose[s + 1]
		stopLoss = dfLow[s + 1] 

		print('takeProfit ' + str(takeProfit) + ' stopLoss ' + str(stopLoss)) 
	if trade:
		if dfLow[s + 1] < stopLoss:
			perdida +=1
			trade = False
			print ('cierre por stopLoss ' + str(dfLow[s + 1]))
			print(' ')
		elif dfHigh[s + 1] > takeProfit:
			ganada += 1
			trade = False
			print('cierre por takeProfit ' + str(takeProfit))
			print(' ')
	s += 1

print(ganada)
print(perdida)'''

print('-------short----------')
ganadaShort = 0
perdidaShort = 0
trade = False
s = 0

for i in range(999):
	velaAnterior = dfClose[s] - dfOpen[s]
	cola = dfHigh[s + 1] - dfOpen[s + 1]
	cuerpo = dfOpen[s + 1] - dfClose[s + 1]
	horario = hora[s + 1]
	if dfClose[s + 1] <= (dfLow[s + 1] + 3 )  and dfHigh[s + 1] > dfOpen[s + 1] and trade == False and dfClose[s + 1] < dfOpen [s + 1] and cola > cuerpo *1.5 and velaAnterior > 0:
		
		print('horario ' +str(horario))
		print('close ' +str(dfClose[s + 1]) + ' open ' + str(dfOpen[s + 1]) + ' low ' + str(dfLow[s + 1]) + ' high ' + str(dfHigh[s + 1]))
		trade = True
		stopLoss = dfHigh [s + 1] 
		takeProfit = ((dfHigh[s + 1] - dfClose[s + 1]) * -2) + dfClose[s + 1]
		print('takeProfit ' + str(takeProfit) + ' stopLoss ' + str(stopLoss) ) 
	if trade:
		if dfHigh[s + 1] > stopLoss:
			perdidaShort +=1
			trade = False
			print ('cierre por stopLoss ' + str(dfHigh[s + 1]))
			print(horario)
			print(' ')
		elif dfLow[s + 1] <= takeProfit:
			ganadaShort += 1
			trade = False
			print('cierre por takeProfit ' + str(takeProfit))
			print(' ')
	s += 1


print('ganadas long' + str(ganada))
print('perdidas long ' + str(perdida))
print('ganadas short ' + str(ganadaShort))
print('perdidas short ' + str(perdidaShort))

