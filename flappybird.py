import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Game variables
gravity = 0.5
bird_movement = 0
bird_x = 50
bird_y = SCREEN_HEIGHT // 2

pipe_width = 70
pipe_gap = 200
pipe_velocity = 3

# Load Images
background_img = pygame.image.load("background.png")
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

bird_img = pygame.image.load("Flappy.png")
bird_img = pygame.transform.scale(bird_img, (45, 45))
bird_rect = bird_img.get_rect(center=(bird_x, bird_y))

# Pipes
pipes = []
pipe_frequency = 2000
last_pipe = pygame.time.get_ticks()

# Fonts
font = pygame.font.Font(None, 36)

# Score
score = 0
scored_pipes = []

# Retry and Cancel menu
def game_over_menu():
    while True:
        screen.fill(BLACK)
        game_over_text = font.render("Game Over!", True, WHITE)
        retry_text = font.render("Press R to Retry", True, WHITE)
        cancel_text = font.render("Press Q to Quit", True, WHITE)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 200))
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, 300))
        screen.blit(cancel_text, (SCREEN_WIDTH // 2 - cancel_text.get_width() // 2, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Retry
                if event.key == pygame.K_q:
                    return False  # Quit

def draw_pipes(pipe_list):
    for pipe in pipe_list:
        pygame.draw.rect(screen, GREEN, pipe)

def move_pipes(pipe_list):
    for pipe in pipe_list:
        pipe.x -= pipe_velocity
    return [pipe for pipe in pipe_list if pipe.right > 0]

def check_collision(pipe_list):
    for pipe in pipe_list:
        if bird_rect.colliderect(pipe):
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT:
        return True
    return False

def create_pipe():
    height = random.randint(150, SCREEN_HEIGHT - 150 - pipe_gap)
    top_pipe = pygame.Rect(SCREEN_WIDTH, height - pipe_gap - SCREEN_HEIGHT, pipe_width, SCREEN_HEIGHT)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, height, pipe_width, SCREEN_HEIGHT - height)
    return top_pipe, bottom_pipe

clock = pygame.time.Clock()

# Main game loop
while True:
    bird_movement = 0
    bird_rect.center = (bird_x, bird_y)
    pipes = []
    score = 0
    scored_pipes = []
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_movement = -8

        bird_movement += gravity
        bird_rect.y += bird_movement

        time_now = pygame.time.get_ticks()
        if time_now - last_pipe > pipe_frequency:
            pipes.extend(create_pipe())
            last_pipe = time_now

        pipes = move_pipes(pipes)

        if check_collision(pipes):
            running = False

        for pipe in pipes:
            if pipe.centerx < bird_rect.centerx and pipe not in scored_pipes and pipe.height > 0:
                score += 1
                scored_pipes.append(pipe)

        screen.blit(background_img, (0, 0))
        draw_pipes(pipes)
        screen.blit(bird_img, bird_rect)

        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    # Show retry and cancel menu
    retry = game_over_menu()
    if not retry:
        break

pygame.quit()
