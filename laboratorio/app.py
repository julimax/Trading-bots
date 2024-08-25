import sys
sys.path.append('laboratorio')
from herramientas.graficar_indicadores import graficar_indicadores
from herramientas.graficar_entradas import graficar_entradas
from binance.spot import Spot
import keys
from candles import get_candles  
from indicators.rsi import rsi
#from strategies.ema9_ema200 import entradas
from strategies.ema9_20_200 import calcular_entradas

import seaborn as sns
import numpy as np

def obtener_datos():
    """
    Obtiene los datos de velas del cliente de Binance.
    
    Retorno:
    df : DataFrame
        Un DataFrame con los datos de velas obtenidos de Binance.
    """
    client = Spot(keys.API_KEY, keys.SECRET_KEY)
    df = get_candles(client)
    return df

def calcular_indicadores(df):
    """
    Calcula los indicadores EMA y RSI basados en los datos de velas.

    Parámetros:
    df : DataFrame
        Un DataFrame con los datos de velas.
 
    Retorno:
    tuple : (ema9, ema20, ema200, prsi, df_close)
        Los indicadores calculados.
    """
    ema9 = df["close"].ewm(span=9, adjust=False).mean()
    ema20 = df["close"].ewm(span=20, adjust=False).mean()
    ema200 = df["close"].ewm(span=200, adjust=False).mean()  # Eliminé el índice [-1] para obtener EMA completa
    prsi = rsi(df['close'].astype(float))
    df_close = df['close'].astype(float)
    return ema9, ema20, ema200, prsi, df_close

def graficar(ema9, ema20, ema200, prsi, df_close):
    """
    Genera y muestra un gráfico de las medias móviles y RSI.

    Parámetros:
    ema9, ema20, ema200 : Series
        Las medias móviles exponenciales calculadas.
    prsi : Series
        El índice RSI calculado.
    df_close : Series
        Los precios de cierre de las velas.
    """
    sns.set_theme(style='darkgrid')
    fig, ax1 = plt.subplots(figsize=(12, 8), dpi=900)
    
    ax1.plot(df_close, label='Precio de Cierre', color='blue', linewidth=0.5)
    ax1.plot(ema9, label='EMA 9', color='red', linewidth=0.8)
    ax1.plot(ema20, label='EMA 20', color='green', linewidth=0.8)
    ax1.plot(ema200, label='EMA 200', color='purple', linewidth=0.8)
    ax1.set_title('Gráfico de EMA y RSI')
    ax1.set_xlabel('Tiempo')
    ax1.set_ylabel('Precio')
    
    ax1.legend(loc='upper left')
    
    ax2 = ax1.twinx()
    ax2.plot(prsi, color='orange', linewidth=0.8, label='RSI')
    ax2.set_ylabel('RSI')
    ax2.legend(loc='upper right')
    
    plt.savefig('nombre_del_archivo.png', dpi=900)
    plt.show()

def main():
    df = obtener_datos()
    ema9, ema20, ema200, prsi, df_close = calcular_indicadores(df)
    graficar_indicadores(df_close, ema9, ema20, ema200)
    entry_points, stop_loss_points, profit_points = calcular_entradas(df_close, ema200, ema20, ema9)
    graficar_entradas(entry_points, stop_loss_points, profit_points)
    #graficar(ema9, ema20, ema200, prsi, df_close)
    #entradas_cruce(df_close, ema200, ema20, ema9)

if __name__ == "__main__":
    main()
