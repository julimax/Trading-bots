import pandas as pd
import pytz

def get_candles(client):
    candles = client.klines("BTCUSDT", "5m", limit=1500)

    df = pd.DataFrame(candles, columns=['date', 'open', 'high', 'low', 'close', 'volume', 'a', 'b', 'c', 'd', 'e', 'f'])
    df['date'] = pd.to_datetime(df['date'], unit='ms').dt.tz_localize(pytz.UTC).dt.tz_convert('America/Argentina/Buenos_Aires')
    # Seleccionar solo las columnas de interés (las primeras seis)
    df_ohlc = df[['date', 'open', 'high', 'low', 'close', 'volume']]
    return df 

