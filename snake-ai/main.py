import pygame
import neat
import os
import random
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

    def reset(self):
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
             return True
         return False

    def eval_genomes(self, genomes, config):
        for genome_id, genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            self.reset()
            fitness = self.run_game(genome, net)
            genome.fitness = fitness

    def run_game(self, genome, net):
        self.game_active = True
        while self.game_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == self.update_event and self.game_active:
                    self.snake.move()

            output = net.activate(self.get_inputs())
            decision = output.index(max(output))
            self.make_move(decision)
            self.apple_collision()
            self.display_surface.fill(BG_COLOR)
            self.snake.draw()
            self.apple.draw()
            self.text_surface = self.font.render(f"SCORE: {self.score}", False, (255, 255, 255))
            self.display_surface.blit(self.text_surface, (10,10))
            pygame.display.update()

            if self.collision():
                self.game_active = False
                return self.score

    def get_inputs(self):
        head_x, head_y = self.snake.body[0]
        apple_x, apple_y = self.apple.pos

        inputs = [
            int(apple_x > head_x),  # Apple right
            int(apple_x < head_x),  # Apple left
            int(apple_y > head_y),  # Apple below
            int(apple_y < head_y),  # Apple above
            self.snake.direction.x,  # Current direction x
            self.snake.direction.y   # Current direction y
        ]
        return inputs

    def make_move(self, decision):
        if decision == 0:
            self.snake.direction = pygame.Vector2(1, 0)  # Right
        elif decision == 1:
            self.snake.direction = pygame.Vector2(-1, 0) # Left
        elif decision == 2:
            self.snake.direction = pygame.Vector2(0, -1) # Up
        elif decision == 3:
            self.snake.direction = pygame.Vector2(0, 1)  # Down

    def run_neat(self, config_file):
        config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file)
        p = neat.Population(config)
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)
        winner = p.run(self.eval_genomes, 50)

        print(f'\nBest genome:\n{winner}')

if __name__ == "__main__":
    config_path = os.path.join(os.path.dirname(__file__), 'config-feedforward.txt')
    main = Main()
    main.run_neat(config_path)