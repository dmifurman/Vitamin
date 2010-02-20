
#$Rev: 114 $     
#$Author: fnight $  
#$Date: 2009-08-16 18:32:27 +0400 (Вс, 16 авг 2009) $ 

#This file is part of Vitamin Project

def _arguments(*types):    
    def custom(func):        
        def function(*args):
            for index in range(len(args)):
                if types[index] != None and not type(args[index]) is types[index]:
                    return "Wrong argunent types"
            return func(*args)
        return function
    return custom

@_arguments(str)
def upper(arg):
    return arg.upper()

@_arguments(str)
def lower(arg):
    return arg.lower()

@_arguments(str, None)
def format(string, arg):
    return string.format(arg)

nulline = "\n"
