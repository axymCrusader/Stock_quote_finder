import yfinance as yf
import pandas as pd


def main(start_date, end_date, stocks):
    data = yf.download(stocks, start=start_date, end=end_date)

    close_prices = data['Close']
    low_prices = data['Low']
    high_prices = data['High']

    with pd.ExcelWriter('stock_data.xlsx') as writer:
        close_prices.to_excel(writer, sheet_name='Close')
        low_prices.to_excel(writer, sheet_name='Low')
        high_prices.to_excel(writer, sheet_name='High')


if __name__ == '__main__':
    start_date = '2022-01-01'
    end_date = '2022-12-31'
    stocks = ['AAPL', 'GOOGL', 'TSLA', 'AMZN', 'MSFT']
    main(start_date, end_date, stocks)

