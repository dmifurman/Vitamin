from unittest import TestCase
from vitamin.modules.tpl.lexical import TemplateAnalyzer
from vitamin.modules.tpl.template import Template
from vitamin.modules.tpl.context import Context

    
class RenderTest(TestCase):
    
    def setUp(self):
        self.load = TemplateAnalyzer().load
    
    def test_text(self):        
        text = """text me [name > upper()]"""
        result = Template(text)
        a = result.render(Context(name="Avatar"))
        print(a)
        
#    def test_chain(self):        
#        text = """[name > foo(arg1, arg2)]"""
#        result = self.load(text)
#        self.assertTrue(len(result) == 1)
#        self.assertTrue(isinstance(result[0], ChainChunk))    
#        
#    def test_if(self):
#        text = """{if name > 1} привет {else} пока {/if}"""
#        result = self.load(text)
#        self.assertTrue(len(result) == 1)
#        self.assertTrue(isinstance(result[0], QualChunk))
#        
#    def test_for(self):
#        text = """{for name in iter} пока {/for}"""
#        result = self.load(text)
#        self.assertTrue(len(result) == 1)
#        self.assertTrue(isinstance(result[0], LoopChunk))
#        
#    def test_block(self):
#        text = """{block: name} привет {/block}"""
#        result = self.load(text)
#        self.assertTrue(len(result) == 1)
#        self.assertTrue(isinstance(result[0], BlockChunk))
#        
#    def test_mod(self):
#        text = """{crazy+}{crazy-}при{/crazy}вет{/crazy}"""
#        result = self.load(text)
#        self.assertTrue(len(result) == 1)
#        self.assertTrue(isinstance(result[0], ModChunk))
#        
#    def test_comment(self):
#        text = """{#'Комментарий'}"""
#        result = self.load(text)
#        self.assertTrue(len(result) == 0)
#        
#    def test_extend(self):
#        text = """{#extend:base method:implicit}"""
#        result = self.load(text)
#        self.assertTrue(len(result) == 1)
#        self.assertTrue(isinstance(result[0], ExtendChunk))
