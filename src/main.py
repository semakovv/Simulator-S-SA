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
volumeButton = button.link(600, 400)
volume = 0.5
frameButton = button.link(600, 600)
# resolution = button.link(600, 800)
frame = 30
class redraw():
    """
    
    """
    def menu():
        """
        
        """
        window.blit(backGround, (0, 0))
        # window.fill((255, 255, 255))
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
        pygame.mixer.stop()
        # window.fill((255, 255, 255))
        soundGame.play(-1)
        soundGame.set_volume(volume)
        # if menuButton.press(window):
        #     soundGame.stop()
        #     return "menu"
        # else:
        #     return "game"
    
    def setting():
        """
        
        """
        window.blit(backGround, (0, 0))
        # window.fill((255, 255, 255))
        volume = settings.parameters(volumeButton).setVolume()
        frame = settings.parameters(frameButton).setFrame()
        soundGame.play(-1)
        soundGame.set_volume(volume)
            

        # frameButton.move(window, "frame")
        # if menuButton.press(window):
        #     return "menu"
        # else:
        #     return "game"
        return "setting"
#   
run = True
gameState = "menu"
#mainloop
while run:
    clock.tick(frame)
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
    print(gameState)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
    pygame.display.update()

pygame.quit()
