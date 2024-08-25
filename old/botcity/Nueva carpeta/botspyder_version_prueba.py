import ccxt
import pandas as pd 
import pandas_ta as ta
import time
import  schedule as schedule
from matplotlib import pyplot as plt
from datetime import datetime

#import numpy as np
plt.style.use('seaborn-darkgrid')


exchange = ccxt.binance()


#def technical_signals(df):
global wallet
wallet  = 1000.0

global ejecution
ejecution = 'off'

entradas = 0

valor_in_short = 0


def execute_connection(symbol='ETH/USDT', timeframe='1m'):
    global df
    
    raw_data = exchange.fetch_ohlcv(symbol, timeframe, limit=100)
	#print (raw_data[:-1])
    
    df= pd.DataFrame(raw_data, columns =['date', 'open', 'high', 'low', 'close', 'volume'])
                            
    df['date'] = pd.to_datetime(df['date'], unit= 'ms')
    
    print(f"Executing connection and data processing at... {datetime.now().isoformat()}")
    print(df)
    #print(df['close'], nrows = 98)
    #pd.df('close', nrows =98)
    #print(df['close'].iloc[98:])
    
    #plt.plot(df['close'])
    #plt.plot(df['high'])
    #plt.plot(df['low'])
    price = df["close"][98]
    priceClose = df["close"]
    Ema25 = df["close"][:-1].ewm(span=25, adjust=False).mean()
    Ema9 = df["close"][:-1].ewm(span=9, adjust=False).mean()
    Ema200 = df["close"][:-1].ewm(span = 200, adjust=False).mean()
   
    print(Ema25)
    plt.plot(Ema25,color='black')
    plt.plot(Ema9,color='red')
    plt.plot(Ema200,color='blue')
    plt.plot(priceClose,color='orange')
    valor_anterior =  Ema9[98]   
    valor_actual =    Ema25[98]
    valor_Ema200 = Ema200[98]
    print(valor_anterior)
    print(valor_actual)
    print(valor_Ema200)
    print ('precio ' + str(price))

    #return df
    
    global estado
    global ejecution
    global entradas


    if ((valor_actual < valor_anterior and valor_actual > valor_Ema200) and  estado != "long" ):
        print('open long')
        estado = 'long'
        ejecution = 'on'
        entradas = entradas + 1
        print(estado)
        print('entradas ' + str(entradas))
        
    elif (valor_actual > valor_anterior and  estado != "short" and valor_actual < valor_Ema200):
    
        print('open short')
        estado = 'short'
        ejecution='on'
        entradas = entradas + 1
        print(estado)
        print('entradas ' + str(entradas))
        
        
    elif (valor_actual > valor_anterior and  estado == "long"):
        
            print('on long')
            ejecution = 'off'
            print('entradas ' + str(entradas))
    
    elif (valor_actual < valor_anterior and  estado == "short"):
            print('on short')
            ejecution = 'off'
            print('entradas ' + str(entradas))
    #print(estado)
    
    balance(estado, ejecution)
    
global in_possession

    
def balance(estado, ejecution):
    global wallet
    global in_possession
    global valor_in_short
    global entry_short
    

    
    if estado == "long" and ejecution == "on":
        if valor_in_short != 0:
            wallet = valor_in_short   
    if estado == "long" and ejecution == "on":           
       in_possession = wallet/df['close'][99]
       wallet = in_possession * df['close'][99]
       print('In possession = ' + str(in_possession) +'ETH  valor = $' + str(wallet))
       
    elif estado == "long" and ejecution == "off":
       # if in_possession == 0:
        #    in_possession = 1000
        
        wallet = in_possession*df['close'][99]
        print('In possession = ' + str(in_possession) +'ETH  valor = $' + str(wallet))
        
    elif estado == "short" and ejecution =="on":
        in_possession = wallet/df['close'][99]

      
    
        print('valor $'+ str(wallet))
        
     
    elif estado == "short" and ejecution == 'off':
        valor_in_short = wallet - ((in_possession*df['close'][99])-wallet)
        
        print('valor $'+ str(valor_in_short))    
        


global estado 
estado='t'
#technical_signals(execute_connection())
    
    



#execute_connection(symbol='ETH/USDT', timeframe='1m')
schedule.every(5).seconds.do(execute_connection)
#schedule.every(10).seconds.do(technical_signals(execute_connection()))
                              
while True:
    schedule.run_pending()
    time.sleep(1)
    
    
    
    
    
    
    
    
    