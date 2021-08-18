from Log import *
from ArgCheck import *
from Warnings import *

class mTransform:
    def transform(*args):
        print("Creating transformation:", *args)
        

class PLANTOBJECT:
    ID = 1
    name = "MAIN OBJECT"
    def __init__(self, name):
        self.name = name
        self.ID = "{} {}".format(PLANTOBJECT.name, PLANTOBJECT.ID)
        
    def setPoint(self, position, direction, angle=0):
        ArgCheck.check(self.ID, (position, direction, angle), ("num", "num", "num"))
        #print("  >{}: Adding point at {}, direction: {}".format(self.ID, position, direction))
        ArgCheck.checkTuple(self.ID, position, 3, "Point coordinates")
        ArgCheck.checkTuple(self.ID, direction, 3, "Direction vector")
        print("{}:\n\tAdding point at {}, direction: {}, angle: {}".format(self.ID, position, direction, angle))
        return self
        
    def numberOfPoints(self, *args):
        print("{}:\n\tObtaining number of points...".format(self.ID))
        return self
        
    def directionAt(self, *args):
        print("{}:\n\tObtaining direction...".format(self.ID))
        return self
        
    def pointAt(self, *args):
        print("{}:\n\tObtaining position of connection point...".format(self.ID))
        return self
        
    def setLinearDimension(self, name, point1, point2):
        ArgCheck.check(self.ID, (name, point1, point2), (str, "num", "num"))
        ArgCheck.checkTuple(self.ID, point1, 3, "Point 1 coordinates")
        ArgCheck.checkTuple(self.ID, point2, 3, "Point 2 coordinates")
        print("{}:\n\tAdding linear dimension at {}, {}".format(self.ID, point1, point2))
        return self
        
        
class PRIMITIVE:
    def translate(self, x):
        ArgCheck.check(self.ID, x, "num")
        ArgCheck.checkTuple(self.ID, x, 3, "Translation vector")
        print("{}:\n\ttranslation: {}".format(self.ID, x))
        return self
        
    def rotateX(self, x):
        ArgCheck.check(self.ID, x, "num")
        print("{}:\n\tRotation by X: {} deg".format(self.ID, x))
        return self
        
    def rotateY(self, x):
        ArgCheck.check(self.ID, x, "num")
        print("{}:\n\tRotation by Y: {} deg".format(self.ID, x))
        return self
        
    def rotateZ(self, x):
        ArgCheck.check(self.ID, x, "num")
        print("{}:\n\tRotation by Z: {} deg".format(self.ID, x))
        return self
        
    def erase(self):
        print("{}:\n\tObject was erased.".format(self.ID))
        return self
        
    def uniteWith(self, object):
        ArgCheck.check(self.ID, object, PRIMITIVE)
        print("{}:\n\tUniting {} with {}\n\tCreating new object.".format(self.ID, self.ID, object.ID))
        newObject = MODIFIED_OBJECT(self.ID, object.ID)
        self.ID = newObject.ID
        return newObject
        
    def subtractFrom(self, object):
        ArgCheck.check(self.ID, object, PRIMITIVE)
        print("{}:\n\tSubtracting {} from {}\n\tCreating new object.".format(self.ID, object.ID, self.ID))
        newObject = MODIFIED_OBJECT(self.ID, object.ID)
        self.ID = newObject.ID
        return newObject
        
    def intersectWith(self, object):
        ArgCheck.check(self.ID, object, PRIMITIVE)
        print("{}:\n\tCreating new object at intersection of {} and {}".format(self.ID, self.ID, object.ID))
        newObject = MODIFIED_OBJECT(self.ID, object.ID)
        self.ID = newObject.ID
        return newObject
        
    def parameters(self):
        print("{}:\n\tGetting {} parameters".format(self.ID, self.ID))
        return self
        
    def transformationMatrix(self):
        print("{}:\n\tGetting {} transformation matrix".format(self.ID, self.ID))
        return self
        
    def setTransformationMatrix(self, *args):
        print("{}:\n\tSetting {} transformation matrix\n\t{}".format(self.ID, self.ID, *args))
        return self


class MODIFIED_OBJECT(PRIMITIVE):
    name = "MODIFIED_OBJECT"
    ID = 1
    def __init__(self, parent1, parent2, *args):
        self.ID = "{} {}".format(MODIFIED_OBJECT.name, MODIFIED_OBJECT.ID)
        self.parent1 = parent1
        self.parent2 = parent2
        MODIFIED_OBJECT.ID += 1
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tObject created using {} and {}".format(self.parent1, self.parent2))
        
        
class CYLINDER(PRIMITIVE):
    name = "CYLINDER"
    ID = 1
    def __init__(self, s, *, R, H, O):
        self.ID = "{} {}".format(CYLINDER.name, CYLINDER.ID)
        CYLINDER.ID += 1
        ArgCheck.check(self.ID, (R, H, O), "num")
        ArgCheck.checkValues(self.ID, {'R':R, 'H':H})
        ArgCheck.checkValues(self.ID, {'O':O}, True)
        ArgCheck.checkIfGreater(self.ID, R, O, 'R', 'O')
        self.s = s
        self.R = R
        self.H = H
        self.O = O
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tRadius   (R):  {}".format(self.R))
        print("\tHeight   (H):  {}".format(self.H))
        print("\tInner r  (O):  {}".format(self.O))
   
   
class TORUS(PRIMITIVE):
    name = "TORUS"
    ID = 1
    def __init__(self, s, *, R1, R2):
        self.ID = "{} {}".format(TORUS.name, TORUS.ID)
        TORUS.ID += 1
        ArgCheck.check(self.ID, (R1, R2), ("num", "num"))
        ArgCheck.checkValues(self.ID, {"R1":R1, "R2":R2})
        ArgCheck.checkIfGreater(self.ID, R1, R2, 'R1', 'R2')
        self.s = s
        self.R1 = R1
        self.R2 = R2
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tMain radius  (R1): {}".format(self.R1))
        print("\tSec radius   (R2):  {}".format(self.R2))
       
       
class ARC3D(PRIMITIVE):
    name = "ARC3D"
    ID = 1
    def __init__(self, s, *, D, R, A):
        self.ID = "{} {}".format(ARC3D.name, ARC3D.ID)
        ARC3D.ID += 1
        ArgCheck.check(self.ID, (D, R, A), "num")
        ArgCheck.checkValues(self.ID, {"D":D, "R":R, "A":A})
        self.s = s
        self.D = D
        self.R = R
        self.A = A
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tPipe radius  (D):  {}".format(self.D))
        print("\tBend radius  (R):  {}".format(self.R))
        print("\tBend angle   (A):  {}".format(self.A))
        
            
class ARC3D2(PRIMITIVE):
    name = "ARC3D2"
    ID = 1
    def __init__(self, s, *, D, D2, R, A):
        self.ID = "{} {}".format(ARC3D2.name, ARC3D2.ID)
        ARC3D2.ID += 1
        ArgCheck.check(self.ID, (D, D2, R, A), "num")
        ArgCheck.checkValues(self.ID, {"D":D, "D2":D2, "R":R, "A":A})
        self.s = s
        self.D = D
        self.D2 = D2
        self.R = R
        self.A = A
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tPipe radius    (D):  {}".format(self.D))
        print("\tPipe radius 2 (D2):  {}".format(self.D2))
        print("\tBend radius    (R):  {}".format(self.R))
        print("\tBend angle     (A):  {}".format(self.A))
            

class ARC3DS(PRIMITIVE):
    name = "ARC3DS"
    ID = 1
    def __init__(self, s, *, D, R, A, S):
        self.ID = "{} {}".format(ARC3DS.name, ARC3DS.ID)
        ARC3DS.ID += 1
        ArgCheck.check(self.ID, (D, R, A, S), "num")
        ArgCheck.checkValues(self.ID, {"D":D, "R":R, "A":A, "S":S})
        self.s = s
        self.D = D
        self.R = R
        self.A = A
        self.S = S
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tPipe radius (D):  {}".format(self.D))
        print("\tBend radius (R):  {}".format(self.R))
        print("\tBend angle  (A):  {}".format(self.A))
        print("\tSegments    (S):  {}".format(self.S))
        
        
class BOX(PRIMITIVE):
    name = "BOX"
    ID = 1
    def __init__(self, s, *, L, W, H):
        self.ID = "{} {}".format(BOX.name, BOX.ID)
        BOX.ID += 1
        ArgCheck.check(self.ID, (L, W, H), "num")
        ArgCheck.checkValues(self.ID, {"L":L, "W":W, "H":H})
        self.s = s
        self.L = L
        self.W = W
        self.H = H
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tX length (H):  {}".format(self.H))
        print("\tY width  (L):  {}".format(self.L))
        print("\tZ height (W):  {}".format(self.W))
        
        
class CONE(PRIMITIVE):
    name = "CONE"
    ID = 1
    def __init__(self, s, *, R1, R2, H, E):
        self.ID = "{} {}".format(CONE.name, CONE.ID)
        CONE.ID += 1
        ArgCheck.check(self.ID, (R1, R2, H, E), "num")
        ArgCheck.checkValues(self.ID, {"R1":R1, "R2":R2, "H":H, "E":E})
        self.s = s
        self.R1 = R1
        self.R2 = R2
        self.H = H
        self.E = E
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tBottom radius (R1):  {}".format(self.R1))
        print("\tUpper radius  (R2):  {}".format(self.R2))
        print("\tHeitht         (H):  {}".format(self.H))
        print("\tEccentricity   (E):  {}".format(self.E))


class ELLIPSOIDHEAD(PRIMITIVE):
    name = "ELLIPSOIDHEAD"
    ID = 1
    def __init__(self, s, *, R):
        self.ID = "{} {}".format(ELLIPSOIDHEAD.name, ELLIPSOIDHEAD.ID)
        ELLIPSOIDHEAD.ID += 1
        ArgCheck.check(self.ID, R, "num")
        ArgCheck.checkValues(self.ID, {"R":R})
        self.s = s
        self.R = R
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tRadius     (R):  {}".format(self.R))

        
class ELLIPSOIDHEAD2(PRIMITIVE):
    name = "ELLIPSOIDHEAD2"
    ID = 1
    def __init__(self, s, *, R):
        self.ID = "{} {}".format(ELLIPSOIDHEAD2.name, ELLIPSOIDHEAD2.ID)
        ELLIPSOIDHEAD2.ID += 1
        ArgCheck.check(self.ID, R, "num")
        ArgCheck.checkValues(self.ID, {"R":R})
        self.s = s
        self.R = R
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tRadius   (R):  {}".format(self.R))
        
        
class ELLIPSOIDSEGMENT(PRIMITIVE):
    name = "ELLIPSOIDSEGMENT"
    ID = 1
    def __init__(self, s, *, RX, RY, A1, A2, A3, A4):
        self.ID = "{} {}".format(ELLIPSOIDSEGMENT.name, ELLIPSOIDSEGMENT.ID)
        ELLIPSOIDSEGMENT.ID += 1
        ArgCheck.check(self.ID, (RX, RY, A1, A2, A3, A4), "num")
        ArgCheck.checkValues(self.ID, {"RX":RX, "RY":RY, "A1":A1, "A2":A2, "A3":A3, "A4":A4})
        self.s = s
        self.RX = RX
        self.RY = RY
        self.A1 = A1
        self.A2 = A2
        self.A3 = A3
        self.A4 = A4
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tBig axis                (RX):  {}".format(self.RX))
        print("\tSmall axis              (RY):  {}".format(self.RY))
        print("\tComplete rotation angle (A1):  {}".format(self.A1))
        print("\tStart angle of rotation (A2):  {}".format(self.A2))
        print("\tStart angle of ellipse  (A3):  {}".format(self.A3))
        print("\tEnd angle of ellipse    (A4):  {}".format(self.A4))
        
        
class HALFSPHERE(PRIMITIVE):
    name = "HALFSPHERE"
    ID = 1
    def __init__(self, s, *, R):
        self.ID = "{} {}".format(HALFSPHERE.name, HALFSPHERE.ID)
        HALFSPHERE.ID += 1
        ArgCheck.check(self.ID, R, "num")
        ArgCheck.checkValues(self.ID, {"R":R})
        self.s = s
        self.R = R
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tRadius     (R):  {}".format(self.R))
        
        
class PYRAMID(PRIMITIVE):
    name = "PYRAMID"
    ID = 1
    def __init__(self, s, *, L, W, H, HT):
        self.ID = "{} {}".format(PYRAMID.name, PYRAMID.ID)
        PYRAMID.ID += 1
        ArgCheck.check(self.ID, (L, W, H, HT), "num")
        ArgCheck.checkValues(self.ID, {"L":L, "W":W, "HT":HT})
        ArgCheck.checkValues(self.ID, {"H":H}, True)
        self.s = s
        self.L = L
        self.W = W
        self.H = H
        self.HT = HT
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tX length        (L):  {}".format(self.L))
        print("\tY width         (W):  {}".format(self.W))
        print("\tFrustum height  (H):  {}".format(self.H))
        print("\tTotal height   (HT):  {}".format(self.HT))

        
class ROUNDRECT(PRIMITIVE):
    name = "ROUNDRECT"
    ID = 1
    def __init__(self, s, *, L, W, H, R2, E):
        self.ID = "{} {}".format(ROUNDRECT.name, ROUNDRECT.ID)
        ROUNDRECT.ID += 1
        ArgCheck.check(self.ID, (L, W, H, R2, E), "num")
        ArgCheck.checkValues(self.ID, {"L":L, "W":W, "H":H, "R2":R2, "E":E})
        self.s = s
        self.L = L
        self.W = W
        self.H = H
        self.R2 = R2
        self.E = E
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tX length       (L):  {}".format(self.L))
        print("\tY width        (W):  {}".format(self.W))
        print("\tZ height       (H):  {}".format(self.H))
        print("\tCircle radius (R2):  {}".format(self.R2))
        print("\tEccentricity   (E):  {}".format(self.E))
        
        
class SPHERESEGMENT(PRIMITIVE):
    name = "SPHERESEGMENT"
    ID = 1
    def __init__(self, s, *, R, P, Q):
        self.ID = "{} {}".format(SPHERESEGMENT.name, SPHERESEGMENT.ID)
        SPHERESEGMENT.ID += 1
        ArgCheck.check(self.ID, (R, P, Q), "num")
        ArgCheck.checkValues(self.ID, {"R":R, "P":P, "Q":Q})
        self.s = s
        self.R = R
        self.P = P
        self.Q = Q
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tSphere radius  (R):  {}".format(self.R))
        print("\tSegment height (P):  {}".format(self.P))
        print("\tStart height   (Q):  {}".format(self.Q))
        
        
class TORISPHERICHEAD(PRIMITIVE):
    name = "TORISPHERICHEAD"
    ID = 1
    def __init__(self, s, *, R):
        self.ID = "{} {}".format(TORISPHERICHEAD.name, TORISPHERICHEAD.ID)
        TORISPHERICHEAD.ID += 1
        ArgCheck.check(self.ID, R, "num")
        ArgCheck.checkValues(self.ID, {"R":R})
        self.s = s
        self.R = R
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tRadius   (R):  {}".format(self.R))
       

class TORISPHERICHEAD2(PRIMITIVE):
    name = "TORISPHERICHEAD2"
    ID = 1
    def __init__(self, s, *, R):
        self.ID = "{} {}".format(TORISPHERICHEAD2.name, TORISPHERICHEAD2.ID)
        TORISPHERICHEAD2.ID += 1
        ArgCheck.check(self.ID, R, "num")
        ArgCheck.checkValues(self.ID, {"R":R})
        self.s = s
        self.R = R
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tRadius   (R):  {}".format(self.R))      
        
        
class TORISPHERICHEADH(PRIMITIVE):
    name = "TORISPHERICHEADH"
    ID = 1
    def __init__(self, s, *, R, H):
        self.ID = "{} {}".format(TORISPHERICHEADH.name, TORISPHERICHEADH.ID)
        TORISPHERICHEADH.ID += 1
        ArgCheck.check(self.ID, (R, H), "num")
        ArgCheck.checkValues(self.ID, {"R":R, "H":H})
        self.s = s
        self.R = R
        self.H = H
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tRadius   (R):  {}".format(self.R)) 
        print("\tHeight   (H):  {}".format(self.H))
        

# main plant object, use it as the first argument in the script
s = PLANTOBJECT("test_object")