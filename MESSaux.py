from enum import Enum
import melee

def character_go_to_x(x, character_state, controller):
	"Setup function."
	if abs(character_state.position.x - x) > 1:
		controller.tilt_analog(melee.enums.Button.BUTTON_MAIN, int((character_state.position.x - x)<0), 0.5)
		print(character_state.position.x)
		return -1

def action_to_input_queue(action: str, parameter: int = 0):
	'''
	Gets called once a strategy decision is made... 
	The parent caller will do something different depending on how long the input_queue ends up being.
	(Some inputs are repeated simple inputs e.g. crouch, and some inputs are a fixed sequence e.g. JC grab.)
	'''
	input_queue = []
	match action:
		case "crouch":
			pass
		case "dash-jc-grab":
			pass
	return input_queue

def input_queue_to_controller(queue: list, controller: melee.controller.Controller):
	# presumably we are using something resembling an internal encoding format... let's decode that here?
	# dunno if this is overcomplicating things.
	pass


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

	def consult(self):
		return 

class StrategyNode(object):
	'''
	Nodes can be 

	It must provide information such that when Strategy calls consult(), the currently-active StrategyNode
	informs the action that is passed back...	
	'''	

	def __init__(self):
		pass


class stageEnum(Enum):
	FD = 0x20



def compose_codestring():
	S1 = """
$pepiscode [hiatus heather]

C21B148C 00000025
3C608048 60630530
48000021 7C8802A6
38A000F0 3D808000
618C31F4 7D8903A6
4E800421 480000F8
4E800021 2A08024C
20000000 000000FF
00000020 000001E0
00000000 00000000
00000000 FFFFFFFF
FFFFFFFF 00000000
3F800000 3F800000
3F800000 00000000
00000000 00000000
00000000 00000000
00000000 00000000
00000000 00000000
00000000 09000400
00FF0000 09007800
40000401 00000000
00000000 3F800000
3F800000 3F800000
09000400 00FF0000
09007800 40000401
00000000 00000000
3F800000 3F800000
3F800000 09030400
00FF0000 09007800
40000401 00000000
00000000 3F800000
3F800000 3F800000
09030400 00FF0000
09007800 40000401
00000000 00000000
3F800000 3F800000
3F800000 BB610014
60000000 00000000
		"""
	return S1 
