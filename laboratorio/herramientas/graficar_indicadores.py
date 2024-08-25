from matplotlib import pyplot as plt

def graficar_indicadores(df_close, ema9, ema20, ema200):
    plt.figure(figsize=(12, 8), dpi=900)

    # Gráfico de precio y EMAs
    plt.plot(df_close, color='green', linewidth=0.8, label='Close')
    plt.plot(ema9, color='red', linewidth=0.8, label='EMA9')
    plt.plot(ema20, color='black', linewidth=0.8, label='EMA20')
    plt.plot(ema200, color='blue', linewidth=0.8, label='EMA200')