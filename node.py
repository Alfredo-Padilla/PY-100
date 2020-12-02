import pygame as pg
import constants as CONST
import instructions as INST
from pygame_utils import wrapline



# Init
pg.init()
screen = pg.display.set_mode((CONST.SCREEN_W, CONST.SCREEN_H))

# Constantes
'''
COLOR_INACTIVE = pg.Color('darkgrey')
COLOR_ACTIVE = pg.Color('white')
FONT = pg.font.Font(None, 32)
FONT_SM = pg.font.Font(None, 26)
N_LINEAS = 10
'''

# Clase Nodo
class Node:
	def __init__(self, x, y, w, h, text='', demo_mode=False):
		# Puertos
		self.UP = None
		self.RIGHT = None
		self.DOWN = None
		self.LEFT = None

		# Registros
		self.ACC = 0
		self.BAK = 0

		self.TAGS = []
		self.CURRENT_INST = 0


		self.active = False
		self.demo_mode = demo_mode
		self.rect = pg.Rect(x, y, w, h)
		
		self.color = CONST.COLOR_INACTIVE
		self.text = text
		self.txt_surface = []
		for i in range(CONST.N_LINEAS):
			try:
				self.txt_surface.append( CONST.FONT_SM.render(text[i], 1, self.color))
				#print('Hay texto ',text[i])
			except IndexError:
				self.txt_surface.append( CONST.FONT_SM.render('', 1, self.color))
				#print('NO hay texto')
				
		#print(self.text)

		w_reg = int(w/5)
		h_reg = int(h/5)
		
		# ACC
		self.acc = pg.Rect(x+w, y, w_reg, h_reg)
		self.acc_title = CONST.FONT_SM.render('ACC', True, self.color)
		self.acc_surface = CONST.FONT_SM.render(str(self.ACC), True, self.color)
		
		# BAK
		self.bak = pg.Rect(x+w, y+h_reg, w_reg, h_reg)
		self.bak_title = CONST.FONT_SM.render('BAK', True, self.color)
		self.bak_surface = CONST.FONT_SM.render(str(self.BAK), True, self.color)

		# LAST
		self.last = pg.Rect(x+w, y+(h_reg*2), w_reg, h_reg)
		self.last_title = CONST.FONT_SM.render('LAST', True, self.color)
		self.last_surface = CONST.FONT_SM.render('N/A', True, self.color)

		# MODE
		self.mode = pg.Rect(x+w, y+(h_reg*3), w_reg, h_reg)
		self.mode_title = CONST.FONT_SM.render('MODE', True, self.color)
		self.mode_surface = CONST.FONT_SM.render('IDLE', True, self.color)

		# IDLE
		self.idle = pg.Rect(x+w, y+(h_reg*4), w_reg, h_reg)
		self.idle_title = CONST.FONT_SM.render('IDLE', True, self.color)
		self.idle_surface = CONST.FONT_SM.render('0%', True, self.color)
	
	def get_text(self):
		if self.demo_mode:
			ret = [i.strip() for i in wrapline(self.text.upper(), CONST.FONT_SM, 800)]
			return [i.strip() for i in wrapline(self.text.upper(), CONST.FONT_SM, 400)]
		else:
			ret = [i.strip() for i in wrapline(self.text.upper(), CONST.FONT_SM, 250)]
		return ret

	def render_text(self, color=None):
		if color == None:
			color = self.color

		aux = self.get_text()
		#print(aux)
		aux = self.text.split('\r')
		#print(aux)
		#print(type(aux), aux)
		for l in range(len(self.txt_surface)):
			try:
				self.txt_surface[l] = CONST.FONT.render(aux[l], 10, color)  
			except IndexError:
				self.txt_surface[l] = CONST.FONT.render('', 10, color)

		#print(aux)
		return aux

	def get_line(self, line):
		return self.get_text()[line]

	def render_line(self, line, color=None):
		if color == None:
			color = self.color
		try:
			self.txt_surface[line] = CONST.FONT.render(self.get_line(line), 10, color)  
		except IndexError:
			self.txt_surface[line] = CONST.FONT.render('', 10, color)

	# EVENTOS
	def handle_event(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
			else:
				self.active = False
			self.color = CONST.COLOR_ACTIVE if self.active else CONST.COLOR_INACTIVE
		
		elif event.type == pg.KEYDOWN and self.active:
			if event.key == pg.K_RETURN:
				self.text += event.unicode
				#print(self.text)
			elif event.key == pg.K_BACKSPACE:
				self.text = self.text[:-1]
			else:
				self.text += event.unicode.upper()
			
		self.render_text()
		self.register_tags()
		self.clean_tags()


	def draw(self, screen):
		#self.render_text()
		for i in self.txt_surface:
			if i == self.CURRENT_INST:
				self.txt_surface[i] = self.render_line(i, CONST.COLOR_RUNNING)
			screen.blit(i, (self.rect.x+10, self.rect.y+30*self.txt_surface.index(i)+10 ) )
		pg.draw.rect(screen, self.color, self.rect, 2)
		
		# ACC
		pg.draw.rect(screen, self.color, self.acc, 2)
		screen.blit(self.acc_title, (self.acc.x+15, self.acc.y+10))
		self.acc_surface = CONST.FONT_SM.render(str(self.ACC), True, self.color)
		screen.blit(self.acc_surface, (self.acc.x+30, (self.acc.y + self.acc.h-30) ))

		# BAK
		pg.draw.rect(screen, self.color, self.bak, 2)
		screen.blit(self.bak_title, (self.bak.x+15,self.bak.y+10))
		self.bak_surface = CONST.FONT_SM.render(str(self.BAK), True, self.color)
		screen.blit(self.bak_surface, (self.bak.x+30, (self.bak.y + self.bak.h-30) ))

		# LAST
		pg.draw.rect(screen, self.color, self.last, 2)
		screen.blit(self.last_title, (self.last.x+15, self.last.y+10))
		screen.blit(self.last_surface, (self.last.x+20, (self.last.y + self.last.h-30) ))

		# MODE
		pg.draw.rect(screen, self.color, self.mode, 2)
		screen.blit(self.mode_title, (self.mode.x+10, self.mode.y+10))
		screen.blit(self.mode_surface, (self.mode.x+15, (self.mode.y + self.mode.h-30) ))

		# IDLE
		pg.draw.rect(screen, self.color, self.idle, 2)
		screen.blit(self.idle_title, (self.idle.x+15, self.idle.y+10))
		screen.blit(self.idle_surface, (self.idle.x+25, (self.idle.y + self.idle.h-30) ))


	def next_inst(self):
		if self.CURRENT_INST+1 < len(self.text.split('\r')):
			self.CURRENT_INST += 1
		else:
			self.CURRENT_INST = 0

	def run_inst(self):
		print('run_inst()',id(self))
		ret = True

		#print(self.TAGS)
		insts = self.render_text()
		if len(insts) < self.CURRENT_INST+1:
			self.CURRENT_INST = 0
		print('Inst actual: ',self.CURRENT_INST)
		if insts[self.CURRENT_INST] != '':
			print("\nInstrucciones: ",insts)
			print("Inst actual:", self.CURRENT_INST)
			if insts[self.CURRENT_INST] in self.TAGS:
				print('Ignorando el tag')
				self.next_inst()
			else:
				print(str(self.CURRENT_INST)+': '+insts[self.CURRENT_INST])
				ret = INST.inst_launcher(self, insts[self.CURRENT_INST])
				if ret:
					self.render_line(self.CURRENT_INST, color=CONST.COLOR_RUNNING)
					self.next_inst()

		return ret

	def register_tags(self):
		txt = self.get_text()

		for line in txt:
			if len(line) > 0:
				if line[-1] == ':':
					aux = line.split(' ')[-1]
					if aux not in self.TAGS:
						self.TAGS.append(aux)
						#print(aux)

	def clean_tags(self):
		txt = ' '.join(self.get_text())
		if len(self.TAGS) > 0:
			for tag in self.TAGS:
				if tag not in txt:
					self.TAGS.remove(tag)

	def move_to_port(self, port, cont):
		ret = True
		if port=='UP' and self.UP.CONT_A==None:
			self.UP.CONT_A = int(cont)
			print("- - - moviendo a UP: ",cont)
			print("- - - nuevo contenido de UP: ",self.UP.CONT_A)
		
		elif port=='RIGHT' and self.RIGHT.CONT_A==None:
			self.RIGHT.CONT_A = int(cont)
			print("- - - moviendo a RIGHT: ",cont)
			print("- - - nuevo contenido de RIGHT: ",self.RIGHT.CONT_A)
		
		elif port=='DOWN' and self.DOWN.CONT_B==None:
			self.DOWN.CONT_B = int(cont)
			print("- - - moviendo a DOWN: ",cont)
			print("- - - nuevo contenido de DOWN: ",self.DOWN.CONT_B)
		
		elif port=='LEFT' and self.LEFT.CONT_B==None:
			self.LEFT.CONT_B = int(cont)
			print("- - - moviendo a LEFT: ",cont)
			print("- - - nuevo contenido de LEFT: ",self.LEFT.CONT_B)
		
		elif port=='NIL':
			print("- - - moviendo a NIL: ",cont)

		else:
			ret = False
		
		return ret
		#print("move_to_port: ", cont)
	
	def move_from_port(self, port):
		ret = False
		print('- - - Lanzando move_from_port() con puerto:', port)

		#if self.RIGHT!=None:
			#print("CONT B: ",self.RIGHT.CONT_A)
		if port == 'UP' and self.UP.CONT_B!=None:
			ret = self.UP.CONT_B
			self.UP.CONT_B = None
			print("- - - moviendo de UP: ",ret)
			print("- - - nuevo contenido de UP: ",self.UP.CONT_B)
		
		elif port == 'RIGHT' and self.RIGHT.CONT_B!=None:
			print()
			ret = self.RIGHT.CONT_B
			self.RIGHT.CONT_B = None
			print("- - - moviendo de RIGHT: ",ret)
			print("- - - nuevo contenido de RIGHT: ",self.RIGHT.CONT_B)
		
		elif port == 'DOWN' and self.DOWN.CONT_A!=None:
			ret = self.DOWN.CONT_A
			self.DOWN.CONT_A = None
			print("- - - moviendo de DOWN: ",ret)
			print("- - - nuevo contenido de DOWN: ",self.DOWN.CONT_A)
		
		elif port == 'LEFT' and self.LEFT.CONT_A!=None:
			ret = self.LEFT.CONT_A
			self.LEFT.CONT_A = None
			print("- - - moviendo de LEFT: ",ret)
			print("- - - nuevo contenido de LEFT: ",self.LEFT.CONT_A)

		elif port == 'NIL':
			ret = 0
			print("- - - moviendo de NIL: ",0)

		#print("move_from_port: ",ret)
		return ret

	def dest_port_is_empty(self, port):
		ret = False

		if port == 'UP':
			if self.UP.CONT_A == None:
				ret = True
		elif port == 'RIGHT':
			if self.RIGHT.CONT_A == None:
				ret = True
		elif port == 'DOWN': 
			if self.DOWN.CONT_B == None:
				ret = True
		elif port == 'LEFT': 
			if self.LEFT.CONT_B == None:
				ret = True
		elif port == 'NIL':
				ret = True

		print('dest_port_is_empty() -> ',ret)
		return ret
	
	def org_port_is_empty(self, port):
		ret = False

		if port=='UP': 
			if self.UP.CONT_B == None:
				ret = True
		elif port=='RIGHT': 
			if self.RIGHT.CONT_B == None:
				ret = True
		elif port=='DOWN': 
			if self.DOWN.CONT_A == None:
				ret = True
		elif port=='LEFT': 
			if self.LEFT.CONT_A == None:
				ret = True

		print('org_port_is_empty() -> ',ret)
		return ret
	# ======= #
	# MEMORIA #
	# ======= #
	# MOV 
	def MOV(self, org, dst, t_org, t_dst):
		ret = True
	
		if t_org == 'int':
			if t_dst == 'acc':
				self.ACC = int(org)
				print("- - - nuevo contenido de ACC: ",self.ACC)
			elif t_dst == 'port':
				ret = self.move_to_port(dst, org)
		
		elif t_org == 'acc':
			ret = self.move_to_port(dst, self.ACC)
		
		elif t_org == 'port' and not self.org_port_is_empty(org):
			if t_dst == 'acc':
				aux = self.move_from_port(org)
				if aux != False:
					self.ACC = aux
					print("- - - nuevo contenido de ACC: ",self.ACC)
				else:
					ret = False
			elif self.dest_port_is_empty(dst):
				aux = self.move_from_port(org)
				if aux and t_dst == 'port':
					ret = self.move_to_port(dst, int(aux))
				else:
					ret = False

			else:
				ret = False
		else:
			ret = False
		
		return ret

	# SWP
	def SWP(self):
		aux = self.ACC
		self.ACC = self.BAK
		self.BAK = aux
		return True

	def SAV(self):
		self.BAK = self.ACC
		return True

	# =========== #
	# OPERACIONES #
	# =========== #
	# ADD
	def ADD(self, org, t_org):
		ret = True
		
		self.ACC = int(self.ACC)
		if t_org == 'int':
			self.ACC += int(org)
		elif t_org == 'acc':
			self.ACC += int(self.ACC)
		elif t_org == 'port':
			if self.dest_port_is_empty(org):
				aux = self.move_from_port(org)
				print('Sumando desde puerto: ', aux)
				if aux != False:
					self.ACC += int(aux)
				else:
					ret = False
			else:
				ret = True
		else:
			ret = False
		
		return ret
	
	# SUB
	def SUB(self, org, t_org):
		ret = True

		self.ACC = int(self.ACC)
		if t_org == 'int':
			self.ACC -= int(org)
		elif t_org == 'acc':
			self.ACC -= int(org)
		elif t_org == 'port':
			aux = self.move_from_port(org)
			#print("SUB: ", aux)
			if aux:
				self.ACC -= int(aux)
			else:
				ret = False
		else:
			ret = False
		
		return ret

	# NEG
	def NEG(self):
		self.ACC = int(self.ACC) * -1
		print(self.ACC)
		return True


	# ====== #
	# SALTOS #
	# ====== #
	# JMP
	def JMP(self, i):
		ret = False

		if i == 0:
			self.CURRENT_INST = 0
		elif i < len(self.text):
			self.CURRENT_INST = i-1
		else:
			self.CURRENT_INST = 0
			ret = True

		return ret

	# JEZ
	def JEZ(self, i):
		ret = False
		
		if int(self.ACC) == 0:
			if i < len(self.text):
				self.CURRENT_INST = i-1
			else:
				self.CURRENT_INST = 0
			
			ret = True

		return ret

	# JNZ
	def JNZ(self, i):
		ret = False
		
		if int(self.ACC) != 0:
			if i == 0:
				self.CURRENT_INST = 0
			elif i < len(self.text):
				self.CURRENT_INST = i-1
			else:
				self.CURRENT_INST = 0

			ret = True

		return ret

	# JGZ
	def JGZ(self, i):
		ret = False
		
		if int(self.ACC) > 0:
			if i < len(self.text):
				self.CURRENT_INST = i-1
			else:
				self.CURRENT_INST = 0

			ret = True

		return ret

	# JLZ
	def JLZ(self, i):
		ret = False
		
		if int(self.ACC) < 0:
			if i < len(self.text):
				self.CURRENT_INST = i-1
			else:
				self.CURRENT_INST = 0

			ret = True

		return ret


def main():
	clock = pg.time.Clock()
	node1 = Node(10,  10, 350, 350)
	node2 = Node(500, 10, 350, 350)
	node3 = Node(10,  410, 350, 350)
	node4 = Node(500, 410, 350, 350)
	
	nodes = [node1, node2, node3, node4]
	
	done = False
	while not done:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				done = True
			for n in nodes:
				n.handle_event(event)
				

		screen.fill((30, 30, 30))
		for n in nodes:
			n.draw(screen)

		pg.display.flip()
		clock.tick(30)

if __name__ == '__main__':
	main()
	pg.quit()