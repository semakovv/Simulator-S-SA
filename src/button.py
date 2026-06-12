import pygame
import settings

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

	def press(self, surface):
		"""
		
		"""
		action = False
		mousePosition = pygame.mouse.get_pos()
		if self.frontRect.collidepoint(mousePosition):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				self.clicked = True
				action = True
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False
		surface.blit(self.frontImage, (self.frontRect.x, self.frontRect.y))
		# print(mousePosition)
		# print(action)
		return action
	
	def move(self, surface):
		"""
		
		"""
		xMousePosition = pygame.mouse.get_pos()[0]
		surface.blit(self.backImage, (self.backRect.x, self.backRect.y))
		surface.blit(self.frontImage, (self.frontRect.x, self.frontRect.y))
		mousePosition = pygame.mouse.get_pos()
		if self.frontRect.collidepoint(mousePosition):
			if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
				# if link.press(surface):
				self.clicked = True
				# self.frontRect.x = surface.get_width() - xMousePosition + (self.frontWidth // 2) + self.backRect.x
				print(self.frontRect.x)
				self.frontRect.x = xMousePosition
				surface.blit(self.frontImage, (self.frontRect.x, self.frontRect.y))
		if pygame.mouse.get_pressed()[0] == 0:
			self.clicked = False


		num = self.backWidth + self.frontWidth - self.frontRect.x
		# print(num)
		return num


# volumeButton = link(600, 400, volumeFrontButtonImage)
# frameButton = link(600, 600, frameFrontButtonImage)
# volume = settings.parameters(volumeButton)
# frame = settings.parameters(frameButton)
#         window.blit(volumeBackButtonImage, (600, 400))
#         window.blit(frameBackButtonImage, (600, 400))
        # if volumeButton.press(window):
        #     return "setting"
        # if frameButton.press(window):
        #     return "setting"