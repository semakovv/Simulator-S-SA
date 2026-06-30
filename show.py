def handleEvent(self, event):
        if event.type == pygame.KEYDOWN:
            if self.current_node.get('choices'):
                if event.key == pygame.K_UP:
                    self.selected_choice = (self.selected_choice - 1) % len(self.current_node['choices'])
                elif event.key == pygame.K_DOWN:
                    self.selected_choice = (self.selected_choice + 1) % len(self.current_node['choices'])
                elif event.key == pygame.K_RIGHT:
                    choice = self.current_node['choices'][self.selected_choice]
                    next_node = choice.get('next_node')
                    if next_node and next_node in self.nodes:
                        self.current_node = self.nodes[next_node]
                        self.selected_choice = 0 
            else:
                if event.key == pygame.K_SPACE:
                    next_node = self.current_node.get('next_node')
                    if next_node and next_node in self.nodes:
                        self.current_node = self.nodes[next_node]
                        self.selected_choice = 0
                if event.key == pygame.K_RETURN:
                    self.__restoringStage()
                    self.__loadDialog()


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

        if self.current_node.get('choices') and len(self.current_node['choices']) > 0:
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