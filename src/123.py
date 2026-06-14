# console.py
import pygame

class Cli:
    def __init__(self):
        self.active = False           # видна ли консоль
        self.input_line = ""          # текущая строка ввода
        self.output_lines = []        # строки вывода (для истории команд)
        self.history = []             # история введённых команд
        self.history_index = -1
        self.font = pygame.font.SysFont("monospace", 24)
        self.bg_color = (0, 0, 0, 200)  # чёрный полупрозрачный
        self.text_color = (0, 255, 0)   # зелёный текст
        self.width = 800
        self.height = 400

    def toggle(self):
        """Открыть/закрыть консоль"""
        self.active = not self.active
        if not self.active:
            self.input_line = ""   # очищаем строку при закрытии

    def handle_event(self, event):
        """Обработка событий, когда консоль активна"""
        if not self.active:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self._execute_command()
            elif event.key == pygame.K_BACKSPACE:
                self.input_line = self.input_line[:-1]
            elif event.key == pygame.K_ESCAPE:
                self.toggle()
            else:
                if event.unicode and event.unicode.isprintable():
                    self.input_line += event.unicode

    def _execute_command(self):
        """Разбор и выполнение команды"""
        if not self.input_line:
            return
        self.history.append(self.input_line)
        self.history_index = -1
        cmd = self.input_line.strip().lower()
        self.output_lines.append(f"> {self.input_line}")
        # Пример простых команд
        if cmd == "help":
            self.output_lines.append("Доступны: help, clear, say <текст>")
        elif cmd == "clear":
            self.output_lines.clear()
        elif cmd.startswith("say "):
            self.output_lines.append(cmd[4:])
        else:
            self.output_lines.append(f"Неизвестная команда: {cmd}")
        self.input_line = ""

    def draw(self, surface):
        if not self.active:
            return
        # Создаём поверхность с прозрачностью
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        surf.fill(self.bg_color)
        # Отрисовка вывода (последние 10 строк)
        y = 10
        for line in self.output_lines[-10:]:
            text = self.font.render(line, True, self.text_color)
            surf.blit(text, (10, y))
            y += self.font.get_height() + 2
        # Строка ввода
        input_text = f"> {self.input_line}"
        input_surf = self.font.render(input_text, True, self.text_color)
        input_y = self.height - self.font.get_height() - 10
        surf.blit(input_surf, (10, input_y))
        # Курсор (мигающий)
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            cursor_surf = self.font.render("_", True, self.text_color)
            cursor_x = 10 + input_surf.get_width()
            surf.blit(cursor_surf, (cursor_x, input_y))
        # Рамка
        pygame.draw.rect(surf, self.text_color, surf.get_rect(), 2)
        # Позиционируем консоль в центре или внизу
        surface.blit(surf, (surface.get_width()//2 - self.width//2,
                            surface.get_height()//2 - self.height//2))