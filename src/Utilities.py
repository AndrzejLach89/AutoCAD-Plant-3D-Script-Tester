from Settings import *

class BreakLine:
    def __init__(self, x='-', length=-1):
        if not isinstance(length, int):
            length = Settings.LineLength
        elif length < 0:
            length = Settings.LineLength
        if not isinstance(x, str):
            x = '-'
        if len(x) > 1:
            x = x[0]
        self.content = ''.rjust(length, x)
        
    def __str__(self):
        return self.content