import pygame
import json
import saves_parser as sp

class dialogueManager:
    def __init__(self, screen, font=None):
        self.screen = screen
        self.font = font or pygame.font.Font(None, 36)
        self.stage = None
        self.nodes = {}
        self.current_node = None
        self.current_stage = None
        self.result = "False"
        self.window_width = 1920
        self.window_height = 300
        self.bg_color = (0, 0, 0, 200)
        self.border_color = (255, 255, 255)
        self.text_color = (255, 255, 255)
        self.choice_color = (180, 180, 180)
        self.choice_selected_color = (255, 255, 0)
        self.selected_choice = 0

        self.rect = pygame.Rect(0, 0, self.window_width, self.window_height)
        self.rect.centerx = screen.get_width() // 2
        self.rect.bottom = screen.get_height() - 30
        self.json_path = "data/stages.json"
        self.stage = sp.saveManager().downloadSave()
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.nodes = json.load(f)
        self.current_node = self.nodes[self.stage]
        self.current_stage = self.stage
        
    def __loadDialog(self):
            self.stage = sp.saveManager().downloadSave()
            with open(self.json_path, 'r', encoding='utf-8') as f:
                self.nodes = json.load(f)
            self.current_node = self.nodes[self.stage]
            self.current_stage = self.stage

    def __restoringStage(self):
        if self.current_node["success"] == "True":
            self.result = "True"
            self.nodes[self.current_stage]["result"] = "True"
            with open(self.json_path, 'w', encoding='utf-8') as f:
                json.dump(self.nodes, f, indent=4, ensure_ascii=False)
            self.__loadDialog()

    def current_PC(self):
        return self.nodes[self.current_stage]["PC"]

    def handleEvent(self, event):
        # self.__loadDialog()
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_choice = (self.selected_choice - 1) % len(self.current_node['choices'])
                elif event.key == pygame.K_DOWN:
                    self.selected_choice = (self.selected_choice + 1) % len(self.current_node['choices'])
                elif event.key == pygame.K_RIGHT:
                    choice = self.current_node['choices'][self.selected_choice]
                    next_node = choice.get('next_node')
                    if next_node and next_node in self.nodes:
                        self.current_node = self.nodes[next_node]
                
            if event.key == pygame.K_SPACE:
                next_node = self.current_node.get('next_node')
                if next_node and next_node in self.nodes:
                    self.current_node = self.nodes[next_node]
                    self.selected_choice = 0
            if event.key == pygame.K_RETURN:
                self.__restoringStage()


    def draw(self):
        surf = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        surf.fill(self.bg_color)
        pygame.draw.rect(surf, self.border_color, surf.get_rect(), 2)

        y = 20
        speaker = self.current_node.get('speaker', '')
        if speaker:
            speaker_surf = self.font.render(f"{speaker}:", True, (200, 200, 255))
            surf.blit(speaker_surf, (20, y))
            y += self.font.get_height() + 2

        text_lines = self._wrapText(self.current_node.get('text', ''), self.font, self.window_width - 40)
        for line in text_lines:
            text_surf = self.font.render(line, True, self.text_color)
            surf.blit(text_surf, (20, y))
            y += self.font.get_height() + 2

        if self.current_node.get('choices'):
            y += 20
            for i, choice in enumerate(self.current_node['choices']):
                color = self.choice_selected_color if i == self.selected_choice else self.choice_color
                choice_surf = self.font.render(f"> {choice['text']}", True, color)
                surf.blit(choice_surf, (40, y))
                y += self.font.get_height() + 5
        else:
            if self.current_node.get('next_node'):
                hint = "Нажмите ПРОБЕЛ, чтобы продолжить"
            else:
                hint = "Нажмите ENTER, чтобы завершить"
            hint_surf = self.font.render(hint, True, (150, 150, 150))
            surf.blit(hint_surf, (20, self.window_height - 40))

        self.screen.blit(surf, self.rect)

    def _wrapText(self, text, font, max_width):
        lines = []
        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            if not paragraph.strip():
                lines.append('')
                continue
            words = paragraph.split(' ')
            current_line = []
            for word in words:
                test_line = ' '.join(current_line + [word])
                if font.size(test_line)[0] <= max_width:
                    current_line.append(word)
                else:
                    if current_line:
                        lines.append(' '.join(current_line))
                        current_line = [word]
                    else:
                        for i in range(0, len(word), max_width // (font.size('W')[0] or 1)):
                            lines.append(word[i:i + max_width // (font.size('W')[0] or 1)])
                        current_line = []
            if current_line:
                lines.append(' '.join(current_line))
        return lines