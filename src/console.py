import pygame
import os

class machines():
    def __init__(self, name):
        self.name = name

class сli():

    def __init__(self):
        self.inputClient = "hello"
        self.fontSize = 30
        self.name = os.path.basename(os.getcwd())

    def draw(self, surface):
        for event in pygame.event.get():
            if event.unicode and event.unicode.isprintable():
                self.inputClient += event.unicode
        console = pygame.Surface((800, 600))
        console.fill((0, 0, 0))
        font = pygame.font.SysFont('monospace', self.fontSize)
        text = font.render(self.inputClient, 1, (255, 255, 255))
        console.blit(text, (console.get_rect()[0], console.get_rect()[1]))
        surface.blit(console, (560, 240))

