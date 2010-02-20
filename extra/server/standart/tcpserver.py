from http.server import HTTPServer
from http.server import BaseHTTPRequestHandler
from extra.server.interfaces.iserver import (IServer, IHandler)

def specialize(mapper, foreign):
    mapper.foreign = foreign
    
class RequestMapper(IHandler, BaseHTTPRequestHandler):

    def do_GET(self):
        try:                     
            self.server.getRedirect().go(self)
        except Exception as msg:
            print(msg)
           
    def getPath(self):
        return self.path
        
    def setPath(self, path):
        self.path = path
    
    def sendCode(self, code:int):
        self.send_response(200)
    
    def sendHeader(self, name, value):
        self.send_header(name, value)
           
    def send(self, buf):
        self.wfile.write(buf)
    
    def closeSession(self):
        pass
    
    def closeHeaders(self):
        self.end_headers()

class SimpleHttpServer(IServer):
    
    def __init__(self, settings):
        self.server = HTTPServer((settings.ip, settings.port), settings.handler)
        setattr(self.server, "getRedirect", self.getRedirect)
        setattr(self.server, "setRedirect", self.setRedirect)
                   
    def run(self):
        self.server.serve_forever() 
    
    def kill(self):
        self.server.socket.close() 

    def setRedirect(self, object:"IProgram"):
        self.foreign = object
    
    def getRedirect(self):
        return self.foreign
