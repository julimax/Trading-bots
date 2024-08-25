import config
from binance.client import Client
import pandas as pd
from datetime import datetime
client = Client(config.apyKey, config.apySecurity)

#client.futures_change_leverage(symbol='ADAUSDT',leverage=10)
#client.futures_change_position_mode(self, **params)

client.futures_create_order(symbol='GMTUSDT',positionSide='LONG',side='SELL',type='MARKET',quantity=5)


#a = client.futures_position_information()

#b= (a[12])
#o=type(b)
#print(b)