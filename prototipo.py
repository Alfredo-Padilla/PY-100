import pygame as pg
import constants as CONST
from node import Node
from port import Ports
from button import Button



def debug(nodo_1_1, nodo_1_2, i):
	# INT a ACC
	if i==0: nodo_1_1.MOV(10, nodo_1_1.ACC, 'int', 'acc')
	
	# INT a PUERTO
	elif i==1: nodo_1_2.MOV(20, 'DOWN', 'int', 'port')

	# ACC a PUERTO
	elif i==2: nodo_1_1.MOV('ACC', 'RIGHT', 'acc', 'port')

	# PUERTO a ACC
	elif i==3: nodo_1_2.MOV('LEFT', 'ACC', 'port', 'acc')

	# PUERTO a PUERTO
	elif i==4: nodo_1_1.MOV(5, 'RIGHT', 'int', 'port')
	elif i==5: nodo_1_2.MOV('LEFT', 'DOWN', 'port', 'port')

def main():
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
	puertos = [puerto_1_1, puerto_1_2, puerto_2_1, puerto_3_1, puerto_3_2, puerto_4_1, puerto_5_1, puerto_5_2]

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

	# BOTONES
	w, h = pg.display.get_surface().get_size()
	button_play = Button(40, h-100, 100, 75, 'PLAY')
	buttons = [button_play]

	# MAIN
	done = False
	paused = False
	i = 0
	while not done:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				done = True
			for n in nodes:
				n.handle_event(event)
			for b in buttons:
				b.handle_event(event)

		screen.fill((30, 30, 30))
		
		for n in nodes:
			n.draw(screen)
		
		for p in puertos:
			p.draw(screen)

		for b in buttons:
			b.draw(screen)

		# DEBUG
		if i <= 5:
			debug(nodo_1_1, nodo_1_2, i)
			i += 1
			paused = True
			

		pg.display.flip()
		clock.tick(30)
		if paused:
			pg.time.delay(1000)
			paused = False

if __name__ == '__main__':
	main()
	pg.quit()