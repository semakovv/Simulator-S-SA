import pygame

movingButtonImage = pygame.image.load("assets/images/movingButton.png")
holdingButtonImage = pygame.image.load("assets/images/holdingButton.png")

#button class
class link():
	"""
	
	"""
	def __init__(self, x, y, frontImage = movingButtonImage, backImage = holdingButtonImage):
		"""
		
		"""
		self.frontImage = frontImage
		self.backImage = backImage
		self.frontWidth = frontImage.get_width()
		self.frontHeight = frontImage.get_height()
		self.backWidth = backImage.get_width()
		self.backHeight = backImage.get_height()
		self.frontRect = self.frontImage.get_rect()
		self.backRect = self.backImage.get_rect()
		self.frontRect.topleft = (x, y)
		self.backRect.topleft = (x, y)
		self.clicked = False
		self.offset = 0


	def press(self, surface):
		"""
		
		"""
		mousePosition = pygame.mouse.get_pos()
		mousePress = pygame.mouse.get_pressed()
		action = False
		if mousePress[0] == 1 and self.frontRect.collidepoint(mousePosition) and not(self.clicked):
			self.clicked = True
			action = True
			# print(self.clicked)
		if mousePress[0] == 0:
			self.clicked = False
		surface.blit(self.frontImage, self.frontRect)
		return action
	
		# mousePosition = pygame.mouse.get_pos()
		# mousePress = pygame.mouse.get_pressed()
		# if self.frontRect.collidepoint(mousePosition):
		# 	if mousePress[0] == 1 and self.clicked == False:
		# 		self.clicked = True
		# if mousePress[0] == 0:
		# 	self.clicked = False
		# surface.blit(self.frontImage, self.frontRect)
		# # print(mousePosition)
		# # print(self.clicked)
		# return self.clicked

	def move(self, surface, name = ""):
		"""
		
		"""
		mousePosition = pygame.mouse.get_pos()
		mousePress = pygame.mouse.get_pressed()
		min_x = self.backRect.x
		max_x = self.backRect.x + self.backRect.width - self.frontWidth
		if mousePress[0] == 1 and self.frontRect.collidepoint(mousePosition) and not(self.clicked):
			self.clicked = True
			# print(self.clicked)
			self.offset = mousePosition[0] - self.frontRect.x
		if self.clicked:
			self.frontRect.x = mousePosition[0] - self.offset
			self.frontRect.x = max(min_x, min(self.frontRect.x, max_x))
		if mousePress[0] == 0:
			self.clicked = False
		procent = (self.frontRect.x - self.backRect.x) // 10
		surface.blit(self.backImage, self.backRect)
		surface.blit(self.frontImage, self.frontRect)
		font = pygame.font.SysFont("comicsans", 30, True)
		text = font.render(f"{name} - {procent}%", 1, (255, 255, 255))
		surface.blit(text, (self.backRect.x , self.backRect.y - 40))
		return procent
