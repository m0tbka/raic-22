"""Overloaded float functions"""

after_point = 6
epsilon = 1e-6


def equal_float(self, other):
    """self == other"""
    return abs(round(self - epsilon * 0.5, after_point) - round(other - epsilon * 0.5, after_point)) <= epsilon


def lt_float(self, other):
    """self < other"""
    return round(self - epsilon * 0.5, after_point) - round(other - epsilon * 0.5, after_point) < epsilon


def le_float(self, other):
    """self <= other"""
    return round(self - epsilon * 0.5, after_point) - round(other - epsilon * 0.5, after_point) <= epsilon


# class Float(float):
#     EPS = 1e-9
#
#     def __add__(self, other):
#         """self + other"""
#         return Float(super(Float, self).__add__(other))
#
#     def __sub__(self, other):
#         """self - other"""
#         return Float(super(Float, self).__sub__(other))
#
#     def __mul__(self, other):
#         """self * other"""
#         return Float(super(Float, self).__mul__(other))
#
#     def __truediv__(self, other):
#         """self / other"""
#         return Float(super(Float, self).__truediv__(other))
#
#     def __eq__(self, other):
#         """self == other"""
#         return super(Float, Float(abs(self - other))).__eq__(Float.EPS)
#
#     def __ne__(self, other):
#         """self != other"""
#         return not self == other
#
#     def __lt__(self, other):
#         """self < other"""
#         return super(Float, self - other).__lt__(Float.EPS)
#
#     def __le__(self, other):
#         """self <= other"""
#         return super(Float, self - other).__le__(Float.EPS)
#
#     def __gt__(self, other):
#         """self > other"""
#         return super(Float, self - other).__gt__(Float.EPS)
#
#     def __ge__(self, other):
#         """self >= other"""
#         return super(Float, self - other).__ge__(Float.EPS)
