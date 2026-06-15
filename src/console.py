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
        self.fontSize = 20
        self.fontRect_x = 0
        self.fontRect_y = 0
        self.fontRect = (self.fontRect_x, self.fontRect_y)
        self.font = pygame.font.SysFont('monospace', self.fontSize)
        self.lines = []
        self.history = []
        self.consoleWidth = 1000
        self.consoleHeight = 800
        self.console = pygame.Surface((self.consoleWidth, self.consoleHeight))
        self.consoleRect_x = 460
        self.consoleRect_y = 140
        self.consoleRect = (self.consoleRect_x, self.consoleRect_y)
        # self.name = os.path.basename(os.getcwd())

    def inputCLI(self, event):
        """
        
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                print("Введено:", self.inputClient)
                self.history.append(self.inputClient)
                self.lines.append("> " + self.inputClient)
                result = self._commands(self.inputClient)
                if result:
                    self.lines.append(result)
                self.inputClient = ""
            elif event.key == pygame.K_BACKSPACE:
                self.inputClient = self.inputClient[:-1]
            else:
                if event.unicode.isprintable():
                    self.inputClient += event.unicode
    
    def _commands(self, command):
        """
        
        """
        parts = command.split(" ")
        if not parts:
            return
        command = parts[0]
        if command == "help":
            self.lines.append("help clear ip ping")
        elif command == "ip" and parts[1] == "add" and parts[2] == "route" and len(parts) >= 3:
            self.lines.append("")
        elif command == "ping" and parts[1] != "" and len(parts) == 2:
            for i in range(1, 4):
                self.lines.append(f"64 bytes from {parts[1]}: icmp_seq=1 ttl=55 time=269 ms")
        elif command == "clear":
            self.lines.clear()
        else:
            self.lines.append(f"Error {command}")

    def outputCLI(self, surface):
        """
        
        """
        y = 10
        self.console.fill((0, 0, 0))
        for line in self.lines[-20:]:
            text = self.font.render(line, True, (255, 255, 255))
            self.console.blit(text, (0, y))
            y += self.fontSize + 2
        # text = self.font.render(">" + self.inputClient + "_", True, (255, 255, 255))
        # self.console.blit(text, self.fontRect)
        # self.fontRect_y += self.fontSize
        input_display = "> " + self.inputClient + "_"
        input_surf = self.font.render(input_display, True, (255, 255, 255))
        input_y = self.consoleHeight - self.fontSize - 10
        self.console.blit(input_surf, (10, input_y))
        surface.blit(self.console, self.consoleRect)
        # surface.blit(self.console, self.consoleRect)



