from decimal import *
from typing import List
import sys
import time

from breaker_core.datasource.bytessource import Bytessource
from breaker_discord.binance.strategy import Strategy
from breaker_discord.client.client_binance import ClientBinance


class StrategyLevel(Strategy):

    def __init__(self, client_binance:ClientBinance, bytessource_binance:Bytessource, id_user:str, threshold_u:Decimal, threshold_l:Decimal) -> None:
        super().__init__()
        self.client_binance = client_binance
        self.id_user = id_user
        self.id_strategy = 'st-level'
        self.bytessource_strategy = bytessource_binance.join(['user', id_user, 'strategy', self.id_strategy])
        self.dict_level = {
            'BTC':1000
        }
        self.threshold_u = threshold_u 
        self.threshold_l = threshold_l

    # def add_symbolpair(self, symbolpiar)
    def set_value(self, key, value):
        config = self.bytessource_strategy.join('config.json').read_json()
        config[key] = value
        self.bytessource_strategy.join('config.json').write_json(config)

    def generate_list_order_now(self):
        timestamp_ms = int(time.time() * 1000)
        dict_wallet = self.client_binance.get_wallet()
        dict_symbol_info = {}
        dict_symbol_info['BTCUSDT'] = self.client_binance.get_symbol_info('BTCUSDT')
        dict_price = {} 
        dict_price['BTCUSDT'] = self.client_binance.get_avg_price('BTCUSDT')
        history = {}
        return self.generate_list_order(timestamp_ms, dict_wallet, dict_symbol_info, dict_price, history)


    def generate_list_order(self, timestamp_ms, dict_wallet, dict_symbol_info, dict_price, history):
        list_order = []
        list_post = []
        for symbol in dict_wallet:
            if symbol in self.dict_level:
                value_wallet = dict_wallet[symbol]['value']
                value_strategy = self.dict_level[symbol]
                value_frac = value_wallet / value_strategy
                
                if (value_frac < self.threshold_l) or (self.threshold_u < value_frac):
                    value_diff = Decimal(value_strategy) - Decimal(value_wallet) #TODO move this cast 
                    symbolpair = symbol + 'USDT'
                    symbol_info = dict_symbol_info[symbolpair]
                    price = Decimal(dict_price[symbolpair]) #TODO move this cast
                    order = ClientBinance.order_generate_by_value_market_static(symbolpair, symbol_info, price, value_diff)
                    list_order.append(order)

                    #TODO have it post other things as well
                    list_post.append('Bringing ' + symbol + ' into level')

        if len(list_order) == 0:
            list_post.append('All values seem within bounds, no action required')

        return list_order, list_post