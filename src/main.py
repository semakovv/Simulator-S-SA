import pygame
import button
import settings
import cmd_parser
import stages_parser

pygame.init()

gameSettings = settings.parameters()
volumeButton = button.link(600, 400)
volume = gameSettings.getVolume()
frameButton = button.link(600, 600)
frame = gameSettings.getFrame()
resolution = gameSettings.getResolution()

window = pygame.display.set_mode(resolution)
pygame.display.set_caption("Simulator S&SA DEMO")
backGround = pygame.image.load("assets/images/backgrounds/backGround.jpg")
# pygame.display.set_icon("")

clock = pygame.time.Clock()

soundMenu = pygame.mixer.Sound("assets/sounds/soundMenu.mp3")
soundGame = pygame.mixer.Sound("assets/sounds/soundGame.mp3")

startButtonImage = pygame.image.load("assets/images/buttons/startButton.png")
startButton = button.link(600, 400, startButtonImage)
menuButtonImage = pygame.image.load("assets/images/buttons/menuButton.jpg")
menuButton = button.link(1800, 0, menuButtonImage)
settingsButtonImage = pygame.image.load("assets/images/buttons/settingsButton.jpeg")
settingsButton = button.link(1800, 0, settingsButtonImage)
exitButtonImage = pygame.image.load("assets/images/buttons/exitButton.png")
exitButton = button.link(1000, 400, exitButtonImage)

cliItemImage = pygame.image.load("assets/images/items/cliItem.jpg")
cliItem = button.link(560, 240, cliItemImage)
closeItemImage = pygame.image.load("assets/images/items/closeItem.png")
closeItem = button.link(1360, 240, closeItemImage)

class redraw():
    """
    
    """
    def menu():
        """
        
        """
        window.blit(backGround, (0, 0))
        if startButton.press(window):
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
        if menuButton.press(window):
            return "menu"
        return "game"
    
    def setting():
        """
        
        """
        global gameSettings, volume, frame
        window.blit(backGround, (0, 0))
        volumeProcent = volumeButton.move(window, "volume")
        frameProcent = frameButton.move(window, "frame")
        gameSettings.setVolume(volumeProcent)
        gameSettings.setFrame(frameProcent)
        volume = gameSettings.getVolume()
        frame = gameSettings.getFrame()
        if menuButton.press(window):
            return "menu"
        return "setting"

run = True
terminal = cmd_parser.сli()
gameState = "menu"
gameMusic = ""
gameEvent = "desktop"
stage = stages_parser.dialogueManager(window)
stage.loadDialogue("data/stages.json")

while run:
    clock.tick(frame)
    # print(gameEvent)
    # print(gameState)
    # print(f"{frame} кадров в секунду\nзадержка 0 секунд")
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if stage.active:
            stage.handleEvent(event)
        else:
            if gameState == "game":
                stage.start("stage1")

        if gameState == "menu":
            gameState = redraw.menu()
        elif gameState == "game":
            gameState = redraw.game()
            if stage.active:
                stage.draw()
            if gameEvent == "desktop":
                if cliItem.press(window):
                    gameEvent = "cli"
            else:
                if closeItem.press(window):
                    gameEvent = "desktop"
            if gameEvent == "cli":
                terminal.inputCLI(event)
                terminal.outputCLI(window)
        elif gameState == "setting":
            gameState = redraw.setting()
            soundMenu.set_volume(volume)
            soundGame.set_volume(volume)
        elif gameState == "exit":
            run = False

        if gameState != gameMusic:
            gameMusic = gameState
            if gameMusic == "menu":
                pygame.mixer.stop()
                soundMenu.play(-1)
            elif gameMusic == "game":
                pygame.mixer.stop()
                soundGame.play(-1)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
    pygame.display.update()
    
pygame.quit()
