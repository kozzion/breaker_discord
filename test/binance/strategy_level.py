from decimal import Decimal
import time 
import os
import json
from breaker_discord.binance.simulator import Simulator
import numpy as np

from pathlib import Path
from breaker_core.datasource.bytessource import Bytessource

from breaker_discord.client.client_binance import ClientBinance
from breaker_discord.binance.strategy_level import StrategyLevel



path_file_config_breaker = os.environ['PATH_FILE_CONFIG_BREAKER']
with open(path_file_config_breaker, 'r') as file:
    dict_config = json.load(file)

binance_api_key = dict_config['binance_api_key']
binance_secret_key = dict_config['binance_secret_key']

bytessource_bot = Bytessource.from_dict(dict_config['bytessource_bot'])
bytessource_binance = bytessource_bot.join(['binance'])

client_binance = ClientBinance(binance_api_key, binance_secret_key)
id_user = '102797880246419456'



# get dataset
path_file_data_set = Path('dataset.tmp')
if not path_file_data_set.exists():
    timestamp_ms = int(time.time() * 1000)
    timestamp_ms_100d = timestamp_ms - (100 * 24 * 60 * 60 * 1000) 
    list_timestamp, list_price = client_binance.get_list_price_historical('BTCUSDT', timestamp_ms_100d)
    data_set = {'list_timestamp':list_timestamp,'list_price':list_price}
    with path_file_data_set.open('w') as file:
        data_set = json.dump(data_set, file)
else:
    with path_file_data_set.open('r') as file:
        data_set = json.load(file)
    list_timestamp = data_set['list_timestamp']
    list_price = data_set['list_price']

# get symbol_info
path_file_symbol_info = Path('symbol_info.tmp')
if not path_file_symbol_info.exists():
    symbol_info = client_binance.get_symbol_info('BTCUSDT')
    with path_file_symbol_info.open('w') as file:
        symbol_info = json.dump(symbol_info, file)
else:
    with path_file_symbol_info.open('r') as file:
        symbol_info = json.load(file)

list_timestamp = list_timestamp[:2000]
list_price = list_price[:2000]

# remove trend 
array_trend = np.linspace(list_price[0], list_price[-1], num=len(list_timestamp))
list_price = ((np.array(list_price) - array_trend) + max(list_price)).tolist() 


# build simulator
simulator = Simulator('BTCUSDT', list_timestamp, list_price, symbol_info)

# do actual simulation
threshold_u = Decimal(1.001)
threshold_l = Decimal(0.999)
strategy = StrategyLevel(client_binance, bytessource_binance, id_user, threshold_u, threshold_l)
result = simulator.evaluate(strategy)

# show resut
Simulator.plot_result(result, threshold_u, threshold_l)

