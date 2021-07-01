class ArgCheck:
    def check(ID, arguments, types):
        argType = type(arguments)
        typeType = type(types)
        if (argType == list or argType == tuple):
            status = ArgCheck.checkCollection(ID, arguments, types)
        else:
            status = ArgCheck.checkItem(ID, arguments, types)
        return status
        
    def checkItem(ID, arg, typ):
        #if type(argument) == type:
        status = True
        if typ == "num":
            if (type(arg) != int and type(arg) != float):
                status = False
                typ = "int/float"
        elif issubclass(type(arg), typ):
            status = True
        else:
            status = False
        if not status:
            msg = "{}: Argument of type {}, required {}!".format(ID, type(arg), typ)
            Log.updateLog(msg)
        return status
        
    def checkCollection(ID, arguments, types):
        status = True
        num = (int, float)
        typeType = type(types)
        argType = type(arguments)
        if (typeType != list and typeType != tuple) and (argType == list or argType == tuple):
            t1 = []
            while len(t1) < len(arguments):
                t1.append(types)
            types = tuple(t1)
        if ((argType == list or argType == tuple) and (typeType == list or typeType == tuple)):
            if len(arguments) != len(types):
                msg = "{}: Wrong arguments number! {} arguments given, {} required.".format(ID, len(arguments), len(types))
                Log.updateLog(msg)
                print(msg)
                status = False
                return status
        cnt = 0
        for a, t in zip(arguments, types):
            if type(a) == tuple or type(a) == list:
                ArgCheck.checkCollection(ID, a, t)
            elif t == "num":
                if type(a) != int and type(a) != float:
                    msg = "{}: Argument at position {} of type {}, required {}!".format(ID, cnt, type(a), "int/float")
                    Log.updateLog(msg)
                    print(msg)
                    status = False
            #elif type(a) != t:
            elif type(a) != t:#issubclass(a, t):
                msg = "{}: Argument at position {} of type {}, required {}!".format(ID, cnt, type(a), t)
                Log.updateLog(msg)
                print(msg)
                status = False
            cnt += 1
        return status