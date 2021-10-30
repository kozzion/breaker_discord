import datetime
import matplotlib.pyplot as plt
from breaker_core.datasource.bytessource import Bytessource
from breaker_core.datasource.bytessource_bytearray import BytessourceBytearray

from breaker_discord.client.client_binance import ClientBinance
from breaker_discord.command.command import Command

class CommmandBinance(Command):

    def __init__(self, client_binance:ClientBinance, bytessource_binance:Bytessource) -> None:
        self.client_binance = client_binance
        self.bytessource_binance = bytessource_binance
        self.list_id_user_authorized = []
        self.dict_list_order_pending = {}
        help_message = '\n'
        help_message += '!binance \{subcommand\}\n'
        help_message += 'subcommand: the filename of an existing file to post suggestions: show\n'
        super().__init__('binance', help_message)

    async def execute(self, list_argument, message) -> None:
        print('execute')
        if len(list_argument) == 0:       
            await message.channel.send("Please provide a \{subcommand\} argument.")   
            return

        keyword = list_argument[0] 
        list_argument = list_argument[1:]
        if keyword == 'show':
            await self.execute_show(list_argument, message)    
        elif keyword == 'wallet':
            await self.execute_wallet(list_argument, message) 
        elif keyword == 'trade':
            await self.execute_trade(list_argument, message)  
        elif keyword == 'pending':
            await self.execute_pending(list_argument, message)   
        elif keyword == 'execute':
            await self.execute_execute(list_argument, message)    
        else:
            await message.channel.send("Unknown subcommand: " + keyword)   

    async def execute_show(self, list_argument, message) -> None:
        print('execute_show')
        if len(list_argument) == 0:       
            await message.channel.send("Please provide a \{symbolpair\} argument such as BTCUSDT.")   
            return
        symbolpair = list_argument[0]
        list_timestamp, list_price = self.client_binance.get_list_price(symbolpair)
        print(symbolpair)
        plt.figure()
        plt.plot(list_timestamp, list_price)
        plt.title(symbolpair)
        plt.xlabel('timestamp')
        plt.ylabel('price')

        print('logplotevent!')
        path_file_plot = 'plot.png' #TODO make bytearray_source getable as tempfilepath
        plt.savefig(path_file_plot)
        with open(path_file_plot, 'rb') as file:
             #TODO make bytearray_source getable as tempfilepath
            bytessource_post = BytessourceBytearray(file.read())
        await self.bot.post_bytessource(bytessource_post, path_file_plot, message.channel)

    async def execute_wallet(self, list_argument, message) -> None:
        dict_wallet = self.client_binance.get_wallet()
        str_message = 'showing wallet for user\n'
        str_message += '```symbol'.rjust(10) + 'amount'.ljust(10)  + 'value'.ljust(10)  + '\n'
        total = 0
        for symbol in dict_wallet:
            amount = '{:.3f}'.format(dict_wallet[symbol]['amount'])
            value = '{:.3f}'.format(dict_wallet[symbol]['value'])
            total += dict_wallet[symbol]['value']
            str_message += symbol.ljust(10) + amount.rjust(10) + value.rjust(10) + '\n'
        
        str_total = '{:.3f}'.format(total)
        str_message += 'total'.ljust(10) + ''.rjust(10) + str_total.rjust(10) + '\n'
        str_message += '```'
        await message.channel.send(str_message)  


    async def execute_strategy(self, list_argument, message) -> None:
        print()
        dict_wallet = self.client_binance.get_wallet()

    async def execute_trade(self, list_argument, message) -> None:
        id_user = str(message.author.id)
        if id_user != '102797880246419456':
            await message.channel.send("Subcommand trade not authorized for user " + message.author.name)   
            return

        if len(list_argument) < 1:       
            await message.channel.send("Please provide a \{symbol\} argument such as BTC or a symbolpair such as BTCUSDT")   
            return
        
        if len(list_argument) < 2:       
            await message.channel.send("Please provide a \{amount\} argument can be positive for but or negative for sell")   
            return
        
        await message.channel.send("Adding pening order for user: " + message.author.name)   
        if 'USDT' in list_argument[0]: #TODO could be better, like endswith
            symbolpair = list_argument[0]
        else:
            symbolpair = list_argument[0] + 'USDT' 
        amount = float(list_argument[1])

        order, order_stats = self.client_binance.order_generate_by_value_market(symbolpair, amount)
        if not id_user in self.dict_list_order_pending:
            self.dict_list_order_pending[id_user] = []
        
        self.dict_list_order_pending[id_user].append(order)
        await self.execute_pending(list_argument, message)

    async def execute_accept(self, list_argument, message) -> None:
        id_user = str(message.author.id)
        await self.execute_pending(list_argument, message)

    async def execute_pending(self, list_argument, message) -> None:
        id_user = str(message.author.id)
        if not id_user in self.dict_list_order_pending:
            await message.channel.send("No order pending")   
            return
        if len(self.dict_list_order_pending[id_user]) == 0:
            await message.channel.send("No order pending")   
            return

        str_message = 'listing order pending for ' + id_user
        str_message += '```'
        for order_pending in self.dict_list_order_pending[id_user]:
            str_message += str(order_pending)
        str_message += '```'
        await message.channel.send(str_message)   

    async def execute_execute(self, list_argument, message) -> None:
        id_user = str(message.author.id)
        if not id_user in self.dict_list_order_pending:
            await message.channel.send("No order pending")   
            return
        if len(self.dict_list_order_pending[id_user]) == 0:
            await message.channel.send("No order pending")   
            return
        for order_pending in self.dict_list_order_pending[id_user]:
            order_response = self.client_binance.order_execute(order_pending)
        self.dict_list_order_pending[id_user] = []
    #     list_order_pending
    # self.dict_list_order_pending
    #     for order in list
    #      order_response = self.client_binance.order_execute(order)
    #     print(order_response)

# # fetch 1 minute klines for the last day up until now
# klines = 

# # fetch 30 minute klines for the last month of 2017
# klines = client.get_historical_klines("ETHBTC", Client.KLINE_INTERVAL_30MINUTE, "1 Dec, 2017", "1 Jan, 2018")

# # fetch weekly klines since it listed
# klines = client.get_historical_klines("NEOBTC", Client.KLINE_INTERVAL_1WEEK, "1 Jan, 2017")
