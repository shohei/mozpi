import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import threading
from ws4py.client.tornadoclient import TornadoWebSocketClient

port = 9090

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    loader = tornado.template.Loader(".")
    self.write(loader.load("server.html").generate())

class HelloHandler(tornado.web.RequestHandler):
  def get(self):
    ws = MyClient("ws://localhost:9090/ws",protocols=['chat','http-only'],message=m)
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
    #self.write_message("The server says: 'Hello'. Connection was accepted.")
    #t=threading.Thread(target=self.hello)
    #t.start()

  def on_message(self, message):
    self.write_message(message)
    print 'received and echoing:', message

  def on_close(self):
    print 'connection closed...'

  #debug method
  def hello(self):
    print "hello"
    self.write_message("hello")
    t=threading.Timer(3,self.hello)
    t.start()

application = tornado.web.Application([
  (r'/ws', WSHandler),
  (r'/', MainHandler),
  (r'/hello', HelloHandler),
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
])

if __name__ == "__main__":
  application.listen(port)
  print "server started at "+str(port)
  tornado.ioloop.IOLoop.instance().start()
