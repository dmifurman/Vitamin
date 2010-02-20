
#$Rev: 117 $     
#$Author: fnight $  
#$Date: 2009-08-20 18:16:18 +0400 (Чт, 20 авг 2009) $ 

#This file is part of Vitamin Project

def convertFromStr(arg):

    if arg.startswith("\""):
        return arg[1:-1]
            
    try:
        f = float(arg)
        try:
            return int(arg)
        except ValueError:
            return f
    except ValueError:
        return None


class Context(dict):

    def __init__(self, **kwargs):
        self.update(kwargs)
        self.methodsAvalible = (x for x in dir(methods) if not x.startswith("_"))
        
    def getQuicker(self, name):
        try:  
            if "." in name: 
                parameters = name.split(".")
                anchor = self.values[parameters[0]]
            else:
                return self[name]
                
            for parameter in parameters[1:]:
                anchor = getattr(anchor, parameter)
            return anchor  
        except KeyError:
            if name in self.methodsAvalible:
                return getattr(methods, name)
            else:
                raise Exception("Contest miss {0}".format(name))                       
        
    def get(self, name): 
        value = convertFromStr(name)
        if value != None: return value    
        return self.getQuicker(name)      

class Aggregator(list):

    def __init__(self):
        self.modAvalible = (x for x in dir(modificators) if not x.startswith("_"))
        self.modCache = {}
        self.modLine = {}
        self.modTemp = []

    def pushMod(self, name, state):
        if not name in self.modCache:    
            self.modCache[name] = getattr(modificators, name)
        if not name in self.modLine:
            self.modLine[name] = []         
        self.modLine[name].append(state)
        self.modTemp.append([])

    def decMod(self, name):
        result = "".join(self.modTemp[-1])
        if self.modLine[name][-1]:
            result = self.modCache[name](result)
        
        del self.modTemp[-1]
        self.append(result)
        
        del self.modLine[name][-1]
        if len(self.modLine[name]) == 0:
            del self.modLine[name]
            
    def append(self, item):
        if self.modTemp:
            self.modTemp[-1].append(item)
        else:
            list.append(self, item)
            
    def delete(self, index):
        del self[index]

    def join(self):
        return "".join(self)
    

            

