# noinspection PyProtectedMember
class Locus:
    # (x0,y0) - left upper, (x1, y1) - right bottom
    # noinspection PyUnusedLocal
    def __init__(self, *, left=0, bottom=0, width=0, height=0, locus=None, **kwargs):
        self.__x0 = left
        self.__w = width
        self.__h = height
        self.__y1 = bottom
        if locus:
            self.__x0 = locus.__x0
            if not self.__w:
                self._w = locus.__w
            if not self.__h:
                self.__h = locus.__h
            self.__y1 = locus.__y1

    def inside(self, x, y):
        return self.__x0 <= x <= self.__x0 + self.__w and self.__y1 - self.__h <= y <= self.__y1

    def left_bottom(self):
        return self.__x0, self.__y1

    def rectangle(self):
        return self.__x0, self.__y1, self.__x0 + self.__w, self.__y1 - self.__h

    def move(self, dx, dy):
        self.__x0 += dx
        self.__y1 += dy

    def __sub__(self, other):
        x, y = self.left_bottom()
        x1, y1 = other.left_bottom()
        return x - x1, y - y1

    def up(self, d):
        return Locus(left=self.__x0, bottom=self.__y1 - d, width=self.__w, height=self.__h)

    def __repr__(self):
        return str(self.__y1)



