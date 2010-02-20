class ParserException(Exception): pass

class ParserError(ParserException):
    
    def __init__(self, state, tokens):
        try:
            self.token = tokens[state.index]
        except:
            self.token = tokens[state.index - 1]
        self.state = state
        
class FatalParserError(Exception):pass

class NoSpecError(ParserException):
    
    def __init__(self, line, part):
        self.line = line
        self.pos = part

    def __str__(self):
        return "\n" + repr("Нет спецификации для распознавания паттерна '{1}' в строке {0}".format(self.line, self.pos))

class FunctionError(ParserException):
    
    def __init__(self, msg):
        self.msg = msg
        
    def __str__(self):
        return repr("Can not process\n" + self.msg)
