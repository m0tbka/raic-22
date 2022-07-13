"""More detailed and complicated unit properties"""

from model.unit import Unit

from strategy.float import equal_float, lt_float, le_float
from strategy.geometry import Vec, Line, Segment, Circle


class UnitAdv:
    """Unit and its properties"""

    unit: Unit
    weapons: dict
    ticks_per_seconds: float
    max_unit_forward_speed: float
    max_unit_backward_speed: float
    speed_limit_circle: Circle
    acceleration_limit_circle: Circle

    def __init__(self, unit: Unit, weapons: dict, max_unit_forward_speed: float, max_unit_backward_speed: float,
                 unit_acceleration: float, ticks_per_seconds: float):
        self.ticks_per_seconds = ticks_per_seconds
        """Ticks per seconds"""
        self.unit = unit
        """Unit itself"""
        self.weapons = weapons
        """Available weapons"""
        self.max_unit_forward_speed = max_unit_forward_speed * (
                1 - (1 - weapons[self.unit.weapon].aim_movement_speed_modifier) * self.unit.aim) / ticks_per_seconds
        """Maximal unit forward speed at this moment"""
        self.max_unit_backward_speed = max_unit_backward_speed * (
                1 - (1 - weapons[self.unit.weapon].aim_movement_speed_modifier) * self.unit.aim) / ticks_per_seconds
        """Maximal unit backward speed at this moment"""
        self.speed_limit_circle = Circle(
            (Vec() + self.unit.direction) * (max_unit_forward_speed - max_unit_backward_speed) / 2,
            (self.max_unit_forward_speed + self.max_unit_backward_speed) / 2)
        """Speed limit circle, it limits target speed"""
        self.acceleration_limit_circle = Circle(Vec() + self.unit.position + self.unit.velocity,
                                                unit_acceleration / ticks_per_seconds)
        """Limit of next speed"""

    def move_to_position(self, position: Vec) -> Vec:
        """Returns velocity vector to move in several steps to 'position'"""

        vec_unit_position = position - self.unit.position
        """Vector from unit.position to 'position'"""

        if position in self.acceleration_limit_circle:
            """'position' in acceleration_limit_circle that means TargetVector equals vec_unit_to_position"""
            return vec_unit_position

        if position in self.speed_limit_circle:
            """'position' in speed_limit_circle that means TargetVector equals 
                vector from unit.position to point(acceleration_limit_circle ⋂ 'position')"""

            intersection_acceleration_position = \
                self.acceleration_limit_circle.intersection_with_segment(position=position)[0]
            """Intersection acceleration_limit_circle with 
                vector form acceleration_limit_circle.centre_pos to 'position'"""

            return intersection_acceleration_position - self.unit.position

        """'position' is out of any of circles that means TargetVector equals some vector.. beginning at unit.position 
            and ending at some point on acceleration_limit_circle..."""

        intersection_speed_circle_vec_unit_position = \
            self.speed_limit_circle.intersection_with_segment(position=position)[0]
        """Intersection of speed_limit_circle and vec_unit_position"""

        intersection_acceleration_previous_intersection = \
            self.acceleration_limit_circle.intersection_with_segment(
                position=intersection_speed_circle_vec_unit_position)[0]
        """Intersection of acceleration_limit_circle and intersection_speed_circle_vec_unit_position"""

        return intersection_acceleration_previous_intersection - self.unit.position

    def turn_to_position(self, position: Vec) -> Vec:
        """Returns direction(vector of length 1) to turn in several steps
            centre of view_field in the direction of the position"""

        new_direction = position - self.unit.position
        """New vector direction(any length)"""

        if lt_float(new_direction.len, 0.6):
            """Checking and recounting vector length that it follows the rules"""
            new_direction *= (1 / new_direction.len)

        return new_direction
