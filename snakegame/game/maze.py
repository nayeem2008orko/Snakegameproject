import pygame
import random
class Maze:
    def __init__(self, cols, rows, hard_mode=False, medium_mode = False,d = 0):
        self.walls = []

        # Border walls (always added)
        for x in range(cols):
            self.walls.append((x, 0))
            self.walls.append((x, rows - 1))
        for y in range(rows):
            self.walls.append((0, y))
            self.walls.append((cols - 1, y))

        if hard_mode or medium_mode:
            self.add_scattered_obstacles(cols, rows,d)

    def add_scattered_obstacles(self, cols, rows,density):
        center_area = pygame.Rect(cols // 2 - 4, rows // 2 - 4, 8, 8)
        wall_count = (cols * rows) // density  # Adjust density here

        attempts = 0
        while len(self.walls) < wall_count + (2 * cols + 2 * rows):  # base wall count
            x = random.randint(1, cols - 2)
            y = random.randint(1, rows - 2)

            if (x, y) not in self.walls and not center_area.collidepoint(x, y):
                self.walls.append((x, y))

            attempts += 1
            if attempts > 5000:  # just in case
                break

    def check_collision(self, pos):
        return pos in self.walls

    def draw(self, screen, size,density):
        if density>0:
            for wall in self.walls:
                rect = pygame.Rect(wall[0]*size, wall[1]*size, size, size)
                pygame.draw.rect(screen, (100, 100, 100), rect)
