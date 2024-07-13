from settings import *

class Snake:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.body = [pygame.Vector2(START_COL - col, START_ROW) for col in range(START_LENGHT)]
        self.direction = pygame.Vector2(1,0)
        self.ate = False

    def move(self):
        if self.ate == False:
            body_copy = self.body[:-1]
            new_head = body_copy[0] + self.direction
            body_copy.insert(0, new_head)
            self.body = body_copy[:]
        else:
            body_copy = self.body[:]
            new_head = body_copy[0] + self.direction
            body_copy.insert(0, new_head)
            self.body = body_copy[:]
            self.ate = False

    def draw(self):
        for point in self.body:
            rect = pygame.Rect(point.x * CELL_SIZE, point.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(self.display_surface, COLOR, rect)

    def reset(self):
        self.body = [pygame.Vector2(START_COL - col, START_ROW) for col in range(START_LENGHT)]
        self.direction = pygame.Vector2(1,0)
