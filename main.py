import tornado.ioloop
import tornado.web

import optparse
import logging

from ctrl import ChatController

def ParseLogLevel(level:str)->int:
    levels:dict[str,int] = {
        "info":logging.INFO,
        "warn":logging.WARN,
        "error":logging.ERROR,
    }

    default:int = logging.warn

    for s,l in levels.items():
        if s.lower() == level:
            default = l
            break

    return default

def MakeApp(bToken:str,latToken:str,model:str="gpt3.5",proxy:str="")->tornado.web.Application:
    logging.warning("[MakeApp] Using token p-b({}) p-lat({})".format(bToken,latToken))

    app = tornado.web.Application([
        (r'/v1/chat/completions',ChatController)
    ])
    app.settings["p-b"] = bToken
    app.settings["p-lat"] = latToken
    app.settings["proxy"] = proxy

    app.settings["model"] = model
    return app

def Main()->None:
    parser = optparse.OptionParser()
    parser.add_option("-b","",dest="b",help="p-b token of poe")
    parser.add_option("","--lat",dest="lat",help="p-lat token of poe")
    parser.add_option("-l","--logLevel",dest="logLevel",help="log level",default="warn")
    parser.add_option("-p","--port",dest="port",help="listen port",default="18081")
    parser.add_option("","--proxy",dest="proxy",help="http proxy",default="")
    parser.add_option("","--model",dest="model",help="ai model",default="")
    parser.parse_args()
    options,_ = parser.parse_args()

    bToken:str = options.b
    latToken:str = options.lat
    logLevel:str = options.logLevel
    port:int = int(options.port)
    proxy:str = options.proxy


    logging.basicConfig(level=ParseLogLevel(logLevel))
    logging.info("[Main] listen on 0.0.0.0:{}".format(port))

    app:tornado.web.Application = MakeApp(bToken,latToken,proxy=proxy)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    Main()