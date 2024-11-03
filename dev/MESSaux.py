import melee
import numpy as np
from MESSabstract import Strategy, Response


class StrategyPlayer():
    """
    Entity that interfaces with a Strategy, which is just a data-structure.
    """
    loaded_strategy: Strategy = None
    controller: melee.Controller = None
    # --
    current_response: Response = None

    def consult(self):
        pass


class ConsoleInterface():
    """
    object exposing callables to interface with the libmelee `console`.
    """
    running = False
    console = None
    controller1 = None
    controller2 = None
    gamestate = None

    def __init__(self, console: melee.Console):
        self.console = console

    def setup(self):
        self.console.run()
        # self.console.connect()
        print("Connecting to console...")
        if not self.console.connect():
            print("ERROR: Failed to connect to the console.")
            raise RuntimeError
        print("Console connected")
        self.controller1 = melee.Controller(console=self.console, port=1)
        self.controller2 = melee.Controller(console=self.console, port=2)
        self.controller1.connect()
        self.controller2.connect()
        self.running = True

    def step(self):
        if self.running:
            # Trying to ask for a step before setup has occurred can cause
            # unpredictable behaviour.
            self.gamestate = self.console.step()


def character_go_to_x(x: float, facing: str,
                      character_state: melee.gamestate.PlayerState,
                      controller: melee.controller.Controller):
    """
    Setup function.
    Off spawn platform, walk (close) to the given position and then pivot.
    (cant dash forward out of walk-- need to 'stand' for one frame at the
    transition. lol)
    """
    print([character_state.character, character_state.action,
           "R" if character_state.facing else "L"])

    PIVOT_SIZE = 8.0
    TARGET_SIZE = 0.7

    if abs(character_state.position.x - x) > PIVOT_SIZE:
        # walk.
        controller.tilt_analog(
            melee.enums.Button.BUTTON_MAIN,
            0.75 if (character_state.position.x - x) < 0 else 0.25, 0.5
            )
        return 0
    elif (
        (abs(character_state.position.x - x) <= PIVOT_SIZE)
        and
        (abs(character_state.position.x - x) > TARGET_SIZE)
         ):
        # dash (set up for pivot)
        if character_state.action == melee.enums.Action.STANDING:
            controller.tilt_analog(
                melee.enums.Button.BUTTON_MAIN,
                1.0 if (character_state.position.x - x) < 0 else 0.0, 0.5)
        else:
            "try and force stand-out-of-walk for one frame"
            controller.tilt_analog(
                melee.enums.Button.BUTTON_MAIN,
                0.5, 0.5)
        return 0
    else:
        # absolute difference in position is <1.5
        # either pivot or shieldstop. either way, this is last in sequence
        if (facing == "L" and character_state.facing is False) or (
                facing == "R" and character_state.facing is True):
            controller.press_button(melee.enums.Button.BUTTON_L)
        else:
            controller.tilt_analog(
                melee.enums.Button.BUTTON_MAIN,
                0.0 if character_state.facing else 1.0, 0.5)
        print("might be done!")
        print([character_state.position.x, x])
        return 1  # i.e. this is last in sequence.


def jumpsquat(character: melee.enums.Character):
    match character:
        case (melee.enums.Character.FALCO |
              melee.enums.Character.JIGGLYPUFF |
              melee.enums.Character.DK):
            return 5
        case (melee.enums.Character.CPTFALCON |
              melee.enums.Character.MARTH |
              melee.enums.Character.DOC):
            return 4
        case (melee.enums.Character.FOX |
              melee.enums.Character.PIKACHU |
              melee.enums.Character.SHEIK):
            return 3


def angle_to_meleecircle(angle: int, quadrant: str):
    """returns an X and Y that are on the rim of the unit circle.
    input in degrees. intended for use with DI and WDs"""
    if (angle > 90.0) or (angle < 0.0):
        print("error in angle_to_meleecircle: need 0<angle<90 for clarity")
        raise
    # numpy likes radians...
    angle_radians = np.pi * angle/180.0
    xc_u = np.cos(angle_radians)
    yc_u = np.sin(angle_radians)

    "next, map 0..1 to 0.5..1"
    match quadrant:
        case "UL":
            xc = 0.5 - xc_u/2
            yc = 0.5 + yc_u/2
        case "UR":
            xc = 0.5 + xc_u/2
            yc = 0.5 + yc_u/2
        case "BL":
            xc = 0.5 - xc_u/2
            yc = 0.5 - yc_u/2
        case "BR":
            xc = 0.5 + xc_u/2
            yc = 0.5 - yc_u/2
        case _:
            print("error in angle_to_meleecircle: " +
                  "specified an invalid quadrant")
            raise
    return (xc, yc)


def action_to_input_queue(
        action: str,
        parameter: int = 0,
        character: melee.enums.Character = 1):
    '''
    Gets called once a strategy decision is made...
    The parent caller will do something different depending on how long the
    input_queue ends up being.
    (Some inputs are repeated simple inputs e.g. crouch, and some inputs are a
    fixed sequence e.g. JC grab.)
    '''
    input_queue = []
    match action:
        case "crouch":
            pass
        case "dash-jc-grab":
            pass
        case "wd-left-23":
            input_queue.extend("jump" * jumpsquat(character))
            input_queue.append("airdodge-left-23")
        case "wd-right-23":
            input_queue.extend("jump" * jumpsquat(character))
            input_queue.append("airdodge-right-23")

    print(input_queue)
    return input_queue


def input_queue_item_to_controller(
        queue_entry: str,
        controller: melee.controller.Controller
        ):
    # presumably we are using something resembling an internal encoding
    # format... let's decode that here?
    # dunno if this is overcomplicating things.
    match queue_entry:
        case "airdodge-left-23":
            controller.press_button(melee.enums.Button.BUTTON_R)
            (xc, yc) = angle_to_meleecircle(23, "BL")
            controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, xc, yc)
        case "airdodge-right-23":
            controller.press_button(melee.enums.Button.BUTTON_R)
            (xc, yc) = angle_to_meleecircle(23, "BR")
            controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, xc, yc)
