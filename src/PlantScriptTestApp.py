# This tool was created for debugging Plant 3D part scripts during developement. It makes it possible to check for script errors without
# running Plant 3D, registering scripts and restarting it over and over again.
# Comment all the imports in your script file, then import * from this file to your script and invoke script function at the end of the
# script to check for errors. If no problems were found, continue with checking your script in Plant 3D.
# Author: Andrzej Lach
from PlantScriptTest import *
from ScriptReader import *
from Settings import *
import tkinter as tk
from tkinter import filedialog as tkf
import os
    
'''class Console:
    text = tk.StringVar()
    
    def clear():
        Console.text.set('')
        
    def add(text):
        if type(text) == string:
            Console.text.set("{}\n{}".format(Console.text.get(), text))
        else:
            try:
                for i in text:
                    Console.text.set("{}\n{}".format(Console.text.get(), i))
            except:
                return'''

class App:
    def __init__(self, root):
        self.clearConsole()
        self.root = root
        self.root.title("PlantScriptTest App")
        self.path = tk.StringVar()
        self.showScriptVar = tk.IntVar()
        self.updateVar()
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
        #self.clearButton = tk.Button(self.subFrame
        self.runButton = tk.Button(self.mainFrame, text="TEST SCRIPT", command=self.runTest, state="disabled", bg="green", fg="white")
        self.runButton.pack(fill='x')
        #self.consoleFrame = tk.Frame(self.root, height=600)
        #self.consoleFrame.pack(fill='both', expand=True)
        #os.system('xterm -into %d -geometry 40x20 -sb &' % self.consoleFrame.winfo_id())
        
        self.root.resizable(False, False)
        self.root.mainloop()
    
    def updateVar(self):
        if Settings.ShowScriptBody:
            self.showScriptVar.set(1)
        else:
            self.showScriptVar.set(0)
            
    def updateSettings(self):
        if self.showScriptVar.get() == 1:
            Settings.ShowScriptBody = True
        else:
            Settings.ShowScriptBody = False
    
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
    
    def runTest(self):
        if len(self.paths) < 1:
            return
        elif len(self.paths) == 1:
            self.runSingleTest()
        elif len(self.paths) > 1:
            self.runMultipleTests()
        self.resetID()
        
    def runSingleTest(self):
        if self.path.get() == "" or self.path.get() == " " or self.path.get() == None:
            return
        if os.path.exists(self.path.get()):
            ScriptReader(self.path.get())
        
    def runMultipleTests(self):
        for i in self.paths:
            self.path.set(i)
            self.runSingleTest()
            
    def resetID(self):
        classes = [PLANTOBJECT,
            MODIFIED_OBJECT,
            CYLINDER,
            TORUS,
            ARC3D,
            ARC3D2,
            ARC3DS,
            BOX,
            CONE,
            ELLIPSOIDHEAD,
            ELLIPSOIDHEAD2,
            ELLIPSOIDSEGMENT,
            HALFSPHERE,
            PYRAMID,
            ROUNDRECT,
            SPHERESEGMENT,
            TORISPHERICHEAD,
            TORISPHERICHEAD2,
            TORISPHERICHEADH]
        for i in classes:
            i.ID = 1
            
root = tk.Tk()
app = App(root)