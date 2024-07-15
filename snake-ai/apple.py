from settings import *
from snake import Snake
from random import choice
from math import sin

class Apple:
    def __init__(self, snake):
        self.snake = snake
        self.pos = pygame.Vector2(0, 0)
        self.display_surface = pygame.display.get_surface()
        self.set_pos()
        self.surface = pygame.image.load('./assets/apple.png').convert_alpha()

    def set_pos(self):
         available_pos = [pygame.Vector2(x, y) for x in range(COLS) for y in range(ROWS) if pygame.Vector2(x,y) not in self.snake.body]
         self.pos = choice(available_pos)

    def draw(self):
            scale = 1 + sin(pygame.time.get_ticks() / 500) / 3
            self.scaled_surface = pygame.transform.smoothscale_by(self.surface, scale)
            self.scaled_rect = self.scaled_surface.get_rect(
                 center = (self.pos.x * CELL_SIZE + CELL_SIZE / 2, self.pos.y * CELL_SIZE + CELL_SIZE / 2))
            self.display_surface.blit(self.scaled_surface, self.scaled_rect)

