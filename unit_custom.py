"""More detailed and complicated unit properties"""

from model.unit import Unit

from strategy.float import Float
from strategy.geometry import Vec, Circle


class UnitAdv:
    """Unit and its properties"""

    unit: Unit
    weapons: dict
    max_unit_forward_speed: Float
    max_unit_backward_speed: Float
    speed_limit_circle: Circle
    acceleration_limit_circle: Circle

    def __init__(self, unit: Unit, weapons: dict, max_unit_forward_speed: Float, max_unit_backward_speed: Float):
        self.unit = unit
        """Unit itself"""
        self.weapons = weapons
        """Available weapons"""
        self.max_unit_forward_speed = max_unit_forward_speed * (
                    1 - (1 - weapons[self.unit.weapon].aim_movement_speed_modifier) * self.unit.aim)
        """Maximal unit forward speed at this moment"""
        self.max_unit_backward_speed = max_unit_backward_speed * (
                    1 - (1 - weapons[self.unit.weapon].aim_movement_speed_modifier) * self.unit.aim)
        """Maximal unit backward speed at this moment"""
        self.speed_limit_circle = Circle(
            (Vec() + self.unit.direction) * (max_unit_forward_speed - max_unit_backward_speed) / 2,
            (self.max_unit_forward_speed + self.max_unit_backward_speed) / 2)
        """Speed limit circle, it limits target speed"""
        self.acceleration_limit_circle = Circle(Vec() + self.unit.position + self.unit.velocity, Float(1))
        """Limit of next speed"""

    def move_to_position(self, position: Vec):
        """Returns velocity vector to move in several steps to 'position'"""

        vec_unit_to_position = position - self.unit.position
        """Vector from unit.position to 'position'"""

