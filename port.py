import pygame as pg
import constants as CONST

# Init
pg.init()
screen = pg.display.set_mode((1900, 1060))

class Ports:
	CONT_A = None
	CONT_B = None
	def __init__(self, x, y, w, h, vert=True):
		self.x = x
		self.y = y
		self.w = w
		self.h = h

		self.number_a = CONST.FONT.render(self.CONT_A, True, CONST.COLOR_INACTIVE)
		self.number_b = CONST.FONT.render(self.CONT_B, True, CONST.COLOR_INACTIVE)
		self.arrow_a = pg.image.load('./img/arrow_sm.png')
		self.arrow_b = pg.image.load('./img/arrow_sm.png')

		self.vert = vert



	def draw(self, screen):
		self.number_a = CONST.FONT.render(str(self.CONT_A), True, CONST.COLOR_INACTIVE)
		self.number_b = CONST.FONT.render(str(self.CONT_B), True, CONST.COLOR_INACTIVE)
		
		if self.CONT_A != None:
			screen.blit(self.number_a, (self.x, self.y))

		if self.vert:
			screen.blit(self.arrow_a,  (self.x+60, self.y))
			screen.blit(pg.transform.rotate(self.arrow_b, 180), (self.x+100, self.y))
			if self.CONT_B != None:
				screen.blit(self.number_b, (self.x+120, self.y))
		else:
			screen.blit(pg.transform.rotate(self.arrow_a, -90), (self.x, self.y+20))
			screen.blit(pg.transform.rotate(self.arrow_b, 90), (self.x, self.y+60))
			if self.CONT_B != None:
				screen.blit(self.number_b, (self.x, self.y+80))



def main():
    clock = pg.time.Clock()
    ports_v = Ports(10, 10, 100, 100, vert=True)
    ports_h = Ports(100, 100, 100, 100, vert=False)
    ports = [ports_v, ports_h]

    done = False
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

        screen.fill((30, 30, 30))
        for p in ports:
            p.draw(screen)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    main()
    pg.quit()