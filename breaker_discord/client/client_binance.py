import decimal
import time

from decimal import *

from binance.client import Client
from binance.exceptions import BinanceAPIException 
from binance.exceptions import BinanceOrderException
from binance.exceptions import BinanceRequestException

class ClientBinance(object):

    def __init__(self, binance_api_key, binance_secret_key) -> None:
        super().__init__()
        
        self.client = Client(binance_api_key, binance_secret_key)

    def read_orders(self):
        response = self.client.get_all_orders(symbol='BNBBTC', requests_params={'timeout': 5})
        return response

    def read_trades(self):
        list_symbol = []
        return self.client.get_my_trades(symbol='BNBBTC')

    def read_assets(self):
        return self.client.get_asset_details()

    def read_asset_balance(self):
        return self.client.get_asset_balance(asset='BTC')

    def get_list_price_historical(self, 
        symbolpair:str, 
        timstamp_ms_start:int, 
        timstamp_ms_end:int=None,
        code_interval:str='1m',
        code_pricetype='close'):

        #TODO no idea if there is any limit here
        list_kline = self.client.get_historical_klines(
            symbolpair, 
            code_interval, 
            timstamp_ms_start, 
            timstamp_ms_end, 
            limit=1000)
        
        list_timestamp = []
        list_price = []
        for kline in list_kline:
            if code_pricetype == 'close':
                list_timestamp.append(float(kline[6]))
                list_price.append(float(kline[4]))
        return list_timestamp, list_price

    def get_list_price(self, symbolpair, code_interval='1m', code_pricetype='close'):
    #         KLINE_INTERVAL_1MINUTE = '1m'
    # KLINE_INTERVAL_3MINUTE = '3m'
    # KLINE_INTERVAL_5MINUTE = '5m'
    # KLINE_INTERVAL_15MINUTE = '15m'
    # KLINE_INTERVAL_30MINUTE = '30m'
    # KLINE_INTERVAL_1HOUR = '1h'
    # KLINE_INTERVAL_2HOUR = '2h'
    # KLINE_INTERVAL_4HOUR = '4h'
    # KLINE_INTERVAL_6HOUR = '6h'
    # KLINE_INTERVAL_8HOUR = '8h'
    # KLINE_INTERVAL_12HOUR = '12h'
    # KLINE_INTERVAL_1DAY = '1d'
    # KLINE_INTERVAL_3DAY = '3d'
    # KLINE_INTERVAL_1WEEK = '1w'
    # KLINE_INTERVAL_1MONTH = '1M'
        list_kline = self.client.get_klines(symbol=symbolpair, interval=code_interval)
        list_timestamp = []
        list_price = []
        for kline in list_kline:
            if code_pricetype == 'close':
                list_timestamp.append(float(kline[6]))
                list_price.append(float(kline[4]))
        return list_timestamp, list_price

        #return self.client.get_klines(symbol='BNBBTC', interval=Client.KLINE_INTERVAL_30MINUTE)
        # kline layout
    #     [
    #     1499040000000,      # Open time
    #     "0.01634790",       # Open
    #     "0.80000000",       # High
    #     "0.01575800",       # Low
    #     "0.01577100",       # Close
    #     "148976.11427815",  # Volume
    #     1499644799999,      # Close time
    #     "2434.19055334",    # Quote asset volume
    #     308,                # Number of trades
    #     "1756.87402397",    # Taker buy base asset volume
    #     "28.46694368",      # Taker buy quote asset volume
    #     "17928899.62484339" # Can be ignored
    # ]


    def get_wallet(self, list_symbol=['IOTA', 'BTC']):
        dict_wallet = {}
        for symbol in list_symbol:
            ammount_free = float(self.client.get_asset_balance(asset=symbol)['free'])
            ammount_locked = float(self.client.get_asset_balance(asset=symbol)['locked'])
            price = float(self.client.get_avg_price(symbol=symbol + 'USDT')['price'])
            amount = ammount_free + ammount_locked
            asset = {}
            asset['amount'] = amount
            asset['price'] = price
            asset['value'] = amount * price
            dict_wallet[symbol] = asset
        #add USDT
        asset = {}
        asset['amount'] = float(self.client.get_asset_balance(asset='USDT')['free'])
        asset['price'] = 1
        asset['value'] = asset['amount']
        dict_wallet['USDT'] = asset
        return dict_wallet

    def order_generate_by_value_limit(self, symbol, desired_value):
        price = float(self.client.get_avg_price(symbol=symbol + 'USDT')['price'])
        if 0 < desired_value:
            side = 'BUY'
        else:
            side = 'SELL'
        
        amount = abs(desired_value / price)
        type = 'LIMIT'
        timeInForce = 'GTC'

        order = {}
        order['type_order'] = 'order_limit'
        order['symbol'] = symbol + 'USDT'
        order['side'] = side
        order['type'] = type
        order['timeInForce'] = timeInForce
        order['quantity'] = float(round(amount, 6)) #TODO define the 6 here
        order['price'] = price

        order_stats = {}
        order_stats['transactioncost'] = 0 
        return order, order_stats

    def get_symbol_info(self, symbolpair:str):
        return self.client.get_symbol_info(symbolpair)
    
    def get_avg_price(self, symbolpair:str):
        return self.client.get_avg_price(symbolpair)['price']


    @staticmethod
    def get_min_notional(symbol_info):
        list_filter = symbol_info['filters']
        for filter in list_filter:
            if filter['filterType'] == 'MIN_NOTIONAL':
                return Decimal(filter['minNotional'])
        raise Exception('no min notional defined')

    @staticmethod
    def get_lot_size(symbol_info):

        list_filter = symbol_info['filters']
        for filter in list_filter:
            if filter['filterType'] == 'LOT_SIZE':
                return Decimal(filter['minQty']), Decimal(filter['maxQty']), Decimal(filter['stepSize'])
        raise Exception('no lot size defined')

    @staticmethod
    def get_closest_lot(symbol_info:dict, amount:Decimal, price:Decimal) -> Decimal:
        assert(isinstance(symbol_info, dict))
        assert(isinstance(amount, Decimal))
        assert(isinstance(price, Decimal))

        min_size, max_size, step_size = ClientBinance.get_lot_size(symbol_info)
        min_notional = ClientBinance.get_min_notional(symbol_info)

        count_lot = int(round(amount/step_size))
        amount = count_lot * step_size

        while (amount * price) < min_notional:
            amount += step_size
        amount = max(min_size, min(amount, max_size))
        return amount

    def order_generate_by_value_market(self, symbolpair, desired_value:Decimal):
        desired_value = Decimal(desired_value) #TODO make redundant
        symbol_info = self.client.get_symbol_info(symbolpair)
        price = Decimal(self.client.get_avg_price(symbol=symbolpair)['price'])
        return ClientBinance.order_generate_by_value_market_static(symbolpair, symbol_info, price, desired_value)

    @staticmethod
    def order_generate_by_value_market_static(symbolpair:str, symbol_info:dict, price:Decimal, desired_value:Decimal):
        assert(isinstance(symbolpair, str))
        assert(isinstance(symbol_info, dict))
        assert(isinstance(price, Decimal))
        assert(isinstance(desired_value, Decimal))

        if 0 < desired_value:
            side = 'BUY'
        else:
            side = 'SELL'
        
        amount = Decimal(abs(desired_value / price))
        quantity = ClientBinance.get_closest_lot(symbol_info, amount, price)
        order = {}
        order['type_order'] = 'order_market'
        order['symbol'] = symbolpair
        order['side'] = side
        order['quantity'] = quantity
        order['expected_fee'] = quantity * price * Decimal(0.001)
        return order

    def order_execute(self, order):
        try:
            type_order = order['type_order']
            if type_order == 'order_limit':
                order_response = self.client.create_order(
                    symbol=order['symbol'],
                    side=order['side'],
                    type=order['type'],
                    timeInForce=order['timeInForce'],
                    quantity=order['quantity'],
                    price=order['price'])
            elif type_order == 'order_market':
                if order['side'] == 'BUY':
                    order_response = self.client.order_market_buy(
                        symbol=order['symbol'],
                        quantity=order['quantity'])
                else:
                    order_response = self.client.order_market_sell(
                        symbol=order['symbol'],
                        quantity=order['quantity'])
            else:
                raise Exception('Unknown type order: ' + type_order)

        except BinanceAPIException as e:
            # error handling goes here
            print(e)
            raise e
        except BinanceOrderException as e:
            # error handling goes here
            print(e)
            raise e


        return order_response
