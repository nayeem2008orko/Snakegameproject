import pygame

class Maze:
    def __init__(self, cols, rows):
        self.walls = []
        for x in range(cols):
            self.walls.append((x, 0))
            self.walls.append((x, rows - 1))
        for y in range(rows):
            self.walls.append((0, y))
            self.walls.append((cols - 1, y))

    def check_collision(self, pos):
        return pos in self.walls

    def draw(self, screen, size):
        for wall in self.walls:
            rect = pygame.Rect(wall[0]*size, wall[1]*size, size, size)
            pygame.draw.rect(screen, (100, 100, 100), rect)
