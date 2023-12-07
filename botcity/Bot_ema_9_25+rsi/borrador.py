

import config
from rsi import rsi
from binance.client import Client
import pandas as pd
from datetime import datetime
import time
import  schedule as schedule
import pandas as pd





client = Client(config.apyKey, config.apySecurity)

infoTrade = client.futures_position_information()
infoTradeShort = infoTrade[56]
positionShort = float(infoTradeShort['positionAmt']) *-1 


print(positionShort)
client.futures_create_order(symbol='BNBUSDT',positionSide='short',side='BUY',type='MARKET',quantity=positionShort)