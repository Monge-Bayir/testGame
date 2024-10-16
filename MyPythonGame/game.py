import pygame


pygame.init()
win = pygame.display.set_mode((500, 500))

pygame.display.set_caption('Cubes Game')

walkRight = [pygame.image.load('Game/right-1.png'), pygame.image.load('Game/right-2.png'),
             pygame.image.load('Game/right-3.png'), pygame.image.load('Game/right-4.png')]

walkLeft = [pygame.image.load('Game/left-1.png'), pygame.image.load('Game/left-2.png'),
            pygame.image.load('Game/left-3.png'), pygame.image.load('Game/left-4.png')]

playerStand = pygame.image.load('Game/right-1.png')

clock = pygame.time.Clock()

bg = pygame.image.load('Game/fone.png')

x = 50
y = 435
width = 46
height = 56
speed = 5

isJump = False
jumpCount = 10

left = False
right = False
walkCount = 0
lastMove = 'right'


class Kill():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.speed = 8 * facing

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)



run = True
bullets = []

def drawWindow():
    global walkCount
    win.blit(bg, (0, 0))

    if walkCount + 1 >= 20:
        walkCount = 0

    if left:
        win.blit(walkLeft[walkCount // 5], (x, y))
        walkCount += 1
    elif right:
        win.blit(walkRight[walkCount // 5], (x, y))
        walkCount += 1
    else:
        win.blit(playerStand, (x, y))

    for bullet in bullets:
        bullet.draw(win)

    pygame.display.update()


while run:
    clock.tick(20)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.speed
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_f]:
        if lastMove == 'right':
            facing = 1
        else:
            facing = -1
        if len(bullets) < 5:
            bullets.append(Kill(round(x + width // 2), round(y + width // 2), 5, (255, 0, 0), facing))


    if keys[pygame.K_LEFT] and x > 5:
        x -= speed
        left = True
        right = False
        lastMove = 'left'

    elif keys[pygame.K_RIGHT] and x < 500 - width - 5:
        x += speed
        left = False
        right = True
        lastMove = 'right'

    else:
        left = False
        right = False
        walkCount = 0

    if not(isJump):
        if keys[pygame.K_SPACE]:
            isJump = True
    else:
        if jumpCount >= -10:
            if jumpCount < 0:
                y += (jumpCount ** 2) / 2
            else:
                y -= (jumpCount ** 2) / 2
            jumpCount -= 1

        else:
            isJump = False
            jumpCount = 10

    drawWindow()

pygame.quit()