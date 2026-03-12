from .host import Host
# from melee.enums import Stage
from melee.enums import Button
from ..data_structures.helpers import angle_to_meleecircle, jumpsquat


def goto(x1: float, x2: float, platform1: bool, platform2: bool, host: Host):
    # TODO: validation checks --
    # . are the x positions actually on stage?
    # . are the platform x positions actually on platform?
    # . did user ask for a platform position on FD?

    # TODO: platform setup :)) I'm skipping over it!!

    gs = host.console.step()
    # stage = gs.stage
    js1 = jumpsquat(gs.players[1].character)
    js2 = jumpsquat(gs.players[2].character)

    def xdiffs(gs):
        return (x1 - gs.players[1].position.x, x2 - gs.players[2].position.x)

    p1states = []
    for wd_count in range(25):
        p1_xdiff, p2_xdiff = xdiffs(gs)
        for internal_count in range(20):
            if internal_count == 0:
                host.p1.simple_press(0.5, 0.5, Button.BUTTON_X)
                host.p2.simple_press(0.5, 0.5, Button.BUTTON_X)
                host.p1.flush()
                host.p2.flush()

            if internal_count == js1 + 2:
                quad = "BL" if p1_xdiff < 0 else "BR"
                angle = 30 if abs(p1_xdiff) > 12 else 72
                xc, yc = angle_to_meleecircle(angle, quad)
                host.p1.simple_press(xc, yc, Button.BUTTON_R)
                host.p1.flush()
            if internal_count == js2 + 2:
                quad = "BL" if p2_xdiff < 0 else "BR"
                angle = 30 if abs(p2_xdiff) > 12 else 72
                xc, yc = angle_to_meleecircle(angle, quad)
                host.p2.simple_press(xc, yc, Button.BUTTON_R)
                host.p2.flush()

            # if internal_count == 12:
            #     from .vis import print_gamestate
            #     print_gamestate(gs)

            gs = host.console.step()
            p1states.append(gs.players[1].action)

        print([d for d in xdiffs(gs)])
        if all(abs(d) < 1 for d in xdiffs(gs)):
            return

    breakpoint()
    raise RuntimeError(
        "Couldn't get to the specified init position in 25 wavedashes. "
        "Check for impossible position?"
    )
