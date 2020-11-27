import pygame as pg
import constants as CONST
import json
from node import Node
from port import Ports
from button import Button
from buttons import Button_Reset, Button_Pause, Button_Play, Button_SpeedUp
from io_modules import Input, Output
from rules import RuleBox


F_NAMES = (
	'data_pipe',
	'signal_multiplier',
	'differential_converter',
	'sequence_generator',
	'signal_compliator'
)

class Runner():
	def __init__(self):
		self.paused = False
		self.running = False
		self.error = False
		self.p_name = F_NAMES[3]+'.json'
		self.speed = 500

	def reset(self, nodes, ports, io):
		self.speed = 500

		for n in nodes:
			n.ACC = 0
			n.BAK = 0
			n.CURRENT_INST[0] = 0
			n.render_text()
			n.TAGS = []

		for p in ports:
			p.CONT_A = None
			p.CONT_B = None

		for i in io:
			for j in i:
				j.DATA_INDEX = 0
				try: 
					j.SOLUTIONS = []
				except AttributeError:
					pass
	def alternate_speed(self):
		if self.speed == 500:
			self.speed = 10
		else:
			self.speed = 500

	def load_data(self, f_name, d_name):
		with open(f_name, 'r') as f:
			data = f.read()
		return json.loads(data)[d_name]

	def load_code(self, f_name, nodes):
		with open(f_name, 'r') as f:
			data = json.loads(f.read())['code']

		for i in range(len(data)):
			#print('\r'.join(data[i]))
			nodes[i].text = '\r'.join(data[i])
			#print('\n\n',nodes[i].text)

		return nodes

	# Devuelve una lista de tuplas
	# [( (numero de inputs),  (nombres de inputs) ),
	#  ( (numero de outputs), (nombres de outputs) )]
	def load_io(self, f_name):
		with open(f_name, 'r') as f:
			data = json.loads(f.read())['io']

		ret = []
		ret.append((data['input']['number'], data['input']['names']))
		ret.append((data['output']['number'], data['output']['names']))

		#print(ret)
		return ret

	def run(self):
		pg.init()
		screen = pg.display.set_mode((1900, 1000))

		clock = pg.time.Clock()

		# RULES
		r = RuleBox(1400, 40, 450, 160, self.load_data('problems\\'+self.p_name, "rules"), title=self.load_data('problems\\'+self.p_name, 'title'))


		# NODOS
		nodo_1_1 = Node(40,  40, 350, 395)
		nodo_1_2 = Node(600, 40, 350, 395)
		nodo_2_1 = Node(40,  470, 350, 395)
		nodo_2_2 = Node(600, 470, 350, 395)
		nodes = [nodo_1_1, nodo_1_2, nodo_2_1, nodo_2_2]
		nodes = self.load_code('problems\\'+self.p_name, nodes)

		# OPCIONES DE IO
		io_options = self.load_io('problems\\'+self.p_name)
		#print(io_options[0][0])
		num_inputs = io_options[0][0]
		num_outputs = io_options[1][0]
		#print(num_inputs, num_outputs)

		nam_inputs = io_options[0][1]
		nam_outputs = io_options[1][1]
		#print(nam_inputs, nam_outputs)

		for n in nodes:
			print(id(n.CURRENT_INST))


		# PUERTOS
		puerto_1_1 = Ports(200, 10, 100, 100, vert=True, io_i=True, name=nam_inputs[0])
		if  num_inputs == 2:
			puerto_1_2 = Ports(750, 10, 100, 100, vert=True, io_i=True, name=nam_inputs[1])
		else:
			puerto_1_2 = Ports(750, 10, 100, 100, vert=True)
		puerto_2_1 = Ports(525, 190, 100, 100, vert=False)
		puerto_3_1 = Ports(200, 445, 100, 100, vert=True)
		puerto_3_2 = Ports(750, 445, 100, 100, vert=True)
		puerto_4_1 = Ports(525, 640, 100, 100, vert=False)

		puerto_5_1 = Ports(200, 870, 100, 100, vert=True, io_o=True, name=nam_outputs[0])
		if num_outputs == 2:
			puerto_5_2 = Ports(750, 870, 100, 100, vert=True, io_o=True, name=nam_outputs[1])
		else:
			puerto_5_2 = Ports(750, 870, 100, 100, vert=True, io_o=True)
		ports = [puerto_1_1, puerto_1_2, puerto_2_1, puerto_3_1, puerto_3_2, puerto_4_1, puerto_5_1, puerto_5_2]

		# IO
		inputs = []
		outputs = []
		for i in range(num_inputs):
			inputs.append(Input(1400 + 50*i, 240, 50, 720, [str(i) for i in self.load_data('problems\\'+self.p_name, 'input')[i]], nam_inputs[i]))

		for i in range(num_outputs):
			outputs.append(Output(1575 + 100*i, 240, 50, 720, [str(i) for i in self.load_data('problems\\'+self.p_name, 'output')[i]], nam_outputs[i]))
			#print(outputs[i])
		

		# ENLAZAR IO Y PUERTOS
		
		inputs[0].PORT = puerto_1_1
		if num_inputs == 2:
			inputs[1].PORT = puerto_1_2

		outputs[0].PORT = puerto_5_1
		if num_outputs == 2:
			outputs[1].PORT = puerto_5_2

		io = [inputs, outputs]


		# ENLAZAR PUERTOS Y NODOS
		nodo_1_1.UP = puerto_1_1
		nodo_1_1.RIGHT = puerto_2_1
		nodo_1_1.DOWN = puerto_3_1
		nodo_1_1.LEFT = None
		#print(nodo_1_1.RIGHT)

		nodo_1_2.UP = puerto_1_2
		nodo_1_2.RIGHT = None
		nodo_1_2.DOWN = puerto_3_2
		nodo_1_2.LEFT = puerto_2_1
		#print(nodo_1_2.LEFT)

		nodo_2_1.UP = puerto_3_1
		nodo_2_1.RIGHT = puerto_4_1
		nodo_2_1.DOWN = puerto_5_1
		nodo_2_1.LEFT = None
		#print(nodo_1_1.RIGHT)

		nodo_2_2.UP = puerto_3_2
		nodo_2_2.RIGHT = None
		nodo_2_2.DOWN = puerto_5_2
		nodo_2_2.LEFT = puerto_4_1
		#print(nodo_1_2.LEFT)

		# BOTONES
		w, h = pg.display.get_surface().get_size()
		button_reset = Button_Reset(40, h-100, 100, 75, 'RESET')
		button_pause = Button_Pause(180, h-100, 100, 75, 'PAUSE')
		button_play = Button_Play(320, h-100, 100, 75, 'PLAY')
		button_speed = Button_SpeedUp(460, h-100, 100, 75, 'SPEED')
		
		buttons = [button_reset, button_pause, button_play, button_speed]

		# MAIN
		done = False
		node_index = 0
		while not done:
			for event in pg.event.get():
				if event.type == pg.QUIT:
					done = True
				for n in nodes:
					n.handle_event(event)
					
				for b in buttons:
					aux = b.handle_event(event)
					#print(aux)
					if aux:
						if aux == 1:
							self.running = False
							self.paused = False
							self.reset(nodes, ports, io)
							node_index = 0
						elif aux == 2 and self.running:
							self.paused = True
						elif aux == 3 and not self.running:
							self.running = True
							self.paused = False
						elif aux == 4 and self.running:
							self.alternate_speed()
						else:
							pass
					
			if self.running and not self.paused and not self.error:
				for i in inputs:
					i.feed_data()
					#print(" == Input == CONT_B",i.PORT.CONT_B)
				#inputs[node_index%2].feed_data()

				print('\n\n---------------\nNodo actual: ',node_index)
				nodes[node_index].run_inst()
				pg.time.delay(self.speed)
				if node_index+1 < len(nodes):
					node_index += 1
				else:
					node_index = 0

				for o in outputs:
					self.error = o.get_data()
					#print(" == Output == CONT_B",o.PORT.CONT_B)
				#inputs[node_index%2].feed_data()

			#print('Pausado: ',self.paused)
			#print('Corriendo: ',self.running)
					
			screen.fill((30, 30, 30))
			r.draw(screen)
			
			for i in io:
				for j in i:
					j.draw(screen)
			
			for n in nodes:
				n.draw(screen)
			
			for p in ports:
				p.draw(screen)

			for b in buttons:
				b.draw(screen)
			
			pg.display.flip()
			clock.tick(30)

def main():
	r = Runner()
	r.run()

if __name__ == '__main__':
	main()
	pg.quit()