# Hacer una clase para cada tipo de boton,
# pueden heredar la clase base y sobreescribir handle_event()
import pygame as pg
import constants as CONST
from button import Button_blueprint

class Button_Reset(Button_blueprint):
	def handle_event(self, event):
		ret = False
		if event and event.type == pg.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
				ret = 1
			else:
				self.active = False
			self.color = CONST.COLOR_ACTIVE if self.active else CONST.COLOR_INACTIVE
			self.text_surface = CONST.FONT.render(self.text, True, self.color)

		return ret

class Button_Pause(Button_blueprint):
	def handle_event(self, event):
		ret = False
		if event and event.type == pg.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
				ret = 2
			else:
				self.active = False
			self.color = CONST.COLOR_ACTIVE if self.active else CONST.COLOR_INACTIVE
			self.text_surface = CONST.FONT.render(self.text, True, self.color)
			
		return ret

class Button_Play(Button_blueprint):
	def handle_event(self, event):
		ret = False
		if event and event.type == pg.MOUSEBUTTONDOWN:
			if self.rect.collidepoint(event.pos):
				self.active = not self.active
				ret = 3
			else:
				self.active = False
			self.color = CONST.COLOR_ACTIVE if self.active else CONST.COLOR_INACTIVE
			self.text_surface = CONST.FONT.render(self.text, True, self.color)
			
		return ret



