import pygame
import sys
import random
import os
from game.snake import Snake
from game.food import Food
from game.maze import Maze
def resource_path(relative_path):
    import sys
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_highscore_file(difficulty):
    # Hidden folder inside the user's AppData (or temp dir)
    import tempfile
    folder = os.path.join(tempfile.gettempdir(), "snake_highscores")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, f"highscore_{difficulty.lower()}.dat")

def read_highscore(difficulty):
    filename = get_highscore_file(difficulty)
    if os.path.exists(filename):
        with open(filename, "r") as f:
            try:
                return int(f.read())
            except:
                return 0
    return 0

def write_highscore(difficulty, score):
    filename = get_highscore_file(difficulty)
    highscore = read_highscore(difficulty)
    if score > highscore:
        with open(filename, "w") as f:
            f.write(str(score))
        return score
    return highscore
# Initialize Pygame
pygame.init()
pygame.mixer.init()
# Load sounds
hover_sound = pygame.mixer.Sound(resource_path("Sounds/hover.wav"))
click_sound = pygame.mixer.Sound(resource_path("Sounds/click.wav"))
eat_sound = pygame.mixer.Sound(resource_path("Sounds/eat.wav"))
pygame.mixer.music.load(resource_path("Sounds/bgm.mp3"))
pygame.mixer.music.set_volume(0.3)  # Optional: adjust background volume
# Fullscreen, borderless setup
screen = pygame.display.set_mode((0, 0), pygame.NOFRAME | pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
ROWS, COLS = 20, 20  # Grid dimensions

# Font
font = pygame.font.SysFont("Arial", 30)

# Clock
clock = pygame.time.Clock()

# Utility Functions
def draw_text(surface, text, font, color, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect(center=(x, y))
    surface.blit(textobj, textrect)
class Button:
    def __init__(self, rect, text, font, idle_color, hover_color, text_color):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.idle_color = idle_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.idle_color
        pygame.draw.rect(surface, color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return self.hovered and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

def main_menu():
    pygame.mixer.music.play(-1)  # Loop background music

    button_font = pygame.font.SysFont("Arial", 36)
    start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    exit_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 70, 200, 50)

    hovered = {"start": False, "exit": False}

    while True:
        screen.fill((0, 0, 0))
        draw_text(screen, "Snake Game", font, (0, 255, 0), WIDTH // 2, HEIGHT // 2 - 100)

        mouse_pos = pygame.mouse.get_pos()

        for button, rect, key in [
            ("Start Game", start_button, "start"),
            ("Exit", exit_button, "exit")
        ]:
            color = (50, 150, 50) if hovered[key] else (0, 100, 0)
            if rect.collidepoint(mouse_pos):
                if not hovered[key]:
                    hover_sound.play()
                hovered[key] = True
            else:
                hovered[key] = False
            pygame.draw.rect(screen, color, rect)
            draw_text(screen, button, button_font, (255, 255, 255), rect.centerx, rect.centery)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    click_sound.play()
                    pygame.mixer.music.stop()
                    return
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    if start_button.collidepoint(mouse_pos):
                        click_sound.play()
                        pygame.mixer.music.stop()
                        return
                    elif exit_button.collidepoint(mouse_pos):
                        click_sound.play()
                        pygame.quit()
                        sys.exit()
def choose_difficulty(screen, font):
    while True:
        screen.fill((0, 0, 50))
        draw_text(screen, "Choose Difficulty", font, (255, 255, 255), WIDTH // 2, HEIGHT // 2 - 100)
        draw_text(screen, "1. Easy", font, (0, 255, 0), WIDTH // 2, HEIGHT // 2 - 30)
        draw_text(screen, "2. Medium", font, (255, 255, 0), WIDTH // 2, HEIGHT // 2 + 30)
        draw_text(screen, "3. Hard", font, (255, 0, 0), WIDTH // 2, HEIGHT // 2 + 90)
        draw_text(screen, "ESC to go back", font, (255, 255, 255), WIDTH // 2, HEIGHT - 60)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    return "Easy"
                elif event.key == pygame.K_2:
                    return "Medium"
                elif event.key == pygame.K_3:
                    return "Hard"
                elif event.key == pygame.K_ESCAPE:
                    return None

def loading_screen(screen, font, difficulty):
    screen.fill((30, 30, 30))
    tips = [
        "Press P to pause",
        "Use W/A/S/D to move",
        "Avoid obstacles in Hard/Medium mode"
    ]
    tip = random.choice(tips)
    draw_text(screen, f"Loading {difficulty} Mode...", font, (255, 255, 255), WIDTH // 2, HEIGHT // 2 - 40)
    draw_text(screen, tip, font, (200, 200, 200), WIDTH // 2, HEIGHT // 2 + 20)
    pygame.display.flip()
    pygame.time.delay(2000)
    screen.fill((30, 30, 30))
    draw_text(screen, "Press any key to continue", font, (255, 255, 255), WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                waiting = False  # exit the wait on any key press

def death_screen(screen, font, score, highscore):
    screen.fill((0, 0, 0))
    draw_text(screen, f"You Died! Score: {score}", font, (255, 0, 0), WIDTH // 2, HEIGHT // 2 - 60)
    draw_text(screen, f"High Score: {highscore}", font, (255, 255, 0), WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Press F to Retry or X to Exit", font, (255, 255, 255), WIDTH // 2, HEIGHT // 2 + 60)
    pygame.display.flip()

def run_game_loop(difficulty):
    size = min(WIDTH // COLS, HEIGHT // ROWS)
    # Setup game parameters
    if difficulty == "Easy":
        base_speed = 7
        density = 0
        wrap_around = True
    elif difficulty == "Medium":
        base_speed = 10
        density = 80
        wrap_around = False
    else:  # Hard
        base_speed = 12
        density = 50
        wrap_around = False
    speed = base_speed
    hard_mode = (difficulty == "Hard")
    medium_mode = (difficulty == "Medium")
    snake = Snake(COLS, ROWS, speed, wrap_around, density)
    maze = Maze(COLS, ROWS, hard_mode, medium_mode, density)
    food = Food(COLS, ROWS, snake, maze)
    score = 0

    running = True
    while running:
        screen.fill((0, 0, 0))
        maze.draw(screen, size, density)
        snake.move()

        if snake.eat(food):
            eat_sound.play()
            score += 1
            food = Food(COLS, ROWS, snake, maze)
            if score%10 == 0:
                speed += 2
        # Check collision only if wrapping is disabled
        if (not snake.wrap_around and snake.head() in maze.walls) or snake.collides_with_self():
            running = False
            break


        food.draw(screen,size)
        snake.draw(screen, size)
        draw_text(screen, f"Score: {score}", font, (255, 255, 255), WIDTH // 2, 30)
        pygame.display.flip()
        clock.tick(speed)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
                    pause_menu()
                elif event.key in [pygame.K_w, pygame.K_w]:
                    snake.change_direction("UP")
                elif event.key in [pygame.K_s, pygame.K_s]:
                    snake.change_direction("DOWN")
                elif event.key in [pygame.K_a, pygame.K_a]:
                    snake.change_direction("LEFT")
                elif event.key in [pygame.K_d, pygame.K_d]:
                    snake.change_direction("RIGHT")

    return score,difficulty

def pause_menu():
    paused = True
    while paused:
        screen.fill((20, 20, 20))
        draw_text(screen, "Game Paused", font, (255, 255, 255), WIDTH // 2, HEIGHT // 2 - 40)
        draw_text(screen, "Press R to Resume or M for Main Menu", font, (200, 200, 200), WIDTH // 2, HEIGHT // 2 + 10)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    paused = False
                elif event.key == pygame.K_m:
                    main()
                    return

def main():
    while True:
        main_menu()
        while True:
            difficulty = choose_difficulty(screen, font)
            if difficulty is None:
                break  # Back to main menu

            loading_screen(screen, font, difficulty)

            score,difficulty = run_game_loop(difficulty)
            highscore = write_highscore(difficulty, score)
            death_screen(screen, font, score,highscore)

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_f:
                            waiting = False  # retry
                        elif event.key == pygame.K_x:
                            pygame.quit()
                            sys.exit()

# Start the game
main()