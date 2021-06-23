# This tool was created for debugging Plant 3D part scripts during developement. It makes it possible to check for script errors without
# running Plant 3D, registering scripts and restarting it over and over again.
# Comment all the imports in your script file, then import * from this file to your script and invoke script function at the end of the
# script to check for errors. If no problems were found, continue with checking your script in Plant 3D.
# Author: Andrzej Lach
from PlantScriptTest import *
import tkinter as tk
from tkinter import filedialog as tkf
import os

class ScriptReader:
    def __init__(self, path):
        self.path = path
        self.script = self.readScript()
    
    def readScript(self):
        try:
            with open(self.path, 'r') as file:
                data = file.read()
        except:
            data = ""
        return data
        
    def prepareScript(self):
        name = os.path.splitext(os.path.basename(self.path))[0]
        self.script = self.script.replace('@', '#@')
        self.script = self.script.replace("import ", "#import ")
        self.script = self.script.replace("from ", "#from ")
        self.script = "import PlantScriptTest\n" + self.script + "\n" + name + "(s)"
        
    def executeScript(self):
        exec(self.script)
        
class UI:
    def __init__(self, root):
        self.root = root
        self.path = tk.StringVar()
        self.pathFrame = tk.Frame(self.root)
        self.pathFrame.pack()
        self.pathLabel = tk.Label(self.pathFrame, textvariable=self.path)
        self.pathLabel.pack(side='left', fill='x')
        self.pathButton = tk.Button(self.pathFrame, text="Browse", command=self.getPath)
        self.pathButton.pack(side="right")
        self.runButton = tk.Button(self.root, text="Run test", command=self.runTest)
        self.runButton.pack()
        self.root.mainloop()
    def getPath(self):
        path = tkf.askopenfile()
        print(path.name)
        if path == "" or path == " ":
            return
        else:
            self.path.set(path.name)
    def runTest(self):
        if self.path.get() == "" or self.path.get() == " " or self.path.get() == None:
            return
        test = ScriptReader(self.path.get())
        test.prepareScript()
        test.executeScript()
        
root = tk.Tk()
app = UI(root)