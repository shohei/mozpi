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
            print "writing to ",
            print str(client)
            client.write_message(msg)
    except:
        print FAIL,
        print client,
        print ": stream is dead"+ENDC

class MainHandler(web.RequestHandler):
    def get(self):
        loader = tornado.template.Loader(".")
        self.write(loader.load("index.html").generate())
        print "[Main] open MyClient socket ->:9090"
        ws = MyClient('ws://localhost:'+str(port_server)+'/ws', protocols=['http-only', 'chat'])
        ws.connect()

k=0
class MyClient(TornadoWebSocketClient):
     def opened(self):
        global k 
        print "==============MyClient opened "+str(k)+" times.============"
        self.send("hello "+str(datetime.datetime.now()))
        k=k+1

     def received_message(self, m): 
        print "[MyClient] Received ",
        print m
        print "[MyClient] open MyClient2 -> :8888"
        ws2 = MyClient2('ws://localhost:'+str(port_client)+'/ws', protocols=['http-only', 'chat'],message=m)
        ws2.connect()

     def closed(self, code, reason=None):
        ioloop.IOLoop.instance().stop()
        print "[MyClient] close MyClient socket -> :9090"

i=0
s=0
class MyClient2(TornadoWebSocketClient):
    def __init__(self,url,protocols=None,extensions=None,io_loop=None,ssl_options=None,headers=None,message=None):
        super(MyClient2,self).__init__(url,protocols=None,extensions=None,io_loop=None,ssl_options=None,headers=None)
        self.message = str(message)

    def opened(self):
        global i
        print OKGREEN+"[MyClient2] open socket->:8888, ",
        print str(self),
        print self.message+ENDC
        self.send(self.message)
        print "************MyClient2 opened "+str(i)+" times.************"
        i=i+1

    def received_message(self, m): 
        print OKGREEN+"[MyClient2] received from :8888-> ",
        print m+ENDC

    def closed(self, code, reason=None):
        global s
        print str(code),reason,
        print OKGREEN+"[MyClient2] close ->:8888, ",
        print str(self)+ENDC
        print "************MyClient2 closed "+str(s)+" times.************"
        s=s+1

j=0
class WSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print '[WSHandler] connection opened... at 8888'
        #self.write_message("The server says: 'Hello'. Connection was accepted.")
        print '[WSHandler] appending client'+str(self)
        clients.append(self)
  
    def on_message(self, message):
        global j
        print WARNING+str(j)+'[WSHandler] writing HTML to all the clients: ', message+ENDC
        #self.write_message(message)
        send_to_all_clients(message)
        j=j+1
  
    def on_close(self):
        print '[WSHandler] connection closed... :8888'
        clients.remove(self)

application = web.Application([
        (r"/", MainHandler),
        (r'/ws', WSHandler),
        (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./"}),
])


application.listen(port_client)
print "[START] server open at "+str(port_client)
ioloop.IOLoop.instance().start()
