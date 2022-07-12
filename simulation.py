"""Simulation next position functions"""

from strategy.geometry import Vec, Line, Segment, Circle, Float
from strategy.physics import Charge, ObstacleCharge, ZoneCharge
from math import pi


def simulations_around(obsts: dict, zone: ZoneCharge, centre_pos: Vec, step: Float, angle: Float) -> Vec:
    """Simulates all positions around 'centre_pos' in 'step' and on every 'angle' in radians.
        Returns position with maximal charge"""

    step_vector = Vec(step, 0)
    angle_now = angle
    simulated_pos = centre_pos + step_vector
    maximum = [count_charge(obsts, zone, simulated_pos), simulated_pos]
    cou = 0

    while angle_now < Float(2 * pi):
        simulated_pos = centre_pos + (step_vector >> angle_now)
        new_charge = count_charge(obsts, zone, simulated_pos)
        if maximum[0] < new_charge:
            maximum = [new_charge, simulated_pos]
        angle_now += angle
        cou += 1

    # print(f"Actions: {cou}; Angle: {angle}, {angle_now}")
    return maximum[1]


def count_charge(obsts: dict, zone: ZoneCharge, position: Vec) -> Float:
    """Returns summary charge at 'position'"""

    quantity = zone.get_charge_at_pos(position)
    # print("first", position, quantity)
    for obs in obsts:
        quantity += obsts[obs].get_charge_at_pos(position)
        # print(quantity)

    return quantity
