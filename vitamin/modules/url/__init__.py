from vitamin.interfaces import IModuleURL
import re
from .rule import Rule
from vitamin.config import Tweak, Parameter

__all__ = ["RequestManager"]

class RequestManager(IModuleURL, Tweak("URL")):
       
    def __init__(self):
        self.ROUTES = Parameter()
        self.tweak()
        
        self.rules = []
        self._add_rules(self.ROUTES)
        
    #===========================================================================
    # go, info to IModule
    #===========================================================================
    
    def go(self, context):
        url = self._format(context.handler.getPath())
        for rule in self.rules:
            result, args = rule.check(url)
            if result: 
                print("Requested block '{0}' with args {1}".format(rule.block, args))
                context.block = rule.block
                context.arguments = args            
        
    def info(self): 
        return "Standart vitamin URL module"
    
    #===========================================================================
    # end
    #===========================================================================

    def _block(self, matchobj):
        "Вытаскивает из matchobj имя первой группы и возвращает его"
        name = matchobj.group(1)
        vars = matchobj.group(3)
        if vars:
            return "(?P<{0}>{1})".format(name, vars)
        else:
            return "(?P<{0}>.*?)".format(name)
    
    def _convert(self, pretty):    
        """Преобразует pretty-look паттерн в вид питоновской
        регулярки"""   
        return re.sub("[{](.*?)([[](.*)[]])?[}]", self._block, pretty)
        
    def _addRule(self, pretty, block):
        """Преобразует пару pretty-pattern и 
        func в объект Rule"""
        pattern = self._format(self._convert(pretty))
        
        pattern += "$"
        print(pattern)
        rule = Rule(block, re.compile(pattern))
        self.rules.append(rule)
        
    def _format(self, url):
        if url == "/": return url
        if url.endswith("/"): return url[:-1]
        return url
               
    def _add_rules(self, dictRoutes):
        for pretty, block in dictRoutes.items():
            self._addRule(pretty, block)

