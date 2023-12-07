import config
from rsi import rsi
from binance.client import Client
import pandas as pd
from datetime import datetime
import time
import  schedule as schedule


client = Client(config.apyKey, config.apySecurity)

############################################ PARAMETROS ###########################################################################

global leverage 
global porcentaje
global entradas
entradas = 0
leverage = 20 
porcentaje = 25

##########################################     execute_connection   #################################################################################

def execute_connection():

	print('-------------botsaurio2--------------')

	datos()

	signal()

	print('BNB price $' + str(price))

	if tradeL() == True:
		print('on long entryPrice $' + str(infoTradeLong['entryPrice']))
		

	if tradeS() == True:
		print('on short entryPrice $'+ str(infoTradeShort['entryPrice']))
	

	if tradeS() == False and tradeL() == False:
		print('status none')

	print('Ema de 25 = ' + str(Ema25Last) + ' parametro Long ' + str(parametroLong))
	print('Ema de 9 = ' + str(Ema9Last) + ' parametro Short ' + str(parametroShort))
	#print('RSI = ' + str(rsi))

	print('Balance $' + str(saldo))
	print('Entradas ' + str(entradas))


###########################################################################################################################

def datos():


	global Ema25Last
	global Ema9Last
	global rsi
	global price
	global quantity
	global positionLong
	global positionShort
	global infoTradeLong
	global infoTradeShort
	global price
	global saldo
	global rsiLast
	global rsi
	global parametroLong
	global parametroShort
	global profitShort
	global profitLong

	try:
		candles=client.futures_klines(symbol='BNBUSDT', interval=Client.KLINE_INTERVAL_3MINUTE,limit=210)
	except:
		print ('no connection')
		pass


	df = pd.DataFrame(candles, columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])


	Ema25 = df["close"][:-1].ewm(span=25, adjust=False).mean()
	Ema25Last = Ema25[208]
	Ema9 = df["close"][:-1].ewm(span=9, adjust=False).mean()
	Ema9Last = Ema9[208]


	parametroLong = (Ema25Last+(Ema25Last*0.004))
	parametroShort = (Ema25Last-(Ema25Last*0.004))


	infoTrade = client.futures_position_information()
	balance = client.futures_account_balance()


	#prsi = df['close'].astype(float)
	#rsi(prsi)
	#rsi = rsi(prsi)
	#rsi = rsi[209]

	
	#rsi(prsi)
	
	prsi = df['close'].astype(float)
	rsiLast = rsi(prsi)
	print('rsi ' + str(rsiLast[209]))


	price = float(infoTrade [58]['markPrice'])

	saldo = float(balance[6]['balance'])

	quantity = saldo / porcentaje * leverage / price
	quantity = quantity = "{:.2f}".format(quantity)
	print('quantity' + str(quantity))

	infoTradeLong = infoTrade[58]
	infoTradeShort = infoTrade[59]

	profitLong = float(infoTradeLong['unRealizedProfit'])
	profitShort = float(infoTradeShort['unRealizedProfit'])

	positionLong = float(infoTradeLong['positionAmt'])
	positionShort = float(infoTradeShort['positionAmt']) * -1

	tradeL()
	tradeS()

###########################################################################################################################

def signal():
	global entradas

	if tradeS() == False and Ema9Last < Ema25Last and price > parametroShort:
		open_short()
		print('Open Short')
		entradas += 1
	if tradeL() == False and Ema9Last > Ema25Last and price < parametroLong:
		open_long()
		print('Open Long')
		entradas += 1
	if tradeS() == True and (rsiLast[209] < 12 or ((Ema9Last > Ema25Last) and (profitShort < -0.02 or profitShort > 0.02))):
		close_short()
		print('Close Short')
	if tradeL() == True and (rsiLast[209] > 88 or ((Ema9Last < Ema25Last) and (profitLong < -0.02 or profitLong > 0.02))):
		close_long()
		print('Close Long')

###########################################################################################################################

def open_long():
	client.futures_create_order(symbol='BNBUSDT',positionSide='LONG',side='BUY',type='MARKET',quantity=quantity)

def close_long():
	client.futures_create_order(symbol='BNBUSDT',positionSide='LONG',side='SELL',type='MARKET',quantity=positionLong)

def open_short():
	client.futures_create_order(symbol='BNBUSDT',positionSide='SHORT',side='SELL',type='MARKET',quantity=quantity)

def close_short():
	client.futures_create_order(symbol='BNBUSDT',positionSide='SHORT',side='BUY',type='MARKET',quantity=positionShort)


###########################################################################################################################

def tradeL():

	global tradeLong
	tradeLong = bool

	trade = float(infoTradeLong['entryPrice'])


	if trade != 0.0:
		
		return True
	else:

		return False

	
		

def tradeS():

	global tradeShort
	tradeShort = bool

	trade = float(infoTradeShort['entryPrice'])

	if trade != 0:

		return True

	else:
		 return False
	

###################################################################################################################



schedule.every(3).seconds.do(execute_connection)

                              
while True:
    schedule.run_pending()
    time.sleep(1)
    
    