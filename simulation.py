"""Simulation next position functions"""

from strategy.float import equal_float, lt_float, le_float
from strategy.geometry import Vec, Line, Segment, Circle
from strategy.physics import Charge, ObstacleCharge, ZoneCharge

from math import pi


def simulations_around(obsts: dict, zone: ZoneCharge, centre_pos: Vec, step: float, angle: float) -> Vec:
    """Simulates all positions around 'centre_pos' in 'step' and on every 'angle' in radians.
        Returns position with maximal charge"""

    step_vector = Vec(step, 0)
    angle_now = angle
    simulated_pos = centre_pos + step_vector
    maximum = [count_charge(obsts, zone, simulated_pos), simulated_pos]

    cou = 0

    while lt_float(angle_now, 2 * pi):
        simulated_pos = centre_pos + (step_vector >> angle_now)
        new_charge = count_charge(obsts, zone, simulated_pos)
        if lt_float(maximum[0], new_charge):
            maximum = [new_charge, simulated_pos]
        angle_now += angle
        cou += 1

    print(f"Actions: {cou}; Angle: {angle}, {angle_now}")
    return maximum[1]


def count_charge(obsts: dict, zone: ZoneCharge, position: Vec) -> float:
    """Returns summary charge at 'position'"""

    quantity = zone.get_charge_at_pos(position)
    for obs in obsts:
        quantity += obsts[obs].get_charge_at_pos(position)

    return quantity
