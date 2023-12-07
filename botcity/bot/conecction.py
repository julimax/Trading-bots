import config
from binance.client import Client
import pandas as pd
from datetime import datetime
import time
import  schedule as schedule

client = Client(config.apyKey, config.apySecurity)

def execute_connection():

	candles=client.futures_klines(symbol='BNBUSDT', interval=Client.KLINE_INTERVAL_1MINUTE,limit=210)

	df= pd.DataFrame(candles, columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])

	dataSll = df.tail(100)

	ssl(dataSll)

execute_connection()