import config
from binance.client import Client
import pandas as pd
from datetime import datetime
import  schedule as schedule
import time
import pandas as pd



try:
	client = Client(config.apyKey, config.apySecurity)
except:
	pass
	
def numberCoin():
	global numberLong
	global numberShort

	infoTrade = client.futures_position_information() 
	count = 0

	for i in infoTrade:
		if infoTrade[count]['symbol'] == 'BTCUSDT' and infoTrade[count]['positionSide'] == 'LONG':
			numberLong = count
		if infoTrade[count]['symbol'] == 'BTCUSDT' and infoTrade[count]['positionSide'] == 'SHORT':
			numberShort = count
		

		count += 1



def datos():
	global infoTradeLong
	global infoTradeShort
	global marginLong
	global profitLong
	global marginShort
	global profitShort
	global quantity
	global positionAmtLong
	global positionAmtShort

	try:
		infoTrade = client.futures_position_information()
		
	except:

		print ('sin conexión')
		pass

	price = float(infoTrade [numberLong]['markPrice'])

	print ('price ' + str(price))
	leverage = 25
	quantity = leverage / price / 4
	quantity = "{:.3f}".format(quantity)
	print(quantity)
	marginLong = float(infoTrade[numberLong]['notional'])/leverage
	marginShort = float(infoTrade[numberShort]['notional'])/leverage*-1
	infoTradeLong = infoTrade[numberLong]
	infoTradeShort = infoTrade[numberShort]
	profitLong = float(infoTradeLong['unRealizedProfit'])
	profitShort = float(infoTradeShort['unRealizedProfit'])
	positionAmtLong = float(infoTradeLong['positionAmt'])
	print (positionAmtLong)
	positionAmtShort = float(infoTradeShort['positionAmt'])*-1
	print ('Long ' + str(marginLong) + ' profit ' + str(profitLong))
	print ('Short ' + str(marginShort) + ' profit ' + str(profitShort))

	print (quantity)


def lectura (): 
	
	global entryLong
	global entryShort
	print ('entradas long ')
	print ('entradas short ')

	if (infoTradeLong['entryPrice'] == '0.0' or (marginLong < (-1)*profitLong)):
		print('open trade long')
		open_long()

	if (infoTradeShort['entryPrice'] == '0.0' or (marginShort < (-1)*profitShort)):

		print('open trade short')
		open_short()

	if (marginLong < profitLong):
		print ('Take profit long')
		close_long()
	if (marginShort < profitShort):
		print ('take profit short')
		close_short()





def open_long():
	client.futures_create_order(symbol='BTCUSDT',positionSide='LONG',side='BUY',type='MARKET',quantity=quantity)

def close_long():
	client.futures_create_order(symbol='BTCUSDT',positionSide='LONG',side='SELL',type='MARKET',quantity=positionAmtLong)

def open_short():
	client.futures_create_order(symbol='BTCUSDT',positionSide='SHORT',side='SELL',type='MARKET',quantity=quantity)

def close_short():
	client.futures_create_order(symbol='BTCUSDT',positionSide='SHORT',side='BUY',type='MARKET',quantity=positionAmtShort)

def execute_connection():
	print('----------Termibot_1.0----------------')
	
	numberCoin()

	datos() 
	if infoTradeLong['symbol'] == 'BTCUSDT' and infoTradeShort['symbol'] == 'BTCUSDT' and infoTradeLong['positionSide'] == 'LONG' and infoTradeShort['positionSide'] == 'SHORT':
		lectura()
	else:
		print('falla del lectura')



schedule.every(4).seconds.do(execute_connection)
while True:
	schedule.run_pending()
	time.sleep(1)
'''                    
while True:
	try:	   
		schedule.run_pending()
	except:
		print('shedule fail')
		pass
   
	time.sleep(1)
'''