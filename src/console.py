import pygame
import os
from collections import deque 

class machines():
    """
    
    """
    def __init__(self, name):
        self.name = name

class сli():
    """
    
    """
    def __init__(self):
        self.inputClient = ""
        self.fontSize = 30
        self.fontRect_x = 0
        self.fontRect_y = 0
        self.fontRect = (self.fontRect_x, self.fontRect_y)
        self.font = pygame.font.SysFont('monospace', self.fontSize)
        self.history = []
        self.consoleWidth = 800
        self.consoleHeight = 600
        self.console = pygame.Surface((self.consoleWidth, self.consoleHeight))
        self.consoleRect_x = 560
        self.consoleRect_y = 240
        self.consoleRect = (self.consoleRect_x, self.consoleRect_y)
        # self.name = os.path.basename(os.getcwd())

    def inputCLI(self, event):
        """
        
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("Введено:", self.inputClient)
                self.history.append(self.inputClient)
                self._commands(self.inputClient)
                self.inputClient = ""
            elif event.key == pygame.K_BACKSPACE:
                self.inputClient = self.inputClient[:-1]
            else:
                if event.unicode.isprintable():
                    self.inputClient += event.unicode
    
    def _commands(self, command):
        """
        
        """
        command = command.split(" ")

        if command[0] == "help":
            self.inputClient = "ip"
        else:
            self.inputClient = "Error"

    def outputCLI(self, surface):
        """
        
        """
        self.console.fill((0, 0, 0))
        text = self.font.render(">" + self.inputClient + "_", True, (255, 255, 255))
        self.console.blit(text, self.fontRect)
        # self.fontRect_y += self.fontSize
        surface.blit(self.console, self.consoleRect)


