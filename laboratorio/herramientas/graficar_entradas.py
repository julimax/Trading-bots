from matplotlib import pyplot as plt

def graficar_entradas(entry_points, stop_loss_points, profit_points):
    """
    Genera y muestra un gráfico de las medias móviles y puntos de entrada, stop loss y profit.

    Parámetros:
    df_close : Series
        Los precios de cierre de las velas.
    ema9, ema20, ema200 : Series
        Las medias móviles exponenciales calculadas.
    entry_points, stop_loss_points, profit_points : dict
        Puntos de entrada, stop loss y profit para las operaciones long y short.

    Retorno:
    None
    """
 

    # Añadir leyendas
    plt.legend(loc='upper left')

    # Añadir puntos de entrada, stop loss y profit
    for point in entry_points['long']:
        plt.annotate('Entry Long', xy=point, xytext=(point[0], point[1] + 10),
                     arrowprops=dict(facecolor='orange', shrink=0.05), color='orange')
    for point in stop_loss_points['long']:
        plt.annotate('Stop Loss', xy=point, xytext=(point[0], point[1] - 10),
                     arrowprops=dict(facecolor='red', shrink=0.05), color='red')
    for point in profit_points['long']:
        plt.annotate('Profit', xy=point, xytext=(point[0], point[1] + 10),
                     arrowprops=dict(facecolor='green', shrink=0.05), color='green')

    for point in entry_points['short']:
        plt.annotate('Entry Short', xy=point, xytext=(point[0], point[1] - 10),
                     arrowprops=dict(facecolor='orange', shrink=0.05), color='orange')
    for point in stop_loss_points['short']:
        plt.annotate('Stop Loss', xy=point, xytext=(point[0], point[1] + 10),
                     arrowprops=dict(facecolor='red', shrink=0.05), color='red')
    for point in profit_points['short']:
        plt.annotate('Profit', xy=point, xytext=(point[0], point[1] - 10),
                     arrowprops=dict(facecolor='green', shrink=0.05), color='green')

    # Mostrar el gráfico
    plt.title('Gráfico de Estrategia de Trading')
    plt.xlabel('Tiempo')
    plt.ylabel('Precio')
    plt.show()