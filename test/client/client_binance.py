import os
import json
import time
import matplotlib.pyplot as plt
import numpy as np

from breaker_core.datasource.jsonqueue import Jsonqueue
from breaker_core.datasource.bytessource import Bytessource

from breaker_discord.client.client_binance import ClientBinance

path_file_config_breaker = os.environ['PATH_FILE_CONFIG_BREAKER']
with open(path_file_config_breaker, 'r') as file:
    dict_config = json.load(file)

binance_api_key = dict_config['binance_api_key']
binance_secret_key = dict_config['binance_secret_key']



client = ClientBinance(binance_api_key, binance_secret_key)

list_order = client.read_orders()
print(list_order)

list_trade = client.read_trades()
print(list_trade)

# dict_asset = client.read_assets()
# for asset_key, asset in dict_asset.items():
#     print(asset_key)
#     print(asset)

timestamp_ms = int(time.time() * 1000)
timestamp_ms_500m = timestamp_ms - (10000 * 60 * 1000) 

list_timestamp_h, list_price_h = client.get_list_price_historical('BTCUSDT', timestamp_ms_500m)
list_timestamp_n, list_price_n = client.get_list_price('BTCUSDT')
list_price_h = (np.array(list_price_h) + 1000).tolist()
print(len(list_price_h))
plt.figure()
plt.plot(list_timestamp_h, list_price_h)
plt.plot(list_timestamp_n, list_price_n)
plt.show()
# import matplotlib.pyplot as plt
# plt.figure()
# plt.plot(list_timestamp, list_price)
# plt.title('BTCUSDT')
# plt.xlabel('timestamp')
# plt.ylabel('price')
# plt.show()

# balance = client.read_asset_balance()
# print(balance)
client.get_symbol_info('BTCUSDT')




order, order_stats = client.order_generate_by_value_market('BTCUSDT', 10)
print(order)
