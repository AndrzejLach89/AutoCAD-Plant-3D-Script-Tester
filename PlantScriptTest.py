# This tool was created for debugging Plant 3D part scripts during developement. It makes it possible to check for script errors without
# running Plant 3D, registering scripts and restarting it over and over again.
# Comment all the imports in your script file, then import * from this file to your script and invoke script function at the end of the
# script to check for errors. If no problems were found, continue with checking your script in Plant 3D.
# Author: Andrzej Lach

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


class mTransform:
    def transform(*args):
        print("Creating transformation:", *args)
        

class PLANTOBJECT:
    ID = 0
    name = "MAIN OBJECT"
    def __init__(self, name):
        self.name = name
        self.ID = "{} {}".format(PLANTOBJECT.name, PLANTOBJECT.ID)
        
    def setPoint(self, position, direction):
        ArgCheck.check(self.ID, (position, direction), ("num", "num"))
        print("  >{}: Adding point at {}, direction: {}".format(self.ID, position, direction))
        return self
        
    def numberOfPoints(self, *args):
        print("  >{}: Obtaining number of points...".format(self.ID))
        return self
        
    def directionAt(self, *args):
        print("  >{}: Obtaining direction...".format(self.ID))
        return self
        
    def pointAt(self, *args):
        print("  >{}: Obtaining position of connection point...".format(self.ID))
        return self
        
    def setLinearDimension(name, vector1, vector2):
        ArgCheck.check(self.ID, (name, vector1, vector2), (str, "num", "num"))
        print(">>" +self.ID +": Adding linear dimension: ", *args)
        print(">>{}: Adding linear dimension at {}, {}".format(self.ID, vector1, vector2))
        return self
        
        
class PRIMITIVE:
    def translate(self, x):
        ArgCheck.check(self.ID, x, "num")
        print("  >" + self.ID + " translation: ", x[0], x[1], x[2])
        return self
        
    def rotateX(self, x):
        ArgCheck.check(self.ID, x, "num")
        print("  >" + self.ID + " rotation by X:", x)
        return self
        
    def rotateY(self, x):
        ArgCheck.check(self.ID, x, "num")
        print("  >" + self.ID + " rotation by Y:", x)
        return self
        
    def rotateZ(self, x):
        ArgCheck.check(self.ID, x, "num")
        print("  >" + self.ID + " rotation by Z:", x)
        return self
        
    def erase(self):
        print("  >" + self.ID + " was erased")
        return self
        
    def uniteWith(self, object):
        ArgCheck.check(self.ID, object, PRIMITIVE)
        newObject = MODIFIED_OBJECT()
        print("  >" + self.ID + " was united with " + object.ID)
        print("  >" + newObject.ID + " was created")
        return newObject
        
    def subtractFrom(self, object):
        ArgCheck.check(self.ID, object, PRIMITIVE)
        newObject = MODIFIED_OBJECT()
        print("  >" + object.ID + " was subtracted from " + self.ID)
        print("  >" + newObject.ID + " was created")
        return newObject
        
    def intersectWith(self, object):
        ArgCheck.check(self.ID, object, PRIMITIVE)
        newObject = MODIFIED_OBJECT()
        print("  >" + object.ID + " intersecting with " + self.ID)
        print("  >" + newObject.ID + " was created")
        return newObject
        
    def parameters(self):
        print("  >Obtaining " + self.ID + "parameters...")
        return self
        
    def transformationMatrix(self):
        print("  >Obtaining " + self.ID + "transformation matrix...")
        return self
        
    #def numberOfPoints(self, *args):
    #    print("  >Obtaining " + self.ID + "number of points...")
    #    return self

    #def directionAt(self, *args):
    #    print("  >Obtaining " + self.ID + "direction at connection point...")
    #    return self
        
    #def pointAt(self, *args):
    #    print("  >Obtaining " + self.ID + "position of connection point...")
    #    return self
        
    #def setPoint(self, *args):
    #    print("  >Appending connection point to " + self.ID + "...")
    #    return self
        
    def setTransformationMatrix(self, *args):
        print("  >Setting " + self.ID + "transformation matrix...")
        return self


class MODIFIED_OBJECT(PRIMITIVE):
    name = "MODIFIED_OBJECT"
    ID = 0
    def __init__(self, *args):
        self.ID = "{} {}".format(MODIFIED_OBJECT.name, MODIFIED_OBJECT.ID)
        MODIFIED_OBJECT.ID += 1
        
        
class CYLINDER(PRIMITIVE):
    name = "CYLINDER"
    ID = 0
    def __init__(self, s, *, R, H, O):
        self.ID = "{} {}".format(CYLINDER.name, CYLINDER.ID)
        CYLINDER.ID += 1
        ArgCheck.check(self.ID, (R, H, O), "num")
        self.s = s
        self.R = R
        self.H = H
        self.O = O
        self.describe()
        
    def describe(self):
        print("Creating " + self.ID + ":")
        print("\t" + "Radius: " + str(self.R))
        print("\t" + "Height: " + str(self.H))
        print("\t" + "Inner r:" + str(self.O))
        if self.R <= self.O:
            print("------->ERROR:")
            print("R <= O")
   
   
class TORUS(PRIMITIVE):
    name = "TORUS"
    ID = 0
    def __init__(self, s, *, R1, R2):
        self.ID = "{} {}".format(TORUS.name, TORUS.ID)
        TORUS.ID += 1
        ArgCheck.check(self.ID, (R1, R2), ("num", "num"))
        self.s = s
        self.R1 = R1
        self.R2 = R2
        self.describe()
        
    def describe(self):
        print("Creating " + self.ID + ":")
        print("\t" + "Main radius: " + str(self.R1))
        print("\t" + "Sec radius:  " + str(self.R2))
        if self.R1 <= self.R2:
            print("------->ERROR:")
            print("R1 <= R2")
       
       
class ARC3D(PRIMITIVE):
    name = "ARC3D"
    ID = 0
    def __init__(self, s, *, D, R, A):
        self.ID = "{} {}".format(ARC3D.name, ARC3D.ID)
        ARC3D.ID += 1
        ArgCheck.check(self.ID, (D, R, A), "num")
        self.s = s
        self.D = D
        self.R = R
        self.A = A
        self.describe()
        
    def describe(self):
        print("Creating " + self.ID + ":")
        print("\t" + "Pipe radius:  " + str(self.D))
        print("\t" + "Bend radius:  " + str(self.R))
        print("\t" + "Bend angle :  " + str(self.A))
        
            
class ARC3D2(PRIMITIVE):
    name = "ARC3D2"
    ID = 0
    def __init__(self, s, *, D, D2, R, A):
        self.ID = "{} {}".format(ARC3D2.name, ARC3D2.ID)
        ARC3D2.ID += 1
        ArgCheck.check(self.ID, (D, D2, R, A), "num")
        self.s = s
        self.D = D
        self.D2 = D2
        self.R = R
        self.A = A
        self.describe()
        
    def describe(self):
        print("Creating " + self.ID + ":")
        print("\t" + "Pipe radius  :  " + str(self.D))
        print("\t" + "Pipe radius 2:  " + str(self.D2))
        print("\t" + "Bend radius  :  " + str(self.R))
        print("\t" + "Bend angle   :  " + str(self.A))
            

class ARC3DS(PRIMITIVE):
    name = "ARC3DS"
    ID = 0
    def __init__(self, s, *, D, R, A, S):
        self.ID = "{} {}".format(ARC3DS.name, ARC3DS.ID)
        ARC3DS.ID += 1
        ArgCheck.check(self.ID, (D, R, A, S), "num")
        self.s = s
        self.D = D
        self.R = R
        self.A = A
        self.S = S
        self.describe()
        
    def describe(self):
        print("Creating " + self.ID + ":")
        print("\t" + "Pipe radius:  " + str(self.D))
        print("\t" + "Bend radius:  " + str(self.R))
        print("\t" + "Bend angle :  " + str(self.A))
        print("\t" + "Segments   :  " + str(self.S))
        
        
class BOX(PRIMITIVE):
    name = "BOX"
    ID = 0
    def __init__(self, s, *, L, W, H):
        self.ID = "{} {}".format(BOX.name, BOX.ID)
        BOX.ID += 1
        ArgCheck.check(self.ID, (L, W, H), "num")
        self.s = s
        self.L = L
        self.W = W
        self.H = H
        self.describe()
        
    def describe(self):
        print("Creating " + self.ID + ":")
        print("\t" + "Y width    :  " + str(self.L))
        print("\t" + "Z height   :  " + str(self.W))
        print("\t" + "X length   :  " + str(self.H))
        
        
class CONE(PRIMITIVE):
    name = "CONE"
    ID = 0
    def __init__(self, s, *, R1, R2, H, E):
        self.ID = "{} {}".format(CONE.name, CONE.ID)
        CONE.ID += 1
        ArgCheck.check(self.ID, (R1, R2, H, E), "num")
        self.s = s
        self.R1 = R1
        self.R2 = R2
        self.H = H
        self.E = E
        self.describe()
        
    def describe(self):
        print("Creating " + self.ID + ":")
        print("\t" + "Bottom radius :  " + str(self.R1))
        print("\t" + "Upper radius  :  " + str(self.R2))
        print("\t" + "Heitht        :  " + str(self.H))
        print("\t" + "Eccentricity  :  " + str(self.E))


class ELLIPSOIDHEAD(PRIMITIVE):
    name = "ELLIPSOIDHEAD"
    ID = 0
    def __init__(self, s, *, R):
        self.ID = "{} {}".format(ELLIPSOIDHEAD.name, ELLIPSOIDHEAD.ID)
        ELLIPSOIDHEAD.ID += 1
        ArgCheck.check(self.ID, R, "num")
        self.s = s
        self.R = R
        self.describe()
        
    def describe(self):
        print("Creating " + self.ID + ":")
        print("\t" + "Radius     :  " + str(self.R))

        
class ELLIPSOIDHEAD2(PRIMITIVE):
    name = "ELLIPSOIDHEAD2"
    ID = 0
    def __init__(self, s, *, R):
        self.ID = "{} {}".format(ELLIPSOIDHEAD2.name, ELLIPSOIDHEAD2.ID)
        ELLIPSOIDHEAD2.ID += 1
        ArgCheck.check(self.ID, R, "num")
        self.s = s
        self.R = R
        self.describe()
        
    def describe(self):
        print("Creating " + self.ID + ":")
        print("\t" + "Radius     :  " + str(self.R))
        
        
class ELLIPSOIDSEGMENT(PRIMITIVE):
    name = "ELLIPSOIDSEGMENT"
    ID = 0
    def __init__(self, s, *, RX, RY, A1, A2, A3, A4):
        self.ID = "{} {}".format(ELLIPSOIDSEGMENT.name, ELLIPSOIDSEGMENT.ID)
        ELLIPSOIDSEGMENT.ID += 1
        ArgCheck.check(self.ID, (RX, RY, A1, A2, A3, A4), "num")
        self.s = s
        self.RX = RX
        self.RY = RY
        self.A1 = A1
        self.A2 = A2
        self.A3 = A3
        self.A4 = A4
        self.describe()
        
    def describe(self):
        print("Creating " + self.ID + ":")
        print("\t" + "Big axis                :  " + str(self.RX))
        print("\t" + "Small axis              :  " + str(self.RY))
        print("\t" + "Complete rotation angle :  " + str(self.A1))
        print("\t" + "Start angle of rotation :  " + str(self.A2))
        print("\t" + "Start angle of ellipse  :  " + str(self.A3))
        print("\t" + "End angle of ellipse    :  " + str(self.A4))
        
        
class HALFSPHERE(PRIMITIVE):
    name = "HALFSPHERE"
    ID = 0
    def __init__(self, s, *, R):
        self.ID = "{} {}".format(HALFSPHERE.name, HALFSPHERE.ID)
        HALFSPHERE.ID += 1
        ArgCheck.check(self.ID, R, "num")
        self.s = s
        self.R = R
        self.describe()
        
    def describe(self):
        print("Creating " + self.ID + ":")
        print("\t" + "Radius     :  " + str(self.R))
        
        
class PYRAMID(PRIMITIVE):
    name = "PYRAMID"
    ID = 0
    def __init__(self, s, *, L, W, H, HT):
        self.ID = "{} {}".format(PYRAMID.name, PYRAMID.ID)
        PYRAMID.ID += 1
        ArgCheck.check(self.ID, (L, W, H, HT), "num")
        self.s = s
        self.L = L
        self.W = W
        self.H = H
        self.HT = HT
        self.describe()
        
    def describe(self):
        print("Creating " + self.ID + ":")
        print("\t" + "X length       :  " + str(self.L))
        print("\t" + "Y width        :  " + str(self.W))
        print("\t" + "Frustum height :  " + str(self.H))
        print("\t" + "Total height   :  " + str(self.HT))

        
class ROUNDRECT(PRIMITIVE):
    name = "ROUNDRECT"
    ID = 0
    def __init__(self, s, *, L, W, H, R2, E):
        self.ID = "{} {}".format(ROUNDRECT.name, ROUNDRECT.ID)
        ROUNDRECT.ID += 1
        ArgCheck.check(self.ID, (L, W, H, R2, E), "num")
        self.s = s
        self.L = L
        self.W = W
        self.H = H
        self.R2 = R2
        self.E = E
        self.describe()
        
    def describe(self):
        print("Creating " + self.ID + ":")
        print("\t" + "X length       :  " + str(self.L))
        print("\t" + "Y width        :  " + str(self.W))
        print("\t" + "Z height       :  " + str(self.H))
        print("\t" + "Circle radius  :  " + str(self.R2))
        print("\t" + "Eccentricity   :  " + str(self.E))
        
        
class SPHERESEGMENT(PRIMITIVE):
    name = "SPHERESEGMENT"
    ID = 0
    def __init__(self, s, *, R, P, Q):
        self.ID = "{} {}".format(SPHERESEGMENT.name, SPHERESEGMENT.ID)
        SPHERESEGMENT.ID += 1
        ArgCheck.check(self.ID, (R, P, Q), "num")
        self.s = s
        self.R = R
        self.P = P
        self.Q = Q
        self.describe()
        
    def describe(self):
        print("Creating " + self.ID + ":")
        print("\t" + "Sphere radius  :  " + str(self.R))
        print("\t" + "Segment height :  " + str(self.P))
        print("\t" + "Start height   :  " + str(self.Q))
        
        
class TORISPHERICHEAD(PRIMITIVE):
    name = "TORISPHERICHEAD"
    ID = 0
    def __init__(self, s, *, R):
        self.ID = "{} {}".format(TORISPHERICHEAD.name, TORISPHERICHEAD.ID)
        TORISPHERICHEAD.ID += 1
        ArgCheck.check(self.ID, R, "num")
        self.s = s
        self.R = R
        self.describe()
        
    def describe(self):
        print("Creating " + self.ID + ":")
        print("\t" + "Radius     :  " + str(self.R))
       

class TORISPHERICHEAD2(PRIMITIVE):
    name = "TORISPHERICHEAD2"
    ID = 0
    def __init__(self, s, *, R):
        self.ID = "{} {}".format(TORISPHERICHEAD2.name, TORISPHERICHEAD2.ID)
        TORISPHERICHEAD2.ID += 1
        ArgCheck.check(self.ID, R, "num")
        self.s = s
        self.R = R
        self.describe()
        
    def describe(self):
        print("Creating " + self.ID + ":")
        print("\t" + "Radius     :  " + str(self.R))       
        
        
class TORISPHERICHEADH(PRIMITIVE):
    name = "TORISPHERICHEADH"
    ID = 0
    def __init__(self, s, *, R, H):
        self.ID = "{} {}".format(TORISPHERICHEADH.name, TORISPHERICHEADH.ID)
        TORISPHERICHEADH.ID += 1
        ArgCheck.check(self.ID, (R, H), "num")
        self.s = s
        self.R = R
        self.H = H
        self.describe()
        
    def describe(self):
        print("Creating " + self.ID + ":")
        print("\t" + "Radius     :  " + str(self.R))     
        print("\t" + "Height     :  " + str(self.R))     
        

# main plant object, use it as the first argument in the script
s = PLANTOBJECT("test_object")