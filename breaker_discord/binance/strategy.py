class Strategy(object):

    def __init__(self) -> None:
        super().__init__()


    def generate_list_order(self, timestamp, dict_wallet:dict, dict_symbol_info:dict, dict_price:dict, history):
        raise NotImplementedError()