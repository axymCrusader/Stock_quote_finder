import pandas as pd
import yfinance as yf

def main(start_date, end_date, stocks):
    data = yf.download(stocks, start=start_date, end=end_date)

    # Resample the data to monthly frequency
    monthly_data = data.resample('M').ffill()

    # Calculate the mean, variance, and covariance matrix for each type of price
    stats = {}
    for price_type in ['Open', 'High', 'Low', 'Close']:
        price_data = monthly_data[price_type]
        returns = price_data.pct_change()
        stats[price_type] = {
            'prices': price_data,
            'mean': returns.mean(),
            'variance': returns.var(),
            'cov_matrix': returns.cov(),
        }

    # Save the calculated statistics and monthly prices to an Excel file
    with pd.ExcelWriter('stock_data.xlsx') as writer:
        for price_type, stat in stats.items():
            stat['prices'].to_excel(writer, sheet_name=f'{price_type} Prices')
            stat['mean'].to_excel(writer, sheet_name=f'{price_type} Mean Returns')
            stat['variance'].to_excel(writer, sheet_name=f'{price_type} Variance')
            stat['cov_matrix'].to_excel(writer, sheet_name=f'{price_type} Covariance Matrix')

if __name__ == '__main__':
    start_date = '2018-01-01'
    end_date = '2021-12-31'
    stocks = ['AAPL', 'SONY', 'TSLA', 'META', 'NFLX']
    main(start_date, end_date, stocks)
