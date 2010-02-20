from vitamin.config import Tweak, Parameter

class Templates(Tweak("Templates")):
    
    def __init__(self, load_from=None):   
             
        self.LOADER = Parameter()
        self.tweak()
        self.loader = self.LOADER(load_from)        
    
    def load(self, name):    
            
        return self.loader.load(name)
        
