import pygame
from sys import exit

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird")

# window dimensions
window_width = 600
window_height = 800
window = pygame.display.set_mode((window_width, window_height))

# images
bird_images = [pygame.image.load("assets/bird_down.png"),
               pygame.image.load("assets/bird_mid.png"),
               pygame.image.load("assets/bird_up.png")]
skyline_image = pygame.image.load("assets/background.png")
game_over_image = pygame.image.load("assets/game_over.png")
ground_image = pygame.image.load("assets/ground.png")
start_image = pygame.image.load("assets/start.png")
top_pipe_image = pygame.image.load("assets/pipe_top.png")
bottom_pipe_image = pygame.image.load("assets/pipe_bottom.png")

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def main():
    run = True
    while run:
        quit_game()
        clock.tick(60)
        window.fill((0, 0, 0))  # Fill the window with black
        pygame.display.update()
main()