from extra.server.interfaces.iprogram import IProgram

class DummyHandler(IProgram):

    def __init__(self):
        IProgram.__init__(self)

    def go(self, ihandler):
    
        ihandler.sendCode(200)
        ihandler.sendHeader("Content-type", "text/html")
        ihandler.closeHeaders()
    
        ihandler.send(self.info().encode())
    
    def restart(self):
        pass
        
    def info(self):
        return "DummyHandler: version 0.1"       
