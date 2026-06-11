import pygame

#button class
class link():
	"""
	
	"""
	def __init__(self, x, y, image):
		"""
		
		"""
		self.image = image
		width = image.get_width()
		height = image.get_height()
		self.rect = self.image.get_rect()
		self.rect.topleft = (x, y)
		self.clicked = False

	def press(self, surface):
		"""
		
		"""
		action = False
		mousePosition = pygame.mouse.get_pos()
		if self.rect.collidepoint(mousePosition):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		surface.blit(self.image, (self.rect.x, self.rect.y))
		# print(action)
		return action
	
	def move(self, surface):
		"""
		
		"""
		action = False
		mousePosition = pygame.mouse.get_pos()
		if self.rect.collidepoint(mousePosition):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		surface.blit(self.image, (pygame.mouse.get_pos()[0], self.rect.y))
		# print(action)
		return action
	