
from MESSaux import *

class Strategy(object):
	'''
	Instances of `Strategy()` will be `consult()`-able, and will remember which node they are on ...
	It should always return a set of inputs that 
	'''
	nodes = []
	root_node = None

	current_node = None

	def __init__(self, UID: str):
		pass

	def consult(self):
		pass

	def traverse(self):
		if (current_node is None) and (isinstance(root_node, StrategyNode)):
			root_node.traverse()

class TrivialStrategy(Strategy):
	'''
	TS1 = Strategy(base_action = "crouch", )
	'''
	sequence = None
	frame_pos_in_seq = 0

	def __init__(self, ID: str):
		super(TrivialStrategy, self).__init__(ID)

	def consult(self, controller: melee.controller.Controller):
		"""eventually this will have an internal log of which strategies are ongoing, 
		and which action is ongiong, and also where in the sequence we are."""
		"FOR NOW: just run a wavedash over and over lol"
		sequence = action_to_input_queue("wd-left-23") if np.random.randint(2) else action_to_input_queue("wd-right-23")

		input_queue_item_to_controller(sequence[frame_pos_in_seq] , controller)
		# finally, increment position(?)
		# reset the counter if we have run out of sequence, I think.
		# TODO: figure out how "yielding" will work?
		if frame_pos_in_seq == len(sequence):
			frame_pos_in_seq = 0
		else: 
			frame_pos_in_seq += 1



class StrategyNode(object):
	'''
	Nodes can be 

	It must provide information such that when Strategy calls consult(), the currently-active StrategyNode
	informs the action that is passed back...	
	'''	

	def __init__(self):
		pass
