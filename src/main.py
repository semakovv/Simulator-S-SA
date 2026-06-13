import pygame
import button
import settings
#
pygame.init()
#
winWidth = 1920
winHeigth = 1080
window = pygame.display.set_mode((winWidth, winHeigth))
pygame.display.set_caption("Simulator S&SA DEMO")
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
menuButton = button.link(1800, 0, menuButtonImage)
settingsButton = button.link(1800, 0, settingsButtonImage)
exitButton = button.link(1000, 400, exitButtonImage)
#
soundMenu = pygame.mixer.Sound("assets/sounds/soundMenu.mp3")
soundGame = pygame.mixer.Sound("assets/sounds/soundGame.mp3")
#
gameSettings = settings.parameters()
volumeButton = button.link(600, 400)
volume = gameSettings.getVolume()
frameButton = button.link(600, 600)
frame = gameSettings.getFrame()
# resolution = button.link(600, 800)


class redraw():
    """
    
    """
    def menu():
        """
        
        """
        window.blit(backGround, (0, 0))
        # window.fill((255, 255, 255))
        soundGame.stop()
        soundMenu.play(-1)
        soundMenu.set_volume(volume)
        if startButton.press(window):
            return "game"
        elif settingsButton.press(window):
            return "setting"
        elif exitButton.press(window):
            return "exit"
        else:
            return "menu"

    def game():
        """
        
        """
        window.blit(backGround, (0, 0))
        # window.fill((255, 255, 255))
        soundMenu.stop()
        soundGame.play(-1)
        soundGame.set_volume(volume)
        if menuButton.press(window):
            return "menu"
        else:
            return "game"
    
    def setting():
        """
        
        """
        global gameSettings, volume, frame
        window.blit(backGround, (0, 0))
        # window.fill((255, 255, 255))
        volumeProcent = volumeButton.move(window, "volume")
        frameProcent = frameButton.move(window, "frame")
        gameSettings.setVolume(volumeProcent)
        gameSettings.setFrame(frameProcent)
        volume = gameSettings.getVolume()
        frame = gameSettings.getFrame()
        soundMenu.set_volume(volume)
        soundGame.set_volume(volume)
        if menuButton.press(window):
            return "menu"
        else:
            return "setting"
#   
run = True
gameState = "menu"
#mainloop
while run:
    clock.tick(frame)
    # print(gameState)
    # print(volume)
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
