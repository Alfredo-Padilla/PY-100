import pygame as pg
import constants as CONST
import json

class RuleBox:
	def __init__(self, x, y, w, h, txt, title="Title"):
		self.rect = pg.Rect(x, y, w, h)
		self.color = CONST.COLOR_INACTIVE
		self.title = CONST.FONT.render(' - '+title+' - ', True, self.color)
		
		self.txt = txt
		self.txt_surface = []
		for i in range(len(txt)):
			self.txt_surface.append(CONST.FONT.render(str(txt[i]), True, self.color))

	def draw(self, screen):
		pg.draw.rect(screen, self.color, self.rect, 2)
		size = ( (self.rect.x+self.rect.w/2) - self.title.get_size()[0]/2,
			 	self.rect.y-30)
		screen.blit(self.title, size)
		for i in range(len(self.txt_surface)):
			screen.blit(self.txt_surface[i], (self.rect.x+10, self.rect.y+ 30*i+10))



def main():
	pg.init()
	screen = pg.display.set_mode((1900, 1060))
	clock = pg.time.Clock()

	inst = ['Instrucciones', 'de', 'prueba']
	rb = RuleBox(50, 50, 400, 100, inst)

	done = False
	while not done:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				done = True
				

		screen.fill((30, 30, 30))
		rb.draw(screen)

		pg.display.flip()
		clock.tick(30)


if __name__ == '__main__':
	main()
	pg.quit()
