import math
class Vector():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.mag = math.sqrt(self.x*self.x + self.y*self.y)

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
        return Vector(self.x/self.mag, self.y/self.mag)
