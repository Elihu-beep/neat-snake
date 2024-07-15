from settings import *
from snake import Snake
from apple import Apple

class Main:
    def __init__(self):

        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.score = 0

        pygame.font.init() 
        self.font = pygame.font.SysFont('Calibri', 24)

        self.snake = Snake()
        self.apple = Apple(self.snake)

        self.update_event = pygame.event.custom_type()
        pygame.time.set_timer(self.update_event, 200)
        self.game_active = False
        
        pygame.display.set_caption('Snake')

    def input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.snake.direction = pygame.Vector2(-1,0) if self.snake.direction.x != 1 else self.snake.direction
        if keys[pygame.K_RIGHT]:
            self.snake.direction = pygame.Vector2(1,0) if self.snake.direction.x != -1 else self.snake.direction
        if keys[pygame.K_UP]:
            self.snake.direction = pygame.Vector2(0,-1) if self.snake.direction.y != 1 else self.snake.direction
        if keys[pygame.K_DOWN]:
            self.snake.direction = pygame.Vector2(0,1) if self.snake.direction.y != -1 else self.snake.direction
        
    def reset(self):
        print("Score: ", self.score)
        self.snake.reset()
        self.apple.set_pos()
        self.snake.update_head()
        self.snake.update_tail()
        self.snake.update_body()
        self.score = 0
        self.game_active = False

    def apple_collision(self):
        if self.snake.body[0] == self.apple.pos:
            self.snake.ate = True
            self.apple.set_pos()
            self.score += 1

    def collision(self):
         if self.snake.body[0] in self.snake.body[1:] or \
         self.snake.body[0][0] >= COLS  or self.snake.body[0][0] < 0 or \
         self.snake.body[1][1] >= ROWS or self.snake.body[1][1] < 0:
             self.reset()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                if event.type == self.update_event and self.game_active:
                    self.snake.move()

                if event.type == pygame.KEYDOWN and not self.game_active:
                    self.game_active = True
            
            self.display_surface.fill(BG_COLOR)
            self.input()
            self.apple_collision()
            self.snake.draw()
            self.apple.draw()
            self.collision()
            self.text_surface = self.font.render(f"SCORE: {self.score}", False, (255, 255, 255))
            self.display_surface.blit(self.text_surface, (10,10))

            pygame.display.update()

main = Main()
main.run()
