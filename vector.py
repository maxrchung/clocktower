import math
class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        if x == None and y == None:
            self.mag = None
        elif x == None:
            self.mag = x
        elif y == None:
            self.mag = y
        else:
            self.mag = math.sqrt(self.x*self.x + self.y*self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __ne__(self, other):
        return self.x != other.x or self.y != other.y
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)
    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self
    def __mul__(self, scale):
        return Vector(self.x * scale, self.y * scale)
    def __imul__(self, scale):
        self.x *= scale
        self.y *= scale
        return self
    __rmul__ = __mul__
    def __div__(self, scale):
        return Vector(self.x/scale, self.y/scale)
    def __idiv__(self, scale):
        self.x /= scale
        self.y /= scale
        return self
    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def get_norm(self):
        if self.mag > 0.0:
            return Vector(self.x/self.mag, self.y/self.mag)
        return Vector(0.0, 0.0)
    def moveTowards(self, target, increment):
        temp = Vector(target.x, target.y)
        if temp.x == None:
            temp.x = self.x
        if temp.y == None:
            temp.y = self.y
        # get raw difference
        diff_norm = (temp - self).get_norm()
        # add scaled increment
        self += diff_norm*increment
        # if the new difference's normal is not equal to the
        # original difference's normal, then we have overshot
        testDiff_norm = (temp - self).get_norm()
        # RED FLAG: SET THINGS EQUAL BY VALUE, NOT BY REFERENCE
        if diff_norm != testDiff_norm:
            self.x = temp.x
            self.y = temp.y
        
        return self
    def reverse(self):
        return -1*self
