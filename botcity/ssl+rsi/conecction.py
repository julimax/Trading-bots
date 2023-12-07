import config
from binance.client import Client
from sslChanel import ssl
from rsi import rsi
import pandas as pd
from datetime import datetime
import time
import  schedule as schedule


client = Client(config.apyKey, config.apySecurity)

############################################ PARAMETROS ###########################################################################

global leverage 
global porcentaje
global entradas
global lastTrade
global stopLossLong
global stopLossShort
stopLossShort = 2000
stopLossLong = 0
lastTrade = 'none'
entradas = 0
leverage = 20 
porcentaje = 30

##########################################     execute_connection   #################################################################################

def execute_connection():

	print('-------------botsaurio2--------------')

	try:
		datos()
	except:
		print ('no connection')
		pass
	try:
		signal()
	except:
		pass

	print('BNB price $' + str(price) + ' ema200 ' + str(ema200Last))

	if tradeL() == True:
		print('on long entryPrice $' + str(infoTradeLong['entryPrice']) + 'stop loss long' + str(stopLossLong))
		

	if tradeS() == True:
		print('on short entryPrice $'+ str(infoTradeShort['entryPrice']) + 'stop loss short' + str(stopLossShort))
	

	if tradeS() == False and tradeL() == False:
		print('status none')


	print('Balance $' + str(saldo))
	print('Entradas ' + str(entradas))





###########################################################################################################################

def datos():

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
	global ssl
	global sslLow
	global sslHigh
	global profitShort
	global profitLong
	global price2
	global df
	global profitShort
	global profitLong
	global sslHighLast
	global sslLowLast
	global ema200Last

	try:
		candles=client.futures_klines(symbol='BNBUSDT', interval=Client.KLINE_INTERVAL_5MINUTE,limit=210)
	except:
		print ('no connection')
		pass


	df = pd.DataFrame(candles, columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])



	infoTrade = client.futures_position_information()
	balance = client.futures_account_balance()


	
	prsi = df['close'].astype(float)
	rsi(prsi)
	rsiLast = rsi(prsi)
	print('rsi ' + str(rsiLast[209]))

	price2 = df['close'].astype(float)
	


	price = float(infoTrade [61]['markPrice'])
	
	saldo = float(balance[6]['balance'])

	quantity = saldo / porcentaje * leverage / price
	quantity = quantity = "{:.2f}".format(quantity)
	print('quantity' + str(quantity))

	infoTradeLong = infoTrade[61]
	infoTradeShort = infoTrade[62]

	profitLong = float(infoTradeLong['unRealizedProfit'])
	profitShort = float(infoTradeShort['unRealizedProfit'])

	positionLong = float(infoTradeLong['positionAmt'])
	positionShort = float(infoTradeShort['positionAmt']) * -1

	ema200 = df["close"][:-1].ewm(span=200, adjust=False).mean()
	ema200Last = float(ema200[208])

	high = df['high'].astype(float)
	smaHigh = high.rolling(window = 10).mean()
	smahigh = float(smaHigh[208])

	parametroLong = (smahigh+(smahigh*0.0025))
	parametroShort = (smahigh-(smahigh*0.0025))

	try:
		sslHigh = ssl()[0]
	except:
		pass
	try:
		sslLow = ssl()[1]
	except:
		pass

	sslHighLast = ssl()[2]
	sslLowLast = ssl()[3]

	print('sslHigh ' + str(sslHigh) + ' parametroLong ' + str(parametroLong))
	print('sslLow ' + str(sslLow) + ' parametroShort ' + str(parametroShort))


	tradeL()
	tradeS()

###########################################################################################################################


def signal():
	global entradas
	global stopLossLong
	global stopLossShort
	

	if tradeS() == False and sslLow > sslHigh and sslLowLast > sslHighLast and price > parametroShort and price < ema200Last:
		open_short()
		print('Open Short')
		entradas += 1
		stopLossShort = sslLow
		
	if tradeL() == False and sslLow < sslHigh and sslLowLast < sslHighLast and price < parametroLong and price > ema200Last:
		open_long()
		print('Open Long')
		entradas += 1
		stopLossLong = sslLow
		
	if tradeS() == True and (rsiLast[209] < 12 or price > stopLossShort):
		close_short()
		print('Close Short')
		stopLossShort = 2000
	if tradeS() == True and sslHigh > sslLow and profitShort > 0.025:
		close_short()
		print('Close Short')	
		stopLossShort = 2000
	if tradeL() == True and (rsiLast[209] > 88 or price < stopLossLong):
		close_long()
		print('Close Long')
		stopLossLong = 0
	if tradeL() == True and sslHigh < sslLow and profitLong > 0.025:
		close_long()
		print('Close Long')
		stopLossLong = 0

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

'''
def ssl():
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
			sslH.append(price2[it])
			sslL.append(price2[it])
    
		if price2[it] > smaLow[it] and Hlv == 'none':
			sslH.append(smaHigh[it])
        	#sslH[it] = smaHigh[it]
        	#sslL[it] = smaLow[it]
			sslL.append(smaLow[it])
        
		if price2[it] > smaHigh[it] and Hlv == 'inverted':
			sslH.append(smaHigh[it])
        	#sslH[it] = smaHigh[it]
        	#sslL[it] = smaLow[it]
			sslL.append(smaLow[it])
			Hlv = 'none'

        
		if price2[it] < smaHigh[it] and Hlv == 'inverted':
			sslH.append(smaLow[it])
        	#sslH[it] = smaHigh[it]
        	#sslL[it] = smaLow[it] 
			sslL.append(smaHigh[it])
       
        
		if price2[it] < smaLow[it] and Hlv == 'none':
			sslH.append(smaLow[it])
        	#sslH[it] = smaHigh[it]
        	#sslL[it] = smaLow[it]
			sslL.append(smaHigh[it])
			Hlv = 'inverted'
        
		it += 1
	print (sslH[48], sslL[48])
	return (sslH[48], sslL[48])
'''
###################################################################################################################

schedule.every(3).seconds.do(execute_connection)

                              
while True:
    schedule.run_pending()
    time.sleep(1)
    
