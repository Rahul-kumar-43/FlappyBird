import pygame
from sys import exit

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Flappy Bird")

# window dimensions
window_width = 551
window_height = 722
window = pygame.display.set_mode((window_width, window_height))

# images
bird_images = [pygame.image.load("FlappyBird_python/assets/bird_down.png"),
               pygame.image.load("FlappyBird_python/assets/bird_mid.png"),
               pygame.image.load("FlappyBird_python/assets/bird_up.png")]
skyline_image = pygame.image.load("FlappyBird_python/assets/background.png")
game_over_image = pygame.image.load("FlappyBird_python/assets/game_over.png")
ground_image = pygame.image.load("FlappyBird_python/assets/ground.png")
start_image = pygame.image.load("FlappyBird_python/assets/start.png")
top_pipe_image = pygame.image.load("FlappyBird_python/assets/pipe_top.png")
bottom_pipe_image = pygame.image.load("FlappyBird_python/assets/pipe_bottom.png")

scroll_speed = 1
bird_start_position = (100,250)

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = bird_start_position
        self.image_index = 0
        self.vel = 0
        self.flap = False

    def update(self,user_input):
        self.image_index += 1
        if self.image_index >=30:
            self.image_index = 0
        self.image = bird_images[self.image_index // 10]

        self.vel +=0.5
        if self.vel > 7:
            self.vel = 7
        if self.rect.y < 500:
            self.rect.y +=int(self.vel)
        if self.vel == 0:
            self.flap = False
        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0:
            self.flap = True
            self.vel = -7


class Ground(pygame.sprite.Sprite):
    def __init__(self ,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image = ground_image
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = x,y
    
    def update(self):
        # Move grond
        self.rect.x -= scroll_speed
        if self.rect.x <= -window_width:
            self.kill()

def quit_game():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def main():

    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    x_pos_ground ,y_pos_ground = 0,520
    ground = pygame.sprite.Group()
    ground.add(Ground(x_pos_ground,y_pos_ground))
    run = True
    while run:
        quit_game()
        window.fill((0, 0, 0))  # Fill the window with black
        # the background

        user_input = pygame.key.get_pressed()
        window.blit(skyline_image, (0, 0))

        if len(ground) <=2:
            ground.add(Ground(window_width,y_pos_ground))

        ground.draw(window)
        bird.draw(window)
        ground.update()
        bird.update(user_input)
        clock.tick(60)
        pygame.display.update()
main()