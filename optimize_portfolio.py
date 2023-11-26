import yfinance as yf
import numpy as np
from scipy.optimize import minimize, Bounds


def fetch_stock_data(tickers, start_date, end_date):
    data = yf.download(tickers, start=start_date, end=end_date)
    return data['Close'], data['Open'], data['High']


def calculate_statistics(data):
    mean_returns = data.pct_change().mean()
    variance = data.pct_change().var()
    cov_matrix = data.pct_change().cov()
    return mean_returns, variance, cov_matrix


def optimize_portfolio(weights, mean_returns, cov_matrix):
    portfolio_return = np.dot(weights, mean_returns)
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))
    return portfolio_return, portfolio_volatility


def objective_function(weights, mean_returns, cov_matrix):
    portfolio_return, portfolio_volatility = optimize_portfolio(weights, mean_returns, cov_matrix)
    return portfolio_volatility


def constraint_return(weights, mean_returns, cov_matrix, target_return):
    portfolio_return, _ = optimize_portfolio(weights, mean_returns, cov_matrix)
    return portfolio_return - target_return


def constraint_volatility(weights, mean_returns, cov_matrix, target_volatility):
    _, portfolio_volatility = optimize_portfolio(weights, mean_returns, cov_matrix)
    return portfolio_volatility - target_volatility


def close_portfolio(tickers, start_date, end_date):
    close_prices, open_prices, high_prices = fetch_stock_data(tickers, start_date, end_date)

    # Рассчитываем статистику
    close_mean_returns, close_variance, close_cov_matrix = calculate_statistics(close_prices)
    max_weight = 0.4
    print(close_mean_returns)
    print(close_variance)
    print(close_cov_matrix)
    # Оптимизируем веса для минимизации волатильности при заданной ожидаемой доходности
    target_return_min_risk = 0.03  # Задайте ваш минимальный уровень доходности
    constraints_min_risk = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1},
                            {'type': 'eq',
                             'fun': lambda weights: constraint_return(weights, close_mean_returns, close_cov_matrix,
                                                                      target_return_min_risk)},
                            {'type': 'ineq', 'fun': lambda weights: max_weight - weights})

    bounds = Bounds(0, 1)
    result_min_risk = minimize(objective_function, np.ones(len(tickers)) / len(tickers),
                               args=(close_mean_returns, close_cov_matrix),
                               method='SLSQP', constraints=constraints_min_risk, bounds=bounds)

    # Оптимизированные веса для минимального риска при заданной ожидаемой доходности
    optimized_weights_min_risk = result_min_risk.x

    # Выводим оптимизированные веса и портфель для минимального риска
    print("\nИнвестиционный портфель минимального риска при заданной ожидаемой доходности:")
    print(tickers)
    print(f"Доли: {optimized_weights_min_risk}")
    print(f"Доходность: {target_return_min_risk:.4f}")
    print(f"Риск: {result_min_risk.fun:.4f}")

    # Оптимизируем веса для максимизации доходности при заданной волатильности
    target_volatility_max_return = 0.2  # Задайте ваш максимальный уровень волатильности
    constraints_max_return = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1},
                              {'type': 'eq', 'fun': lambda weights: constraint_volatility(weights, close_mean_returns,
                                                                                          close_cov_matrix,
                                                                                          target_volatility_max_return)},
                              {'type': 'ineq', 'fun': lambda weights: max_weight - weights})

    bounds = Bounds(0, 1)
    result_max_return = minimize(lambda weights: -optimize_portfolio(weights, close_mean_returns, close_cov_matrix)[0],
                                 np.ones(len(tickers)) / len(tickers),
                                 method='SLSQP', constraints=constraints_max_return, bounds=bounds)

    # Оптимизированные веса для максимальной доходности при заданной волатильности
    optimized_weights_max_return = result_max_return.x

    # Выводим оптимизированные веса и портфель для максимальной доходности
    print("\nИнвестиционный портфель максимальной доходности при заданной волатильности:")
    print(tickers)
    print(f"Доли: {optimized_weights_max_return}")
    print(f"Доходность: {-result_max_return.fun:.4f}")
    print(f"Риск: {target_volatility_max_return:.4f}")
    pass


def high_portfolio(tickers, start_date, end_date):
    close_prices, open_prices, high_prices = fetch_stock_data(tickers, start_date, end_date)

    # Рассчитываем статистику
    high_mean_returns, high_variance, high_cov_matrix = calculate_statistics(high_prices)
    max_weight = 0.4
    print(high_mean_returns)
    print(high_variance)
    print(high_cov_matrix)
    # Оптимизируем веса для минимизации волатильности при заданной ожидаемой доходности
    target_return_min_risk = 0.03  # Задайте ваш минимальный уровень доходности
    constraints_min_risk = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1},
                            {'type': 'eq',
                             'fun': lambda weights: constraint_return(weights, high_mean_returns, high_cov_matrix,
                                                                      target_return_min_risk)},
                            {'type': 'ineq', 'fun': lambda weights: max_weight - weights})

    bounds = Bounds(0, 1)
    result_min_risk = minimize(objective_function, np.ones(len(tickers)) / len(tickers),
                               args=(high_mean_returns, high_cov_matrix),
                               method='SLSQP', constraints=constraints_min_risk, bounds=bounds)

    # Оптимизированные веса для минимального риска при заданной ожидаемой доходности
    optimized_weights_min_risk = result_min_risk.x

    # Выводим оптимизированные веса и портфель для минимального риска
    print("\nИнвестиционный портфель минимального риска при заданной ожидаемой доходности:")
    print(tickers)
    print(f"Доли: {optimized_weights_min_risk}")
    print(f"Доходность: {target_return_min_risk:.4f}")
    print(f"Риск: {result_min_risk.fun:.4f}")

    # Оптимизируем веса для максимизации доходности при заданной волатильности
    target_volatility_max_return = 0.2  # Задайте ваш максимальный уровень волатильности
    constraints_max_return = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1},
                              {'type': 'eq', 'fun': lambda weights: constraint_volatility(weights, high_mean_returns,
                                                                                          high_cov_matrix,
                                                                                          target_volatility_max_return)},
                              {'type': 'ineq', 'fun': lambda weights: max_weight - weights})

    bounds = Bounds(0, 1)
    result_max_return = minimize(lambda weights: -optimize_portfolio(weights, high_mean_returns, high_cov_matrix)[0],
                                 np.ones(len(tickers)) / len(tickers),
                                 method='SLSQP', constraints=constraints_max_return, bounds=bounds)

    # Оптимизированные веса для максимальной доходности при заданной волатильности
    optimized_weights_max_return = result_max_return.x

    # Выводим оптимизированные веса и портфель для максимальной доходности
    print("\nИнвестиционный портфель максимальной доходности при заданной волатильности:")
    print(tickers)
    print(f"Доли: {optimized_weights_max_return}")
    print(f"Доходность: {-result_max_return.fun:.4f}")
    print(f"Риск: {target_volatility_max_return:.4f}")
    pass

def open_portfolio(tickers, start_date, end_date):
    close_prices, open_prices, high_prices = fetch_stock_data(tickers, start_date, end_date)

    # Рассчитываем статистику
    open_mean_returns, open_variance, open_cov_matrix = calculate_statistics(open_prices)
    max_weight = 0.4
    print(open_mean_returns)
    print(open_variance)
    print(open_cov_matrix)
    # Оптимизируем веса для минимизации волатильности при заданной ожидаемой доходности
    target_return_min_risk = 0.03  # Задайте ваш минимальный уровень доходности
    constraints_min_risk = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1},
                            {'type': 'eq',
                             'fun': lambda weights: constraint_return(weights, open_mean_returns, open_cov_matrix,
                                                                      target_return_min_risk)},
                            {'type': 'ineq', 'fun': lambda weights: max_weight - weights})

    bounds = Bounds(0, 1)
    result_min_risk = minimize(objective_function, np.ones(len(tickers)) / len(tickers),
                               args=(open_mean_returns, open_cov_matrix),
                               method='SLSQP', constraints=constraints_min_risk, bounds=bounds)

    # Оптимизированные веса для минимального риска при заданной ожидаемой доходности
    optimized_weights_min_risk = result_min_risk.x

    # Выводим оптимизированные веса и портфель для минимального риска
    print("\nИнвестиционный портфель минимального риска при заданной ожидаемой доходности:")
    print(tickers)
    print(f"Доли: {optimized_weights_min_risk}")
    print(f"Доходность: {target_return_min_risk:.4f}")
    print(f"Риск: {result_min_risk.fun:.4f}")

    # Оптимизируем веса для максимизации доходности при заданной волатильности
    target_volatility_max_return = 0.2  # Задайте ваш максимальный уровень волатильности
    constraints_max_return = ({'type': 'eq', 'fun': lambda weights: np.sum(weights) - 1},
                              {'type': 'eq', 'fun': lambda weights: constraint_volatility(weights, open_mean_returns,
                                                                                          open_cov_matrix,
                                                                                          target_volatility_max_return)},
                              {'type': 'ineq', 'fun': lambda weights: max_weight - weights})

    bounds = Bounds(0, 1)
    result_max_return = minimize(lambda weights: -optimize_portfolio(weights, open_mean_returns, open_cov_matrix)[0],
                                 np.ones(len(tickers)) / len(tickers),
                                 method='SLSQP', constraints=constraints_max_return, bounds=bounds)

    # Оптимизированные веса для максимальной доходности при заданной волатильности
    optimized_weights_max_return = result_max_return.x

    # Выводим оптимизированные веса и портфель для максимальной доходности
    print("\nИнвестиционный портфель максимальной доходности при заданной волатильности:")
    print(tickers)
    print(f"Доли: {optimized_weights_max_return}")
    print(f"Доходность: {-result_max_return.fun:.4f}")
    print(f"Риск: {target_volatility_max_return:.4f}")
    pass


def main():
    tickers = ['AAPL', 'SONY', 'TSLA', 'META', 'NFLX']
    start_date = '2019-01-01'
    end_date = '2021-01-01'
    np.set_printoptions(floatmode="fixed")
    print('------------------------------------------CLOSE------------------------------------------')
    close_portfolio(tickers, start_date, end_date)
    print('------------------------------------------HIGH-------------------------------------------')
    high_portfolio(tickers, start_date, end_date)
    print('------------------------------------------OPEN-------------------------------------------')
    open_portfolio(tickers, start_date, end_date)
    print('-----------------------------------------------------------------------------------------')


if __name__ == "__main__":
    main()
