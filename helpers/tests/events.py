from unittest import TestCase
from helpers.events import Event

class EvenstTest(TestCase):
    
    def test_procession(self):
        t = False
        def change():
            nonlocal t
            t = True
        a = Event()
        a += change
        a()
        self.assertTrue(t)
        
    def test_clear_and_len(self):
        a = Event()
        a += print
        self.assertEqual(len(a), 1)
        a.clear()
        self.assertEqual(len(a), 0)
