import config
from binance.client import Client
import pandas as pd
from datetime import datetime
import time
import  schedule as schedule

client = Client(config.apyKey, config.apySecurity)


ejecution = 'off'
entradas = 0

estado= 'none'
global quantity
candles=client.futures_klines(symbol='GMTUSDT', interval=Client.KLINE_INTERVAL_1MINUTE,limit=30)

	#print(price)

df= pd.DataFrame(candles, columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])
avbl = client.futures_account_balance()
balance=float(avbl[6]['balance'])  
price = float(df['close'][29]) 
quantity = int(balance/price*2*1) 

###########################################################################################################################

def execute_connection():

	print('-------------botsaurio2--------------')
	global quantity
	global estado
	global price
	global df

	candles=client.futures_klines(symbol='GMTUSDT', interval=Client.KLINE_INTERVAL_1MINUTE,limit=30)

	#print(price)

	df= pd.DataFrame(candles, columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])
	price = float(df['close'][29]) 
	price_close = float(df['close'][28]) 
 

	print(quantity)      
	df['date'] = pd.to_datetime(df['date'], unit= 'ms')
	hora=df['date'][29]
	Ema25 = df["close"][:-1].ewm(span=25, adjust=False).mean()
	Ema9 = df["close"][:-1].ewm(span=9, adjust=False).mean()
	print (str(hora)+' UTC price GMT $'+str(price)) 
	valor_anterior =  Ema25 [27]
	valor_actual =    Ema25 [28]
	print('Ema 25 ' + str(valor_anterior))
	print('Price Close ' + str(valor_actual))

	#print(df)
	#print (Ema21)


	
	#print('quantity '+str(quantity))

	signal(valor_actual,valor_anterior,estado)



###########################################################################################################################

def signal(valor_actual,valor_anterior,estado1):

	global entradas
	global estado
	print (estado)
	avbl2 = client.futures_account_balance()
	print ('Wallet $' + str(avbl2[6]['balance'])  + ' Cantidad '+str(quantity)+'GMT')
	if (valor_actual > valor_anterior and  estado != "long"):
		print('open long')
		
		ejecution = 'on'
		entradas = entradas + 1
		print(estado)
		print('entradas ' + str(entradas))
		#estado='long'
		open_long()
        
	elif (valor_actual < valor_anterior and  estado != "short"):
    
		print('open short')
		
		ejecution='on'
		entradas = entradas + 1
		print(estado)
		print('entradas ' + str(entradas))
		open_short()
		#estado='short'
	elif (valor_actual > valor_anterior and  estado == "long"):
        
		print('on long')
		ejecution = 'off'
		print('entradas ' + str(entradas))
    
	elif (valor_actual < valor_anterior and  estado == "short"):
		print('on short')
		ejecution = 'off'
		print('entradas ' + str(entradas))
##########################################################################################################################################

def open_long():
	global quantity
	global estado
	if estado == 'short':
		#client.futures_create_order(symbol='GMTUSDT',side='BUY',type='MARKET',quantity=quantity)
		datos(estado)
		avbl = client.futures_account_balance()
		balance=float(avbl[6]['balance'])  
		quantity = int(balance/price*2*1)
	#client.futures_create_order(symbol='GMTUSDT',side='BUY',type='MARKET',quantity=quantity)
	estado = 'long'

def open_short():
	global quantity
	global estado
	if estado == 'long':
		
		datos(estado)
		#client.futures_create_order(symbol='GMTUSDT',side='SELL',type='MARKET',quantity=quantity)
	
		
		entry_price = (a[6]['entryPrice'])
		balance=float(avbl[6]['balance'])  
		quantity = int(balance/price*2*1)
	#client.futures_create_order(symbol='GMTUSDT',side='SELL',type='MARKET',quantity=quantity)
	estado = 'short'



###################################################################################################################


def datos(estado):
	leer = pd.read_excel("datos.xlsx")
	print (leer)




###################################################################################################################

schedule.every(5).seconds.do(execute_connection)

                              
while True:
    schedule.run_pending()
    time.sleep(1)
    
    