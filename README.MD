# PlantScriptTest  

## About  
This tool was created for debugging Plant 3D part scripts during developement. It makes it possible to check for script errors without  
running Plant 3D, registering scripts and restarting it over and over again.  

This script covers all (as far as I know) the primitives and their methods. You can add custom classes to "extClasses.py" file or use  
"getClasses.py" on decompiled Plant 3D scripts to generate "extClasses.py" containing additional classes to be handled during script  
testing.  

## Manual  
### Using PlantScriptTest module  
Comment all the imports and parameter section in your script file, then import * from this file to your script and invoke script function    
at the end of the script to check for errors. If no problems were found, continue with checking your script in Plant 3D.  
Script checks parameters type, if type errors are found, they are logged the console and to "scriptLog.txt" file.  
### Additional classes  
Additional classes can be put in "extClasses.py" file. You can write your own classes, or use getClasses.py script, placed in a folder
with decompiled Plant 3D standard scripts. to generate a file automatically. It is not recommended to generate a file containing all  
Plant 3D standard scripts, because the size of the file will be huge, and trying to use it in tests will probably raise Memory Error.  
getClasses.py will scan the directory it is placed in and all the subdirectories for decompiled script files (with .pyc_dis extension)  
and generate extClasses.py file, which has to be put in PlantScriptTest program directory.
Plant 3D standard scripts can be decompiled from bytecode with EasyPythonDecompiler.

### Using PlantScriptTestApp app  
Just run the app, find the script file and run test.  

## License  
This script is released under MIT License.  

## Author  
Andrzej Lach