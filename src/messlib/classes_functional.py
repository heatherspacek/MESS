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
