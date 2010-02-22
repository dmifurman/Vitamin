
#$Rev: 117 $     
#$Author: fnight $  
#$Date: 2009-08-20 18:16:18 +0400 (Чт, 20 авг 2009) $ 

#This file is part of Vitamin Project

import random as _random

def upper(string):
    return string.upper()
        
def crazy(string):    
    lst = list(string)
    _random.shuffle(lst)
    return "".join(lst)

def pretty(string, lst=[]):    
    lst = string.splitlines()
    lst = [x for x in lst if x.strip() != ""]
    return "\n".join(lst)

