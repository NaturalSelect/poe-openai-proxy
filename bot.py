from poe_api_wrapper import AsyncPoeApi

import logging

class PoeBot:
    token:str

    bot:AsyncPoeApi

    proxy:list[str]

    model:str

    def __init__(self,token:str,model:str="gpt3.5",proxy:list[str]=None) -> None:
        self.token = token
        self.bot == None
        self.proxy=proxy
        self.model=model

    async def createBot(self) -> None:
        if self.bot != None:
            return

        autoProxy = self.proxy != None and len(self.proxy) != 0
        bot = AsyncPoeApi({"p-b":self.token},self.proxy,autoProxy)
        await bot.create()
        self.bot = bot
        logging.info("create bot success, token({}) proxy({})".format(self.token,self.proxy))

    async def Chat(self,msg:str) -> str:
        self.createBot()

        logging.info("asking question({})".format(msg))
        response = self.bot.send_message(self.model,msg)
        answer = ""
        async for chunk in response:
            answer += chunk["response"]
        return answer