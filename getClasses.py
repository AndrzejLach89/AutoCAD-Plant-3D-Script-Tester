import os

class Log:
    def updateLog(content):
        content = "\n" + content
        with open('generationErrors.log', 'a') as file:
            file.write(content)
        


class Method:
    def __init__(self, input, path):
        self.ID = '???'
        self.status = True
        self.data = input
        self.path = path
        self.name = self.getName()
        if self.status:
            self.parameters = self.getParameters()
            self.methodBody = self.writeMethodBody()
        
    def getName(self):
        #print(argStart)
        nm = self.data[4:]
        argStart = nm.index('(')
        nm = nm[:argStart]
        argStart = self.data.index('(')
        self.data = self.data[argStart:]
        #print(self.data)
        #print(nm)
        if "__init__" in nm or ' ' in nm:
            self.status = False
            message = "Data error, skipping file:\n{}: NAME = {}'".format(self.path, nm)
            print('Writing error info to generationErrors.log')
            print(message)
            Log.updateLog(message)
        return nm
        
    def getParameters(self):
        endIndex = self.data.index(')')
        data = self.data[:endIndex]
        data = data.replace('(', '')
        #data = data.replace('**kw', '')
        data = data.replace(' ', '')
        parameters = []
        parametersRaw = data.split(',')
        for i in parametersRaw:
            #if i == 's':
            #    continue
            if i == '':
                continue
            #if i == '**kw':
            #    continue
            if 'ID=' in i:
                self.ID = i[3:]
                continue
            if '=' in i:
                eq = i.index('=')
                param = i[:eq]
            else:
                param = i
            parameters.append(param)
        return parameters
        
    def writeMethodBody(self):
        indent = '    '
        args = ''
        cnt = 0
        for i in self.parameters:
            args = args + i
            if cnt< len(self.parameters) - 1:
                args = args + ', '
            cnt += 1
        #header = "def {} ({}):\n".format(self.name, args)
        classComment = '#{}\n#{}\n'.format(self.ID, self.path)
        classHeader = classComment + 'class {}(PRIMITIVE):'.format(self.name)
        classBody = classHeader + '\n{}name="{}"\n{}ID=1\n'.format(indent, self.name, indent)
        initHeader = '{}def __init__(self, {}):'.format(indent, args)
        initBodyDef = indent + indent + 'self.{} = {}\n'
        initBody = initHeader + '\n'
        initBody = initBody + '{}{}self.ID = {}.name + " " + str({}.ID)\n'.format(indent, indent, self.name, self.name)
        initBody = initBody + '{}{}{}.ID += 1\n'.format(indent, indent, self.name)
        paramList = ''
        cnt = 0
        for i in self.parameters:
            if i == 's' or i == '**kw':
                cnt += 1
                continue
            paramList = paramList + i
            if cnt< len(self.parameters) - 2:
                paramList = paramList + ', '
            cnt += 1
        initBody = initBody + '{}{}ArgCheck.check(self.ID, ({}), "num")\n'.format(indent, indent, paramList)
        for i in self.parameters:
            if i == '**kw':
                continue
            initBody = initBody + initBodyDef.format(i, i)
        initBody = initBody + '{}{}self.describe()\n\n'.format(indent, indent)
        
        describeHeader = '{}def describe(self):\n'.format(indent)
        describeBody = '{}{}print("Creating " + self.ID + ":")'.format(indent, indent) + '\n'
        paramList = paramList.replace(' ', '')
        para = paramList.split(',')
        for i in para:#mList.replace(',', '').replace(' ', ''):
            if i == '' or i == ' ':
                continue
            line = '{}{}print("{}\t: " + str(self.{}))'.format(indent, indent, i, i) + '\n'
            describeBody = describeBody + line
        describeBody = describeHeader + describeBody + '\n\n'
        mainBody = classBody + initBody + describeBody
        #print(mainBody)
        return mainBody
        
        

class GetMethods:
    def __init__(self, path=None):
        if path != None:
            self.path = path
        else:
            self.path = os.path.split(os.path.abspath(__file__))[0]
        self.validNames = []
        self.files = self.getFiles(self.path)
        self.methodNames = self.readMethods()
        self.names = {}
        self.methods = self.createMethods()
        self.writeMethods()
            
    def getFiles(self, path):
        items = os.listdir(path)
        #print(items)
        dirs = []
        files = []
        for i in items:
            itemPath = os.path.join(path, i)
            if os.path.isfile(itemPath):
                if os.path.splitext(i)[1] == ".pyc_dis" or os.path.splitext(i)[1] == "pyc_dis":
                    files.append(itemPath)
            elif os.path.isdir(itemPath):
                dirs.append(itemPath)
        for i in dirs:
            dfiles = self.getFiles(i)
            files.extend(dfiles)
        return files
        
    def readMethods(self):
        names = []
        for i in self.files:
            with open(i, 'r') as file:
                content = file.read()
            contentSplitted = content.split('\n')
            for j in contentSplitted:
                if "def " in j:
                    names.append((j, i))
                    break
        return names
        
    def createMethods(self):
        methods = []
        for i in self.methodNames:
            newMethod = Method(i[0], i[1])
            if newMethod.name in self.validNames:
                print("Duplicate: skipping {}".format(newMethod.name))
                Log.updateLog(("Duplicate: skipping {}".format(newMethod.name)))
                continue
            else:
                if newMethod.status:
                    self.validNames.append(newMethod.name)
                    methods.append(newMethod)
        return methods
        
    def checkDuplicates(self):
        for i in self.methods:
            if i.name in self.names:
                print("DUPLICATE: {}".format(i.name))
            self.names.append(i.name)
        
    def writeMethods(self):
        content = 'from ArgCheck import *\nfrom Log import *\nfrom BasicObjects import *\n\n\n'
        for i in self.methods:
            content = content + i.methodBody + '\n'
        with open("extClasses.py", 'w') as file:
            file.write(content)
        
files = GetMethods()