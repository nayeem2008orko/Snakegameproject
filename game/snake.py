import pygame

class Snake:
    def __init__(self, cols, rows):
        self.body = [(cols // 2, rows // 2)]
        self.direction = (0, -1)
        self.growing = False
        self.speed = 10
        self.segment_img = pygame.image.load("Graphics/snake_segment.png").convert_alpha()
        self.head_img = pygame.image.load("Graphics/snake_head.png").convert_alpha()

    def change_direction(self, dir):
        x, y = self.direction
        if dir == "W" and y == 0:
            self.direction = (0, -1)
        elif dir == "S" and y == 0:
            self.direction = (0, 1)
        elif dir == "A" and x == 0:
            self.direction = (-1, 0)
        elif dir == "D" and x == 0:
            self.direction = (1, 0)

    def move(self):
        head = self.head()
        dx, dy = self.direction
        new_head = (head[0] + dx, head[1] + dy)
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
