from poe_api_wrapper import AsyncPoeApi

import logging

class PoeBot:
    bToken:str

    latToken:str

    bot:AsyncPoeApi|None

    proxy:str

    model:str

    def __init__(self,bToken:str,latToken:str,model:str="capybara",proxy:str="") -> None:
        self.bToken = bToken
        self.latToken = latToken
        self.bot = None
        self.proxy = proxy
        self.model = model

    async def createBot(self) -> None:
        if self.bot != None:
            return

        logging.info("try to create bot({})".format(self.model))
        proxies=[]
        if self.proxy != "":
            proxies = [{"http":self.proxy,"https":self.proxy}]
        bot = AsyncPoeApi({"b":self.bToken,"lat":self.latToken},proxies,len(proxies) == 0)
        logging.info("bot({}) creating".format(self.model))
        await bot.create()
        self.bot = bot
        logging.info("create bot success, p-b({}) p-lat({}) proxy({})".format(self.bToken,self.latToken,self.proxy))

    async def Chat(self,msg:str) -> str:
        await self.createBot()

        logging.info("asking bot({}) question({})".format(self.model,msg))
        answer = ""
        async for chunk in self.bot.send_message(self.model,msg):
            logging.info("recv message({}) from bot".format(chunk["response"]))
            answer += chunk["response"]
        return answer