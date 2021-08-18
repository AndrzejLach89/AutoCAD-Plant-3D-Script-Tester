import os
import traceback
import datetime
from TestResults import *
from PlantScriptTest import *
from Settings import *
from Utilities import *


class ScriptReader:
    def __init__(self, path):
        self.path = path
        self.addedLines = 2
        self.scriptName = ''
        TestResults.clearResults()
        self.script = self.readScript()
        self.prepareScript()
        self.executeScript()
    
    def readScript(self):
        try:
            with open(self.path, 'r') as file:
                data = file.read()
        except:
            data = ""
        return data
        
    def prepareScript(self):
        def getIndent(line):
            indent = 0
            for i in line:
                if i == ' ':
                    indent += 1
                elif i == '\t':
                    indent += 4
                else:
                    break
            return indent
        def checkLine(line):
            empty = ['', ' ', '\n', '\t']
            if len(line) == 0:
                return False
            if line == '':
                return False
            if line[0] == '\n':
                return False
            if not line[0] == ' ' or line[0] == '\t' or line[0] == '#' or '"""' in line or "'''" in line:
                return False
            notEmpty = False
            for i in line:
                if i not in empty:
                    notEmpty = True
            if notEmpty:
                return True
            else:
                return False
        '''def breakline(x='-', length=-1):
            if length < 0:
                length = Settings.LineLength
            if not isinstance(x, str):
                x = '-'
            if len(x) > 1:
                x = x[0]
            return ''.rjust(length, x)'''
        name = os.path.splitext(os.path.basename(self.path))[0]
        self.scriptName = name
        self.script = self.script.replace('@', '#@')
        self.script = self.script.replace('\t', '    ')
        
        dependencies = []
        script = "import PlantScriptTest\n"
        self.scriptSplitted = self.script.split('\n')
        function = False
        indent = ''
        cnt = 0
        for i in self.scriptSplitted:
            # place when function definition begins
            if not function and "def " in i:
                function = True
                addGlobals = True
                indent = ''
                try:
                    mc = 1
                    while not checkLine(self.scriptSplitted[cnt+mc]):
                        mc += 1
                    indentLength = getIndent(self.scriptSplitted[cnt+mc])
                except:
                    indentLength = 4
                indent = ''.rjust(indentLength, ' ')
                line = f'{i}\n'
            # imports outside the function definition
            elif not function and "import" in i:
                line = f'#{i}\n'
                if "from" not in i:
                    dependencies.append(i)
                addGlobals = False
            # lines before function definition
            elif not function:
                line = f'#{i}\n'
                addGlobals = False
            # lines inside and below the function definition
            else:
                line = f'{i}\n'
                addGlobals = False
            script = script + line
            # add imports inside function definition
            if addGlobals:
                script = script + self.addDependencies(dependencies, indent) + '\n'
            cnt += 1
        # add a line to invoke tested function
        self.script = f'{script}\n{name}(s)'
        if Settings.ShowScriptBody:
            print(BreakLine())
            print("SCRIPT BODY")
            print(BreakLine())
            print(self.script)
            print(BreakLine('='))
    
    def addDependencies(self, dependencies, indent):
        output = ''
        for i in dependencies:
            output = output + f"{indent}try:\n{indent}    {i}\n{indent}    print('{i}'.ljust(45, ' ') + ' - module imported')\n{indent}except:\n{indent}    print('{i}'.ljust(45, ' ') + ' - module could not be imported')\n"
            self.addedLines += 5
        return output
        
    def executeScript(self):
        print('Testing script: {}'.format(self.path))
        print(BreakLine('='))
        print('Checking activation parameters...')
        self.checkActivation()
        print('Executing script...')
        print(BreakLine('-'))
        try:
            exec(self.script)
            errorMessage = "NO EXECUTION ERRORS FOUND"
            self.updateMainLog(errorMessage)
        except Exception as e:
            errorMessage = self.prepareMessage(traceback.format_exc())
            self.updateLog(errorMessage)
            self.updateMainLog(errorMessage)
            TestResults.addExecution(errorMessage)
        Warnings.pushResults()
        TestResults.printResults()
        
    def prepareMessage(self, message, *args):
        def findNumber(line):
            cnt = 0
            number = ''
            started = False
            startIndex = None
            endIndex = None
            for i in line:
                try:
                    int(i)
                    if not started:
                        startIndex = cnt
                    started = True
                    number = number + i
                except:
                    if started:
                        endIndex = cnt
                        break
                cnt += 1
            if number == '':
                number = None
            return (number, startIndex, endIndex)
        def findLineInfo(messageLines):
            cnt = 0
            lineNumber = 0
            found = False
            for i in messageLines:
                if "File" in i and "line" in i and "<" in i:
                    found = True
                    lineNumber = cnt
                cnt += 1
            if not found:
                return None
            else:
                return lineNumber
        def updateLineNumber(line, data):
            number = str(int(data[0]))
            start = data[1]
            end = data[2]
            newLine = line[:start] + number + line[end:]
            return newLine
        def updateScriptName(line, name):
            try:
                start = line.index('<')
                end = line.index('>')+1
                newLine = line[:start] + name + line[end:]
            except:
                return line
            return newLine
        
        messageSplitted = message.split('\n')
        
        lineInfoNumber = findLineInfo(messageSplitted)
        if lineInfoNumber == None:
            return message
        info = findNumber(messageSplitted[lineInfoNumber])
        try:
            newLineNumber = int(info[0]) - self.addedLines
            if len(str(newLineNumber)) != len(str(info[0])):
                endIndex = info[2] + len(str(newLineNumber)) - len(str(info[0]))
            else:
                endIndex = info[2]
            lineInfoData = (newLineNumber, info[1], endIndex)
        except:
            lineInfoData = info
        if None in lineInfoData:
            return message
        messageSplitted[lineInfoNumber] = updateLineNumber(messageSplitted[lineInfoNumber], lineInfoData)
        messageSplitted[lineInfoNumber] = updateScriptName(messageSplitted[lineInfoNumber], self.scriptName)
        
        newLines = messageSplitted[lineInfoNumber:]
        msg = '\n'.join(newLines)
        if len(msg) > 1:
            msg = msg[:-1]
        return msg
        
    def updateLog(self, message):
        header = '{}\t{}'.format(self.scriptName, datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
        msg = '{}\n{}\n{}\n'.format(header, message, ''.rjust(80, '-'))
        if len(self.scriptName) > 0:
            filename = self.scriptName+'.log'
        else:
            filename = "unnamed.log"
        Log.writeMessage(filename, msg)
        
    def updateMainLog(self, message):
        header = '{}\t{}'.format(self.scriptName, datetime.datetime.now().strftime("%Y-%m-%d  %H:%M:%S"))
        msg = '{}\n{}\n{}\n'.format(header, message, ''.rjust(80, '-'))
        filename = 'tested scripts.log'
        Log.writeMessage(filename, msg)
        
    def checkActivation(self):
        def checkCategory(line):
            avaliableCategories = ['Support', 'Elbow', 'Coupling', 'Cross', 'Crossover', 'Lateral', 'Nipple', 'Reducer', 'Swage', 'Sleeve', 'Tee', 'Wye', 'BleedRing', 'BlindDisk', 'Cap', 'OrificePlate', 'Plug', 'SpacerDisk', 'SpectacleBlind', 'Strainer', 'Olet', 'ElbowSideOutlet', 'TeeSideOutlet', 'Flange', 'BlindFlange', 'Pipe', 'Valve', 'ValveBody', 'ValveActuator', 'Instrument']
            category = ''
            #@activate(Group="Tee", TooltipShort="Cable tray tee - vertical", TooltipLong="Cable tray tee - vertical",  LengthUnit="mm", Ports=3)
            line = line.split('(')[1]
            line = line.split(',')
            group = []
            for i in line:
                if "Group" in i:
                    group = i.split('=')
                    break
            if len(group) < 2:
                return False
            groupName = group[1]
            groupName = groupName.replace('"', '').replace("'", '').replace(' ', '')
            if groupName not in avaliableCategories:
                return groupName
            else:
                return False
        def checkEmptyLine(line):
            sym = ['', ' ', '\t', '\n']
            empty = True
            for i in line:
                if i not in sym:
                    empty = False
                    break
            return empty
        categoryError = False
        errors = False
        errorsLog = []
        parameters = []
        script = self.script.split('\n')
        inActivation = False
        activationLines = []
        for i in script:
            if not inActivation and '@activate' in i:
                categoryError = checkCategory(i)
                inActivation = True
            elif "@group" in i:
                continue
            elif inActivation and "@param" not in i and checkEmptyLine(i):
                break
            elif inActivation and "def(" in i:
                break
            if inActivation and "@param" in i:
                activationLines.append(i)
        cnt = 0
        while cnt < len(activationLines):
            line = activationLines[cnt].split('(')
            item = line[0]
            if 'activate' in item:
                pass
            elif 'group' in item:
                pass
            elif 'param'  in item:
                elements = line[1].split(',')
                parameters.append(elements[0].split('=')[0])
            cnt += 1
        
        definition = ''
        for i in script:
            if i[:3] == 'def':
                definition = i
                break
        if len(definition) == 0:
            print('Parameters not found')
            return
        defParams = definition.split('(')[1].split(',')
        cnt = 0
        while cnt < len(defParams):
            defParams[cnt] = defParams[cnt].replace(' ', '')
            defParams[cnt] = defParams[cnt].replace(')', '')
            defParams[cnt] = defParams[cnt].replace(':', '')
            try:
                defParams[cnt] = defParams[cnt].split('=')[0]
            except:
                pass
            cnt += 1
        
        ERRORS = False
        # check errors
        if categoryError != False:
            errorsLog.append(f'Unknown part category: {categoryError}!')
            ERRORS = True
        if defParams[0] != 's':
            errorsLog.append("Plant object reference (s) not found in function definition")
            ERRORS = True
        for i in defParams:
            if i == '**kw' or i=='ID' or i=='s':
                continue
            if i not in parameters:
                errorsLog.append("Parameter '{}' from function definition not found in activation section!".format(i))
                ERRORS = True
        for i in parameters:
            if i not in defParams:
                errorsLog.append("Parameter '{}' from activation section not found in function definition!".format(i))
                ERRORS = True
                
        if not ERRORS:
            errorMessage = "NO ACTIVATION ERRORS FOUND"
            self.updateMainLog(errorMessage)
        else:
            errorMessage = "ACTIVATION ERRORS FOUND"
            for i in errorsLog:
                TestResults.addActivation(i)
            self.updateMainLog(errorMessage)