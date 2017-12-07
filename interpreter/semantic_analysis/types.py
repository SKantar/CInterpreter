class CType(object):
    order = ('char', 'int', 'float', 'double')

    def __init__(self, ttype):
        self.type = ttype

    def _calc_type(self, other):
        left_order = CType.order.index(self.type)
        right_order = CType.order.index(other.type)
        return CType(CType.order[max(left_order, right_order)])

    def __add__(self, other):
        return self._calc_type(other)

    def __eq__(self, other):
        return self.type == other.type

    def __repr__(self):
        return '{}'.format(
            self.type,
        )

    def __str__(self):
        return self.__repr__()