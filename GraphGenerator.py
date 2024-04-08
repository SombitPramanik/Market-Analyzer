import matplotlib
matplotlib.use('Agg')  # Set the backend to 'Agg'

import io
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def TwentyByFiftySMAWithGCS(name, data_point):
    path = f"./Data/{name}.csv"        
    data = pd.read_csv(path, parse_dates=['Date'], index_col='Date')
    data['24_SMA'] = data.Close.rolling(window=20, min_periods=1).mean()
    data['55_SMA'] = data.Close.rolling(window=50, min_periods=1).mean()
    data['Signal'] = np.where(data['24_SMA'] > data['55_SMA'], 1, 0)
    data['Position'] = data.Signal.diff()
    
    fig, ax = plt.subplots(figsize=(14, 7))
    data.iloc[-data_point:]['Close'].plot(ax=ax, color='k', label='Close Price')
    data.iloc[-data_point:]['24_SMA'].plot(ax=ax, color='b', label='24-day SMA')
    data.iloc[-data_point:]['55_SMA'].plot(ax=ax, color='g', label='55-day SMA')
    
    buy_signals = data.iloc[-data_point:][data.iloc[-data_point:]['Position'] == 1]
    sell_signals = data.iloc[-data_point:][data.iloc[-data_point:]['Position'] == -1]
    
    ax.plot(buy_signals.index, buy_signals['24_SMA'], '^', markersize=15, color='g', label='buy')
    ax.plot(sell_signals.index, sell_signals['24_SMA'], 'v', markersize=15, color='r', label='sell')
    
    ax.set_ylabel('Price in Rupees', fontsize=15)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_title(name, fontsize=20)
    ax.legend()
    ax.grid()

    # Save plot to a bytes object
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data_bytes = buffer.getvalue()
    plt.close(fig)

    return plot_data_bytes
