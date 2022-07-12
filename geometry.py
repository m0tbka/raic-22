"""Vector geometry with all methods"""

from model.vec2 import Vec2

from strategy.float import Float

from math import pi, sqrt, cos, sin


class Vec(Vec2):
    """Vectors with useful operations"""

    def __init__(self, x: Float = 0, y: Float = 0):
        super(Vec, self).__init__(x, y)
        self.len = self.get_len()
        """The length of the vector"""

    def get_len(self) -> Float:
        """Returns the length of the vector"""
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __add__(self, other):
        """Creates new vector equals to sum of two vectors"""

        return Vec(
            self.x + other.x,
            self.y + other.y
        )

    def __sub__(self, other):
        """Creates new vector equals to sub of two vectors"""

        return Vec(
            self.x - other.x,
            self.y - other.y
        )

    def __truediv__(self, other):
        """Creates new vector equals to truediv of two vectors"""

        return Vec(
            self.x / other,
            self.y / other
        )

    def __mul__(self, other):
        """Creates new vector equals to cross_product of two vectors or mult vector and number"""

        new = None
        if type(other) is Vec:
            """Counts mult of two vectors(dot_product)"""
            other: Vec
            new = self.x * other.x + self.y + other.y

        else:
            """Counts mult of vector and number"""
            new = Vec(
                self.x * other,
                self.y * other
            )

        return new

    def __pow__(self, other):
        """Counts cross_product of two vector"""

        other: Vec
        return self.x * other.y - self.x * other.x

    def __lshift__(self, other: Float):
        """Returns rotated anticlockwise vector by an angle(radians) 'other'"""

        return Vec(
            Float(cos(other) * self.x - sin(other) * self.y),
            Float(sin(other) * self.x + cos(other) * self.y)
        )

    def __rshift__(self, other: Float):
        """Returns rotated clockwise vector by an angle(radians) 'other'"""

        return Vec(
            Float(cos(other) * self.x + sin(other) * self.y),
            Float(-sin(other) * self.x + cos(other) * self.y)
        )

    def __eq__(self, other):
        """Returns True if self equal other else False"""
        return self.x == other.x and self.y == other.y


class Figure:
    """Class of all geometry 2D figures"""

    square: Float

    def count_square(self) -> Float:
        """Counts square of the figure"""
        pass

    # def intersection_square(self, other) -> Float:
    #     """Counts square of the intersection of two figures"""
    #     pass


class Line(Figure):
    """Lines and their properties"""

    a: Float
    b: Float
    c: Float
    normal: Vec
    first_point: Vec
    second_point: Vec

    def __init__(self, first_point: Vec = None, second_point: Vec = None, a: Float = -1, b: Float = 1, c: Float = 0):
        if first_point is None or second_point is None:
            self.a = a
            """Coefficient A of line"""
            self.b = b
            """Coefficient B of line"""
            self.c = c
            """Coefficient C of line"""
            self.first_point = Vec(Float(0), self[0])
            """One of the point line include"""
            self.second_point = Vec(Float(0), self[1])
            """Another of the point line include"""
        else:
            self.first_point = first_point
            """One of the point line include"""
            self.second_point = second_point
            """Another of the point line include"""
            self.a = self.count_coefficient_a()
            """Coefficient A of line"""
            self.b = self.count_coefficient_b()
            """Coefficient B of line"""
            self.c = self.count_coefficient_c()
            """Coefficient C of line"""
        self.normal = self.count_normal()
        """Normal of line"""

    def count_normal(self) -> Vec:
        """Counts normal of line"""
        return Vec(self.a, self.b)

    def count_coefficient_a(self, point1: Vec = None, point2: Vec = None) -> Float:
        """Counts coefficient A of line in Ax+By+C=0"""

        if point1 is None:
            point1 = self.first_point

        if point2 is None:
            point2 = self.second_point

        return point1.y - point2.y

    def count_coefficient_b(self, point1: Vec = None, point2: Vec = None) -> Float:
        """Counts coefficient B of line in Ax+By+C=0"""

        if point1 is None:
            point1 = self.first_point

        if point2 is None:
            point2 = self.second_point

        return point2.x - point1.x

    def count_coefficient_c(self, point1: Vec = None, point2: Vec = None) -> Float:
        """Counts coefficient C of line in Ax+By+C=0"""

        if point1 is None:
            point1 = self.first_point

        if point2 is None:
            point2 = self.second_point

        return (point1.x - point2.x) * point1.y + (point2.y - point1.y) * point1.x

    def __getitem__(self, item, first=False):
        """Returns second(first if tag first is True) coordinate of point on line with X(Y if tag first is True) equal
            to item (counts value of y(x) or opposite). Example: a = Line((0, 0), (1, 2)); a[2] -> 4; a[6, True] -> 3"""

        if type(item) is tuple:
            if type(item[1]) is bool:
                first = item[1]
            item = item[0]

        return -(self.a * item + self.c) / self.b if not first else -(self.b * item + self.c) / self.a

    def __contains__(self, item) -> bool:
        """Returns True if item belong to the line(is a subset of the line) else False"""

        if type(item) is Vec:
            """Item is a point"""
            item: Vec

            print("LINE:", item, Vec(item.x, self[item.x]))

            return Vec(item.x, self[item.x]) == item

        """Item is a segment"""
        item: Segment
        return item.a == self.a and item.b == self.b and item.c == self.c

    def __repr__(self):
        return "Line(" + \
               repr(self.a) + \
               ', ' + \
               repr(self.b) + \
               ', ' + \
               repr(self.c) + \
               ', ' + \
               repr(self.first_point) + \
               ', ' + \
               repr(self.second_point) + \
               ')'


class Segment(Line):
    """Segments and all their properties"""

    begin_point: Vec
    end_point: Vec

    def __init__(self, begin_point: Vec, end_point: Vec):
        super().__init__(begin_point, end_point)
        self.begin_point = begin_point
        """Position of the first point of the segment"""
        self.end_point = end_point
        """Position of the end of the segment"""
        self.square = self.count_square()
        """Length(square) of the segment"""

    def count_square(self) -> Float:
        """Counts length(square) of the segment"""
        return (self.end_point - self.begin_point).len

    def __contains__(self, item: Vec) -> bool:
        """Returns True if item(point) belong to the segment(is a subset of the segment) else False"""

        print("IAM:", self)
        print(f"IN: {item} : {super(Segment, self).__contains__(item)} , {(item - self.begin_point) * (item - self.end_point)}")

        return super(Segment, self).__contains__(item) and \
            (item - self.begin_point) * (item - self.end_point) < Float(0)

    # def intersection(self, other) -> Float:
    #     """Returns point of intersection of two segments"""
    #     pass


class Circle(Figure):
    """Circles and their properties"""

    def __init__(self, centre_point: Vec, radius: Float):
        self.centre_point = centre_point
        """Position of centre od circle"""
        self.radius = radius
        """Radius of circle"""
        self.square = self.count_square()
        """Square of circle"""

    def count_square(self) -> Float:
        """Counts square of the circle"""
        return self.radius ** 2 * pi

    def intersection_with_line(self, other: Line) -> tuple:
        """Returns two points of intersection of circle and Line"""

        inter1, inter2 = None, None

        desc = Float(-(4 * other.a ** 2 + 4 * other.b ** 2) * (
                self.centre_point.x ** 2 + self.centre_point.y ** 2 - self.radius ** 2 + 2 * other.c *
                self.centre_point.x / other.a + other.c ** 2 / other.a ** 2) / other.a ** 2 + (
                             -2 * other.a ** 2 * self.centre_point.y + 2 * other.a * other.b * self.centre_point.x + 2
                             * other.b * other.c) ** 2 / other.a ** 4)

        count_y = lambda D: other.a ** 2 * (D - (
                -2 * other.a ** 2 * self.centre_point.y + 2 * other.a * other.b * self.centre_point.x + 2 * other.b
                * other.c) / other.a ** 2) / (2 * other.a ** 2 + 2 * other.b ** 2)
        count_x = lambda D: -other.b * count_y(D) / other.a - other.c / other.a

        if desc == 0.0:
            """There is only one solution(point)"""
            desc = 0
            inter1 = Vec(count_x(desc), count_y(desc))
            inter2 = None
        elif desc > 0.0:
            """There are two different solutions(points)"""
            desc = sqrt(desc)
            inter1 = Vec(count_x(desc), count_y(desc))
            inter2 = Vec(count_x(-desc), count_y(-desc))

        return inter1, inter2

    def intersection_with_segment(self, other: Segment = None, position: Vec = None) -> tuple:
        """Returns up to two points of intersection of circle and Segment if they exist.
            If other is None, Segment will be started at self.centre_point and ended at 'position'.
            If one of the points is None(doesn't exist), it will be at second position(index 1) in returned tuple"""

        inter1, inter2 = None, None
        """Points of intersection"""

        print("First:", other, position)

        if other is None:
            if position is None:
                return inter1, inter2
            other = Segment(position, self.centre_point)

        print("Second:", other, position)

        intersection_line_circle = self.intersection_with_line(other)
        """Intersection of circle and line that contains Segment"""

        print("LineInss:", intersection_line_circle)

        if intersection_line_circle[0] is not None and intersection_line_circle[0] in other:
            """First point belong to Segment"""
            print(111)
            inter1 = intersection_line_circle[0]

        if intersection_line_circle[1] is not None and intersection_line_circle[1] in other:
            """Second point belong to Segment"""
            print(222)
            inter2 = intersection_line_circle[1]

        print("Points:", inter1, inter2)
        print("Ans:", tuple(sorted([inter1, inter2], key=lambda elem: 1 if elem is None else -1)))

        return tuple(sorted([inter1, inter2], key=lambda elem: 1 if elem is None else -1))

    def __contains__(self, item) -> bool:
        """Returns True if intersection of circle and item exists else False"""

        if type(item) is Vec:
            """Item is a point"""
            item: Vec
            return (self.centre_point - item).len <= self.radius

        if type(item) is Line:
            """Item is a line"""
            item: Line
            inters = self.intersection_with_line(item)
            return inters[0] is not None or inters[1] is not None

        if type(item) is Segment:
            """Item is a segment"""
            item: Segment
            return item.begin_point in self and item.end_point in self

        "Item isn't one of the written figures"
        return False

    def __repr__(self):
        return "Circle(" + \
               repr(self.centre_point) + \
               ", " + \
               repr(self.radius) + \
               ")"
