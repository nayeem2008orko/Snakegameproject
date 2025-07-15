import sys
import os
import pygame

def resource_path(relative_path):
    """Get absolute path to resource, works for dev and PyInstaller"""
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

class Snake:
    def __init__(self, cols, rows,speed=7, wrap_around = False,density = 0):
        self.cols = cols
        self.rows = rows
        self.body = [(cols // 2, rows // 2)]
        self.direction = (0, -1)
        self.growing = False
        self.speed = speed
        self.wrap_around = wrap_around
        segment_img_path = resource_path(os.path.join("Graphics", "snake_segment.png"))
        head_img_path = resource_path(os.path.join("Graphics", "snake_head.png"))
        self.segment_img = pygame.image.load(segment_img_path).convert_alpha()
        self.head_img = pygame.image.load(head_img_path).convert_alpha()
    def change_direction(self, dir):
        x, y = self.direction
        if dir == "UP" and y == 0:
            self.direction = (0, -1)
        elif dir == "DOWN" and y == 0:
            self.direction = (0, 1)
        elif dir == "LEFT" and x == 0:
            self.direction = (-1, 0)
        elif dir == "RIGHT" and x == 0:
            self.direction = (1, 0)

    def move(self):
        head = self.head()
        dx, dy = self.direction
        new_x = head[0] + dx
        new_y = head[1] + dy
        if self.wrap_around:
            new_x = new_x % self.cols
            new_y = new_y % self.rows
        else:
            # Stop if out of bounds
            if new_x < 0 or new_x >= self.cols or new_y < 0 or new_y >= self.rows:
                self.body.insert(0, (-1, -1))  # Force collision
                return
        new_head = (new_x, new_y)
        self.body.insert(0, new_head)

        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

    def grow(self):
        self.growing = True

    def head(self):
        return self.body[0]

    def collides_with_self(self):
        return self.head() in self.body[1:]

    def draw(self, screen, size):
        head = True

        for segment in self.body:
            x, y = segment[0] * size, segment[1] * size
            image = self.head_img if head else self.segment_img
            screen.blit(pygame.transform.scale(image, (size, size)), (x, y))
            head = False

    def check_collision(self, maze):
        head = self.head()
        # Collision with self
        if head in self.body[1:]:
            return True
        # Collision with walls (only if wrap_around is off)
        if not self.wrap_around and (head[0] < 0 or head[0] >= self.cols or head[1] < 0 or head[1] >= self.rows):
            return True
        # Collision with maze walls
        return maze.check_collision(head)
    def eat(self, food):
        if self.head() == food.position:
            self.grow()
            return True
        return False