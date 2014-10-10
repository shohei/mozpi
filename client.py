from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop,web
import time,datetime
import tornado.websocket
import tornado.template

port_server = 9090
port_client = 8888

class MainHandler(web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(".")
        self.write(loader.load("index.html").generate())
        print "open MyClient socket"
        ws = MyClient('ws://localhost:'+str(port_server)+'/ws', protocols=['http-only', 'chat'])
        ws.connect()

class MyClient(TornadoWebSocketClient):
     def opened(self):
        self.send("hello "+str(datetime.datetime.now()))

     def received_message(self, m): 
         print "Received from central",
         print m
         ws2 = MyClient2('ws://localhost:'+str(port_client)+'/ws', protocols=['http-only', 'chat'],message=m)
         print "instantiate ws2" 
         ws2.connect()
         print "connected to ws2" 

     def closed(self, code, reason=None):
         ioloop.IOLoop.instance().stop()
         print "close MyClient socket"

class MyClient2(TornadoWebSocketClient):
     def __init__(self,url,protocols=None,extensions=None,io_loop=None,ssl_options=None,headers=None,message=None):
         super(MyClient2,self).__init__(url,protocols=None,extensions=None,io_loop=None,ssl_options=None,headers=None)
         self.message = str(message)

     def opened(self):
        print "open MyClient2 socket. Bypass message to our server."
        print "self.message is : ",
        print self.message
        #self.send("I am Client2")
        self.send(self.message)

     def received_message(self, m): 
         print "[Client2]: ",
         print m

     def closed(self, code, reason=None):
         print "close MyClient2 socket"

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print 'connection opened...'
        self.write_message("The server says: 'Hello'. Connection was accepted.")
  
    def on_message(self, message):
        self.write_message("The server says: " + message + " back at you")
        print 'received:', message
  
    def on_close(self):
        print 'connection closed...'

  
application = web.Application([
        (r"/", MainHandler),
        (r'/ws', WSHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./"}),
])


application.listen(port_client)
print "server open at "+str(port_client)
ioloop.IOLoop.instance().start()
