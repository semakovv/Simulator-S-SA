import pygame
import json

class dialogueManager:
    def __init__(self, screen, font=None):
        self.screen = screen
        self.font = font or pygame.font.Font(None, 36)
        self.active = False
        self.nodes = {}
        self.current_node = None
        self.current_stage = None   # имя стартового узла (главы)
        self.result = False         # успешно ли завершена глава

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

    def loadDialogue(self, json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            self.nodes = json.load(f)

    def start(self, start_node):
        if start_node in self.nodes:
            self.current_stage = start_node
            self.current_node = self.nodes[start_node]
            self.active = True
            self.selected_choice = 0
            self.result = False
        else:
            print(f"Ошибка: узел {start_node} не найден")

    def handleEvent(self, event):
        if not self.active:
            return
        if event.type == pygame.KEYDOWN:
            if self.current_node.get('choices'):
                # обработка выбора
                if event.key == pygame.K_UP:
                    self.selected_choice = (self.selected_choice - 1) % len(self.current_node['choices'])
                elif event.key == pygame.K_DOWN:
                    self.selected_choice = (self.selected_choice + 1) % len(self.current_node['choices'])
                elif event.key == pygame.K_RIGHT:
                    choice = self.current_node['choices'][self.selected_choice]
                    next_node = choice.get('next_node')
                    if next_node == 'end' or next_node not in self.nodes:
                        self.active = False
                        if self.current_node.get('success'):
                            self.result = True
                            if self.current_stage in self.nodes:
                                self.nodes[self.current_stage]['result'] = "True"
                    else:
                        self.current_node = self.nodes[next_node]
                        self.selected_choice = 0
            else:
                # Линейный диалог (без choices)
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    next_node = self.current_node.get('next_node')
                    if next_node and next_node in self.nodes:
                        self.current_node = self.nodes[next_node]
                        self.selected_choice = 0
                    else:
                        # Если next_node нет – завершаем диалог
                        self.active = False
                        if self.current_node.get('success'):
                            self.result = True
                            if self.current_stage in self.nodes:
                                self.nodes[self.current_stage]['result'] = "True"

    def draw(self):
        if not self.active:
            return
        surf = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        surf.fill(self.bg_color)
        pygame.draw.rect(surf, self.border_color, surf.get_rect(), 2)

        # Вывод имени персонажа (если есть)
        y = 20
        speaker = self.current_node.get('speaker', '')
        if speaker:
            speaker_surf = self.font.render(f"{speaker}:", True, (200, 200, 255))
            surf.blit(speaker_surf, (20, y))
            y += self.font.get_height() + 2

        # Текст реплики
        text_lines = self._wrapText(self.current_node.get('text', ''), self.font, self.window_width - 40)
        for line in text_lines:
            text_surf = self.font.render(line, True, self.text_color)
            surf.blit(text_surf, (20, y))
            y += self.font.get_height() + 2

        # Варианты выбора
        if self.current_node.get('choices'):
            y += 20
            for i, choice in enumerate(self.current_node['choices']):
                color = self.choice_selected_color if i == self.selected_choice else self.choice_color
                choice_surf = self.font.render(f"> {choice['text']}", True, color)
                surf.blit(choice_surf, (40, y))
                y += self.font.get_height() + 5
        else:
            if self.current_node.get('next_node'):
                hint = "Нажмите ПРОБЕЛ или ENTER, чтобы продолжить..."
            else:
                hint = "Нажмите ПРОБЕЛ или ENTER, чтобы завершить"
            hint_surf = self.font.render(hint, True, (150, 150, 150))
            surf.blit(hint_surf, (20, self.window_height - 40))

        self.screen.blit(surf, self.rect)

    def _wrapText(self, text, font, max_width):
        lines = []
        paragraphs = text.split('\n')
        for paragraph in paragraphs:
            if not paragraph.strip():
                lines.append('')  # пустая строка для отступа
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
                        # Очень длинное слово – разбиваем принудительно
                        for i in range(0, len(word), max_width // (font.size('W')[0] or 1)):
                            lines.append(word[i:i + max_width // (font.size('W')[0] or 1)])
                        current_line = []
            if current_line:
                lines.append(' '.join(current_line))
        return lines

    def save_result(self, json_path):
        """Сохраняет обновлённый JSON с новым результатом."""
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(self.nodes, f, indent=4, ensure_ascii=False)