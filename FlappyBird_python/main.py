import pygame
from sys import exit
import random

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
score = 0
font = pygame.font.SysFont("Arial",30)
game_stopped = True

class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = bird_images[0]
        self.rect = self.image.get_rect()
        self.rect.center = bird_start_position
        self.image_index = 0
        self.vel = 0
        self.flap = False
        self.alive = True

    def update(self,user_input):
        if self.alive:
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
        if user_input[pygame.K_SPACE] and not self.flap and self.rect.y > 0 and self.alive:
            self.flap = True
            self.vel = -7

        self.image = pygame.transform.rotate(self.image,self.vel * -7)


class Pipe(pygame.sprite.Sprite):
    def __init__(self,x,y,image,pipe_type):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = x,y
        self.enter,self.exit,self.passed = False,False,False
        self.pipe_type = pipe_type
        
    def update(self):
        self.rect.x -= scroll_speed
        if self.rect.x <= -window_width:
            self.kill()

        global score
        if self.pipe_type =="bottom":
            if bird_start_position[0] > self.rect.topleft[0] and not self.passed:
                self.enter = True
            if bird_start_position[0] > self.rect.topright[0] and not self.passed:
                self.exit = True
            if self.enter and self.exit and not self.passed:
                self.passed = True
                score += 1


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
    global score

    bird = pygame.sprite.GroupSingle()
    bird.add(Bird())

    pipe_timer = 0
    pipes = pygame.sprite.Group()

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

        pipes.draw(window)
        ground.draw(window)
        bird.draw(window)

        score_text = font.render('Score: ' + str(score),True,pygame.Color(255,255,255))
        window.blit(score_text,(20,20))

        if bird.sprite.alive:
            pipes.update()
            ground.update()
        bird.update(user_input)


        collisions_pipe = pygame.sprite.spritecollide(bird.sprite,pipes,False)
        collisions_ground = pygame.sprite.spritecollide(bird.sprite,ground,False)
        if collisions_pipe or collisions_ground:
            bird.sprite.alive = False
            if collisions_ground:
                window.blit(game_over_image,(window_width // 2 - game_over_image.get_width() //2,
                                             window_height // 2 - game_over_image.get_height() // 2 ))
                if user_input[pygame.K_r]:
                    score = 0
                    break

        if pipe_timer <= 0 and bird.sprite.alive:
            x_top,x_bottom = 550,550
            y_top = random.randint(-600,-480)
            y_bottom = y_top +random.randint(90,130) + bottom_pipe_image.get_height()
            pipes.add(Pipe(x_top,y_top,top_pipe_image,'top'))
            pipes.add(Pipe(x_bottom,y_bottom,bottom_pipe_image,'bottom'))
            pipe_timer = random.randint(180,250)
        pipe_timer -= 1    
        clock.tick(60)
        pygame.display.update()

# main menu
def main_menu():
    global game_stopped
    while game_stopped:
        quit_game()

        window.fill((0,0,0))
        window.blit(skyline_image,(0,0))
        window.blit(ground_image,(0,520))
        window.blit(bird_images[0],(100,250))
        window.blit(start_image,(window_width // 2  - start_image.get_width() // 2,
                    window_height // 2 - start_image.get_height() // 2))
        
        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE]:
            main()
        pygame.display.update() 
main_menu()
