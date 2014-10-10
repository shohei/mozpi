import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import threading
from ws4py.client.tornadoclient import TornadoWebSocketClient

port = 9090
clients = []

def send_to_all_clients(msg):
    try:
        for client in clients:
            client.write_message(msg)
    except:
        pass

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    loader = tornado.template.Loader(".")
    self.write(loader.load("server.html").generate())

class HelloHandler(tornado.web.RequestHandler):
  def get(self):
    print "Button hit!"
    ws = MyClient("ws://localhost:9090/ws",protocols=['chat','http-only'],message="I'm saying hello.")
    ws.connect()

class MyClient(TornadoWebSocketClient):
  def __init__(self,url,protocols=None,extensions=None,io_loop=None,ssl_options=None,headers=None,message=None):
    super(MyClient,self).__init__(url,protocols=None,extensions=None,io_loop=None,ssl_options=None,headers=None)
    self.message = str(message)

  def opened(self):
    self.send(self.message)
    self.close()
    
  def received_message(self,message):
    pass

  def closed(self,code,reason=None):
    pass

class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    print 'connection opened...'
    clients.append(self)

  def on_message(self, message):
    #self.write_message(message)
    send_to_all_clients(message)
    print 'received and echoing:', message

  def on_close(self):
    print 'connection closed...'
    clients.remove(self)

application = tornado.web.Application([
  (r'/ws', WSHandler),
  (r'/', MainHandler),
  (r'/hello', HelloHandler),
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./"}),
])

if __name__ == "__main__":
  application.listen(port)
  print "server started at "+str(port)
  tornado.ioloop.IOLoop.instance().start()
