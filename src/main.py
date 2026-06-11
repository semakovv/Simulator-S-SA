import pygame
import button
import settings
#
pygame.init()
#
winWidth = 1920
winHeigth = 1080
window = pygame.display.set_mode((winWidth, winHeigth))
pygame.display.set_caption("Simulator S&SA")
backGround = pygame.image.load("assets/images/backGround.jpg")
# pygame.display.set_icon("")
#
clock = pygame.time.Clock()
#
startButtonImage = pygame.image.load("assets/images/startButton.png")
menuButtonImage = pygame.image.load("assets/images/menuButton.jpg")
settingsButtonImage = pygame.image.load("assets/images/settingsButton.jpeg")
exitButtonImage = pygame.image.load("assets/images/exitButton.png")
startButton = button.link(600, 400, startButtonImage)
menuButton = button.link(1000, 0, menuButtonImage)
settingsButton = button.link(1800, 0, settingsButtonImage)
exitButton = button.link(1000, 400, exitButtonImage)

volumeBackButtonImage = pygame.image.load("assets/images/backCounterButton.png")
frameBackButtonImage = pygame.image.load("assets/images/backCounterButton.png")
volumeFrontButtonImage = pygame.image.load("assets/images/frontCounterButton.png")
frameFrontButtonImage = pygame.image.load("assets/images/frontCounterButton.png")
volumeButton = button.link(600, 400, volumeFrontButtonImage)
frameButton = button.link(600, 600, frameFrontButtonImage)
#
#
soundMenu = pygame.mixer.Sound("assets/sounds/soundMenu.mp3")
soundGame = pygame.mixer.Sound("assets/sounds/soundGame.mp3")
#
volume = settings.parameters()
frame = settings.parameters()
# resolution = settings.parameters()

class redraw():
    """
    
    """
    def menu():
        """
        
        """
        window.blit(backGround, (0, 0))
        # window.fill((255, 255, 255))
        soundMenu.play(-1)
        soundMenu.set_volume(volume.setVolume(0))
        if startButton.press(window):
            soundMenu.stop()
            return "game"
        if settingsButton.press(window):
            return "setting"
        if exitButton.press(window):
            return "exit"
        return "menu"

    def game():
        """
        
        """
        window.blit(backGround, (0, 0))
        # window.fill((255, 255, 255))
        soundGame.play(-1)
        soundGame.set_volume(volume.setVolume(0))
        if menuButton.press(window):
            soundGame.stop()
            return "menu"
        return "game"
    
    def setting():
        """
        
        """
        window.blit(backGround, (0, 0))
        window.blit(volumeBackButtonImage, (600, 400))
        window.blit(frameBackButtonImage, (600, 400))
        # window.fill((255, 255, 255))
        if volumeButton.press(window):
            return "setting"
        if frameButton.press(window):
            return "setting"
        if exitButton.press(window):
            return "exit"
        return "setting"

#
run = True
gameState = "menu"
#mainloop
while run:
    clock.tick(frame.setFrame(60))
    # print(gameState)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    if gameState == "menu":
        gameState = redraw.menu()
    if gameState == "game":
        gameState = redraw.game()
    if gameState == "setting":
        gameState = redraw.setting()
    if gameState == "exit":
        run = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
    pygame.display.update()

pygame.quit()
