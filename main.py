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

def MakeApp(token:str,proxy:str)->tornado.web.Application:
    logging.warning("[MakeApp] Using token {}".format(token))

    app = tornado.web.Application([
        (r'/v1/chat/completions',ChatController)
    ])
    app.settings["token"] = token
    if proxy != "":
        proxies:list[str] = list()
        proxies.append(proxy)
        app.settings["proxy"] = proxies
    return app

def Main()->None:
    parser = optparse.OptionParser()
    parser.add_option("-t","--token",dest="token",help="token of poe")
    parser.add_option("-l","--logLevel",dest="logLevel",help="log level")
    parser.add_option("-p","--port",dest="port",help="listen port")
    parser.add_option("","--proxy",dest="proxy",help="http proxy")
    parser.parse_args()
    options,_ = parser.parse_args()

    token:str = options.token
    logLevel:str = options.logLevel
    port:int = int(options.port)
    proxy:str = options.proxy


    logging.basicConfig(level=ParseLogLevel(logLevel))
    logging.info("[Main] listen on 0.0.0.0:{}".format(port))

    app:tornado.web.Application = MakeApp(token,proxy)
    app.listen(port)
    tornado.ioloop.IOLoop.current().start()

if __name__ == "__main__":
    Main()