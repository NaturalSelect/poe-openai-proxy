from tornado.httputil import HTTPServerRequest
import tornado.web

import bot
import proto
import logging

class ChatController(tornado.web.RequestHandler):

    poe:bot.PoeBot

    def __init__(self, application: tornado.web.Application, request: HTTPServerRequest, **kwargs: tornado.web.Any) -> None:
        super().__init__(application, request, **kwargs)
        token:str = application.settings["token"]
        model:str = application.settings["model"]
        proxy:list[str] = application.settings["proxy"]
        self.poe = bot.PoeBot(token,model,proxy)


    async def post(self,*args, **kwargs):
        jsonData:str = str(self.request.body,"utf8")
        req:proto.OpenAIRequest = proto.OpenAIRequest.Unmarshal(jsonData)
        # NOTE: find fist user prompt
        userPrompt:proto.Prompt = None
        for i in req.messages:
            logging.info("prompt role({}) content({})".format(i.role,i.content))
            if i.role == "user":
                userPrompt = i
                break
        if userPrompt == None:
            logging.error("user prompt not found, messages cnt({})".format(len(req.messages)))
            self.send_error(400)
            return

        # NOTE: ask poe bot
        logging.info("user prompt content({})".format(userPrompt.content))
        answer:str = await self.poe.Chat(userPrompt.content)
        logging.info("ask question({}) got answer({})".format(userPrompt.content,answer))

        # NOTE: write response
        resp = proto.OpenAIResponse(proto.Prompt("bot",answer))
        self.set_header("Content-Type","application/json")
        self.write(resp.Marshal())
        logging.info("write response({})".format(resp.Marshal()))