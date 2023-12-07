import ccxt
import pandas as pd 
from datetime import datetime
import time

exchange = ccxt.binance({
	'enableRateLimit':True,
	})

msec = 1000
minute = 60 * msec
hour = 60 * minute

now = exchange.milliseconds()

def get_candles(symbol, timeframe, limit,from_timestamp ):

	try:
		candles = exchange.fetch_ohlcv(
			symbol = symbol,
			timeframe = timeframe,
			limit = limit,
			since = from_timestamp
			)

		header = ['timestamp', 'open', 'high', 'low', 'close', 'volume']
		df = pd.datatime(candles, colums = header)
		df.insert(1, 'datetime',[datetime.fromtimestamp(d/1000) for d in df.timestamp])
		return df.sort_values (by='timestamp', ascending = False)
	except:
			print('no more data')
			pass

def save_candles(symbol, timeframe,limit , from_timestamp):
	while(from_timestamp < now):
		candles = get_candles(symbol, timeframe, limit, from_timestamp)
		print(candles)
		if candles != None:
			from_timestamp = int(candles['timestamp'].iloc[0] + minute)
		else:
				from_timestamp += hour * 1000

save_candles(
	symbol = ' BTC/USDT',
	timeframe = '1h',
	limit = 1000,
	from_timestamp = exchange.parse8601('2019-01-01 00:00:00')
	)
