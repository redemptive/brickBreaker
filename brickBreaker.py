# Pygame setup
import pygame
pygame.init()

# Game window setup
game_width = 800
game_height = 600
game_display = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption('Brick Breaker!')

# Variables
player_x = 0
player_y = game_height
player_move_speed = 10
player_right = False
player_left = False
clock = pygame.time.Clock()
running = True
fps = 60

# Colours
black = (0, 0, 0)
white = (255, 255, 255)

# Functions
def scale_image(image, scale_x, scale_y):
    scaled_image = pygame.transform.scale(image, (int(image.get_size()[0] * scale_x), int(image.get_size()[1] * scale_y)))
    return scaled_image

# Game Objects
class GameObject:
    def __init__(self, sprite, scale_x, scale_y, x_pos, y_pos):
        self.sprite = scale_image(sprite, scale_x, scale_y)
        self.x = x_pos
        self.y = y_pos

    def draw(self):
        game_display.blit(self.sprite, (self.x, self.y))

class Player(GameObject):
    def __init__(self, sprite, scale_x, scale_y, x_pos, y_pos):
        GameObject.__init__(self, sprite, scale_x, scale_y, x_pos, y_pos)
        self.moving_left = False
        self.moving_right = False
        self.speed = 10

    def move(self):
        if self.moving_left:
            self.x -= self.speed
        if self.moving_right:
            self.x += self.speed

class Ball(GameObject):
    def __init__(self, sprite, scale_x, scale_y, x_pos, y_pos):
        GameObject.__init__(self, sprite, scale_x, scale_y, x_pos, y_pos)

# Setup game objects
player = Player(pygame.image.load('./assets/player.png'), 0.5, 0.1, 0, game_height - 50)
ball = Ball(pygame.image.load('./assets/ball.png'), 0.1, 0.1, 0, 0)

# Game loop
while running:

    # Event handlers
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.moving_right = True
            if event.key == pygame.K_LEFT:
                player.moving_left = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player.moving_right = False
            if event.key == pygame.K_LEFT:
                player.moving_left = False

    
    # Player movement
    player.move()

    # Draw objects
    game_display.fill(white)
    player.draw()
    ball.draw()

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()