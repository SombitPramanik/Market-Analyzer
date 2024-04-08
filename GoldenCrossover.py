import os
import pandas as pd

def isGCS(StockDataDirectory, StockName, TimeDelta):
    Data = pd.read_csv(os.path.join(StockDataDirectory, StockName), parse_dates=["Date"], index_col="Date")
    
    if Data.empty:
        return False
    
    Data['24_SMA'] = Data.Close.rolling(window=24, min_periods=1).mean()
    Data['55_SMA'] = Data.Close.rolling(window=55, min_periods=1).mean()
    
    delta_index = Data.index[-1] - pd.Timedelta(days=TimeDelta)
    isGCSPossible = any((Data['24_SMA'].shift(1) < Data['55_SMA'].shift(1)) & (Data['24_SMA'] > Data['55_SMA']) & (Data.index >= delta_index))
    return isGCSPossible
