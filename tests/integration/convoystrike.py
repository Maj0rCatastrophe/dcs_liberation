from theater.caucasus import CaucasusTheater
from theater.nevada import NevadaTheater

from tests.integration.util import *

PLAYER_COUNTRY = "USA"
ENEMY_COUNTRY = "Russia"


def execute(game, player_cp, enemy_cp, departure_cp = None):
    e = ConvoyStrikeEvent(game, player_cp, enemy_cp, enemy_cp.position, PLAYER_COUNTRY, ENEMY_COUNTRY)

    departures = [departure_cp] if departure_cp else game.theater.player_points()
    for departure_cp in departures:
        if e.is_departure_available_from(departure_cp):
            enemy_cp.base.strength = 1
            for _ in range(10):
                print("{} for {} ({}) - {} ({})".format(e, player_cp, departure_cp, enemy_cp, enemy_cp.base.strength))
                e.departure_cp = departure_cp
                e.player_attacking(autoflights_for(e, PLAYER_COUNTRY))

                e.generate()
                execute_autocommit(e)
                e.generate_quick()
                execute_autocommit(e)

                enemy_cp.base.affect_strength(-0.1)


def execute_theater(theater_klass):
    print("Theater: {}".format(theater_klass))
    game, theater = init(PLAYER_COUNTRY, ENEMY_COUNTRY, theater_klass)

    total_events = 0
    while len(theater.enemy_points()) > 0:
        for player_cp, enemy_cp in theater.conflicts():
            execute(game, player_cp, enemy_cp)

            enemy_cp.captured = True

    print("Total: {}".format(total_events))


def execute_all():
    for theater_klass in [CaucasusTheater, PersianGulfTheater, NevadaTheater]:
        execute_theater(theater_klass)


if __name__ == "__main__":
    execute_all()
