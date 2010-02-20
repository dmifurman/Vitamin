from helpers.vitaparse.lexical import Spec, Tokenizer
import unittest
from helpers.vitaparse import ntype, Node, many, oneplus, future, exact, maby, \
    finish, skip, nvalue
from helpers.vitaparse import FatalParserError
from unittest import TestCase

class TestVitaparse(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tokenize(self, text):  
        specs = [
            Spec("space", "\s+"),
            Spec("newline", "\n"),
            Spec("int", "[0-9]+"),
            Spec(",", "[,]"),
            Spec("'", """['"]"""),
            Spec("{", "[{]"),
            Spec("}", "[}]"),
            Spec("(", "[(]"),
            Spec(")", "[)]"),
            Spec(".", "[.]"),
            Spec("text", "\w+"),
            Spec(":", "[:]")       
        ]
        useless = ("newline",
                   "space")
        tokenizer = Tokenizer(specs)
        return [t for t in list(tokenizer(text)) if not t.type in useless]
    
    def test_tokenize(self):
        self.text = "1,2,3,4,5"
        res = self.tokenize(self.text)
        self.assert_(len(res) == 9)
        
    def test_node_creation(self):
        node = ntype("int")
        self.assertTrue(isinstance(node, Node))
        
    def test_node_combine(self):
        node = ntype("int")
        self.assertTrue(isinstance(ntype("int"), Node))
        list(map(self.assertTrue,
            [isinstance(nvalue("smth"), Node),
             isinstance(node + node, Node),
             isinstance(node | node, Node),
             isinstance(many(node), Node),
             isinstance(oneplus(node), Node),
             isinstance(future(), Node),
             isinstance(node.join(node), Node),
             isinstance(maby(node), Node),
             isinstance(exact("smth"), Node),
             isinstance(finish(), Node),
             isinstance(skip(node), Node)]))
        
    def test_simple_parse_with_processing(self):
        
        def parse(tokens):
            integer = ntype("int") >> (lambda t: int(t.value))
            return integer.parse(tokens)[0]
        
        result = parse(self.tokenize("1"))
        self.assertEqual(result, 1)
        
    def test_many_sum_skip(self):
        
        def parse(tokens):
            integer = ntype("int") >> (lambda t: int(t.value))
            comma = skip(ntype(","))
            parser = many(integer + comma)
            return parser.parse(tokens)[0]
        
        result = parse(self.tokenize("1,2,3,4,"))
        self.assertEqual(result, (1, 2, 3, 4))
        
    def test_tuples(self):
        
        def parse(tokens):
            integer = ntype("int") >> (lambda t: int(t.value))
            parser = many(integer + integer)
            return parser.parse(tokens)[0]
        
        result = parse(self.tokenize("1 2 3 4"))
        self.assertEqual(result, ((1, 2), (3, 4)))
        
    def test_oneplus_with_tuples(self):
        
        def parse(tokens):
            integer = ntype("int") >> (lambda t: int(t.value))
            parser = oneplus(integer + integer)
            return parser.parse(tokens)[0]
        
        result = parse(self.tokenize("1 2 3 4"))
        self.assertEqual(result, ((1, 2), (3, 4)))
        
    def test_maby_and_smart_combine(self):
        
        def parse(tokens):
            integer = ntype("int") >> (lambda t: int(t.value))
            point = skip(ntype("."))
            parser = integer + maby(point + integer)       
            return parser.parse(tokens)[0]
        
        result = parse(self.tokenize("1.2"))
        self.assertEqual(result, (1, 2))
        result = parse(self.tokenize("1"))
        self.assertEqual(result, 1)
        
    def test_join(self):
        
        def parse(tokens):
            integer = ntype("int") >> (lambda t: int(t.value))
            comma = skip(ntype(","))
            parser = integer.join(comma)       
            return parser.parse(tokens)[0]
                
        result = parse(self.tokenize("1,2,3,4,5,6"))
        self.assertEqual(result, (1, 2, 3, 4, 5, 6))
        
    def test_exact(self):
        
        def parse(tokens):
            integer = ntype("int") >> (lambda t: int(t.value))
            three = exact("3") >> (lambda t: int(t.value))
            comma = skip(ntype(","))
            parser = integer + comma + three       
            return parser.parse(tokens)[0]
                
        result = parse(self.tokenize("1,3"))
        self.assertEqual(result, (1, 3))
        self.assertRaises(FatalParserError, parse, self.tokenize("1,5"))
        
    def test_finish(self):
        
        def parse(tokens):
            integer = ntype("int") >> (lambda t: int(t.value))
            comma = skip(ntype(","))
            parser = integer.join(comma) + finish()   
            return parser.parse(tokens)[0]
                
        result = parse(self.tokenize("1,2,3,4,5,6"))
        self.assertEqual(result, (1, 2, 3, 4, 5, 6))
        self.assertRaises(FatalParserError, parse, self.tokenize("1,2,3,4,5,6 7"))
        
    def test_strong_with_future(self):
        
        def parse(tokens):
            integer = ntype("int") >> (lambda t: int(t.value))
            comma = skip(ntype(","))
            obr = skip(ntype("{"))
            cbr = skip(ntype("}"))
            br = skip(ntype("'"))
            orbr = skip(ntype("("))
            crbr = skip(ntype(")")) 
            two = skip(ntype(":"))           
            word = ntype("text") >> (lambda t: t.value)
            string = br + word + br            
            dictionary = future()
            tuple = future()            
            elem = (integer | string | tuple | dictionary)
            tuple.define(orbr + elem.join(comma) + crbr)            
            dictionary.define((obr + (elem + two + elem).join(comma) + cbr >> dict))
            parser = dictionary | tuple
            return parser.parse(tokens)[0]
        
        result = parse(self.tokenize("(1,2, 'test', (1,'test2'))"))
        self.assertEqual(result, (1, 2, 'test', (1, 'test2')))
        
        result = parse(self.tokenize("{1:2}"))
        self.assertEqual(result, {1:2})
        
        result = parse(self.tokenize("{1:(1,'test')}"))
        self.assertEqual(result, {1:(1, 'test')})
        
        result = parse(self.tokenize("({1:(1,{1:2})})"))
        self.assertEqual(result, ({1:(1, {1:2})},))
        
