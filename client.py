from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop,web
import time,datetime
import tornado.websocket
import tornado.template

port_server = 9090
port_client = 8888

clients = []
def send_to_all_clients(msg):
    try:
        for client in clients:
            client.write_message(msg)
    except:
         pass

class MainHandler(web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(".")
        self.write(loader.load("index.html").generate())
        ws = MyClient('ws://localhost:'+str(port_server)+'/ws', protocols=['http-only', 'chat'])
        ws.connect()

k=0
class MyClient(TornadoWebSocketClient):
     def opened(self):
        global k 
        self.send("hello "+str(datetime.datetime.now()))
        k=k+1

     def received_message(self, m): 
        ws2 = MyClient2('ws://localhost:'+str(port_client)+'/ws', protocols=['http-only', 'chat'],message=m)
        ws2.connect()

     def closed(self, code, reason=None):
        ioloop.IOLoop.instance().stop()

class MyClient2(TornadoWebSocketClient):
    def __init__(self,url,protocols=None,extensions=None,io_loop=None,ssl_options=None,headers=None,message=None):
        super(MyClient2,self).__init__(url,protocols=None,extensions=None,io_loop=None,ssl_options=None,headers=None)
        self.message = str(message)

    def opened(self):
        self.send(self.message)
        self.close() #I don't know if this is neccesssary

    def received_message(self, m): 
        pass

    def closed(self, code, reason=None):
        pass

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        clients.append(self)
  
    def on_message(self, message):
        send_to_all_clients(message)
  
    def on_close(self):
        clients.remove(self)

application = web.Application([
        (r"/", MainHandler),
        (r'/ws', WSHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./"}),
])


application.listen(port_client)
print "[START] server open at "+str(port_client)
ioloop.IOLoop.instance().start()
