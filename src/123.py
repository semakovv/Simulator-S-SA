# src/console.py
import pygame
import pygame.locals as pl

class GameConsole:
    def __init__(self, game_ref, width, height, font_size=24):
        self.game = game_ref          # ссылка на объект game (например, game_settings)
        self.width = width
        self.height = height
        self.font_size = font_size
        self.is_open = False

        # Внешний вид
        self.bg_color = (0, 0, 0, 180)   # полупрозрачный чёрный
        self.text_color = (0, 255, 0)    # зелёный
        self.font = pygame.font.SysFont('monospace', self.font_size)

        # Состояние консоли
        self.input_line = ""
        self.history = []         # все введённые команды
        self.history_index = -1   # для навигации по стрелкам
        self.output_lines = []    # список кортежей (текст, цвет)

    def toggle(self):
        self.is_open = not self.is_open
        if not self.is_open:
            self.input_line = ""

    def handle_event(self, event):
        if not self.is_open:
            return

        if event.type == pl.KEYDOWN:
            if event.key == pl.K_RETURN:
                self._execute_command()
            elif event.key == pl.K_BACKSPACE:
                self.input_line = self.input_line[:-1]
            elif event.key == pl.K_UP:
                self._navigate_history(-1)
            elif event.key == pl.K_DOWN:
                self._navigate_history(1)
            elif event.key == pl.K_ESCAPE:
                self.toggle()
            else:
                if event.unicode and event.unicode.isprintable():
                    self.input_line += event.unicode

    def _execute_command(self):
        if not self.input_line.strip():
            return

        # сохраняем в историю
        self.history.append(self.input_line)
        self.history_index = -1

        # парсим команду
        parts = self.input_line.strip().split()
        cmd = parts[0].lower()
        args = parts[1:]

        # --- Здесь вы определяете свои команды ---
        if cmd == "help":
            self._add_output("Доступные команды: help, clear, set_volume <0-100>, set_fps <30-144>, echo <text>")
        elif cmd == "clear":
            self.output_lines.clear()
        elif cmd == "set_volume":
            if args and args[0].isdigit():
                vol = int(args[0])
                vol = max(0, min(100, vol))
                self.game.setVolume(vol)   # вызываем метод объекта game
                self._add_output(f"Громкость установлена на {vol}%")
            else:
                self._add_output("Использование: set_volume <0-100>", (255,0,0))
        elif cmd == "set_fps":
            if args and args[0].isdigit():
                fps = int(args[0])
                fps = max(30, min(144, fps))
                self.game.setFrame(fps)
                self._add_output(f"FPS установлен на {fps}")
            else:
                self._add_output("Использование: set_fps <30-144>", (255,0,0))
        elif cmd == "echo":
            self._add_output(" ".join(args))
        else:
            self._add_output(f"Неизвестная команда: {cmd}", (255,0,0))

        self.input_line = ""

    def _navigate_history(self, direction):
        if not self.history:
            return
        if direction == -1:  # вверх
            if self.history_index + 1 < len(self.history):
                self.history_index += 1
        elif direction == 1: # вниз
            if self.history_index - 1 >= -1:
                self.history_index -= 1
        if self.history_index >= 0:
            self.input_line = self.history[self.history_index]
        else:
            self.input_line = ""

    def _add_output(self, text, color=None):
        if color is None:
            color = self.text_color
        self.output_lines.append((text, color))

    def draw(self, surface):
        if not self.is_open:
            return

        # создаём прозрачную поверхность для консоли
        console_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        console_surf.fill(self.bg_color)

        # отрисовка вывода (последние 15 строк)
        y = 10
        for line, col in self.output_lines[-15:]:
            txt = self.font.render(line, True, col)
            console_surf.blit(txt, (10, y))
            y += self.font_size + 2

        # строка ввода
        input_text = f"> {self.input_line}"
        input_surf = self.font.render(input_text, True, self.text_color)
        input_y = self.height - self.font_size - 10
        console_surf.blit(input_surf, (10, input_y))

        # курсор
        if (pygame.time.get_ticks() // 500) % 2 == 0:
            cursor_x = 10 + input_surf.get_width()
            cursor = self.font.render("_", True, self.text_color)
            console_surf.blit(cursor, (cursor_x, input_y))

        # рамка
        pygame.draw.rect(console_surf, self.text_color, console_surf.get_rect(), 2)

        # размещаем консоль внизу экрана
        surface.blit(console_surf, (0, surface.get_height() - self.height))