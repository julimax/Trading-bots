from binance.spot import Spot
import pandas as pd
import keys 
import pytz
from rsi import rsi

# API key/secret are required for user data endpoints
client = Spot(keys.API_KEY, keys.SECRET_KEY)

############################## data ##########################################
candles = client.klines("BTCUSDT", "5m", limit=500)

df= pd.DataFrame(candles, columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])
df['date'] = pd.to_datetime(df['date'], unit='ms').dt.tz_localize(pytz.UTC).dt.tz_convert('America/Argentina/Buenos_Aires')
# Seleccionar solo las columnas de interés (las primeras seis)
df_ohlc = df[['date', 'open', 'high', 'low', 'close', 'volume']]

################################ indicators #######################################
ema25 = df["close"].ewm(span=25, adjust=False).mean()
ema200 = df["close"][:-1].ewm(span=200, adjust=False).mean()
#ema200 = df["close"][:-1].ewm(span=200, adjust=False).mean()
#prsi = df['close'].astype(float)
df_close = df['close'].astype(float)




############################## test ###########################################


def entradas(dfClose, ema200, ema25):

    entry = float
    global entradas
    entradas_ganadas = 0
    entradas_perdidas = 0
    global stop_loss
    on_trade = False
    count = 0

    

    for i in range(len(df_close) - 2):

        if df_close[i] > ema200[i] and on_trade == False:

            if ema25[i] > ema25[i+1]:
                count = count + 1
                on_trade = True
                entry = df_close[i + 2]
                stop_loss = ema200[i + 1]
                profit = entry + (entry - stop_loss)
                print('trade entry: ' + str(entry) + ' stop loss: ' + str(stop_loss) + ' profit: ' + str(profit))
               

        if on_trade == True:

            if df_close[+1] < ema200[i]:
                print('stop loss')
                entradas_perdidas = entradas_perdidas + 1
                on_trade = False

            if df_close[+1] > profit:
                print('profit')
                entradas_ganadas = entradas_ganadas + 1
                on_trade = False


    print(count)

############################## output ##########################################
#print(ema25)
#print(ema200)
#print(rsi(prsi))
#print(df_ohlc)
entradas(df_close, ema200, ema25)