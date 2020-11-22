import pygame as pg
import constants as CONST
import json
from node import Node
from port import Ports
from button import Button
from buttons import Button_Reset, Button_Pause, Button_Play
from io_modules import Input, Output
from rules import RuleBox

class Runner():
	def __init__(self):
		self.paused = False
		self.running = False
		self.error = False

	def reset(self, nodes, ports, io):
		for n in nodes:
			n.ACC = 0
			n.BAK = 0
			n.CURRENT_INST = 0
			n.render_text()
			n.TAGS = []

		for p in ports:
			p.CONT_A = None
			p.CONT_B = None

		for i in io:
			i.DATA_INDEX = 0
			try: 
				i.SOLUTIONS = []
			except AttributeError:
				pass

	def load_data(self, f_name, d_name):
		with open(f_name, 'r') as f:
			data = f.read()
	
		return json.loads(data)[d_name]

	def run(self):
		pg.init()
		screen = pg.display.set_mode((1900, 1000))

		clock = pg.time.Clock()

		# RULES
		r = RuleBox(1400, 40, 450, 150, self.load_data('config.json', 'rules'), title="DATA PIPE")

		# IO
		in_1 = Input(1400, 240, 100, 610, self.load_data('config.json', 'input'), 'IN')
		out_1 = Output(1550, 240, 100, 610, self.load_data('config.json', 'output'), 'OUT')
		io = [in_1, out_1]

		# NODOS
		nodo_1_1 = Node(40,  40, 350, 350)
		nodo_1_2 = Node(600, 40, 350, 350)
		nodo_2_1 = Node(40,  500, 350, 350)
		nodo_2_2 = Node(600, 500, 350, 350)
		nodes = [nodo_1_1, nodo_1_2, nodo_2_1, nodo_2_2]

		# PUERTOS
		puerto_1_1 = Ports(200, 10, 100, 100, vert=True, io_i=True, name='IN')
		puerto_1_2 = Ports(750, 10, 100, 100, vert=True)
		puerto_2_1 = Ports(525, 190, 100, 100, vert=False)
		puerto_3_1 = Ports(200, 440, 100, 100, vert=True)
		puerto_3_2 = Ports(750, 440, 100, 100, vert=True)
		puerto_4_1 = Ports(525, 640, 100, 100, vert=False)
		puerto_5_1 = Ports(200, 870, 100, 100, vert=True, io_o=True, name='OUT')
		puerto_5_2 = Ports(750, 870, 100, 100, vert=True)
		ports = [puerto_1_1, puerto_1_2, puerto_2_1, puerto_3_1, puerto_3_2, puerto_4_1, puerto_5_1, puerto_5_2]

		# ENLAZAR IO Y PUERTOS
		in_1.PORT = puerto_1_1
		out_1.PORT = puerto_5_1

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
		
		buttons = [button_reset, button_pause, button_play]

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
						else:
							pass
					
			if self.running and not self.paused and not self.error:
				in_1.feed_data()
				self.error = out_1.get_data()

				nodes[node_index].run_inst()
				pg.time.delay(500)
				if node_index+1 < len(nodes):
					node_index += 1
				else:
					node_index = 0

			#print('Pausado: ',self.paused)
			#print('Corriendo: ',self.running)
					
			screen.fill((30, 30, 30))

			r.draw(screen)
			for i in io:
				i.draw(screen)
			
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