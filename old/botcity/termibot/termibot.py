import config
from binance.client import Client
import pandas as pd
from datetime import datetime
import  schedule as schedule
import time
import pandas as pd

global entryLong
entryLong = 2
global entryShort 
entryShort = 2

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
		if infoTrade[count]['symbol'] == 'ETHUSDT' and infoTrade[count]['positionSide'] == 'LONG':
			numberLong = count
		if infoTrade[count]['symbol'] == 'ETHUSDT' and infoTrade[count]['positionSide'] == 'SHORT':
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
	leverage = 35
	quantity = leverage / price 
	quantity = "{:.3f}".format(quantity)
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
	#print (price)
	print (infoTradeLong)
	print (infoTradeShort)
	print (quantity)
	#print (marginLong)
	#print (profitLong)
	#print (marginShort)
	#print (profitShort)
	global assd
	#assd = 1+marginLong+marginLong*marginLong/2
	#print ('sdadadad'+str(assd))

def lectura (): 
	
	global entryLong
	global entryShort
	print ('entradas long ' + str(entryLong-1))
	print ('entradas short ' + str(entryShort-1))
	if (infoTradeLong['entryPrice'] == '0.0'):
		entryLong = 1
	if (infoTradeShort['entryPrice'] == '0.0'):
		entryShort = 1
	if (infoTradeLong['entryPrice'] == '0.0' or (marginLong*marginLong) < ((-1)*profitLong )) :
		print('open trade long')
		entryLong = entryLong +1
		print ('entradas long ' + str(entryLong-1))
		#open_long()

	if (infoTradeShort['entryPrice'] == '0.0' or (marginShort*marginShort) < ((-1)*profitShort )):

		print('open trade short')
		entryShort = entryShort +1
		open_short()

	if (marginLong/2 < profitLong):
		print ('Take profit long')
		close_long()
	if (marginShort/2 < profitShort):
		print ('take profit short')
		close_short()





def open_long():
	client.futures_create_order(symbol='ETHUSDT',positionSide='LONG',side='BUY',type='MARKET',quantity=quantity)

def close_long():
	client.futures_create_order(symbol='ETHUSDT',positionSide='LONG',side='SELL',type='MARKET',quantity=positionAmtLong)

def open_short():
	client.futures_create_order(symbol='ETHUSDT',positionSide='SHORT',side='SELL',type='MARKET',quantity=quantity)

def close_short():
	client.futures_create_order(symbol='ETHUSDT',positionSide='SHORT',side='BUY',type='MARKET',quantity=positionAmtShort)

def execute_connection():
	print('----------Termibot_1.0----------------')
	
	numberCoin()

	datos() 
	if infoTradeLong['symbol'] == 'ETHUSDT' and infoTradeShort['symbol'] == 'ETHUSDT' and infoTradeLong['positionSide'] == 'LONG' and infoTradeShort['positionSide'] == 'SHORT':
		lectura()
	else:
		print('falla del lectura')



schedule.every(4).seconds.do(execute_connection)

                              
while True:
	try:	   
		schedule.run_pending()
	except:
		print('shedule fail')
		pass
   
	time.sleep(1)
    