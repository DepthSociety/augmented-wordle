import pygame
pygame.init()

from config import SCREEN_WIDTH, SCREEN_HEIGHT
from scenes.manager import Manager


def main():
    pygame.display.set_caption("Wordle")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    manager = Manager() # Manager sẽ tự khởi tạo các scene

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
        
        # Truyền screen và events vào manager để xử lý
        manager.run(screen, events)
        
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()