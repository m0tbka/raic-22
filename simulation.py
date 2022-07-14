"""Simulation next position functions"""

from strategy.float import equal_float, lt_float, le_float
from strategy.geometry import Vec, Line, Segment, Circle
from strategy.physics import Charge, ObstacleCharge, ZoneCharge
from strategy.unit_custom import UnitAdv

from math import pi


def simulation_next_step(obsts: dict, zone: ZoneCharge, units: dict, my_unit: UnitAdv, angle: float) -> Vec:
    """"""

    step_vector = Vec(my_unit.acceleration_limit_circle.radius, 0)
    angle_now = angle
    simulated_pos = my_unit.acceleration_limit_circle.centre_point + step_vector
    maximum = [count_charge(obsts, zone, units, simulated_pos), simulated_pos]

    while lt_float(angle_now, 2 * pi):
        simulated_pos = my_unit.acceleration_limit_circle.centre_point + (step_vector >> angle_now)

        new_charge = count_charge(obsts, zone, units, simulated_pos)

        if lt_float(maximum[0], new_charge):
            maximum = [new_charge, simulated_pos]

        angle_now += angle

    print(maximum)

    return maximum[1]


def count_charge(obsts: dict, zone: ZoneCharge, units: dict, position: Vec) -> float:
    """Returns summary charge at 'position'"""

    quantity = zone.get_charge_at_pos(position)
    for obs in obsts:

        quantity += obsts[obs].get_charge_at_pos(position)

    return quantity
