import ccxt

class CoinbaseProExchange:
    def __init__(self, api_key, api_secret, password):
        self.exchange = ccxt.coinbasepro({
            'apiKey': api_key,
            'secret': api_secret,
            'password': password,
        })

    def get_balance(self):
        # TODO: Implement get balance
        pass

    def create_order(self, symbol, order_type, side, amount, price=None):
        # TODO: Implement order creation
        pass
