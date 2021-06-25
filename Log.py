class Log:
    argError = 0
    def updateLog(message):
        if Log.argError == 0:
            Log.argError += 1
            Log.createLog(message)
            return
        Log.argError += 1
        #if True:
        try:
            with open("scriptLog.txt", 'r') as file:
                content = file.read()
            lines = content.split("\n")
            lines[0] = "Argument errors: {}".format(Log.argError)
            lines.append(message)
            #newContent = "\n".join(lines)
            newContent = ""
            for i in lines:
                newContent = newContent + i + "\n"
            with open("scriptLog.txt", 'w') as file:
                file.write(newContent)
        #else:
        except:
                content = Log.createLog(message)
        
    def createLog(message):
        msg = "Argument errors: {}\nDetails:\n{}\n".format(Log.argError, message)
        with open("scriptLog.txt", 'w') as file:
            file.write(msg)