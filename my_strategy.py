from model import UnitOrder, ActionOrder
from model.obstacle import Obstacle
from model.loot import Loot
from model.item import Item, ShieldPotions
from model.game import Game
from model.order import Order
from model.constants import Constants

from typing import Optional
from debug_interface import DebugInterface
from debugging.color import Color

from strategy.float import equal_float, lt_float, le_float
from strategy.geometry import Vec, Line, Segment, Circle
from strategy.physics import Charge, ObstacleCharge, ZoneCharge, PointCharge
from strategy.simulation import simulation_next_step, count_charge
from strategy.unit_custom import UnitAdv

from math import pi, nan
from time import time


class MyStrategy:
    ConstData: Constants
    """Constants"""

    ObstacleCharges: dict
    """Obstacle charges on the map like stones. There are charge for each uniq id"""

    UnitsCharge: dict
    """"""

    def __init__(self, constants: Constants):
        MyStrategy.ConstData = constants
        weapons = {None: 0}
        for index, weapon in enumerate(MyStrategy.ConstData.weapons):
            weapons[index] = weapon
        MyStrategy.ConstData.weapons = weapons

        MyStrategy.UnitsCharge = {}
        MyStrategy.ObstacleCharges = {}
        for obs in constants.obstacles:
            MyStrategy.ObstacleCharges[obs.id] = ObstacleCharge(Vec() + obs.position, -10_000,
                                                                obs.radius, obs.radius + 2.5)

        self.zone = ZoneCharge(Vec(), 1000, Circle(Vec(), 300), Circle(Vec(), 300))
        self.prev = [None, None]
        self.my_units = {}
        self.field_of_view_units = {}
        self.field_of_view_obstacles = {}
        self.field_of_view_shield_potions = {}

    def init(self, game: Game):
        self.zone = ZoneCharge(
            Vec(game.zone.next_center.x, game.zone.next_center.y), 20_000,
            Circle(Vec(game.zone.current_center.x, game.zone.current_center.y), game.zone.current_radius - 7),
            Circle(Vec(game.zone.next_center.x, game.zone.next_center.y), game.zone.next_radius - 7))

        self.my_units = {}
        self.field_of_view_units = {}
        self.field_of_view_obstacles = {}
        self.field_of_view_shield_potions = {}

        for unit in game.units:
            if unit.player_id == game.my_id:
                print(f"Unit {unit.id}: {unit.position}, {unit.velocity}, {unit.direction}")

                self.my_units[unit.id] = UnitAdv(unit, MyStrategy.ConstData.weapons,
                                                 MyStrategy.ConstData.max_unit_forward_speed,
                                                 MyStrategy.ConstData.max_unit_backward_speed,
                                                 MyStrategy.ConstData.unit_acceleration,
                                                 MyStrategy.ConstData.ticks_per_second)
                self.field_of_view_units[unit.id] = {}
                self.field_of_view_obstacles[unit.id] = {}
                self.field_of_view_shield_potions[unit.id] = {}

                for id_obs, obs in MyStrategy.ObstacleCharges.items():
                    obs: ObstacleCharge
                    if le_float((obs.centre_pos - unit.position).len - obs.const_circle.radius, 12):
                        self.field_of_view_obstacles[unit.id][id_obs] = obs

                if self.prev[0] is not None and (Vec() + unit.position) != self.prev[0]:
                    self.field_of_view_obstacles[unit.id]['nan'] = PointCharge(Vec() + self.prev[0], -1_00, 0.15)

                for loot in game.loot:
                    loot: Loot
                    if isinstance(loot.item, ShieldPotions):
                        self.field_of_view_shield_potions[unit.id][loot.id] = loot.item

                print("nearer_obs:", len(self.field_of_view_obstacles[unit.id]))
                print("nearer_banks:", len(self.field_of_view_shield_potions[unit.id]))

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

        for id_unit, adv_unit in self.my_units.items():
            adv_unit: UnitAdv
            unit = adv_unit.unit

            print(f"Unit {unit.id}: {unit.position}, {unit.velocity}, {unit.direction}")

            # orders[unit.id] = UnitOrder(adv_unit.move_to_position(self.zone.next_zone.centre_point), adv_unit.turn_to_position(self.zone.next_zone.centre_point), None)

            max_simulated_pos = simulation_next_step(self.field_of_view_obstacles[unit.id], self.zone,
                                                     self.field_of_view_units, adv_unit,
                                                     angle=pi / 180)
            next_pos = (adv_unit.velocity * (1 - 1 / adv_unit.velocity.len) if adv_unit.velocity.len else Vec()) + unit.position
            now_charge = count_charge(self.field_of_view_obstacles[unit.id], self.zone, self.field_of_view_units,
                                      next_pos)

            print(count_charge(self.field_of_view_obstacles[unit.id], self.zone, self.field_of_view_units,
                               max_simulated_pos), now_charge)

            self.debug_draw(debug_interface, max_simulated_pos)

            if le_float(now_charge,
                        count_charge(self.field_of_view_obstacles[unit.id], self.zone, self.field_of_view_units,
                                     max_simulated_pos)):
                print(True)
                orders[unit.id] = UnitOrder(adv_unit.move_to_position(max_simulated_pos, debug=None) * 30,
                                            adv_unit.turn_to_position(max_simulated_pos), None)

            self.prev = [self.prev[1], unit.position]

        print("get_order: --- %s seconds ---" % (time() - start_time))

        print('---' * 15)
        return Order(orders)

    def debug_draw(self, debug_interface: Optional[DebugInterface], maxxx):
        if debug_interface is None:
            return
        debug_interface.clear()
        # debug_interface.add_placed_text(Vec(0, 0.35) + self.my_units[0].position, text=f"Банки: {self.my_units[0].shield_potions}",
        #                                 alignment=Vec(0.5, 0.5), size=0.5, color=Color(0.1, 0, 0.8, 1))
        debug_interface.add_ring(maxxx, 0.01, 0.025, Color(1, 0, 1, 1))
        for id_unit, seconds_unit in self.my_units.items():
            unit: UnitAdv
            # seconds_unit = UnitAdv(unit.unit, self.ConstData.weapons, self.ConstData.max_unit_forward_speed, self.ConstData.max_unit_backward_speed, self.ConstData.unit_acceleration, 1)
            debug_interface.add_ring(seconds_unit.acceleration_limit_circle.centre_point, seconds_unit.acceleration_limit_circle.radius,
                                     0.025, Color(0, 0, 1, 0.7))
            debug_interface.add_ring(seconds_unit.speed_limit_circle.centre_point, seconds_unit.speed_limit_circle.radius, 0.025,
                                     Color(0, 1, 0, 0.7))
            debug_interface.add_segment(seconds_unit.unit.position, seconds_unit.velocity + seconds_unit.unit.position, 0.025, Color(1, 1, 0, 1))

            if self.prev[1] is not None:
                debug_interface.add_ring(self.prev[1], 1, 0.05, Color(0, 1, 1, 1))
                if self.prev[0] is not None:
                    debug_interface.add_placed_text(Vec(0, 2) + seconds_unit.unit.position, str((Vec() + self.prev[0] - self.prev[1]).len)[:min(len(str((Vec() + self.prev[0] - self.prev[1]).len)) - 1, 5)], Vec(0.5, 0.5),
                                                    0.5, Color(1, 0, 1, 1))

            for id_obs, obs in self.field_of_view_obstacles[id_unit].items():
                if isinstance(obs, PointCharge):
                    obs: PointCharge
                    debug_interface.add_ring(obs.centre_pos, 0.01, 0.05, Color(0.5, 1, 0.5, 1))
                    debug_interface.add_gradient_circle(obs.centre_pos, obs.distribution_circle.radius, Color(1, 0, 1, 0.5), Color(0, 1, 1, 0.5))
                else:
                    obs: ObstacleCharge
                    debug_interface.add_circle(obs.centre_pos, obs.const_circle.radius, Color(1, 0, 1, 0.5))
                    debug_interface.add_gradient_circle(obs.centre_pos, obs.distribution_circle.radius, Color(1, 0, 1, 0.5), Color(0, 1, 1, 0.5))

    def debug_update(self, displayed_tick: int, debug_interface: DebugInterface):
        pass

    def finish(self):
        pass


def main():
    pass


if __name__ == '__main__':
    main()
