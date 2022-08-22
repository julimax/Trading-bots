import config
from rsi import rsi
from binance.client import Client
import pandas as pd
from datetime import datetime
import time
import  schedule as schedule
import pandas as pd

precioEntrada = 0
wallet = 100


client = Client(config.apyKey, config.apySecurity)


ejecution = 'off'
entradas = 0

estado= 'none'
global quantity
global valor_in_short
global valor_Ema200
valor_in_short = 0
candles=client.futures_klines(symbol='BNBUSDT', interval=Client.KLINE_INTERVAL_1MINUTE,limit=210)

	#print(price)

df= pd.DataFrame(candles, columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])
avbl = client.futures_account_balance()
balance=float(avbl[6]['balance'])  
price = float(df['close'][209]) 
quantity = int(balance/price*2*1) 
	
datos = pd.DataFrame( columns= ['symbol','estado' ,'positionAmt', 'entryPrice', 'markPrice', 'Profit', 'liquidationPrice', 'leverage'])





###########################################################################################################################

def execute_connection():

	print('-------------botsaurio2--------------')
	global quantity
	global estado
	global price
	global df
	global Ema25actual
	global valor_Ema200
	global rsiLast

	try:
		candles=client.futures_klines(symbol='BNBUSDT', interval=Client.KLINE_INTERVAL_1MINUTE,limit=210)
	except:
		print ('no connection')
		pass

	#print(price)
	try:
		df = pd.DataFrame(candles, columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])
	except:
		pass

	price = float(df['close'][209]) 
	price_close = float(df['close'][208]) 
 

	     
	df['date'] = pd.to_datetime(df['date'], unit= 'ms')
	hora=df['date'][209]
	Ema25 = df["close"][:-1].ewm(span=25, adjust=False).mean()
	Ema9 = df["close"][:-1].ewm(span=9, adjust=False).mean()
	Ema200 = df["close"][:-1].ewm(span=200, adjust=False).mean()
	print (str(hora)+' UTC price BNB $'+str(price)) 
	valor_anterior =  Ema25 [208]
	valor_actual =    Ema9 [208]
	valor_Ema200 = Ema200 [208]
	Ema25actual = df["close"].ewm(span=25, adjust=False).mean()
	Ema25actual = Ema25actual [209]
	#print(df)
	#print (Ema21)

	#print('quantity '+str(quantity))
	prsi = df['close'].astype(float)
	rsi(prsi)
	rsiLast = rsi(prsi)
	print('rsi ' + str(rsiLast))
	
	try:
		signal(valor_actual,valor_anterior,estado)
	except:
		pass



###########################################################################################################################

def signal(valor_actual,valor_anterior,estado1):



	global entradas
	global estado
	global Ema25actual
	global precioEntrada
	global ejecution
	global imbalance_short
	global valor_Ema200
	global rsiLast
	imbalance_short = False
	ejecution = 'off'
	stop_loss = 0
	print (estado)
	print('ema de 200 =' + str(valor_Ema200))
	avbl2 = client.futures_account_balance()
	print ('USDT Futures $' + str(avbl2[6]['balance'])  + ' Cantidad '+str(quantity)+'GMT')
	parametro = (valor_anterior+(valor_anterior*0.0007))
	parametro2 = (valor_anterior-(valor_anterior*0.0007))
	


	price=float(df["close"][209])

	print ('ema25= ' + str(valor_anterior)+ ' parametro long= ' + str(parametro)+' precio= '+str(price))
	print ('ema9= ' + str(valor_actual)+ ' parametro short= ' + str(parametro2)+' precio= '+str(price))
	if (valor_actual > valor_anterior and  estado != "long"):
		
		if (price<parametro)	:	
			
			print('open long')
		
			ejecution = 'on'
			entradas = entradas + 1
			print(estado)
			print('entradas ' + str(entradas))
			estado='long'
			precioEntrada = price
			open_long()
		######stop loss###############################	
		elif (estado == 'short'):
			estado = 'none'
			precioEntrada = "Stop loss lo cerro"
			open_long()
			
			
			
			ejecution == 'off'
            
	elif (valor_actual < valor_anterior and  estado != "short"):

		if (price>parametro2):
			precioEntrada = price
			print('open short')
		
			ejecution='on'
			entradas = entradas + 1
			print(estado)
			print('entradas ' + str(entradas))
			precioEntrada = price
			open_short()
			estado='short'
			imbalance_short = True
		######stop loss###############################	
		elif estado == "long":
			open_short()
			
			
			precioEntrada = "Stop loss lo cerro"
			estado = 'none'
			ejecution == 'off'
			#imbalance_short = True
            
	elif (valor_actual > valor_anterior and  estado == "long"):

		if rsiLast > 80:
			open_short()
			print('take profit')
		else:
			print('on long')
			ejecution = 'off'
			print('entradas ' + str(entradas))
    
	elif (valor_actual < valor_anterior and  estado == "short"):
		if rsiLast < 20:
			open_long()
			print('take profit')
		else:
			print('on short')
			ejecution = 'off'
			print('entradas ' + str(entradas))


	
	balance(estado,ejecution)
	print('entrada '+ str(precioEntrada))

	

##########################################################################################################################################

def open_long():
	global quantity
	global estado
	global precioEntrada
	
	print('entrada '+ str(precioEntrada))
	if estado == 'short':
		
		estado == 'none';
		#client.futures_create_order(symbol='GMTUSDT',side='BUY',type='MARKET',quantity=quantity)
		
		avbl = client.futures_account_balance()
		balance=float(avbl[6]['balance'])  
		quantity = int(balance/price*2*1)
	#client.futures_create_order(symbol='GMTUSDT',side='BUY',type='MARKET',quantity=quantity)
	

def open_short():
	
	
	global quantity
	global estado
	global precioEntrada

	
	print('entrada '+ str(precioEntrada))
	if estado == 'long':
		estado == 'none';		
		
		#client.futures_create_order(symbol='GMTUSDT',side='SELL',type='MARKET',quantity=quantity)
	
		
		#entry_price = (avbl[6]['entryPrice'])aaaaaaaaa
		balance=float(avbl[6]['balance'])  
		quantity = int(balance/price*2*1)
	#client.futures_create_order(symbol='GMTUSDT',side='SELL',type='MARKET',quantity=quantity)
	



###################################################################################################################




######################################################################################################################

def balance(estado1, ejecution1):
    global wallet
    global in_possession
    global valor_in_short
    global entry_short
    cierre = float(df['close'][208])




    if imbalance_short:
        if valor_in_short != 0:
            wallet = valor_in_short
            valor_in_short = 0
            
    if estado == 'none':
        print("Wallet $"+ str(wallet))
 
    if estado == "long" and ejecution == "on":           
       in_possession = wallet/cierre
       wallet = in_possession * cierre
       print('In possession = ' + str(in_possession) +'ETH  valor = $' + str(wallet))
       
    elif estado == "long" and ejecution == "off":
       # if in_possession == 0:
        #    in_possession = 1000
        
        wallet = in_possession*price
        print('In possession = ' + str(in_possession) +'ETH  valor = $' + str(wallet))
        
    elif estado == "short" and ejecution =="on":
        in_possession = wallet/cierre

      
    
        print('valor $'+ str(wallet))
        
     
    elif estado == "short" and ejecution == 'off':
        valor_in_short = wallet + (wallet-(in_possession*price))
        
        print('valor $'+ str(valor_in_short)) 



###################################################################################################################

schedule.every(3).seconds.do(execute_connection)

                              
while True:
    schedule.run_pending()
    time.sleep(1)
    
    