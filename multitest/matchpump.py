from ws4py.client.tornadoclient import TornadoWebSocketClient
from tornado import ioloop,web
import time,datetime
import tornado.websocket
import tornado.template

class MyClient(TornadoWebSocketClient):
     def opened(self):
        print "[Client] connection opened"
        self.send("hello "+str(datetime.datetime.now()))

     def received_message(self, m): 
         print "[Client] Received from central: ",
         print m

     def closed(self, code, reason=None):
         ioloop.IOLoop.instance().stop()
         print "[Client] close MyClient socket"

class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print '[Server] connection opened...'
        self.write_message("The server says: 'Hello'. Connection was accepted.")
  
    def on_message(self, message):
        self.write_message("The server says: " + message + " back at you")
        print '[Server] received:', message
  
    def on_close(self):
        print '[Server] connection closed...'

  
application = web.Application([
        (r'/ws', WSHandler),
])


application.listen(8888)
print "server open at 8888"
ws = MyClient('ws://localhost:8888/ws', protocols=['http-only', 'chat'])
ws.connect()
ioloop.IOLoop.instance().start()
