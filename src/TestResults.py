class TestResults:
    _activation = []
    _execution = []
    _warnings = []
    def addActivation(text):
        if isinstance(text, str):
            TestResults._activation.append(text)
        else:
            try:
                for i in text:
                    TestResults._activation.append(i)
            except:
                return
                
    def addExecution(text):
        if isinstance(text, str):
            TestResults._execution.append(text)
        else:
            try:
                for i in text:
                    TestResults._execution.append(i)
            except:
                return
                
    def addWarning(text):
        if isinstance(text, str):
            TestResults._warnings.append(text)
        else:
            try:
                for i in text:
                    TestResults._warnings.append(i)
            except:
                return
                
    def prepareResults():
        def breakline(x='-', length=80):
            if not isinstance(x, str):
                x = '-'
            if len(x) > 1:
                x = x[0]
            return ''.rjust(length, x)
        results = []
        results.append(breakline('='))
        if len(TestResults._activation) < 1:
            results.append("NO ACTIVATION ERRORS FOUND!")
        else:
            results.append("ACTIVATION ERRORS FOUND!")
            for i in TestResults._activation:
                results.append(i)
        results.append(breakline())
        if len(TestResults._execution) < 1:
            results.append("NO EXECUTION ERRORS FOUND!")
        else:
            results.append("EXECUTION ERRORS FOUND!")
            for i in TestResults._execution:
                results.append(i)
        results.append(breakline())
        if len(TestResults._warnings) < 1:
            results.append("NO WARNINGS FOUND!")
        else:
            results.append("WARNINGS FOUND!")
            for i in TestResults._warnings:
                results.append(i)
        results.append(breakline('='))
        return results
        
    def printResults():
        results = TestResults.prepareResults()
        for i in results:
            print(i)