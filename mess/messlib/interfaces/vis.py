# based on the gamestate

import melee.gamestate
import melee.enums
from pprint import pprint


def draw_gamestate(gamestate: melee.gamestate.GameState):
    ...

    PS_H = 10
    PS_W = 24

    # get stage constants

    # one text character is 8.5 melee units wide, 17 tall.

    # yoshis PLAT height is Y=23.45, X=(28 to 59.5)
    #    ground level is 0 (1-e4)
    #    ... but at ~39, starts sloping below 0
    #    roll to edge is (56.0, 3.50)
    #

    # total width 112 units, 17 sloped on each side.

    #     ,,,,       ,,,,
    #
    #        @>   <@
    # 0    _.---------._
    #      #############
    #      #############

    print()


def print_gamestate(gamestate: melee.gamestate.GameState):
    if gamestate.menu_state != melee.enums.Menu.IN_GAME:
        print("Not in game.")
        return

    condensed_gamestate = {
        "frame": gamestate.frame,
        "stage": gamestate.stage,
        "p1_character": gamestate.players[1].character,
        "p1_percent": gamestate.players[1].percent,
        "p1_action": gamestate.players[1].action,
        "p1_position": gamestate.players[1].position,
        "p2_character": gamestate.players[2].character,
        "p2_percent": gamestate.players[2].percent,
        "p2_action": gamestate.players[2].action,
        "p2_position": gamestate.players[2].position,
    }
    pprint(condensed_gamestate)
