class Event():
    
    def __init__(self):
        self.handlers = []
        
    def __iadd__(self, handler):
        if hasattr(handler, "__call__"):
            self.handlers.append(handler)
        else: 
            raise Exception("Wrong event handler! __call__ please!")
        return self
    
    def __isub__(self, handler):
        if handler in self.handlers:
            del self.handlers[self.handlers.index(handler)]
        return self
                   
    def __call__(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)
            
    def __len__(self):
        return len(self.handlers)
    
    def clear(self):
        self.handlers = []
        
    def attach(self, handles):
        self.handlers += handles
           
class bind():
    
    def __inti__(self, function):
        self.function = function
        
    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs) 
