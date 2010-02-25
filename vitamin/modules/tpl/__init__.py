from vitamin.config import Tweak, Parameter
from vitamin.modules.tpl.mutagen import Mutagen


class Templates(Tweak("Templates")):
    
    def __init__(self, load_from=None):   
             
        self.LOADER = Parameter()
        self.tweak()
        self.loader = self.LOADER(load_from)
        self.mutagen = Mutagen()  
    
    def load(self, name):            
        return self.mutagen.mutate(
            loader=self.loader,
            template=self.loader.load(name))
        
