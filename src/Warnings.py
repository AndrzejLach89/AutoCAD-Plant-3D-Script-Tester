from TestResults import *

class Warnings:
    warnings = []
    def add(text):
        Warnings.warnings.append(text)
        
    def presentResults():
        if len(Warnings.warnings) < 1:
            print("NO WARNINGS FOUND")
            print(''.rjust(80, '-'))
            return
        print("WARNINGS:")
        for i in Warnings.warnings:
            print(i)
        print(''.rjust(80, '-'))
        
    def pushResults():
        TestResults.addWarning(Warnings.warnings)