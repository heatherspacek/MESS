
import melee
from melee.enums import Character

import MESSaux
from dataclasses import dataclass

@dataclass
class Trigger:
	pass

@dataclass
class Response:
	pass
	
@dataclass # saves us from writing an __init__.
class Strategy:
	"""
	A data structure that was specified through the builder UI.
	"""
	character: Character
	triggers: list[Trigger]
	responses: list[Response]

class TrivialStrategy(Strategy):
	
	sequence = None
	frame_pos_in_seq = 0

	def consult(self, controller: melee.controller.Controller):
		"""eventually this will have an internal log of which strategies are ongoing, 
		and which action is ongiong, and also where in the sequence we are."""
		"FOR NOW: just run a wavedash over and over lol"
		sequence = MESSaux.action_to_input_queue("wd-left-23") if np.random.randint(2) else action_to_input_queue("wd-right-23")

		input_queue_item_to_controller(sequence[frame_pos_in_seq] , controller)
		# finally, increment position(?)
		# reset the counter if we have run out of sequence, I think.
		# TODO: figure out how "yielding" will work?
		if frame_pos_in_seq == len(sequence):
			frame_pos_in_seq = 0
		else: 
			frame_pos_in_seq += 1

