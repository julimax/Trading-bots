import config
from binance.client import Client
import pandas as pd
from datetime import datetime
import time
import  schedule as schedule
import pandas as pd
from matplotlib import pyplot as plt

client = Client(config.apyKey, config.apySecurity)

candles=client.futures_klines(symbol='BNBUSDT', interval=Client.KLINE_INTERVAL_1MINUTE,limit=210)

df= pd.DataFrame(candles, columns =['date', 'open', 'high', 'low', 'close', 'volume','a','b','c','d','e','f'])

low = df['low'].astype(float)
high = df['high'].astype(float)
smaLow = low.rolling(window = 10).mean()
smaHigh = high.rolling(window = 10).mean()
price = df['close'].astype(float)
close = float(df['close'][209])

#Hlv = na
#Hlv := close > smaHigh ? 1 : close < smaLow ? -1 : Hlv[1]
#sslDown = Hlv < 0 ? smaHigh: smaLow
#sslUp   = Hlv < 0 ? smaLow : smaHigh

#print(smaHigh)
#print(smaHigh[109])
Hlv = 'none'
sslH = []
sslL = []
it = 0
for i in range(210):
    if it < 9:
        sslH.append(price[it])
        sslL.append(price[it])
    
    if price[it] > smaLow[it] and Hlv == 'none':
        sslH.append(smaHigh[it])
        #sslH[it] = smaHigh[it]
        #sslL[it] = smaLow[it]
        sslL.append(smaLow[it])
        
    if price[it] > smaHigh[it] and Hlv == 'inverted':
        sslH.append(smaHigh[it])
        #sslH[it] = smaHigh[it]
        #sslL[it] = smaLow[it]
        sslL.append(smaLow[it])
        Hlv = 'none'

        
    if price[it] < smaHigh[it] and Hlv == 'inverted':
        sslH.append(smaLow[it])
        #sslH[it] = smaHigh[it]
        #sslL[it] = smaLow[it] 
        sslL.append(smaHigh[it])
       
        
    if price[it] < smaLow[it] and Hlv == 'none':
        sslH.append(smaLow[it])
        #sslH[it] = smaHigh[it]
        #sslL[it] = smaLow[it]
        sslL.append(smaHigh[it])
        Hlv = 'inverted'
        
    it += 1
    

print(sslH)
print('aaaaaa')
print(len(sslH))
print(sslL)
plt.plot(sslH,color = 'orange')
plt.plot(sslL,color = 'blue')



plt.plot(smaLow,color = 'green')
plt.plot(smaHigh,color = 'red')
#plt.plot(price,color = 'orange')
print(smaLow)