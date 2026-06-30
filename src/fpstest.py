import pygame
import time
import statistics

def measure_frame_delay(fps, frames=100):
    """
    Запускает игровой цикл с указанным FPS на заданное количество кадров
    и измеряет фактическую задержку между кадрами.
    Возвращает словарь со статистикой: средняя, мин, макс, стд.
    """
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    clock = pygame.time.Clock()
    
    delays = []
    for _ in range(frames):
        start = time.perf_counter()
        clock.tick(fps)          # ограничение FPS
        elapsed = time.perf_counter() - start
        delays.append(elapsed)
        # Небольшая имитация работы (например, обработка событий)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
        # Здесь можно что-то нарисовать (опционально)
        pygame.display.flip()
    
    pygame.quit()
    
    if delays:
        return {
            'fps': fps,
            'avg': statistics.mean(delays),
            'min': min(delays),
            'max': max(delays),
            'stdev': statistics.stdev(delays) if len(delays) > 1 else 0
        }
    return None

# Пример использования:
if __name__ == "__main__":
    for fps in [30, 60, 120, 144]:
        stats = measure_frame_delay(fps, frames=60)
        if stats:
            print(f"FPS={fps}: средняя задержка={stats['avg']*1000:.2f} мс, "
                  f"мин={stats['min']*1000:.2f} мс, макс={stats['max']*1000:.2f} мс, "
                  f"стд={stats['stdev']*1000:.2f} мс")