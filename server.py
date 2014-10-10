import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import threading

port = 9090

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    loader = tornado.template.Loader(".")
    self.write(loader.load("index.html").generate())

class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    print 'connection opened...'
    self.write_message("The server says: 'Hello'. Connection was accepted.")
    t=threading.Thread(target=self.hello)
    t.start()

  def on_message(self, message):
    self.write_message("The server says: " + message + " back at you")
    print 'received:', message

  def on_close(self):
    print 'connection closed...'

  def hello(self):
      print "hello"
      self.write_message("hello")
      t=threading.Timer(3,self.hello)
      t.start()

application = tornado.web.Application([
  (r'/ws', WSHandler),
  (r'/', MainHandler),
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
])

if __name__ == "__main__":
  application.listen(port)
  print "server started at "+str(port)
  tornado.ioloop.IOLoop.instance().start()
