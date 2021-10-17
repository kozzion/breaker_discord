class Agent(object):

    def __init__(self, id_agent) -> None:
        super().__init__()
        self.id_agent = id_agent

    async def on_voice_state_update(self, list_argument, message) -> None:
        pass