OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

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
        print FAIL,
        print client,
        print ": stream is dead"+ENDC

class MainHandler(web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(".")
        self.write(loader.load("index.html").generate())
        print "[Main] open MyClient socket"
        ws = MyClient('ws://localhost:'+str(port_server)+'/ws', protocols=['http-only', 'chat'])
        ws.connect()

class MyClient(TornadoWebSocketClient):
     def opened(self):
        self.send("hello "+str(datetime.datetime.now()))

     def received_message(self, m): 
         print "[MyClient] Received ",
         print m
         ws2 = MyClient2('ws://localhost:'+str(port_client)+'/ws', protocols=['http-only', 'chat'],message=m)
         ws2.connect()

     def closed(self, code, reason=None):
         ioloop.IOLoop.instance().stop()
         print "[MyClient] close MyClient socket"

class MyClient2(TornadoWebSocketClient):
    def __init__(self,url,protocols=None,extensions=None,io_loop=None,ssl_options=None,headers=None,message=None):
        super(MyClient2,self).__init__(url,protocols=None,extensions=None,io_loop=None,ssl_options=None,headers=None)
        self.message = str(message)

    def opened(self):
        print OKGREEN+"[MyClient2] open socket. Bypass message to our server.",
        print self.message+ENDC
        self.send(self.message)
        self.close()
        #self.finish()

    def received_message(self, m): 
        print OKGREEN+"[MyClient2] received: ",
        print m+ENDC

    def closed(self, code, reason=None):
        #ioloop.IOLoop.instance().stop()
        print OKGREEN+"[MyClient2] close MyClient2 socket"+ENDC

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print '[WSHandler] connection opened...'
        self.write_message("The server says: 'Hello'. Connection was accepted.")
        clients.append(self)
        self.i = 0
  
    def on_message(self, message):
        print self.i,
        print WARNING+'[WSHandler] writing HTML: ', message+ENDC
        send_to_all_clients(message)
        self.i=self.i+1
  
    def on_close(self):
        print '[WSHandler] connection closed...'
  

application = web.Application([
        (r"/", MainHandler),
        (r'/ws', WSHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./"}),
])


application.listen(port_client)
print "[START] server open at "+str(port_client)
ioloop.IOLoop.instance().start()
