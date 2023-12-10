from binance.spot import Spot
import pandas as pd
import keys 
import pytz
from indicators.rsi import rsi
from strategies.ema9_ema200 import entradas
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

plt.savefig('nombre_del_archivo.png', dpi=900)


#print(df_ohlc)