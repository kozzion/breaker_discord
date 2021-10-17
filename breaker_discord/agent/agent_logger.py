class AgentLoggerEvent(object):

    def __init__(self) -> None:
        super().__init__('AgentLoggerEvent')

    def register(self, client_bot): 
        @client_bot.event
        async def on_voice_state_update(member, before, after):
            print('on_voice_state_update_agent')
            print(member)
            print(before)
            print(after)