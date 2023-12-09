from binance.spot import Spot
import pandas as pd
import keys 
import pytz
from rsi import rsi
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np


# API key/secret are required for user data endpoints
client = Spot(keys.API_KEY, keys.SECRET_KEY)

############################## data ##########################################
candles = client.klines("BTCUSDT", "5m", limit=100)

df= pd.DataFrame(candles, columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])
df['date'] = pd.to_datetime(df['date'], unit='ms').dt.tz_localize(pytz.UTC).dt.tz_convert('America/Argentina/Buenos_Aires')
# Seleccionar solo las columnas de interés (las primeras seis)
df_ohlc = df[['date', 'open', 'high', 'low', 'close', 'volume']]

################################ indicators #######################################
ema9 = df["close"].ewm(span=9, adjust=False).mean()
ema20 = df["close"].ewm(span=20, adjust=False).mean()
ema200 = df["close"][:-1].ewm(span=200, adjust=False).mean()
#ema200 = df["close"][:-1].ewm(span=200, adjust=False).mean()
#prsi = df['close'].astype(float)
df_close = df['close'].astype(float)



############################## test ###########################################


def entradas(dfClose, ema200, ema9):

    entry = float
    global entradas
    global entradas_ganadas 
    global entradas_perdidas
    global stop_loss
    on_trade = False
    count = 0
    entradas_ganadas = 0
    entradas_perdidas = 0
    
    
        # long
    for i in range(len(df_close) - 3):
        
        print(df_close[i+3])        
        profit = 500000
        if df_close[i+2] > ema200[i+2] and on_trade == False:

            if ema9[i] > ema9[i+1] and ema9[i+2] > ema9[i+1]:
                count = count + 1
                on_trade = True
                entry = df_close[i + 2]
                stop_loss = ema200[i + 2]
                profit = entry + (entry - stop_loss)
                plt.scatter(i + 2, entry, color='orange', zorder=3, s=5)
                print('trade entry long: ' + str(entry) + ' stop loss: ' + str(stop_loss) + ' profit: ' + str(profit))
               


        if df_close[i+2] < ema200[i+2] and on_trade == True:
            print('stop loss')
            entradas_perdidas = entradas_perdidas + 1
            on_trade = False

        if df_close[i+2] > profit and on_trade == True:
            print('profit')
            entradas_ganadas = entradas_ganadas + 1
            on_trade = False


        on_trade = False 

        # short
    for i in range(len(df_close) - 3):

        profit = 0
        if df_close[i+2] < ema200[i+2] and on_trade == False:

            if ema9[i] < ema9[i+1] and ema9[i+2] < ema9[i+1]:
                count = count + 1
                on_trade = True
                entry = df_close[i + 2]
                stop_loss = ema200[i + 2]
                profit = entry - (stop_loss - entry)
                plt.scatter(i + 2, entry, color='orange', zorder=3, s=5)
                print('trade entry short: ' + str(entry) + ' stop loss: ' + str(stop_loss) + ' profit: ' + str(profit))
               


        if df_close[i+2] < ema200[i] and on_trade == True:
            print('stop loss')
            entradas_perdidas = entradas_perdidas + 1
            on_trade = False

        if df_close[i+2] > profit and on_trade == True:
            print('profit')
            entradas_ganadas = entradas_ganadas + 1
            on_trade = False
        
        on_trade = False
 
    print(count)
    
############################## grafico #######################################
# Utilizar seaborn para configurar el estilo
sns.set_theme(style='darkgrid')

# Datos de ejemplo
x = np.linspace(0, 10, 100)
y = np.sin(x)

plt.figure(figsize=(12, 8), dpi=900)

#plt.show()


plt.plot(df_close,color='green', linewidth=0.8)  
plt.plot(ema9,color='red', linewidth=0.8)  
plt.plot(ema20,color='black', linewidth=0.8)    
plt.plot(ema200,color='blue', linewidth=0.8)   

############################## execution ######################################

entradas(df_close, ema200, ema9)

############################## output ##########################################
#print(ema9)
#print(ema200)
#print(rsi(prsi))
#print(df_ohlc)
print('entradas ganadas '+ str(entradas_ganadas))
print('entradas perdidas '+ str(entradas_perdidas))
plt.savefig('nombre_del_archivo.png', dpi=900)


#print(df_ohlc)