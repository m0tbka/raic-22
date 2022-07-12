class Float(float):
    EPS = 1e-9

    def __eq__(self, other):
        """self == other"""
        return abs(self - other) < Float.EPS

    def __ne__(self, other):
        """self != other"""
        return not self == other

    def __lt__(self, other):
        """self < other"""
        return self - other < Float.EPS

    def __le__(self, other):
        """self <= other"""
        return self - other <= Float.EPS

    def __gt__(self, other):
        """self > other"""
        return self - other > Float.EPS

    def __ge__(self, other):
        """self >= other"""
        return self - other >= Float.EPS
