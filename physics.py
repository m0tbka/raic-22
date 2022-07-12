"""Main physics: potential field, movement"""

from strategy.geometry import Vec, Line, Segment, Circle, Float


class Charge:
    """Charges, their parameters"""

    INF = Float(1e9)
    """Infinity charge"""

    quantity_charge: Float
    centre_pos: Vec
    field_rule: object

    def __init__(self, centre_pos: Vec, quantity_charge: Float,
                 field_rule=None):
        self.centre_pos = centre_pos
        """Central position of charge"""
        self.quantity_charge = quantity_charge
        """Quantity of charge that located at a central position"""
        if field_rule is None:
            field_rule = self.rule
        self.field_rule = field_rule
        """Rule that defines distribution of a charge on field"""

    def rule(self, *args):
        """Standard rule of distribution charge"""
        return self.quantity_charge

    def get_charge_at_pos(self, pos: Vec, *args):
        """Gives quantity of charge at 'pos' in terms of rule(field_rule)"""
        return self.field_rule(pos)


class ObstacleCharge(Charge):
    """Charge of obstacles"""

    obs_radius: Float

    def __init__(self, centre_pos: Vec, quantity_charge: Float, obs_radius: Float):
        super().__init__(centre_pos, quantity_charge)
        self.obs_radius = obs_radius
        """Radius of an obstacle"""
        self.const_circle = Circle(centre_pos, obs_radius)
        """Circle of constant charge"""

    def rule(self, position: Vec) -> Float:
        """Rule for obstacles"""

        if position in self.const_circle:
            """Position in obstacle -> don't need to go here"""
            return self.quantity_charge

        """Position isn't near obstacle -> position is OK"""
        return Float(0)

    def __repr__(self):
        return "ObstacleCharge(" + \
               repr(self.quantity_charge) + \
               ", " + \
               repr(self.centre_pos) + \
               ", " + \
               repr(self.obs_radius) + \
               ")"


class ZoneCharge(Charge):
    """Charge of zones"""

    current_zone: Circle
    next_zone: Circle

    def __init__(self, centre_pos: Vec, quantity_charge: Float, current_zone: Circle, next_zone: Circle):
        super().__init__(centre_pos, quantity_charge)
        self.current_zone = current_zone
        """Circle of current zone"""
        self.next_zone = next_zone
        """Circle of next zone. Center_pos equal to next_zone.center_pos"""

    def rule(self, position: Vec) -> Float:
        """Rule for zone"""

        length_pos_current = (position - self.current_zone.centre_point).len
        """Distance from position to centre of current_zone"""
        length_pos_next = (position - self.next_zone.centre_point).len
        """Distance from position to centre of next_zone"""

        if length_pos_next < self.next_zone.radius:
            """Position in next_zone -> zone is OK"""

            return self.quantity_charge

        if length_pos_current < self.current_zone.radius:
            """Position in current_zone -> need to go to the next_zone"""

            segment_center_pos = Segment(position, self.centre_pos)
            """Segment(1) from center of next_zone to position"""

            intersection_point_next = self.next_zone.intersection_with_line(segment_center_pos)
            "Intersection segment and next_zone circle"
            if intersection_point_next[0] in segment_center_pos:
                intersection_point_next = intersection_point_next[0]
            else:
                intersection_point_next = intersection_point_next[1]

            length_intersection = (position - intersection_point_next).len
            """Length of a segment from position to intersection of next_zone circle and segment(1)"""

            intersection_point_current = self.current_zone.intersection_with_line(segment_center_pos)
            """Intersection segment and current_zone circle"""
            if (intersection_point_current[0] - self.centre_pos) * (position - self.centre_pos) > 0:
                intersection_point_current = intersection_point_current[0]
            else:
                intersection_point_current = intersection_point_current[1]

            length_next_current = (intersection_point_current - intersection_point_next).len
            """Length of a segment from intersection of current_zone circle and segment(1)
                to intersection of next_zone circle and segment(1)"""

            return self.quantity_charge - (length_intersection / length_next_current) * self.quantity_charge

        """Position is out of any zone -> don't go here"""
        return -Charge.INF

    def __repr__(self):
        return "ZoneCharge(" + \
               repr(self.quantity_charge) + \
               ', ' + \
               repr(self.current_zone) + \
               ', ' + \
               repr(self.next_zone) + \
               ')'


class ProjectileCharge(Charge):
    """Charge of projectiles"""

    def __init__(self, centre_pos: Vec, quantity_charge: Float):
        super().__init__(centre_pos, quantity_charge)

