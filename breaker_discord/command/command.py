class Command(object):

    def __init__(self, keyword:str='', help_message:str='') -> None:
        super().__init__()
        self.keyword = keyword
        self.help_message = help_message
        self.bot = None

    async def execute(self, list_argument, message) -> None:
        raise NotImplementedError()