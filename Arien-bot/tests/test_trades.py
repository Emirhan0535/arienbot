import unittest

from arienbot.trades import order, portfolio, trader


class TestOrder(unittest.TestCase):
    def setUp(self):
        self.order = order.Order(
            timestamp=1625423640,
            symbol='BTC/USDT',
            quantity=1.0,
            price=35000.0,
            side='buy'
        )

    def test_order(self):
        self.assertEqual(self.order.timestamp, 1625423640)
        self.assertEqual(self.order.symbol, 'BTC/USDT')
        self.assertEqual(self.order.quantity, 1.0)
        self.assertEqual(self.order.price, 35000.0)
        self.assertEqual(self.order.side, 'buy')


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        self.portfolio = portfolio.Portfolio()

    def test_portfolio(self):
        self.assertEqual(self.portfolio.cash, 100000.0)
        self.assertEqual(len(self.portfolio.holdings), 0)

    def test_add_holding(self):
        self.portfolio.add_holding('BTC/USDT', 1.0, 35000.0)
        self.assertEqual(self.portfolio.cash, 65000.0)
        self.assertEqual(len(self.portfolio.holdings), 1)
        self.assertEqual(self.portfolio.holdings['BTC/USDT']['quantity'], 1.0)
        self.assertEqual(self.portfolio.holdings['BTC/USDT']['price'], 35000.0)


class TestTrader(unittest.TestCase):
    def setUp(self):
        self.trader = trader.Trader()

    def test_trader(self):
        self.assertEqual(self.trader.portfolio.cash, 100000.0)
        self.assertEqual(len(self.trader.portfolio.holdings), 0)

    def test_buy_order(self):
        self.trader.buy_order('BTC/USDT', 1.0, 35000.0)
        self.assertEqual(self.trader.portfolio.cash, 65000.0)
        self.assertEqual(len(self.trader.portfolio.holdings), 1)
        self.assertEqual(self.trader.portfolio.holdings['BTC/USDT']['quantity'], 1.0)
        self.assertEqual(self.trader.portfolio.holdings['BTC/USDT']['price'], 35000.0)

    def test_sell_order(self):
        self.trader.sell_order('BTC/USDT', 1.0, 40000.0)
        self.assertEqual(self.trader.portfolio.cash, 105000.0)
        self.assertEqual(len(self.trader.portfolio.holdings), 0)


if __name__ == '__main__':
    unittest.main()
