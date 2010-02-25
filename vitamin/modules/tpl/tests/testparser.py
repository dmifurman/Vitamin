from unittest import TestCase
from vitamin.modules.tpl.lexical import TemplateAnalyzer
from vitamin.modules.tpl.chunks import TextChunk, ChainChunk, QualChunk, \
    LoopChunk, BlockChunk, ModChunk, ExtendChunk

    
class ParseTest(TestCase):
    
    def setUp(self):
        self.load = TemplateAnalyzer().load
    
    def test_text(self):        
        text = """text"""
        result = self.load(text)
        self.assertTrue(len(result) == 1)
        self.assertTrue(isinstance(result[0], TextChunk))
        
    def test_chain(self):        
        text = """[name > foo(arg1, arg2)]"""
        result = self.load(text)
        self.assertTrue(len(result) == 1)
        self.assertTrue(isinstance(result[0], ChainChunk))    
        
    def test_if(self):
        text = """{if name > 1} привет {else} пока {/if}"""
        result = self.load(text)
        self.assertTrue(len(result) == 1)
        self.assertTrue(isinstance(result[0], QualChunk))
        
    def test_for(self):
        text = """{for name in iter} пока {/for}"""
        result = self.load(text)
        self.assertTrue(len(result) == 1)
        self.assertTrue(isinstance(result[0], LoopChunk))
        
    def test_for_many_val(self):
        text = """{for name, value in iter} пока {/for}"""
        result = self.load(text)
        self.assertTrue(len(result) == 1)
        self.assertTrue(isinstance(result[0], LoopChunk))
        
    def test_block(self):
        text = """{block: name} привет {/block}"""
        result = self.load(text)
        self.assertTrue(len(result) == 1)
        self.assertTrue(isinstance(result[0], BlockChunk))
        
    def test_mod(self):
        text = """{crazy+}{crazy-}при{/crazy}вет{/crazy}"""
        result = self.load(text)
        self.assertTrue(len(result) == 1)
        self.assertTrue(isinstance(result[0], ModChunk))
        
    def test_comment(self):
        text = """{#'Комментарий'}"""
        result = self.load(text)
        self.assertTrue(len(result) == 0)
        
    def test_extend(self):
        text = """{#extend:test_extend_base method:implicit}"""
        result = self.load(text)
        self.assertTrue(len(result) == 1)
        self.assertTrue(isinstance(result[0], ExtendChunk))
        self.assertEqual(result[0].name, "test_extend_base")
        self.assertEqual(result[0].method.strip(), "implicit")
        
        text = """{#extend:test_extend_base}"""
        result = self.load(text)
        self.assertTrue(len(result) == 1)
        self.assertTrue(isinstance(result[0], ExtendChunk))
        self.assertEqual(result[0].name, "test_extend_base")
        self.assertEqual(result[0].method.strip(), "strict")
