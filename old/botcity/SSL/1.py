  #          if mode not in ("sma"):
 #               raise ValueError(f"Mode {mode} not supported yet")
#
 #           df = dataframe.copy()
#
 #           if mode == "sma":
 #               df["smaHigh"] = df["high"].rolling(length).mean()
 #               df["smaLow"] = df["low"].rolling(length).mean()
#
 #           df["hlv"] = np.where(
 #           df["close"] > df["smaHigh"], 1, np.where(df["close"] < df["smaLow"], -1, np.NAN)
 #   )
 #           df["hlv"] = df["hlv"].ffill()
#
  #          df["sslDown"] = np.where(df["hlv"] < 0, df["smaHigh"], df["smaLow"])
 #           df["sslUp"] = np.where(df["hlv"] < 0, df["smaLow"], df["smaHigh"])
#
 #           return df["sslDown"], df["sslUp"]

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