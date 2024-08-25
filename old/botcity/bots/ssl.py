
study("SSL channel", overlay=true)
period=input(title="Period", defval=10)
len=input(title="Period", defval=10)
smaHigh=sma(high, len)
smaLow=sma(low, len)
Hlv = na
Hlv := close > smaHigh ? 1 : close < smaLow ? -1 : Hlv[1]
sslDown = Hlv < 0 ? smaHigh: smaLow
sslUp   = Hlv < 0 ? smaLow : smaHigh

plot(sslDown, linewidth=2, color=red)
plot(sslUp, linewidth=2, color=lime)