from MESSabstract import Input, Action
from melee.enums import Button
from MESSaux import angle_to_meleecircle


class Inputs:
    """organizing class used so elements can be accessed with e.g.
    `Inputs.jump`."""
    airdodge_deep = Input(button=Button.BUTTON_R, coordinates=())
    airdodge_mid = Input(button=Button.BUTTON_R, coordinates=())
    airdodge_shallow = Input(button=Button.BUTTON_R, coordinates=())
    jump_neutral = Input(button=Button.BUTTON_X)
    null = Input()  # Serves to hold last input

    def analog_jump(self, direction_ratio: float):
        return Input(button=Button.BUTTON_X, coordinates=(0.5, ))


class Actions:
    """organizing class used so elements can be accessed with e.g.
    `Actions.wavedash_shallow`."""
    wavedash_shallow = Action(
        sequence=[
            Inputs.jump,
            Inputs.jump,
            Inputs.jump,
            Inputs.airdodge_shallow
            ]
        )

    short_hop = Action(
        sequence=[Inputs.jump,]
    )

    def wavedash_shallow(self, character or jumpsquat here?):
        sequence = []
        return Action(sequence=sequence)
