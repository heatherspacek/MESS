from messlib.classes_abstract import Strategy

# --
import melee


class StrategyPlayer:
    """
    Entity that interfaces with a Strategy, which is just a data-structure.
    Holds a `controller`.
    """

    loaded_strategy: Strategy = None
    controller: melee.Controller = None
    # --
    current_action = None

    def add_trigger(self):
        raise NotImplementedError("use .loaded_strategy.add_trigger")

    def connect_controller(self, controller):
        self.controller = controller

    def perform_input(
        self,
    ):
        pass

    def step(self, gamestate: melee.gamestate.GameState):
        """replacing the old 'consult' paradigm; we just do one new controller
        input per frame."""

        if self.loaded_strategy is None:
            return

        # 0. consult triggers to see if (for example) an ongoing action got
        # interrupted by something. e.g. we went for grab but noticed it
        # whiffed, and now we are holding down to asdi down punish.

        for trigger in self.loaded_strategy.triggers:
            if trigger.check_triggered(gamestate):
                self.current_action = trigger.response
                break

        # 1. if in the middle of an ongoing action (eg. wavedash inputs) just
        # do the next input in the sequence.
        if self.current_action is not None:
            self.controller

        # 2. check remainder of Triggers


class ConsoleInterface:
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
        self.controller1 = melee.Controller(
            console=console, port=1, type=melee.ControllerType.GCN_ADAPTER
        )
        self.controller2 = melee.Controller(
            console=console, port=2, type=melee.ControllerType.STANDARD
        )

    def setup_oneplayer(self):
        self.console.run()
        print("Connecting to console...")
        if not self.console.connect():
            print("ERROR: Failed to connect to the console.")
            raise RuntimeError
        print("Console connected.")
        if not self.controller2.connect():
            print("ERROR: CPU controller failed to connect.")
            raise RuntimeError
        print("CPU controller connected.")
        self.running = True

    def step(self):
        if self.running:
            # Trying to ask for a step before setup has occurred can cause
            # unpredictable behaviour.
            self.gamestate = self.console.step()
