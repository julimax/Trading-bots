import config
from rsi import rsi
from binance.client import Client
import pandas as pd
from datetime import datetime
import time
import  schedule as schedule



client = Client(config.apyKey, config.apySecurity)


###################################################################################################################

def execute_connection():

		print('-------------Velas 1.0 --------------')

		datos()

		signalLong()

		signalShort()


###################################################################################################################

def datos():

		try:
		candles=client.futures_klines(symbol='BNBUSDT', interval=Client.KLINE_INTERVAL_15MINUTE,limit=210)
	except:
		print ('no connection')
		pass

		df = pd.DataFrame(candles, columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])



	dfOpen = float(df[209]['open'])
	dfHigh = float(df[209]['high'])
	dfLow = float(df[209]['low'])
	dfClose = float(df[209]['close'])


	dfOpenAnterior = float(df[208]['open'])
	dfCloseAnterior = float(df[208]['close'])

	velaAnterior = dfOpenAnterior - dfCloseAnterior

	infoTrade = client.futures_position_information()

	price = float[infoTrade[55]['markPrice']]

	balance = client.futures_account_balance()
	balance = int(float(balance[6]['balance']))

	amount = int(balance/5)

	quantity = balance / price
	quantity = "{:.3f}".format(quantity)

	onLong = infoTrade[55]['entryPrice']
	onShort = infoTrade[56]['entryPrice']


	positionLong = float(infoTrade[55]['positionAmt'])
	positionShort = float(infoTrade[55]['positionAmt'])




###################################################################################################################

def signalLong():
	cuerpo = dfClose - dfOpen
	cola = dfOpen - dfLow

	if onLong == '0.0':
		if dfClose <= (dfHigh - 0.95) and dfLow < dfOpen and dfOpen < dfClose and cola > cuerpo *1.5:
			open_long():
			
			print('Open Long__entry Price $' + onLong)

			takeProfit = ((dfClose - dfLow) * 2) + dfClose

			StopLoss = 



###################################################################################################################

###################################################################################################################

def open_long():
	client.futures_create_order(symbol='BNBUSDT',positionSide='LONG',side='BUY',type='MARKET',quantity=quantity)

def close_long():
	client.futures_create_order(symbol='BNBUSDT',positionSide='LONG',side='SELL',type='MARKET',quantity=positionLong)

def open_short():
	client.futures_create_order(symbol='BNBUSDT',positionSide='SHORT',side='SELL',type='MARKET',quantity=quantity)

def close_short():
	client.futures_create_order(symbol='BNBUSDT',positionSide='SHORT',side='BUY',type='MARKET',quantity=positionShort)

###################################################################################################################

schedule.every(3).seconds.do(execute_connection)

                              
while True:
    schedule.run_pending()
    time.sleep(1)
    
    