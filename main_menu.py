import os
import pygame as pg
import constants as CONST
from menu import Menu

pg.init()
screen = pg.display.set_mode((CONST.SCREEN_W, CONST.SCREEN_H))

class MainMenu:
	def __init__(self):
		MARGIN = 290
		self.rect = pg.Rect(MARGIN, MARGIN, CONST.SCREEN_W-MARGIN*2, CONST.SCREEN_H-MARGIN*2)
		self.color_a = CONST.COLOR_ACTIVE
		self.color_i = CONST.COLOR_INACTIVE
		self.r = None

		self.menu_index = 0
		self.text_area = []
		self.text = []
		self.f_names = []
		'''
		problems = self.find_problems()
		for k in problems.keys():
			self.text_area.append( CONST.FONT_LG.render(problems[k], 1, self.color_i) )
			self.text_area[self.menu_index] = CONST.FONT_LG.render(problems[k], 1, self.color_a)
			self.text.append(problems[k])
			self.f_names.append(k)
		'''
		options = (
			'1 - DEMO_MODE',
			'2 - PLAY_MODE')
		for o in options:
			self.text_area.append( CONST.FONT_LG.render(o, 1, self.color_i) )
			self.text_area[self.menu_index] = CONST.FONT_LG.render(o, 1, self.color_a)
			self.text.append(o)


	def draw(self, screen):
		pg.draw.rect(screen, self.color_a, self.rect, 2)

		for i in range(len(self.text_area)):
			#screen.blit(i.d_text, (self.rect.x+50, self.rect.y+50*self.txt.index(i)+50 ))
			if i==self.menu_index:
				self.text_area[i] = CONST.FONT_LG.render('> '+self.text[i], 1, self.color_a)
			else:
				self.text_area[i] = CONST.FONT_LG.render(self.text[i].replace('>',''), 1, self.color_i)
			
			screen.blit(self.text_area[i], (self.rect.x+50, self.rect.y+50*i+50 ))

	def handle_event(self, event):
		key_input = pg.key.get_pressed()   
		if key_input[pg.K_UP]:
			self.prev_index()
		elif key_input[pg.K_DOWN]:
			self.next_index()
		elif key_input[pg.K_RETURN]:
			#print(self.f_names[self.menu_index])
			#self.r = Runner(f_name = self.f_names[self.menu_index])
			#self.r.run()
			if self.menu_index == 0:
				self.m = Menu(demo_mode=True)
			else:
				self.m = Menu(demo_mode=False)
			self.m.run()


	def next_index(self):
		if self.menu_index+1 < len(self.text_area):
			self.menu_index += 1
		else:
			self.menu_index = 0
	
	def prev_index(self):
		if self.menu_index-1 < 0:
			self.menu_index = len(self.text_area)-1
		else:
			self.menu_index -= 1






def main():
	clock = pg.time.Clock()

	m = MainMenu()

	done = False
	while not done:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				done = True

			m.handle_event(event)
			#for i in m.txt:
			#	i.handle_event()

				

		screen.fill((30, 30, 30))
		m.draw(screen)
		
		pg.display.flip()
		clock.tick(30)


if __name__ == '__main__':
	main()
	pg.quit()