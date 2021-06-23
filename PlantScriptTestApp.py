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
        self.script = self.script.replace('@', '#@')
        self.script = self.script.replace("import ", "#import ")
        self.script = self.script.replace("from ", "#from ")
        self.script = "import PlantScriptTest\n" + self.script + "\n" + name + "(s)"
        
    def executeScript(self):
        exec(self.script)
    
    
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
        self.runButton = tk.Button(self.mainFrame, text="TEST SCRIPT", command=self.runTest, state="disabled", bg="green", fg="white")
        self.runButton.pack(fill='x')
        self.root.mainloop()
    
    def getPath(self):
        path = tkf.askopenfile()
        if path == "" or path == " ":
            return
        else:
            self.path.set(path.name)
        self.runButton.config(state="normal")
    
    def runTest(self):
        if self.path.get() == "" or self.path.get() == " " or self.path.get() == None:
            return
        test = ScriptReader(self.path.get())
        
root = tk.Tk()
app = App(root)