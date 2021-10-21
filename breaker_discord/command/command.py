class Command(object):

    def __init__(self, keyword:str='', help_message:str='', list_id_agent_required=[]) -> None:
        super().__init__()
        self.keyword = keyword
        self.help_message = help_message
        self.list_id_agent_required = list_id_agent_required
        self.bot = None

    async def execute(self, list_argument, message) -> None:
        raise NotImplementedError()