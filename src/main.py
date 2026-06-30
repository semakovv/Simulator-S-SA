import pygame
import button
import settings
import commands_parser
import stages_parser
import saves_parser

pygame.init()

gameSettings = settings.parameters()
volumeButton = button.link(600, 400)
frameButton = button.link(600, 600)

window = pygame.display.set_mode((1920, 1080))
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
closeItem = button.link(1460, 140, closeItemImage)

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
        if settingsButton.press(window):
            return "setting"
        return "game"
    
    def setting():
        """
        
        """
        window.blit(backGround, (0, 0))
        volumeProcent = volumeButton.move(window, "volume")
        frameProcent = frameButton.move(window, "frame")
        gameSettings.setVolume(volumeProcent)
        gameSettings.setFrame(frameProcent)
        volume = gameSettings.getVolume()
        soundMenu.set_volume(volume)
        soundGame.set_volume(volume)
        if menuButton.press(window):
            return "menu"
        return "setting"

run = True
stage = stages_parser.dialogueManager(window)
save = saves_parser.saveManager()
gameState = "menu"
gameMusic = ""
frame = gameSettings.getFrame()
gameEvent = save.downloadGameEvent()
terminal = commands_parser.cli(stage.current_CLI())


while run:
    clock.tick(frame)
    # print(gameEvent)
    # print(gameState)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if gameState == "menu":
            gameState = redraw.menu()
        elif gameState == "game":
            gameState = redraw.game()
            if gameEvent == "dialog":
                current_save_stage = save.downloadSave()
                if stage.stage != current_save_stage:
                    stage = stages_parser.dialogueManager(window)
                    if stage.current_CLI() != terminal.machine:
                        terminal = commands_parser.cli(stage.current_CLI())
                stage.draw()
                stage.handleEvent(event)
                gameEvent = save.downloadGameEvent()
            elif gameEvent == "desktop":
                if cliItem.press(window):
                    gameEvent = "cli"
            else:
                if closeItem.press(window):
                    gameEvent = "desktop"
                    gameEvent = save.downloadGameEvent()
            if gameEvent == "cli":

                terminal.inputCLI(event)
                terminal.outputCLI(window)
        elif gameState == "setting":
            gameState = redraw.setting()
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

    pygame.display.update()
    
pygame.quit()
