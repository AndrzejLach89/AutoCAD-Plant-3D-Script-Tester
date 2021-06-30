from Log import *
from ArgCheck import *

class mTransform:
    def transform(*args):
        print("Creating transformation:", *args)
        

class PLANTOBJECT:
    ID = 1
    name = "MAIN OBJECT"
    def __init__(self, name):
        self.name = name
        self.ID = "{} {}".format(PLANTOBJECT.name, PLANTOBJECT.ID)
        
    def setPoint(self, position, direction):
        ArgCheck.check(self.ID, (position, direction), ("num", "num"))
        #print("  >{}: Adding point at {}, direction: {}".format(self.ID, position, direction))
        print("{}:\n\tAdding point at {}, direction: {}".format(self.ID, position, direction))
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
        
    def setLinearDimension(self, name, vector1, vector2):
        ArgCheck.check(self.ID, (name, vector1, vector2), (str, "num", "num"))
        print("{}:\n\tAdding linear dimension at {}, {}".format(self.ID, vector1, vector2))
        return self
        
        
class PRIMITIVE:
    def translate(self, x):
        ArgCheck.check(self.ID, x, "num")
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
        self.s = s
        self.R = R
        self.H = H
        self.O = O
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tRadius:  {}".format(self.R))
        print("\tHeight:  {}".format(self.H))
        print("\tInner r: {}".format(self.O))
        if self.R <= self.O:
            print("\tWarning! R <= 0")
   
   
class TORUS(PRIMITIVE):
    name = "TORUS"
    ID = 1
    def __init__(self, s, *, R1, R2):
        self.ID = "{} {}".format(TORUS.name, TORUS.ID)
        TORUS.ID += 1
        ArgCheck.check(self.ID, (R1, R2), ("num", "num"))
        self.s = s
        self.R1 = R1
        self.R2 = R2
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tMain radius: {}".format(self.R1))
        print("\tSec radius:  {}".format(self.R2))
       
       
class ARC3D(PRIMITIVE):
    name = "ARC3D"
    ID = 1
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
        print("Creating {}:".format(self.ID))
        print("\tPipe radius:  {}".format(self.D))
        print("\tBend radius:  {}".format(self.R))
        print("\tBend angle :  {}".format(self.A))
        
            
class ARC3D2(PRIMITIVE):
    name = "ARC3D2"
    ID = 1
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
        print("Creating {}:".format(self.ID))
        print("\tPipe radius  :  {}".format(self.D))
        print("\tPipe radius 2:  {}".format(self.D2))
        print("\tBend radius  :  {}".format(self.R))
        print("\tBend angle   :  {}".format(self.A))
            

class ARC3DS(PRIMITIVE):
    name = "ARC3DS"
    ID = 1
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
        print("Creating {}:".format(self.ID))
        print("\tPipe radius:  {}".format(self.D))
        print("\tBend radius:  {}".format(self.R))
        print("\tBend angle :  {}".format(self.A))
        print("\tSegments   :  {}".format(self.S))
        
        
class BOX(PRIMITIVE):
    name = "BOX"
    ID = 1
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
        print("Creating {}:".format(self.ID))
        print("\tY width    :  {}".format(self.L))
        print("\tZ height   :  {}".format(self.W))
        print("\tX length   :  {}".format(self.H))
        
        
class CONE(PRIMITIVE):
    name = "CONE"
    ID = 1
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
        print("Creating {}:".format(self.ID))
        print("\tBottom radius :  {}".format(self.R1))
        print("\tUpper radius  :  {}".format(self.R2))
        print("\tHeitht        :  {}".format(self.H))
        print("\tEccentricity  :  {}".format(self.E))


class ELLIPSOIDHEAD(PRIMITIVE):
    name = "ELLIPSOIDHEAD"
    ID = 1
    def __init__(self, s, *, R):
        self.ID = "{} {}".format(ELLIPSOIDHEAD.name, ELLIPSOIDHEAD.ID)
        ELLIPSOIDHEAD.ID += 1
        ArgCheck.check(self.ID, R, "num")
        self.s = s
        self.R = R
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tRadius     :  {}".format(self.R))

        
class ELLIPSOIDHEAD2(PRIMITIVE):
    name = "ELLIPSOIDHEAD2"
    ID = 1
    def __init__(self, s, *, R):
        self.ID = "{} {}".format(ELLIPSOIDHEAD2.name, ELLIPSOIDHEAD2.ID)
        ELLIPSOIDHEAD2.ID += 1
        ArgCheck.check(self.ID, R, "num")
        self.s = s
        self.R = R
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tRadius     :  {}".format(self.R))
        
        
class ELLIPSOIDSEGMENT(PRIMITIVE):
    name = "ELLIPSOIDSEGMENT"
    ID = 1
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
        print("Creating {}:".format(self.ID))
        print("\tBig axis                :  {}".format(self.RX))
        print("\tSmall axis              :  {}".format(self.RY))
        print("\tComplete rotation angle :  {}".format(self.A1))
        print("\tStart angle of rotation :  {}".format(self.A2))
        print("\tStart angle of ellipse  :  {}".format(self.A3))
        print("\tEnd angle of ellipse    :  {}".format(self.A4))
        
        
class HALFSPHERE(PRIMITIVE):
    name = "HALFSPHERE"
    ID = 1
    def __init__(self, s, *, R):
        self.ID = "{} {}".format(HALFSPHERE.name, HALFSPHERE.ID)
        HALFSPHERE.ID += 1
        ArgCheck.check(self.ID, R, "num")
        self.s = s
        self.R = R
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tRadius     :  {}".format(self.R))
        
        
class PYRAMID(PRIMITIVE):
    name = "PYRAMID"
    ID = 1
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
        print("Creating {}:".format(self.ID))
        print("\tX length       :  {}".format(self.L))
        print("\tY width        :  {}".format(self.W))
        print("\tFrustum height :  {}".format(self.H))
        print("\tTotal height   :  {}".format(self.HT))

        
class ROUNDRECT(PRIMITIVE):
    name = "ROUNDRECT"
    ID = 1
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
        print("Creating {}:".format(self.ID))
        print("\tX length       :  {}".format(self.L))
        print("\tY width        :  {}".format(self.W))
        print("\tZ height       :  {}".format(self.H))
        print("\tCircle radius  :  {}".format(self.R2))
        print("\tEccentricity   :  {}".format(self.E))
        
        
class SPHERESEGMENT(PRIMITIVE):
    name = "SPHERESEGMENT"
    ID = 1
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
        print("Creating {}:".format(self.ID))
        print("\tSphere radius  :  {}".format(self.R))
        print("\tSegment height :  {}".format(self.P))
        print("\tStart height   :  {}".format(self.Q))
        
        
class TORISPHERICHEAD(PRIMITIVE):
    name = "TORISPHERICHEAD"
    ID = 1
    def __init__(self, s, *, R):
        self.ID = "{} {}".format(TORISPHERICHEAD.name, TORISPHERICHEAD.ID)
        TORISPHERICHEAD.ID += 1
        ArgCheck.check(self.ID, R, "num")
        self.s = s
        self.R = R
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tRadius     :  {}".format(self.R))
       

class TORISPHERICHEAD2(PRIMITIVE):
    name = "TORISPHERICHEAD2"
    ID = 1
    def __init__(self, s, *, R):
        self.ID = "{} {}".format(TORISPHERICHEAD2.name, TORISPHERICHEAD2.ID)
        TORISPHERICHEAD2.ID += 1
        ArgCheck.check(self.ID, R, "num")
        self.s = s
        self.R = R
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tRadius     :  {}".format(self.R))       
        
        
class TORISPHERICHEADH(PRIMITIVE):
    name = "TORISPHERICHEADH"
    ID = 1
    def __init__(self, s, *, R, H):
        self.ID = "{} {}".format(TORISPHERICHEADH.name, TORISPHERICHEADH.ID)
        TORISPHERICHEADH.ID += 1
        ArgCheck.check(self.ID, (R, H), "num")
        self.s = s
        self.R = R
        self.H = H
        self.describe()
        
    def describe(self):
        print("Creating {}:".format(self.ID))
        print("\tRadius     :  {}".format(self.R))     
        print("\tHeight     :  {}".format(self.R))     
        

# main plant object, use it as the first argument in the script
s = PLANTOBJECT("test_object")