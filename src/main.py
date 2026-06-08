import pygame
import button

pygame.init()

winWidth = 1200
winHeigth = 685
window = pygame.display.set_mode((winWidth, winHeigth))
pygame.display.set_caption("Simulator S&SA")
backGround = pygame.image.load("assets/images/backGround.jpg")
# pygame.display.set_icon("")

clock = pygame.time.Clock()

startButtonImage = pygame.image.load("assets/images/startButton.png")
exitButtonImage = pygame.image.load("assets/images/exitButton.png")
volumeButtonImage = pygame.image.load("assets/images/volumeButton.png")
startButton = button.buttonClass(100, 200, startButtonImage)
exitButton = button.buttonClass(450, 200, exitButtonImage)
volumeButton = button.buttonClass(1100, 0, volumeButtonImage)

def redrawMenu():
    window.blit(backGround, (0, 0))
    # window.fill((255, 255, 255))

    if startButton.draw(window):
        return "start"
    
    if exitButton.draw(window):
        return "exit"
    
    if volumeButton.draw(window):
        pass

    return "menu"

def redrawGame():
    window.blit(backGround, (0, 0))
    # window.fill((255, 255, 255))
    return "game"

run = True
gameState = "menu"

# mainloop
while run:
    clock.tick(60)
    
    # print(gameState)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
    if gameState == "menu":
        gameState = redrawMenu()

    if gameState == "start":
        gameState = redrawGame()

    if gameState == "exit":
        run = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        run = False
    
    pygame.display.update()


pygame.quit()
