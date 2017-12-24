class Number(object):
    types = dict(char=int, int=int, float=float, double=float)
    order = ('char', 'int', 'float', 'double')

    def __init__(self, ttype, value):
        self.type = ttype
        self.value = Number.types[ttype](value)

    def _get_res_type(self, other):
        left_order = Number.order.index(self.type)
        right_order = Number.order.index(other.type)
        ttype = Number.order[max(left_order, right_order)]
        return ttype, Number.types[ttype]

    def __add__(self, other):
        """ self + other """
        ttype, ctype = self._get_res_type(other)
        return Number(ttype, ctype(self.value) + ctype(other.value))

    def __sub__(self, other):
        """ self - other """
        ttype, ctype = self._get_res_type(other)
        return Number(ttype, ctype(self.value) - ctype(other.value))

    def __mul__(self, other):
        """ self * other """
        ttype, ctype = self._get_res_type(other)
        return Number(ttype, ctype(self.value) * ctype(other.value))

    def __truediv__(self, other):
        """ self / other """
        ttype, ctype = self._get_res_type(other)
        if ctype == int:
            return Number(ttype, ctype(self.value) // ctype(other.value))
        return Number(ttype, ctype(self.value) / ctype(other.value))

    def __mod__(self, other):
        """ self % other """
        ttype, ctype = self._get_res_type(other)

        if ctype != int:
            raise TypeError("invalid operands of types '{}' and '{}' to binary ‘operator %’".format(
                self.type,
                other.type
            ))
        return Number(ttype, ctype(self.value) % ctype(other.value))

    def __gt__(self, other):
        """ self > other """
        ttype, ctype = self._get_res_type(other)
        return Number('int', int(ctype(self.value) > ctype(other.value)))

    def __ge__(self, other):
        """ self >= other """
        ttype, ctype = self._get_res_type(other)
        return Number('int', int(ctype(self.value) >= ctype(other.value)))

    def __lt__(self, other):
        """ self < other """
        ttype, ctype = self._get_res_type(other)
        return Number('int', int(ctype(self.value) < ctype(other.value)))

    def __le__(self, other):
        """ self <= other """
        ttype, ctype = self._get_res_type(other)
        return Number('int', int(ctype(self.value) <= ctype(other.value)))

    def __eq__(self, other):
        """ self == other """
        ttype, ctype = self._get_res_type(other)
        return Number('int', int(ctype(self.value) == ctype(other.value)))

    def __ne__(self, other):
        """ self != other """
        ttype, ctype = self._get_res_type(other)
        return Number('int', int(ctype(self.value) != ctype(other.value)))

    def __iadd__(self, other):
        """ self += other """
        ctype = Number.types[self.type]
        result = self + other
        return Number(self.type, ctype(result.value))

    def __isub__(self, other):
        """ self -= other """
        ctype = Number.types[self.type]
        result = self - other
        return Number(self.type, ctype(result.value))

    def __imul__(self, other):
        """ self *= other """
        ctype = Number.types[self.type]
        result = self * other
        return Number(self.type, ctype(result.value))

    def __itruediv__(self, other):
        """ self /= other """
        ctype = Number.types[self.type]
        result = self / other
        return Number(self.type, ctype(result.value))

    def __and__(self, other):
        """ self & other """
        ttype, ctype = self._get_res_type(other)
        return Number(ttype, int(ctype(self.value) & ctype(other.value)))

    def __or__(self, other):
        """ self | other """
        ttype, ctype = self._get_res_type(other)
        return Number(ttype, int(ctype(self.value) | ctype(other.value)))

    def __xor__(self, other):
        """ self ^ other """
        ttype, ctype = self._get_res_type(other)
        return Number(ttype, int(ctype(self.value) ^ ctype(other.value)))


    def __bool__(self):
        return bool(self.value)

    def _not(self):
        return Number('int', 0) if self.value else Number('int', 1)

    def __repr__(self):
        return '{} ({})'.format(
            self.type,
            self.value
        )

    def __str__(self):
        return self.__repr__()