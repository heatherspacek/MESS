from melee.enums import Character, Button
from melee.controller import Controller


from enum import Enum
from dataclasses import dataclass, field

# TODO: come up with better category names than "abstract" and "functional"


class FacingDirection(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"


# This is probably silly.
class Comparison(Enum):
    LESSTHAN = "LESSTHAN"
    GREATERTHAN = "GREATERTHAN"


@dataclass
class Input:
    button: Button | None = None
    coordinates: tuple | None = None
    c_coordinates: tuple | None = None

    def do_input(self, controller: Controller):
        if self.button is not None:
            controller.press_button(self.button)
        if self.coordinates is not None:
            controller.tilt_analog(
                Button.BUTTON_MAIN,
                self.coordinates[0],
                self.coordinates[1]
                )
        if self.c_coordinates is not None:
            controller.tilt_analog(
                Button.BUTTON_C,
                self.c_coordinates[0],
                self.c_coordinates[1]
                )


class StochasticInput(Input):
    # Idea: normal inputs always return a "go to next input" flag, but
    # StochasticInputs can "sometimes" set that flag?
    # Unsure, coming back to it later.
    def do_input(self, controller: Controller):
        pass


@dataclass
class Action:
    sequence: list[Input]
    sequence_position: int = 0
    done_flag: bool = False

    def send_next_input(self, controller: Controller):
        # First determine whether there *is* a next input.
        if len(self.sequence) <= self.sequence_position:
            pass  # no new controller input needed
        else:
            self.input_to_controller(
                self.sequence[self.sequence_position],
                controller
                )

    def input_to_controller(self, input: Input, controller: Controller):
        input.do_input(controller)


@dataclass
class Trigger:
    associated_action: Action | None = None

    # Hacky way to keep nice things about @dataclass
    def __eq__(self, other): return False


@dataclass
class TimeTrigger(Trigger):
    time_value: int = 0


@dataclass
class DistanceTrigger(Trigger):
    distance_value: int = 0
    comparator: Comparison = Comparison.LESSTHAN

    def set_comparator(self, symbol_str: str):
        match symbol_str:
            case "<":
                self.comparator = Comparison.LESSTHAN
            case ">":
                self.comparator = Comparison.GREATERTHAN
            case _:
                raise ValueError("Unknown comparison symbol")

    def get_comparator_symbol(self):
        return ">" if self.comparator == Comparison.GREATERTHAN else "<"


@dataclass
class ActionTrigger(Trigger):
    frame_value: int = 0
    reaction_animation: None = None


@dataclass
class Response:
    pass


@dataclass  # saves us from writing an __init__.
class Strategy:
    """
    A data structure that was specified through the builder UI.
    """
    name: str = "strategy1"
    character: Character = Character.CPTFALCON  # from melee.enums
    triggers: list[Trigger] = field(default_factory=list)
    responses: list[Response] = field(default_factory=list)

    def add_new_trigger(self):
        trigger = Trigger()
        self.triggers.append(trigger)
        return trigger, len(self.triggers)

    def change_trigger_type(self, trigger_ref: Trigger, new_type_string: str):
        list_position = self.triggers.index(trigger_ref)
        match new_type_string:
            case "TimeTrigger":
                self.triggers[list_position] = TimeTrigger()
            case "DistanceTrigger":
                self.triggers[list_position] = DistanceTrigger()
            case "ActionTrigger":
                self.triggers[list_position] = ActionTrigger()

    def delete_trigger_by_index(self, index: int):
        self.triggers.pop(index)

    def delete_trigger_by_reference(self, trigger_ref: Trigger):
        self.triggers.remove(trigger_ref)
