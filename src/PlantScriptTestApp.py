# This tool was created for debugging Plant 3D part scripts during developement. It makes it possible to check for script errors without
# running Plant 3D, registering scripts and restarting it over and over again.
# Comment all the imports in your script file, then import * from this file to your script and invoke script function at the end of the
# script to check for errors. If no problems were found, continue with checking your script in Plant 3D.
# Author: Andrzej Lach
from PlantScriptTest import *
import tkinter as tk
from tkinter import filedialog as tkf
import os
import traceback
import datetime


class ScriptReader:
    def __init__(self, path):
        self.path = path
        self.scriptName = ''
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
        name = os.path.splitext(os.path.basename(self.path))[0]
        self.scriptName = name
        self.script = self.script.replace('@', '#@')
        self.script = self.script.replace("import ", "#import ")
        self.script = self.script.replace("from ", "#from ")
        
        script = "import PlantScriptTest\n"
        self.scriptSplitted = self.script.split('\n')
        function = False
        for i in self.scriptSplitted:
            if not function and "def " in i:
                function = True
            if not function:
                line = '#' + i + '\n'
            else:
                line = i + '\n'
            script = script + line
        self.script = script + '\n' + name + "(s)"
        
        
        #self.script = "import PlantScriptTest\n" + self.script + "\n" + name + "(s)"
        
    def executeScript(self):
        #exec(self.script)
        print('Testing script: {}'.format(self.path))
        print(''.rjust(80, '-'))
        try:
            exec(self.script)
            print('\n' + ''.rjust(80, '-'))
            errorMessage = "NO ERRORS FOUND"
            print(errorMessage)
            self.updateMainLog(errorMessage)
        except Exception as e:
            #exc_type, exc_obj, exc_tb = sys.exc_info()
            #fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
            #print(exc_type, fname, exc_tb.tb_lineno)
            #print(e)
            print('\n' + ''.rjust(80, '-'))
            print("ERROR FOUND\n")
            errorMessage = self.prepareMessage(traceback.format_exc())
            print(errorMessage)
            self.updateLog(errorMessage)
            self.updateMainLog(errorMessage)
        print(''.rjust(80, '-'))
        
    def prepareMessage(self, message):
        def findNumber(line):
            cnt = 0
            number = ''
            started = False
            #closed = False
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
                if "File" in i and "line" in i:
                    found = True
                    lineNumber = cnt
                cnt += 1
            if not found:
                return None
            else:
                return lineNumber
        def updateLineNumber(line, data):
            number = str(int(data[0]) - 1)
            start = data[1]
            end = data[2]
            newLine = line[:start] + number + line[end:]
            return newLine
        def updateScriptName(line, name):
            start = line.index('<')
            end = line.index('>')+1
            newLine = line[:start] + name + line[end:]
            return newLine
        
        messageSplitted = message.split('\n')
        
        lineInfoNumber = findLineInfo(messageSplitted)
        if lineInfoNumber == None:
            return message
        lineInfoData = findNumber(messageSplitted[lineInfoNumber])
        if None in lineInfoData:
            return message
        messageSplitted[lineInfoNumber] = updateLineNumber(messageSplitted[lineInfoNumber], lineInfoData)
        messageSplitted[lineInfoNumber] = updateScriptName(messageSplitted[lineInfoNumber], self.scriptName)
        
        newLines = messageSplitted[lineInfoNumber:]
        msg = '\n'.join(newLines)
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
    
    
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("PlantScriptTest App")
        self.path = tk.StringVar()
        self.mainFrame = tk.Frame(self.root, bg="black")
        self.mainFrame.pack()
        self.pathFrame = tk.Frame(self.mainFrame, bg="black")
        self.pathFrame.pack()
        self.pathLabel = tk.Label(self.pathFrame, textvariable=self.path, width=100, fg="green2", bg="black")
        self.pathLabel.pack(side='left', fill='x')
        self.pathButton = tk.Button(self.pathFrame, text="Browse", command=self.getPath, bg="green", fg="white")
        self.pathButton.pack(side="right")
        self.subFrame = tk.Frame(self.mainFrame)
        self.subFrame.pack(fill='x')
        self.clearButton = tk.Button(self.subFrame, text="CLEAR CONSOLE", command=self.clearConsole, state="disabled", bg="green", fg="white")
        self.clearButton.pack(fill='x')
        #self.reloadButton = tk.Button(self.subFrame, text="RELOAD", command=self.reloadScript, state="disabled", bg="green", fg="white")
        #self.reloadButton.pack(side="right", fill='x')
        self.runButton = tk.Button(self.mainFrame, text="TEST SCRIPT", command=self.runTest, state="disabled", bg="green", fg="white")
        self.runButton.pack(fill='x')
        self.root.mainloop()
    
    def clearConsole(self, *args):
        os.system('cls')
    
    def getPath(self):
        path = tkf.askopenfilenames(filetypes=[('Python file', 'py'), ('Python file', 'pyc_dis')])
        if len(path) < 1:
            return
        elif path == "" or path == " " or path == None:
            return
        else:
            if len(path) == 1:
                self.path.set(path[0])
                self.multi = False
            else:
                self.path.set("MULTIPLE FILES")
                self.multi = True
            self.paths = []
            for i in path:
                self.paths.append(i)
        #print(self.paths)
        self.runButton.config(state="normal")
        self.clearButton.config(state="normal")
        #self.reloadButton.config(state="normal")
        
    def getPath_old(self):
        path = tkf.askopenfile(filetypes=[('Python file', 'py'), ('Python file', 'pyc_dis')])
        if path == "" or path == " " or path == None:
            return
        else:
            self.path.set(path.name)
        self.runButton.config(state="normal")
    
    def runTest(self):
        if len(self.paths) < 1:
            return
        elif len(self.paths) == 1:
            self.runSingleTest()
        elif len(self.paths) > 1:
            self.runMultipleTests()
        
    def runSingleTest(self):
        if self.path.get() == "" or self.path.get() == " " or self.path.get() == None:
            return
        ScriptReader(self.path.get())
        
    def runMultipleTests(self):
        for i in self.paths:
            self.path.set(i)
            self.runSingleTest()
        
root = tk.Tk()
app = App(root)