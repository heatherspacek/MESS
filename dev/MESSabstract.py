
from melee.enums import Character, Button
from melee.controller import Controller

from dataclasses import dataclass, field


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
    def has_been_triggered(self):
        raise NotImplementedError


class TimeTrigger(Trigger):
    def has_been_triggered(self):
        print("does something here")


class DistanceTrigger(Trigger):
    pass


class ActionTrigger(Trigger):
    pass


@dataclass
class Response:
    pass


@dataclass  # saves us from writing an __init__.
class Strategy:
    """
    A data structure that was specified through the builder UI.
    """
    name: str
    character: Character = Character.CPTFALCON  # from melee.enums
    triggers: list[Trigger] = field(default_factory=list)
    responses: list[Response] = field(default_factory=list)

    def add_trigger(self, trigger: Trigger):
        self.triggers.append(trigger)
