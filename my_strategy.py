from model import UnitOrder, ActionOrder
from model.obstacle import Obstacle
from model.game import Game
from model.order import Order
from model.constants import Constants
from typing import Optional
from debug_interface import DebugInterface
from debugging.color import Color

from strategy.float import equal_float, lt_float, le_float
from strategy.geometry import Vec, Line, Segment, Circle
from strategy.physics import Charge, ObstacleCharge, ZoneCharge
from strategy.simulation import simulations_around, count_charge

from math import pi
from time import time


class MyStrategy:
    ConstData: Constants
    """Constants"""

    ObstacleCharges: dict
    """Obstacle charges on the map like stones. There are charge for each uniq id"""

    def __init__(self, constants: Constants):
        MyStrategy.ConstData = constants
        MyStrategy.ConstData.weapons = dict(
            map(lambda weapon: [constants.weapons.index(weapon)] + [weapon], constants.weapons))
        MyStrategy.ConstData.weapons.update({None: 0})
        self.zone = ZoneCharge(Vec(), 1000, Circle(Vec(), 300), Circle(Vec(), 300))
        self.my_units = []
        self.near_obstacles = {}
        MyStrategy.ObstacleCharges = {}
        for obs in constants.obstacles:
            MyStrategy.ObstacleCharges[obs.id] = ObstacleCharge(Vec(obs.position.x, obs.position.y), -10_000,
                                                                obs.radius + 1.5)

    def init(self, game: Game):
        self.zone = ZoneCharge(
            Vec(game.zone.next_center.x, game.zone.next_center.y), 1_000,
            Circle(Vec(game.zone.current_center.x, game.zone.current_center.y), game.zone.current_radius - 1),
            Circle(Vec(game.zone.next_center.x, game.zone.next_center.y), game.zone.next_radius - 1))
        self.my_units = []
        self.near_obstacles = {}
        for unit in game.units:
            if unit.player_id == game.my_id:
                self.my_units.append(unit)
                self.near_obstacles[unit.id] = {}
                for id_obs, obs in MyStrategy.ObstacleCharges.items():
                    obs: Charge
                    if le_float((obs.centre_pos - unit.position).len, 15):
                        self.near_obstacles[unit.id][id_obs] = obs
                print("nearer_obs:", len(self.near_obstacles[unit.id]))

    def get_order(self, game: Game, debug_interface: Optional[DebugInterface]) -> Order:
        start_time = time()

        print(game.current_tick)

        self.init(game)
        consts = MyStrategy.ConstData
        obsts = MyStrategy.ObstacleCharges
        orders = {}

        # print("Visible units:")
        # for unit in game.units:
        #     print(unit)
        # print("EnD")

        for unit in self.my_units:
            print(f"Unit {unit.id}: {unit.position}, {unit.velocity}, {unit.direction}")

            max_simulated_pos = simulations_around(self.near_obstacles[unit.id], self.zone,
                                                   Vec(unit.position.x, unit.position.y),
                                                   step=10 / 3, angle=pi / 360)

            now_charge = count_charge(self.near_obstacles[unit.id], self.zone, Vec(unit.position.x, unit.position.y))

            print(count_charge(self.near_obstacles[unit.id], self.zone, max_simulated_pos), now_charge)

            if lt_float(now_charge, count_charge(self.near_obstacles[unit.id], self.zone, max_simulated_pos)):
                orders[unit.id] = UnitOrder(
                    (max_simulated_pos - Vec(unit.position.x, unit.position.y)) * (consts.max_unit_forward_speed * 2),
                    (max_simulated_pos - Vec(unit.position.x, unit.position.y)) * 2, None)

        print("get_order: --- %s seconds ---" % (time() - start_time))

        print('---' * 15)
        return Order(orders)

    def debug_update(self, displayed_tick: int, debug_interface: DebugInterface):
        pass

    def finish(self):
        pass


def main():
    pass


if __name__ == '__main__':
    main()
