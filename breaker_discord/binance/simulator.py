
import numpy as np
from decimal import Decimal
import matplotlib.pyplot as plt

from breaker_discord.binance.strategy import Strategy

class Simulator(object):

    def __init__(self, symbolpair, list_timestamp, list_price, symbol_info) -> None:
        super().__init__()
        self.symbolpair = symbolpair
        self.symbol_info = symbol_info
        self.list_timestamp = list_timestamp
        self.list_price = list_price

    def evaluate(self, strategy:Strategy):
        dict_symbol_info = {self.symbolpair:self.symbol_info}
        price = self.list_price[0]
        count_order = 0
        dict_wallet_initial = {
            'USDT':{
                'amount':Decimal(10000),
                'price':Decimal(1),
                'value':Decimal(0)},
            'BTC':{
                'amount':Decimal(0),
                'price':Decimal(self.list_price[0]),
                'value':Decimal(0)}}
        sum_cost = 0

        list_sum_cost = []
        list_sum_cost.append(sum_cost)
        list_dict_wallet = []
        list_dict_wallet.append(dict_wallet_initial)

        for timestamp, price in zip(self.list_timestamp[1:], self.list_price[1:]):
            # update_wallet
            price = Decimal(price) #TODO move this cast

            dict_wallet = list_dict_wallet[-1].copy()
            dict_wallet['BTC']['price'] = price
            dict_wallet['BTC']['value'] = price * dict_wallet['BTC']['amount']
            dict_price ={self.symbolpair:price} #TODO maybe remove because this is also in the wallet

            history = {}
            list_order, list_post = strategy.generate_list_order(timestamp, dict_wallet, dict_symbol_info, dict_price, history)
            count_order += len(list_order)

            for order in list_order:
                
                if order['side'] == 'BUY':
                    dict_wallet['USDT']['amount'] -= Decimal(order['quantity']) * price #TODO move this cast
                    dict_wallet['USDT']['value'] -= Decimal(order['quantity']) * price #TODO move this cast
                    dict_wallet['BTC']['amount'] += Decimal(order['quantity'])
                    dict_wallet['BTC']['value'] += Decimal(order['quantity']) * price
                else:
                    dict_wallet['USDT']['amount'] += Decimal(order['quantity']) * price
                    dict_wallet['USDT']['value'] += Decimal(order['quantity']) * price #TODO move this cast
                    dict_wallet['BTC']['amount'] -= Decimal(order['quantity'])
                    dict_wallet['BTC']['value'] -= Decimal(order['quantity']) * price #TODO move this cast
            # print(dict_wallet['BTC']['value'])
            list_dict_wallet.append(dict_wallet)
            list_sum_cost.append(sum_cost)

        total_value_start = 10000
        total_value_end = 0
        for symbol, entry in dict_wallet.items():
            total_value_end += entry['value']
        total_gain = total_value_end / total_value_start
        
        result = {}
        result['total_gain'] = total_gain
        result['list_sum_cost'] = list_sum_cost
        result['count_order'] = count_order
        result['dict_value'] = {}
        result['dict_amount'] = {}
        result['list_timestamp'] = self.list_timestamp
        result['list_price'] = self.list_price
        result['list_total_value'] = []
        result['dict_list_value'] = {}
        result['dict_list_amount'] = {}
        for symbol in dict_wallet:
            result['dict_list_value'][symbol] = []
            result['dict_list_amount'][symbol] = []
        for dict_wallet in list_dict_wallet:
            total_value = 0
            for symbol in dict_wallet:
                amount = dict_wallet[symbol]['amount']
                value = dict_wallet[symbol]['value']
                print(value)
                total_value += value
                result['dict_list_value'][symbol].append(value)
                result['dict_list_amount'][symbol].append(amount)
            result['list_total_value'].append(total_value)
        return result
    
    @staticmethod
    def plot_result(result, threshold_u, threshold_l):
        list_timestamp = result['list_timestamp']
        list_price = result['list_price']
        list_total_value = result['list_total_value']
        list_value_coin = result['dict_list_value']['BTC']
        plt.figure()
        plt.subplot(4,1,1)
        plt.plot(list_timestamp, list_price)

        plt.subplot(4,1,2)
        plt.plot([list_timestamp[0], list_timestamp[-1]], [threshold_u, threshold_u], label='threshold_u')
        plt.plot([list_timestamp[0], list_timestamp[-1]], [threshold_l, threshold_l], label='threshold_l')
        plt.plot(list_timestamp, np.array(list_total_value) /1000, label='value_coin')
        plt.legend()

        plt.subplot(4,1,3)
        plt.plot(list_timestamp, result['list_sum_cost'], label='cost_sum')
        # plt.plot(list_timestamp, list_gain_sum, label='value_total')
        plt.legend()
        plt.show()