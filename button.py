import pygame as pg
import constants as CONST

class Button_blueprint():
	def __init__(self, x, y, w, h, text):
		self.rect = pg.Rect(x, y, w, h)
		self.color = CONST.COLOR_INACTIVE
		self.text = text
		self.text_surface = CONST.FONT.render(text, True, self.color)
		self.active = False

	def handle_event(self, event):
		if event.type == pg.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
			else:
				self.active = False
			self.color = CONST.COLOR_ACTIVE if self.active else CONST.COLOR_INACTIVE
			self.text_surface = CONST.FONT.render(self.text, True, self.color)
			
	def draw(self, screen):
		pg.draw.rect(screen, self.color, self.rect, 2)
		tw, th = CONST.FONT.size(self.text)
		screen.blit(self.text_surface, (self.rect.x+(self.rect.w/2-tw/2), self.rect.y+25))

class Button():
	def __init__(self, x, y, w, h, text, ret):
		self.rect = pg.Rect(x, y, w, h)
		self.color = CONST.COLOR_INACTIVE
		self.text = text
		self.text_surface = CONST.FONT.render(text, True, self.color)
		self.active = False
		self.ret = ret

	def handle_event(self, event):
		ret = False
		if event.type == pg.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
			else:
				self.active = False
			self.color = CONST.COLOR_ACTIVE if self.active else CONST.COLOR_INACTIVE
			self.text_surface = CONST.FONT.render(self.text, True, self.color)
			
			ret = self.ret

		return ret

	def draw(self, screen):
		pg.draw.rect(screen, self.color, self.rect, 2)
		tw, th = CONST.FONT.size(self.text)
		screen.blit(self.text_surface, (self.rect.x+(self.rect.w/2-tw/2), self.rect.y+25))


def main():
	pg.init()
	screen = pg.display.set_mode((1900, 1060))

	clock = pg.time.Clock()	

	boton = Button(100, 100, 100, 75, 'PLAY', False)

	done = False
	while not done:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				done = True
			boton.handle_event(event)

		screen.fill((30, 30, 30))
		boton.draw(screen)
		
		pg.display.flip()
		clock.tick(30)

if __name__ == '__main__':
	main()
	pg.quit()