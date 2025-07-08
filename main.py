import sys
import os
import pygame
from game.snake import Snake
from game.food import Food
from game.maze import Maze

def main():
    pygame.init()
    WIDTH, HEIGHT = 640, 480
    TILE_SIZE = 20
    ROWS, COLS = HEIGHT // TILE_SIZE, WIDTH // TILE_SIZE

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("monospace", 20)

    snake = Snake(COLS, ROWS)
    maze = Maze(COLS, ROWS)
    food = Food(COLS, ROWS, snake, maze)

    score = 0
    running = True

    # Load highscore
    if not os.path.exists("highscore.txt"):
        with open("highscore.txt", "w") as f:
            f.write("0")

    with open("highscore.txt", "r") as f:
        highscore = int(f.read())

    while running:
        clock.tick(snake.speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            snake.change_direction("W")
        elif keys[pygame.K_s]:
            snake.change_direction("S")
        elif keys[pygame.K_a]:
            snake.change_direction("A")
        elif keys[pygame.K_d]:
            snake.change_direction("D")

        snake.move()

        if snake.head() == food.position:
            snake.grow()
            score += 1
            food.respawn(snake, maze)

        if snake.collides_with_self() or maze.check_collision(snake.head()):
            running = False

        screen.fill((0, 0, 0))
        maze.draw(screen, TILE_SIZE)
        food.draw(screen, TILE_SIZE)
        snake.draw(screen, TILE_SIZE)

        text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(text, (10, 10))

        pygame.display.flip()

    # Update highscore if needed
    if score > highscore:
        highscore = score
        with open("highscore.txt", "w") as f:
            f.write(str(highscore))

    # Show Game Over screen
    screen.fill((0, 0, 0))
    game_over_text = font.render("YOU DIED", True, (255, 0, 0))
    score_text = font.render(f"Final Score: {score}", True, (255, 255, 255))
    highscore_text = font.render(f"Highscore: {highscore}", True, (255, 255, 0))
    restart_text = font.render("Press F to Restart", True, (255, 255, 255))
    exit_text = font.render("Press X to Exit Game", True, (255, 255, 255))

    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 70))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 35))
    screen.blit(highscore_text, (WIDTH // 2 - highscore_text.get_width() // 2, HEIGHT // 2))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 35))
    screen.blit(exit_text, (WIDTH // 2 - exit_text.get_width() // 2, HEIGHT // 2 + 65))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    waiting = False
                    main()  # Call main again to restart
                elif event.key == pygame.K_x:
                    waiting = False

    pygame.quit()
    sys.exit()

# Start game
main()
