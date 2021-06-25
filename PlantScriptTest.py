from Log import *
from ArgCheck import *
try:
    from extClasses import *
except:
    print("extClasses.py: file could not be loaded")
from BasicObjects import *


# main plant object, use it as the first argument in the script
s = PLANTOBJECT("test_object")