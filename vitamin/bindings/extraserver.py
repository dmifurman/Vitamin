from extra.server.interfaces.iprogram import IProgram
from vitamin.config import Tweak, Parameter

class ServerProgram(IProgram, Tweak("Loader")):
    
    def __init__(self):
        self.NEXT_NODE = Parameter()
        self.tweak()
        
        self.program = self.NEXT_NODE()
    
    def go(self, iheader):
        self.program.go(iheader)
    
    def info(self):
        return "Vitamin binding for native server system"
        
    def restart(self):
        self.program = self.NEXT_NODE()
