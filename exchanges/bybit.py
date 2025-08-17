import ccxt

class BybitExchange:
    def __init__(self, api_key, api_secret):
        self.exchange = ccxt.bybit({
            'apiKey': api_key,
            'secret': api_secret,
        })

    def get_balance(self):
        # TODO: Implement get balance
        pass

    def create_order(self, symbol, order_type, side, amount, price=None):
        # TODO: Implement order creation
        pass
