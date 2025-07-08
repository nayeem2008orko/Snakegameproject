import pygame
import random

class Food:
    def __init__(self, cols, rows, snake,maze):
        self.cols = cols
        self.rows = rows
        self.position = (0, 0)
        self.respawn(snake, maze)

    def respawn(self, snake, maze):
        while True:
            pos = (random.randint(0, self.cols - 1), random.randint(0, self.rows - 1))
            if pos not in snake.body and (maze is None or pos not in maze.walls):
                self.position = pos
                break

    def draw(self, screen, size):
        rect = pygame.Rect(self.position[0]*size, self.position[1]*size, size, size)
        pygame.draw.rect(screen, (255, 0, 0), rect)
