# Pygame setup
import pygame
import random
pygame.init()

# Variables
no_bricks = 100
clock = pygame.time.Clock()
running = True
fps = 60
lives = 3
game_width = 1000
game_height = 600
brick_width = 50
brick_height = 20

# Game window setup
game_display = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption('Brick Breaker!')

# Colours
black = (0, 0, 0)
white = (255, 255, 255)

class Game():
    def __init__(self, width, height):
        self.black = (0, 0, 0)
        self.width = width
        self.height = height

    @staticmethod
    def collission(GameObject1, GameObject2):
        if (GameObject1.x < GameObject2.x + GameObject2.width and
        GameObject1.x + GameObject1.width > GameObject2.x and
        GameObject1.y < GameObject2.y + GameObject2.height and
        GameObject1.height + GameObject1.y > GameObject2.y):
            return True
        else:
            return False

    @staticmethod
    def scale_image(image, width, height):
        scaled_image = pygame.transform.scale(image, (width, height))
        return scaled_image

# Game Objects
class GameObject:
    def __init__(self, sprite, width, height, x_pos, y_pos):
        self.sprite = Game.scale_image(sprite, width, height)
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
        self.base_speed = 5
        self.x_speed = self.base_speed * random.randint(-1, 1)
        self.y_speed = self.base_speed * random.randint(-1, 1)
        while self.x_speed == 0:
            self.x_speed = self.base_speed * random.randint(-1, 1)
        while self.y_speed == 0:
            self.y_speed = self.base_speed * random.randint(-1, 1)
        self.active = True

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
        elif self.y + self.height > game_height:
            lives -= 1
        else:
            self.y_speed = -(self.y_speed)
    
    def bounce(self):
        if self.x_speed > 0 and self.y_speed < 0:
            self.y_speed = -(self.y_speed)
        elif self.x_speed > 0 and self.y_speed > 0:
            self.x_speed = -(self.x_speed)
        elif self.x_speed < 0 and self.y_speed > 0:
            self.y_speed = -(self.y_speed)
        elif self.x_speed < 0 and self.y_speed < 0:
            self.x_speed = -(self.x_speed)
    
    def bounce_up_left(self):
        self.x_speed = -(self.base_speed)
        self.y_speed = -(self.y_speed)
    
    def bounce_up_right(self):
        self.x_speed = self.base_speed
        self.y_speed = -(self.y_speed)
    
    def update(self):
        self.move()
        self.draw()

class Brick(GameObject):
    def __init__(self, sprite, scale_x, scale_y, x_pos, y_pos):
        GameObject.__init__(self, sprite, scale_x, scale_y, x_pos, y_pos)

# Setup game objects
game = Game(game_width, game_height)
player = Player(pygame.image.load('./assets/player.png'), 100, 20, 0, game_height - 40)
bricks = []
row = 0

for i in range(0, no_bricks):
    if game_width < (i * (brick_width + 10)) - (row * game_width):
        row += 1
        
    bricks.append(Brick(pygame.image.load('./assets/brick.png'), brick_width, brick_height, (i * (brick_width + 10)) - (row * game_width), row * (brick_height + 10)))

ball = Ball(pygame.image.load('./assets/ball.png'), 25, 25, 100, 400)

# Game loop
while running and lives >= 0:

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

    if Game.collission(player, ball):
        if (ball.x + ball.width) < (player.x + (player.width / 4)):
            ball.bounce_up_left()
        if (player.x + player.width - (player.width / 4)) < ball.x:
            ball.bounce_up_right()
        else:
            ball.bounce()

    # Draw objects
    game_display.fill(white)
    player.update()
    ball.update()
    for brick in bricks:
        if Game.collission(ball, brick):
            bricks.remove(brick)
            ball.bounce()
        else:
            brick.draw()

    # Check the ball hasn't fallen down the bottom
    if not ball.active:
        ball = Ball(pygame.image.load('./assets/ball.png'), 25, 25, 100, 100)

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
quit()