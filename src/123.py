import pygame
pygame.init()

screen = pygame.display.set_mode((800, 200))
clock = pygame.time.Clock()

input_text = ""
active = True
font = pygame.font.Font(None, 36)

while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("Введено:", input_text)
                input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                input_text = input_text[:-1]
            else:
                if event.unicode.isprintable():
                    input_text += event.unicode

    screen.fill((0, 0, 0))
    text_surface = font.render(input_text + "_", True, (255, 255, 255))
    screen.blit(text_surface, (20, 80))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()