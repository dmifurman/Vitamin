from unittest import TestCase
from vitamin.modules.tpl.lexical import TemplateAnalyzer
from vitamin.modules.tpl.template import Template
from vitamin.modules.tpl.context import Context

    
class RenderTest(TestCase):
    
    def setUp(self):
        self.load = TemplateAnalyzer().load
    
    def test_chain(self):       
        text = """text me [name > lower()] [name > upper()] [name]"""
        template = Template(text)
        
        a = template.render(Context(name="Avatar"))
        self.assertEqual(a, "text me avatar AVATAR Avatar")
         
    def test_if(self):       
        text = """{if angry < 5}привет{else}пока{/if}"""
        template = Template(text)
        
        a = template.render(Context(angry=10))
        self.assertEqual(a, "пока")
        
        a = template.render(Context(angry=3))
        self.assertEqual(a, "привет")
        
    def test_for(self):
        text = """{for value in range(10)}[value] {/for}"""
        template = Template(text)
        
        a = template.render(Context(range=range))
        self.assertEqual(list(map(int, a.split())), list(range(10)))
        
    def test_for_many_val(self):
        text = """{for var1, var2 in test}[var1]+[var2] {/for}"""
        template = Template(text)
        
        a = template.render(Context(test=((1, 2), (2, 3))))
        self.assertEqual(a.strip(), "1+2 2+3")
        
#    def test_for_iter(self):
#        text = """{for value in names}[value] {/for}"""
#        template = Template(text)
#        
#        a = template.render(Context(names=("Стас", "Вася")))
#        print(a)
        
    def test_block(self):
        text = """{block: name}привет{/block}"""
        template = Template(text)
        a = template.render()
        self.assertEqual(a, "привет")

    def test_mod(self):
        text = """
        {crazy+}перемешанный{crazy-} нормальный {upper+}большой_нормальный{/upper} {/crazy}перемешанный{/crazy}"""
        template = Template(text)
        a = template.render()
        arr = a.split()
        self.assertNotEqual(arr[0], "перемешанный")
        self.assertEqual(arr[1], "нормальный")
        self.assertEqual(arr[2], "большой_нормальный".upper())
        self.assertNotEqual(arr[3], "перемешанный")
     
    def test_comment(self):
        text = """{#'Комментарий'}"""
        template = Template(text)
        a = template.render()
        self.assertEquals(a, "")
#        
#    def test_extend(self):
#        text = """{#extend:base method:implicit}"""
#        result = self.load(text)
#        self.assertTrue(len(result) == 1)
#        self.assertTrue(isinstance(result[0], ExtendChunk))
