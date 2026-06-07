import pygame

winWidth = 1920
winHeigth = 1080
window = pygame.display.set_mode((winWidth, winHeigth))
pygame.display.set_caption("Simulator S&SA")
backGround = pygame.image.load("pictures/BackGroung.jpg")
# pygame.display.set_icon("")

clock = pygame.time.Clock()

def redrawGameWindow():
    window.blit(backGround, (0, 0))

run = True
while run:
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    redrawGameWindow()
pygame.quit()
