from matplotlib import pyplot as plt

def calcular_entradas(df_close, ema200, ema20, ema9):
    """
    Implementa la estrategia de cruce EMA para identificar puntos de entrada, stop loss y profit.

    Parámetros:
    df_close : Series
        Los precios de cierre de las velas.
    ema200, ema20, ema9 : Series
        Las medias móviles exponenciales calculadas.

    Retorno:
    None
    """
    entry_points = {'long': [], 'short': []}
    stop_loss_points = {'long': [], 'short': []}
    profit_points = {'long': [], 'short': []}

    on_trade = {'long': False, 'short': False}
    entradas_ganadas = 0
    entradas_perdidas = 0

    # Estrategia Long
    profit = 500000  # Inicialización para fines de lógica; se actualizará en la primera operación
    for i in range(len(df_close) - 3):
        if df_close[i+2] > ema200[i+2] and not on_trade['long'] and df_close[i+2] < (ema200[i+2] * 1.03):
            if ema9[i+2] > ema20[i+2] and ema9[i+1] < ema20[i+1]:
                on_trade['long'] = True
                entry = df_close[i + 2]
                stop_loss = ema200[i + 2]
                profit = entry + (entry - stop_loss)
                entry_points['long'].append((i + 2, entry))
                stop_loss_points['long'].append((i + 2, stop_loss))
                profit_points['long'].append((i + 2, profit))
                print(f'trade entry long: {entry} stop loss: {stop_loss} profit: {profit}')

        if df_close[i+2] < ema200[i+2] and on_trade['long']:
            print('stop loss')
            entradas_perdidas += 1
            on_trade['long'] = False

        if df_close[i+2] > profit and on_trade['long']:
            print('profit')
            entradas_ganadas += 1
            on_trade['long'] = False

    # Estrategia Short
    profit = 0  # Inicialización para fines de lógica; se actualizará en la primera operación
    for i in range(len(df_close) - 3):
        if df_close[i+2] < ema200[i+2] and not on_trade['short'] and df_close[i+2] > (ema200[i+2] * 0.97):
            if ema9[i+2] < ema20[i+2] and ema9[i+1] > ema20[i+1]:
                on_trade['short'] = True
                entry = df_close[i + 2]
                profit = ema200[i + 2]
                stop_loss = entry - (profit - entry)
                entry_points['short'].append((i + 2, entry))
                stop_loss_points['short'].append((i + 2, stop_loss))
                profit_points['short'].append((i + 2, profit))
                print(f'trade entry short: {entry} stop loss: {stop_loss} profit: {profit}')

        if df_close[i+2] < stop_loss and on_trade['short']:
            print('stop loss')
            entradas_perdidas += 1
            on_trade['short'] = False

        if df_close[i+2] > profit and on_trade['short']:
            print('profit')
            entradas_ganadas += 1
            on_trade['short'] = False

    print(f'entradas ganadas: {entradas_ganadas}')
    print(f'entradas perdidas: {entradas_perdidas}')

    return entry_points, stop_loss_points, profit_points
