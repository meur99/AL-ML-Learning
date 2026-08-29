from enum import IntEnum
from collections import deque
import random
import pygame


class Snake_Game:
    TILE_SIZE = 20 # also step size

    class DIRECTION(IntEnum):
        UP    = 0
        RIGHT = 1
        DOWN  = 2
        LEFT  = 3

        def right(self):
            return Snake_Game.DIRECTION((self.value + 1) % 4)

        def left(self):
            return Snake_Game.DIRECTION((self.value - 1) % 4)

        def coordinates(self):
            ts = Snake_Game.TILE_SIZE
            return [(0, -ts), (ts, 0), (0, ts), (-ts, 0)][self.value]


    def __init__(self):
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))

        self.screen_edges = [ #TRBL
            pygame.Rect(0, -1, 600, 1),
            pygame.Rect(600, 0, 1, 600),
            pygame.Rect(0, 600, 600, 1),
            pygame.Rect(-1, 0, 1, 600)
        ]

        # snake
        self.snake_body = deque([
            pygame.Rect(280, 280, self.TILE_SIZE, self.TILE_SIZE),
            pygame.Rect(260, 280, self.TILE_SIZE, self.TILE_SIZE),
            pygame.Rect(240, 280, self.TILE_SIZE, self.TILE_SIZE),
            pygame.Rect(220, 280, self.TILE_SIZE, self.TILE_SIZE)
        ])

        self.direction = self.DIRECTION.RIGHT
        self.food = self.spawn_food()
        self.game_over = False
        self.reward = 0
        self.update_display()


    def update_snake_position(self, grow=False):
        new_head = self.snake_body[0].move(self.direction.coordinates())
        self.snake_body.appendleft(new_head)

        if not grow:
            self.snake_body.pop()


    def spawn_food(self):
        # add check to not spawn on snake
        while True:
            x = random.randrange(0, 600, 20)
            y = random.randrange(0, 600, 20)
            food = pygame.Rect(x, y, self.TILE_SIZE, self.TILE_SIZE)

            if food.collidelist(self.snake_body) == -1:
                return food


    def update_display(self):
        self.screen.fill("black")
        pygame.draw.rect(self.screen, "red", self.food)
        for r in self.snake_body:
            pygame.draw.rect(self.screen, "white", r)
        pygame.draw.rect(self.screen, "gray", self.snake_body[0])
        pygame.display.flip()


    def get_food_direction(self):
        Sx, Sy = self.snake_body[0].center
        Fx, Fy = self.food.center



        food_direction = [0, 0]
        if (Sy - Fy) > 0: fd += 'N'
        elif (Sy - Fy) < 0: fd += 'S'
        if (Sx - Fx) > 0: fd += 'W'
        elif (Sx - Fx) < 0: fd += 'E'
        return ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'].index(fd)


    def get_obstacle_direction(self):
        straight = self.direction
        left = self.direction.left()
        right = self.direction.right()

        s_head = self.snake_body[0].move(straight)
        l_head = self.snake_body[0].move(left)
        r_head = self.snake_body[0].move(right)

        obstacle_direction = [0, 0, 0]
        obstacles = list(self.snake_body)[1:] + self.screen_edges
        if l_head.collidelist(obstacles) != -1: obstacle_direction[0] = 1
        if s_head.collidelist(obstacles) != -1: obstacle_direction[1] = 1
        if r_head.collidelist(obstacles) != -1: obstacle_direction[2] = 1
        return obstacle_direction


    def get_state(self):
        return dict({
            "score": len(self.snake_body) - 4,
            "snake_direction": self.direction,
            "food_direction": self.get_food_direction(),
            "obstacle_direction": self.get_obstacle_direction(),
            "game_over": self.game_over,
            "reward": self.reward
        })
    

    def move(self, action=(0, 1, 0)):

        if action == (1, 0, 0):
            self.direction = self.direction.left()

        elif action == (0, 1, 0):
            pass

        elif action == (0, 0, 1):
            self.direction = self.direction.right()

        self.update_snake_position()
        
        if self.snake_body[0].colliderect(self.food):
            self.reward = 10
            self.update_snake_position(grow=True)
            self.food = self.spawn_food()

        obstacles = list(self.snake_body)[1:] + self.screen_edges
        if self.snake_body[0].collidelist(obstacles) != -1:
            self.reward = -10
            self.game_over = True

        
        self.update_display()
        return self.get_state()



if __name__ == '__main__':
    game = Snake_Game()
    clock = pygame.time.Clock()

    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    state = game.move(action=(0, 0, 1))

                elif event.key == pygame.K_LEFT:
                    state = game.move(action=(1, 0, 0))

                else:
                    state = game.move()

                for k,v in state.items():
                    print(k, v)

                if state["game_over"]:
                    exit()
                clock.tick(10)