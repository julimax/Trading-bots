import ccxt
import pandas as pd 
import time
import  schedule as schedule
from datetime import datetime
from matplotlib import pyplot as plt
plt.style.use('seaborn-darkgrid')
import pandas_ta as ta 

exchange = ccxt.binance()

def execute_connection(symbol='ETH/USDT', timeframe='1m'):
	raw_data = exchange.fetch_ohlcv(symbol, timeframe, limit=100)
	#print (raw_data)

	df = pd.DataFrame(raw_data[:-1], columns =['date', 'open', 'high', 'low', 'close', 'volume'])

	df['date'] = pd.to_datetime(df['date'], unit= 'ms')
	print(f"Executing connection and data processing at... {datetime.now().isoformat()}")
	print(df)
	plt.plot(df['close'])
	plt.show
	
	df.plot('close')
execute_connection(symbol='ETH/USDT', timeframe='1m')



schedule.every(10).seconds.do(execute_connection)
while True:
    schedule.run_pending()
    time.sleep(1)