from matplotlib import pyplot as plt

def entradas(df_close, ema200, ema9):

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
    profit = 500000
    for i in range(len(df_close) - 3):
        
        #print(df_close[i+2])        
        
        if df_close[i+2] > ema200[i+2] and on_trade == False and df_close[i+2] < (ema200[i+2] * 1.03):

            if ema9[i] > ema9[i+1] and ema9[i+2] > ema9[i+1]:
                count = count + 1
                on_trade = True
                entry = df_close[i + 2]
                stop_loss = ema200[i + 2]
                profit = entry + (entry - stop_loss)
                plt.scatter(i + 2, entry, color='orange', zorder=3, s=5)
                plt.scatter(i + 2, profit, color='green', zorder=3, s=5)
                plt.scatter(i + 2, stop_loss, color='red', zorder=3, s=5)
                print('trade entry long: ' + str(entry) + ' stop loss: ' + str(stop_loss) + ' profit: ' + str(profit))
               


        if df_close[i+2] < ema200[i+2] and on_trade == True:
            print('stop loss')
            entradas_perdidas = entradas_perdidas + 1
            on_trade = False

        if df_close[i+2] > profit and on_trade == True:
            print('profit')
            entradas_ganadas = entradas_ganadas + 1
            on_trade = False



        # short

    profit = 0
    for i in range(len(df_close) - 3):

        #print(df_close[i+2])    
        if df_close[i+2] < ema200[i+2] and on_trade == False and df_close[i+2] > (ema200[i+2] * 1.03):

            if ema9[i] < ema9[i+1] and ema9[i+2] < ema9[i+1]:
                count = count + 1
                on_trade = True
                entry = df_close[i + 2]
                stop_loss = ema200[i + 2]
                profit = entry - (stop_loss - entry)
                plt.scatter(i + 2, entry, color='orange', zorder=3, s=5)
                plt.scatter(i + 2, profit, color='green', zorder=3, s=5)
                plt.scatter(i + 2, stop_loss, color='red', zorder=3, s=5)
                print('trade entry short: ' + str(entry) + ' stop loss: ' + str(stop_loss) + ' profit: ' + str(profit))
               


        if df_close[i+2] > stop_loss and on_trade == True:
            print('stop loss en ' + str (df_close[i+2]))
            entradas_perdidas = entradas_perdidas + 1
            on_trade = False

        print(profit)
        if df_close[i+2] < profit and on_trade == True:
            entradas_ganadas = entradas_ganadas + 1
            on_trade = False
        

 
    print(count)
    print('entradas ganadas '+ str(entradas_ganadas))
    print('entradas perdidas '+ str(entradas_perdidas))