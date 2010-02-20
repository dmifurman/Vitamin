from vitamin.modules.tpl.lexical import TemplateAnalyzer
from vitamin.modules.tpl.context import Context, Aggregator

#$Rev: 122 $     
#$Author: fnight $  
#$Date: 2009-08-28 16:12:56 +0400 (Пт, 28 авг 2009) $ 

#This file is part of Vitamin Project

_analyse = TemplateAnalyzer().load

TEMPLATE_INFO_STRING = \
"""
    '{0}' template info:
        root.chunks: {1};
        total.chunks: {2}; 
"""

class TemplateInfo():
    
    def __init__(self,
        name,
        root_chunks=0,
        total_chunks=0):
    
        self.name = name
        self.root_chunks = root_chunks
        self.total_chunks = total_chunks
        
    def __str__(self):
        return TEMPLATE_INFO_STRING.format(self.name,
                    self.root_chunks,
                    self.total_chunks)
  
class Template():

    def __init__(self, text="", name="default.template.name"):
        
        self.name = name
        self.chunks = []
        self.text = text
        if text: 
            self.chunks = _analyse(text)           

    def render(self, context=None):
        
        aggr = Aggregator()
        [x.render(context, aggr) for x in self.chunks]
        return aggr.join()
    
    def info(self):
        
        root_chunks = len(self.chunks)
        total_chunks = root_chunks
        
        def count_chunks(chunk):
            nonlocal total_chunks
            total_chunks += len(chunk.children)
            (count_chunks(x) for x in chunk.children)
            
        for chunk in self.chunks:
            count_chunks(chunk)
            
        return TemplateInfo(self.name, root_chunks, total_chunks)
                        
                
                
            

