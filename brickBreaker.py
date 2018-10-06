# Pygame setup
import pygame
import random
pygame.init()

# Game window setup
game_width = 800
game_height = 600
game_display = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption('Brick Breaker!')

# Variables
no_bricks = 7
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
        self.width = self.sprite.get_size()[0]
        self.height = self.sprite.get_size()[1]

    def draw(self):
        game_display.blit(self.sprite, (self.x, self.y))

class Player(GameObject):
    def __init__(self, sprite, scale_x, scale_y, x_pos, y_pos):
        GameObject.__init__(self, sprite, scale_x, scale_y, x_pos, y_pos)
        self.moving_left = False
        self.moving_right = False
        self.speed = 10

    def move(self):
        if self.moving_left and self.x > 0:
            self.x -= self.speed
        if self.moving_right and self.x < (game_width - self.width):
            self.x += self.speed

    def update(self):
        self.move()
        self.draw()

class Ball(GameObject):
    def __init__(self, sprite, scale_x, scale_y, x_pos, y_pos):
        GameObject.__init__(self, sprite, scale_x, scale_y, x_pos, y_pos)
        self.x_speed = random.randint(-5, 5)
        self.y_speed = random.randint(-5, 5)

    def move(self):
        if self.x > 0 and self.x_speed < 0:
            self.x += self.x_speed
        elif self.x < (game_width - self.width) and self.x_speed > 0:
            self.x += self.x_speed
        else:
            self.x_speed = -(self.x_speed)

        if self.y > 0 and self.y_speed < 0:
            self.y += self.y_speed
        elif self.y < (game_height - self.height) and self.y_speed > 0:
            self.y += self.y_speed
        else:
            self.y_speed = -(self.y_speed)
    
    def update(self):
        self.move()
        self.draw()

class Brick(GameObject):
    def __init__(self, sprite, scale_x, scale_y, x_pos, y_pos):
        GameObject.__init__(self, sprite, scale_x, scale_y, x_pos, y_pos)

def collission_check(GameObject1, GameObject2):
    if (GameObject1.x < GameObject2.x + GameObject2.width and
   GameObject1.x + GameObject1.width > GameObject2.x and
   GameObject1.y < GameObject2.y + GameObject2.height and
   GameObject1.height + GameObject1.y > GameObject2.y):
        return True
    else:
        return False

# Setup game objects
player = Player(pygame.image.load('./assets/player.png'), 0.5, 0.1, 0, game_height - 50)
ball = Ball(pygame.image.load('./assets/ball.png'), 0.1, 0.1, 100, 100)
bricks = []
for i in range(0, no_bricks):
    bricks.append(Brick(pygame.image.load('./assets/brick.png'), 0.25, 0.1, i * 100, 0))

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

    if collission_check(player, ball):
        ball.x_speed = -(ball.x_speed)
        ball.y_speed = -(ball.y_speed)

    # Draw objects
    game_display.fill(white)
    player.update()
    ball.update()
    for i in range(0, len(bricks)):
        bricks[i].draw()

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()