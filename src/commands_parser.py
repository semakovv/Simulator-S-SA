import pygame
import json
import saves_parser as sp

class cli():
    """
    
    """
    def __init__(self, machine):
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
        self.machine = machine
        self.json_path = "data/machines.json"
        self.nodes = {}
        self.stage = sp.saveManager().downloadSave()
        self.ipAddresses = []
        self.ipRoutes = []
        self.matrixWays = [[0]]
        self.ipAddressList = []
        self.ipRouteList = []

        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.nodes = json.load(f)

        if "machines" in self.nodes[self.stage]:
            for i in self.nodes[self.stage]["machines"].items():
                for j in i[1]["config"].items():
                    if j[0] != "routes":
                        self.matrixWays[0].extend(j[-1])
                        self.ipAddressList.extend(j[-1])
                    else:
                        self.ipRouteList.extend(j[-1])

        for k in self.ipRouteList:
            self.matrixWays.append([k])
        for h in self.matrixWays[1::]:
            for l in range(len(self.matrixWays[0][1::])):
                h.append("0")
            
        for x in range(1, len(self.matrixWays[0][0::])):
            for y in range(1, len(self.matrixWays[0][0::])):
                if self.matrixWays[y][0] != "":
                    if self.matrixWays[0][x] == self.matrixWays[0][y]:
                        self.matrixWays[x][y] = "1"
                if self.matrixWays[y][0] != "":
                    if self.matrixWays[y][0][self.matrixWays[y][0].rfind("."):self.matrixWays[y][0].rfind("/")] == ".0":
                        if self.matrixWays[0][x][:self.matrixWays[0][x].rfind(".")] == self.matrixWays[y][0][:self.matrixWays[y][0].rfind(".")]:
                            self.matrixWays[y][x] = "1"

    def _ping(self, dst):
            """
            
            """
            ping = False
            src = "".join(self.nodes[self.stage]["machines"][self.machine]["config"]["eth0"])
            srcID = self.ipAddressList.index(src)
            if dst + "/25" in self.ipAddressList:
                dstID = self.ipAddressList.index(dst + "/25")
                for i in range(1, len(self.matrixWays[1::])):
                    if self.matrixWays[srcID+1][1::][srcID] == "1" and self.matrixWays[dstID+1][1::][dstID] == "1":
                        print(self.matrixWays[1][1::][srcID], self.matrixWays[i][1::][dstID])
                        if self.matrixWays[1][1::][srcID] == self.matrixWays[i][1::][dstID]:
                            ping = True
                            break
            else:
                return ping
            return ping
                 
    def inputCLI(self, event):
        """
        
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # print("Введено:", self.inputClient)
                self.history.append(self.inputClient)
                self.lines.append(f"{self.machine}> " + self.inputClient)
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
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.nodes = json.load(f)

        for item in self.nodes[self.stage]["machines"][self.machine]["config"].items():
                        if len(item) == 2:
                            if item[0] != "routes":
                                self.ipAddresses.append(item[0])
                                self.ipAddresses.extend(item[1])
                            else:
                                self.ipRoutes.extend(item[1])
        # for machine in self.nodes[self.stage]["machines"].items():
        #     print(machine)

        parts = command.split(" ")
        if not parts:
            return
        command = parts[0]
        if command == "":
            self.lines.append("")
        elif command == "help":
            self.lines.append("help clear ip ping")
        elif command == "ip":
            if parts[1] == "add" and len(parts) >= 2:
                if parts[2] == "address" and len(parts) >= 3:
                    self.nodes[self.stage]["machines"][self.machine]["config"]["eth0"].append(parts[3])
                elif parts[2] == "route" and len(parts) >= 3:
                    self.nodes[self.stage]["machines"][self.machine]["config"]["routes"].append(parts[3])
            elif parts[1] == "del" and len(parts) >= 2:
                if parts[2] == "address" and len(parts) >= 3:
                    self.nodes[self.stage]["machines"][self.machine]["config"]["eth0"].pop(parts[3])
                elif parts[2] == "route" and len(parts) >= 3:
                    self.nodes[self.stage]["machines"][self.machine]["config"]["routes"].pop(parts[3])
            elif parts[1] == "addresses" and len(parts) >= 2:
                self.lines.append("ip addresses: " + " ".join(self.ipAddresses))
            elif parts[1] == "routes" and len(parts) >= 2:
                self.lines.append("ip routes: " + " ".join(self.ipRoutes))
        elif command == "ping" and parts[1] != "" and len(parts) == 2:
            if self._ping(parts[1]):
                for i in range(1, 4):
                    self.lines.append(f"64 bytes from {parts[1]}: icmp_seq=1 ttl=55 time=269 ms")
            else:
                for i in range(1, 4):
                    self.lines.append(f"From {parts[1]} icmp_seq=1 Destination Host Unreachable")
        elif command == "clear":
            self.lines.clear()
        else:
            self.lines.append(f"Error {command}")

        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(self.nodes, f, indent=4)      

    def outputCLI(self, surface):
        """
        
        """
        input_y = 0
        self.console.fill((0, 0, 0))
        for line in self.lines[-38:]:
            text = self.font.render(line, True, (255, 255, 255))
            self.console.blit(text, (0, input_y))
            input_y += self.fontSize
        

        prompt = f"{self.machine}> " + self.inputClient + "_"
        input_surf = self.font.render(prompt, True, (255, 255, 255))
        self.console.blit(input_surf, (0, input_y))
        surface.blit(self.console, self.consoleRect)

