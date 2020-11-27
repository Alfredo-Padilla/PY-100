import pygame as pg
import constants as CONST
import json

class Input:
	

	def __init__(self, x, y, w, h, data, name):
		self.rect = pg.Rect(x, y, w, h)
		self.color = CONST.COLOR_INACTIVE
		self.name = name
		self.draw_name = CONST.FONT.render(name, True, self.color)
		
		self.PORT = None
		self.DATA_INDEX = 0

		self.data = data
		#print(data)
		self.txt_surface = []
		for i in range(len(data)):
			self.txt_surface.append(CONST.FONT.render(str(data[i]), True, self.color))


	def feed_data(self):
		if self.PORT.CONT_B == None and self.DATA_INDEX < len(self.data):
			self.PORT.CONT_B = self.data[self.DATA_INDEX]
			#if self.DATA_INDEX+1 < len(self.data):
			self.DATA_INDEX += 1

	'''
	def render_text(self):
		self.draw_name = CONST.FONT.render(self.name, True, self.color)
		for i in range(len(self.txt_surface)):
			self.txt_surface[i] =  CONST.FONT.render(self.data[i], 10, self.color)
	'''
	def draw(self, screen):
		pg.draw.rect(screen, self.color, self.rect, 2)
		screen.blit(self.draw_name, (self.rect.x +10, self.rect.y-30))
		for i in range(len(self.txt_surface)):
			screen.blit(self.txt_surface[i], (self.rect.x+10, self.rect.y+ 30*i+10))

class Output:

	def __init__(self, x, y, w, h, data, name):
		self.SOLUTIONS = []
		self.rect_1 = pg.Rect(x, y, w, h)
		self.rect_2 = pg.Rect(x+self.rect_1.w, y, w, h)
		self.color = CONST.COLOR_INACTIVE
		self.name = name
		self.draw_name = CONST.FONT.render(name, True, self.color)
		
		self.PORT = None
		self.DATA_INDEX = 0

		#print("Data: ",data)
		self.data = [int(i) for i in data]
		
		self.txt_surface = []
		for i in range(len(data)):
			self.txt_surface.append(CONST.FONT.render(str(data[i]), True, self.color))

		self.sol_surface = []
		for i in range(len(data)):
			self.sol_surface.append(CONST.FONT.render('', True, self.color))

	def get_data(self):
		ret = False

		#print(self.name," == solutions == ",self.SOLUTIONS)
		#print(self.name,' == get data == ',self.PORT.CONT_B,' - ',self.PORT)
		if self.PORT.CONT_B != None and self.DATA_INDEX < len(self.data):
			self.SOLUTIONS.append(self.PORT.CONT_B)
			#print(self.SOLUTIONS)
			self.PORT.CONT_B = None
			
			if self.data[self.DATA_INDEX] == self.SOLUTIONS[self.DATA_INDEX]:
				self.DATA_INDEX += 1
				self.render_text(color=CONST.COLOR_TRUE)
			else:
				#print(self.data[self.DATA_INDEX], self.SOLUTIONS[self.DATA_INDEX])
				self.render_text(color=CONST.COLOR_FALSE)
				print(' == ERROR DE SALIDA == ')
				ret = True

		return ret


	def render_text(self, color=CONST.COLOR_INACTIVE):
		self.draw_name = CONST.FONT.render(self.name, True, self.color)
		for i in range(len(self.txt_surface)):
			self.txt_surface[i] = CONST.FONT.render(str(self.data[i]), 10, self.color)

		for i in range(len(self.SOLUTIONS)):
			self.sol_surface[i] = CONST.FONT.render(str(self.SOLUTIONS[i]), 10, color)

	def draw(self, screen):
		pg.draw.rect(screen, self.color, self.rect_1, 2)
		pg.draw.rect(screen, self.color, self.rect_2, 2)
		screen.blit(self.draw_name, (self.rect_1.x +10, self.rect_1.y-30))
		for i in range(len(self.txt_surface)):
			screen.blit(self.txt_surface[i], (self.rect_1.x+10, self.rect_1.y+ 30*i+10))

		for i in range(len(self.SOLUTIONS)):
			screen.blit(self.sol_surface[i], (self.rect_2.x+10, self.rect_2.y+ 30*i+10))
		#print(self.name," SOLUTIONS ",self.SOLUTIONS)



def load_data(f_name):
	with open(f_name, 'r') as f:
		data = f.read()
	
	return json.loads(data)['input']

def main():
	pg.init()
	screen = pg.display.set_mode((1900, 1060))
	clock = pg.time.Clock()

	data = load_data('config.json')
	print(data)
	i = Input(20, 20, 100, 1000, data, 'IN')

	done = False
	while not done:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				done = True
				

		screen.fill((30, 30, 30))
		i.draw(screen)

		pg.display.flip()
		clock.tick(30)


if __name__ == '__main__':
	main()
	pg.quit()
