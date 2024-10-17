import pygame
from pygame.examples.go_over_there import screen

pygame.init()
win = pygame.display.set_mode((618, 359))

pygame.display.set_caption('Cubes Game')

walkRight = [pygame.image.load('Game/right-1.png').convert_alpha(), pygame.image.load('Game/right-2.png').convert_alpha(),
             pygame.image.load('Game/right-3.png').convert_alpha(), pygame.image.load('Game/right-4.png').convert_alpha()]

walkLeft = [pygame.image.load('Game/left-1.png').convert_alpha(), pygame.image.load('Game/left-2.png').convert_alpha(),
            pygame.image.load('Game/left-3.png').convert_alpha(), pygame.image.load('Game/left-4.png').convert_alpha()]

playerStand = pygame.image.load('Game/right-1.png').convert_alpha()



clock = pygame.time.Clock()

bg = pygame.image.load('Game/fone1.png').convert()

x = 50
y = 250
width = 46
height = 56
speed = 5

isJump = False
jumpCount = 10

left = False
right = False
walkCount = 0
lastMove = 'right'

bg_sound = pygame.mixer.Sound('sound/egor.mp3')
bg_sound.play()

ghost = pygame.image.load('Game/prizrak.png').convert_alpha()
ghost_list_in_game = []

bg_x = 0

gameplay = True
label = pygame.font.Font('fonts/SixtyfourConvergence-Regular.ttf', 40)
lose_label = label.render('Вы проиграли!', False, (193, 196, 199))
restart_label = label.render('Играть заново', False, (115, 132, 148))
restart_label_rect = restart_label.get_rect(topleft=(180, 200))

patron = pygame.image.load('Game/patron.png').convert_alpha()


run = True
bullets = []

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 2500)

def drawWindow():
    global walkCount, bg_x, run, gameplay
    win.blit(bg, (bg_x, 0))
    win.blit(bg, (bg_x + 618, 0))

    player_rect = walkLeft[0].get_rect(topleft=(x, y))


    if ghost_list_in_game:
        for i, el in enumerate(ghost_list_in_game):
            win.blit(ghost, el)
            el.x -= 10

            if el.x < -10:
                ghost_list_in_game.pop(i)

            if player_rect.colliderect(el):
                gameplay = False

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

    if bg_x == -618:
        bg_x = 0
    else:
        bg_x -= 2


while run:
    clock.tick(20)
    keys = pygame.key.get_pressed()
    if gameplay:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == ghost_timer:
                ghost_list_in_game.append(ghost.get_rect(topleft=(620, 250)))
            if event.type == pygame.KEYUP and gameplay and event.key == pygame.K_f:
                bullets.append(patron.get_rect(topleft=(x + 30, y + 10)))


        if keys[pygame.K_f]:
            bullets.append(patron.get_rect(topleft=(x + 30, y + 10)))

        if bullets:
            for i, el in enumerate(bullets):
                win.blit(patron, (el.x, el.y))
                el.x += 4

                if el.x > 630:
                    bullets.pop(i)

                if ghost_list_in_game:
                    for (index, monster) in enumerate(ghost_list_in_game):
                        if el.colliderect(monster):
                            ghost_list_in_game.pop(index)
                            bullets.pop(i)


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

    else:
        win.fill((87, 88, 89))
        win.blit(lose_label, (180, 100))
        win.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed():
            gameplay = True
            player_x = 150
            ghost_list_in_game.clear()
            bullets.clear()

    pygame.display.update()

pygame.quit()