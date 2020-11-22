import pygame as pg
import constants as CONST
from node import Node
from port import Ports
from button import Button
from buttons import Button_Reset, Button_Pause, Button_Play


class Runner():
	def __init__(self):
		self.paused = False
		self.running = False

	def reset(self, nodes, ports):
		for n in nodes:
			n.ACC = 0
			n.BAK = 0
			n.CURRENT_INST = 0
			n.render_text()
			n.TAGS = []

		for p in ports:
			p.CONT_A = None
			p.CONT_B = None

	def run(self):
		pg.init()
		screen = pg.display.set_mode((1900, 1000))

		clock = pg.time.Clock()	

		# NODOS
		nodo_1_1 = Node(40,  40, 350, 350)
		nodo_1_2 = Node(600, 40, 350, 350)
		nodo_2_1 = Node(40,  500, 350, 350)
		nodo_2_2 = Node(600, 500, 350, 350)
		nodes = [nodo_1_1, nodo_1_2, nodo_2_1, nodo_2_2]

		# PUERTOS
		puerto_1_1 = Ports(200, 10, 100, 100, vert=True)
		puerto_1_2 = Ports(750, 10, 100, 100, vert=True)
		puerto_2_1 = Ports(525, 190, 100, 100, vert=False)
		puerto_3_1 = Ports(200, 440, 100, 100, vert=True)
		puerto_3_2 = Ports(750, 440, 100, 100, vert=True)
		puerto_4_1 = Ports(525, 640, 100, 100, vert=False)
		puerto_5_1 = Ports(200, 870, 100, 100, vert=True)
		puerto_5_2 = Ports(750, 870, 100, 100, vert=True)
		ports = [puerto_1_1, puerto_1_2, puerto_2_1, puerto_3_1, puerto_3_2, puerto_4_1, puerto_5_1, puerto_5_2]

		# ENLACAR PUERTOS Y NODOS
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
							self.reset(nodes, ports)
							node_index = 0
						elif aux == 2 and self.running:
							self.paused = True
						elif aux == 3 and not self.running:
							self.running = True
							self.paused = False
						else:
							pass
					
			if self.running and not self.paused:
				#self.paused = not nodes[node_index].run_inst()
				nodes[node_index].run_inst()
				pg.time.delay(500)
				if node_index+1 < len(nodes):
					node_index += 1
				else:
					node_index = 0

			#print('Pausado: ',self.paused)
			#print('Corriendo: ',self.running)
					
			screen.fill((30, 30, 30))
			
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