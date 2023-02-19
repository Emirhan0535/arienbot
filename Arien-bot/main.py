import time
import logging
import threading
from typing import List
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

def main(api_key: str, api_secret: str, symbol: str, interval: int, trade_amount: float, profit_percentage: float, stop_loss_percentage: float):
    client = Client(api_key, api_secret)

    # Check the validity of the symbol
    symbol_info = client.get_symbol_info(symbol)
    if symbol_info is None or symbol_info['status'] != 'TRADING':
        logging.error(f"{symbol} is not a valid trading symbol")
        return

    # Start the trading loop
    while True:
        try:
            # Get the latest price for the symbol
            ticker = client.get_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])

            # Calculate the stop loss and target profit prices
            stop_loss_price = price * (1 - stop_loss_percentage / 100)
            target_profit_price = price * (1 + profit_percentage / 100)

            # Get the account balance
            account = client.get_account()
            balance = float(account['balances'][0]['free'])

            # Calculate the amount of coins to buy
            amount_to_buy = trade_amount / price

            # Buy the coins
            order = client.order_market_buy(symbol=symbol, quantity=amount_to_buy)
            logging.info(f"Bought {amount_to_buy} {symbol} coins at {price} USDT")

            # Wait for the interval
            time.sleep(interval)

            # Get the updated balance
            account = client.get_account()
            updated_balance = float(account['balances'][0]['free'])

            # Calculate the profit or loss
            profit_loss = (updated_balance - balance) * price

            # Check if the stop loss or target profit prices are reached
            if price <= stop_loss_price:
                # Sell the coins
                order = client.order_market_sell(symbol=symbol, quantity=updated_balance)
                logging.info(f"Sold all {symbol} coins at stop loss price {price} USDT with a loss of {profit_loss} USDT")
                break
            elif price >= target_profit_price:
                # Sell the coins
                order = client.order_market_sell(symbol=symbol, quantity=updated_balance)
                logging.info(f"Sold all {symbol} coins at target profit price {price} USDT with a profit of {profit_loss} USDT")
                break
            else:
                logging.info(f"Current {symbol} price is {price} USDT, waiting for target prices...")
        except BinanceAPIException as e:
            logging.error(f"Binance API exception: {e}")
        except BinanceOrderException as e:
            logging.error(f"Binance order exception: {e}")
        except Exception as e:
            logging.error(f"Unexpected exception: {e}")

