import os
from extra.server.interfaces.iprogram import IProgram
from extra.server.config import Tweak, Parameter

class FileSender(IProgram, Tweak("Program")):

    def __init__(self):
        IProgram.__init__(self)
        self.HTML = Parameter()
        self.ERRORS = Parameter()
        self.SHOW_HIDDEN = Parameter(False)
        self.tweak()

    def go(self, ihandler):              
        self.sendFile(ihandler)       
    
    def restart(self):
        pass
        
    def info(self):
        return "HTMLFileHandler: version 0.1"     
    
    ########################end interface
    
    def joinPath(self, dir, path):
        return os.path.join(dir, path[1:]
            if path.startswith("/") else path) 
        
    def sendErrorPage(self, code, ihandler):
        page = self.joinPath(self.ERRORS, str(code) + ".html")
        if os.path.exists(page):
            with open(page, "rb") as f:
                ihandler.sendCode(404)
                ihandler.sendHeader("Content-type", "text/html")
                ihandler.closeHeaders()  
                ihandler.send(f.read())
        else:
            raise Exception("No error html: " + code)
    
    def sendFile(self, ihandler):
        page = self.joinPath(self.HTML, ihandler.getPath())
        if os.path.exists(page):
            if not os.path.isdir(page):
                with open(page, "rb") as f:
                    ihandler.sendCode(200)
                    ihandler.sendHeader("Content-type", "text/html")
                    ihandler.closeHeaders()
                    ihandler.send(f.read())
            else: self.sendDir(page, ihandler)
        else:
            self.sendErrorPage(404, ihandler)
            
    def sendDir(self, path, ihandler):
        _spath = ihandler.getPath()
        ihandler.sendCode(200)
        ihandler.sendHeader("Content-type", "text/html")
        ihandler.closeHeaders()  
        ihandler.send("<h1>List of '{0}' directory</h1><br>".format(_spath).encode())        
        list = os.listdir(path)
        if not self.SHOW_HIDDEN: list = [x for x in list if not x.startswith(".")]
        for item in list:
            ihandler.send("<li><a href={0}>{1}</a><br></li>".format(os.path.join(_spath, item), item).encode())
