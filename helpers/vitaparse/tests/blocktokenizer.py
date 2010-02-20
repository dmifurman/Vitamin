from unittest import TestCase
from helpers.vitaparse.lexical import BlockSpec, BlockTokenizer, Spec

class TestTokenizer(TestCase):
    
    def test_tokenize(self):
        
        tokens = [
            Spec("text", "\w+")
        ]
        
        blocks = [
            BlockSpec("obr", "{{", "}}", tokens)
        ]
        
        tokenizer = BlockTokenizer(blocks, "text")
        a = tokenizer("{{block}}{{end}}")
        self.assertTrue(len(a) == 7)
