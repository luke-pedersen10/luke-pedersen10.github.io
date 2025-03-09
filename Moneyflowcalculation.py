import yfinance as yf
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors  



def calculate_money_flow(tickers, period='5d', interval='1d'):
    
 
    data = yf.download(tickers, period=period, interval=interval)
    results = []
    
    
    for ticker in tickers:
        if isinstance(data.columns, pd.MultiIndex):
            
            ticker_data = data.xs(ticker, axis=1, level=1)
        else:
            ticker_data = data.copy()
        
        
        required_columns = ['High', 'Low', 'Close', 'Volume']
        for col in required_columns:
            if col not in ticker_data.columns:
                raise KeyError(f"Missing expected column: {col} for ticker: {ticker}")
        
       
        ticker_data['Typical Price'] = (ticker_data['High'] + ticker_data['Low'] + ticker_data['Close']) / 3
        
        
        ticker_data['Money Flow'] = ticker_data['Typical Price'] * ticker_data['Volume']
        
     
        ticker_data['Ticker'] = ticker
        
       
        results.append(ticker_data[['Ticker', 'Money Flow']].reset_index())
    

    result_df = pd.concat(results, ignore_index=True)
    return result_df



tickers = ['AAPL', 'MSFT', 'TSLA','GOOGL',"AMZN"]
money_flow_data = calculate_money_flow(tickers)
print(money_flow_data)


heatmap_data = money_flow_data.pivot(index='Date', columns='Ticker', values='Money Flow')


print(heatmap_data.head())

plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, cmap='coolwarm', norm=mcolors.LogNorm())
plt.title("Stock Money Flow Heat Map")
plt.xticks(rotation=45)
plt.show()
