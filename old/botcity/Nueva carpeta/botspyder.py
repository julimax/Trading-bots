import ccxt
import pandas as pd 
import pandas_ta as ta
import time
import  schedule as schedule
from datetime import datetime
from matplotlib import pyplot as plt
import numpy as np
plt.style.use('seaborn-darkgrid')


exchange = ccxt.binance()


#def technical_signals(df):



    
	


def execute_connection(symbol='ETH/USDT', timeframe='1m'):
    global df
    
    raw_data = exchange.fetch_ohlcv(symbol, timeframe, limit=100)
	#print (raw_data[:-1])
    
    df= pd.DataFrame(raw_data[:-1], columns =['date', 'open', 'high', 'low', 'close', 'volume'])
    
    df['date'] = pd.to_datetime(df['date'], unit= 'ms')
    
    #print(f"Executing connection and data processing at... {datetime.now().isoformat()}")
    print(df)
    #print(df['close'], nrows = 98)
    #pd.df('close', nrows =98)
    #print(df['close'].iloc[98:])
    
    plt.plot(df['close'])
    
    Ema21 = df["close"].ewm(span=21, adjust=False).mean()
    print(Ema21)
    plt.plot(Ema21)
    valor_anterior =  Ema21[97]   
    valor_actual =    Ema21[98] 
    print(valor_anterior)
    print(valor_actual)

    #return df
   
    if (valor_actual > valor_anterior):
        print('compra')
        return True
        
    else:
        print('vende')
        return False
        



#technical_signals(execute_connection())
    
    



#execute_connection(symbol='ETH/USDT', timeframe='1m')
schedule.every(10).seconds.do(execute_connection)
#schedule.every(10).seconds.do(technical_signals(execute_connection()))
                              
while True:
    schedule.run_pending()
    time.sleep(1)
    
    
    
    
    
    
    
    
    