import pandas as pd
import yfinance as yf


def main(start_date, end_date, stocks):
    data = yf.download(stocks, start=start_date, end=end_date)

    close_prices = data['Adj Close'].resample('M').ffill()
    high_prices = data['High'].resample('M').ffill()
    low_prices = data['Low'].resample('M').ffill()

    returns_close = close_prices.pct_change()
    close_mean_returns = returns_close.mean()
    close_variance = returns_close.var()
    close_cov_matrix = returns_close.cov()

    returns_high = high_prices.pct_change()
    high_mean_returns = returns_high.mean()
    high_variance = returns_high.var()
    high_cov_matrix = returns_high.cov()

    returns_low = low_prices.pct_change()
    low_mean_returns = returns_low.mean()
    low_variance = returns_low.var()
    low_cov_matrix = returns_low.cov()

    with pd.ExcelWriter('stock_data.xlsx') as writer:
        returns_close.to_excel(writer, sheet_name='Monthly Returns Close')
        close_mean_returns.to_excel(writer, sheet_name='Mean Returns Close')
        close_variance.to_excel(writer, sheet_name='Variance Close')
        close_cov_matrix.to_excel(writer, sheet_name='Covariance Matrix Close')

        returns_high.to_excel(writer, sheet_name='Monthly Returns high')
        high_mean_returns.to_excel(writer, sheet_name='Mean Returns high')
        high_variance.to_excel(writer, sheet_name='Variance high')
        high_cov_matrix.to_excel(writer, sheet_name='Covariance Matrix high')

        returns_low.to_excel(writer, sheet_name='Monthly Returns low')
        low_mean_returns.to_excel(writer, sheet_name='Mean Returns low')
        low_variance.to_excel(writer, sheet_name='Variance low')
        low_cov_matrix.to_excel(writer, sheet_name='Covariance Matrix low')


if __name__ == '__main__':
    start_date = '2022-01-01'
    end_date = '2022-12-31'
    stocks = ['AAPL', 'GOOGL', 'TSLA', 'AMZN', 'MSFT']
    main(start_date, end_date, stocks)
