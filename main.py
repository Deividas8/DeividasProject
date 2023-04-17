import pygame

# add clock to set fps in future
clock = pygame.time.Clock()

# pygame setup
pygame.init()
bg_image_width = 618
bg_image_height = 359
screen = pygame.display.set_mode((bg_image_width, bg_image_height))  # flags=pygame.NOFRAME
pygame.display.set_caption("Pygame 4 Fun")  # set name of screen
icon = pygame.image.load('images/game_icon.png').convert_alpha()
pygame.display.set_icon(icon)  # set custom programm icon

bg = pygame.image.load('images/background.jpeg').convert()  # connecting background image
# zero screen point
bg_x = 0
bg_y = 0

# UNcomment to listen to background music :)
# bg_sound = pygame.mixer.Sound('sounds/main_sound.mp3')  # connecting the music
# bg_sound.play()

# hero
player_anim_count = 0
player_move = 5
# primary position
player_x = 150
player_y = 240
player_go_left_border = 50
player_go_right_border = 200

is_jump = False
jump_height = 9

# creating new list with images
walk_left = [
    pygame.image.load('images/player_left/player_left_1.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left_2.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left_3.png').convert_alpha(),
    pygame.image.load('images/player_left/player_left_4.png').convert_alpha(),
]
walk_right = [
    pygame.image.load('images/player_right/player_right_1.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right_2.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right_3.png').convert_alpha(),
    pygame.image.load('images/player_right/player_right_4.png').convert_alpha(),
]

# bad guy
enemy = pygame.image.load('images/enemy.png').convert_alpha()
enemy_x = bg_image_width
enemy_y = 250
enemy_list = []

# to create enemy periodically
enemy_timer = pygame.USEREVENT  # timer runs periodically. add + 1 not to get zero
pygame.time.set_timer(enemy_timer, 2500)  # works every 2500 ms

# lose screen
label = pygame.font.Font('fonts/TiltPrism-Regular-VariableFont_XROT,YROT.ttf', 40)
lose_label = label.render('You lose!', False, (212, 4, 4))
lose_label_x = 200
lose_label_y = 100
restart_label = label.render('Play again', False, (9, 186, 71))
restart_label_rect = restart_label.get_rect(topleft=(200, 200))

# weapon
bullets_remaining = 8
bullet = pygame.image.load('images/bullet.png').convert_alpha()
bullets = []  # shots that were made are stored here

gameplay = True

# infinite loop
running = True
while running:

    # adding two background pictures for moving background
    screen.blit(bg, (bg_x, bg_y))
    screen.blit(bg, (bg_x + bg_image_width, bg_y))

    if gameplay:
        # making rectangle object to make possible interaction
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y))

        # for enemy
        if enemy_list:  # checking if any in the list
            for (index, element) in enumerate(enemy_list):
                screen.blit(enemy, element)  # drawing
                element.x -= 10  # moving

                if element.x < -10:
                    enemy_list.pop(index)

                if player_rect.colliderect(element):  # checking for collision of rectangles
                    gameplay = False

        # put info about button to "keys" if button is pressed
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:  # turn hero around
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > player_go_left_border:
            player_x -= player_move
        elif keys[
            pygame.K_RIGHT] and player_x < player_go_right_border:
            player_x += player_move

        if not is_jump:
            if keys[pygame.K_SPACE]:
                is_jump = True
        else:
            if jump_height >= -9:
                if jump_height > 0:
                    player_y -= (jump_height ** 2) / 2  # rising a hero
                else:
                    player_y += (jump_height ** 2) / 2  # landing a hero
                jump_height -= 1
            else:
                is_jump = False
                jump_height = 9

        if player_anim_count == 3:
            player_anim_count = 0
        else:
            player_anim_count += 1

        bg_x -= 2  # making background image move
        if bg_x == -bg_image_width: # when first image comest to the end:
            bg_x = 0

        if bullets:
            for (index, element) in enumerate(bullets):
                screen.blit(bullet, (element.x, element.y))
                element.x += 4

                if element.x > bg_image_width:
                    bullets.pop(index)

                # if bullet finds enemy, multiply by zero both :)
                if enemy_list:
                    for (index2, enemy_el) in enumerate(enemy_list):
                        if element.colliderect(enemy_el):
                            enemy_list.pop(index2)
                            bullets.pop(index)

    else:
        screen.fill((87, 88, 89))  # when game is ower, show screen in RGB
        screen.blit(lose_label, (lose_label_x, lose_label_y))
        screen.blit(restart_label, restart_label_rect)

        # restart game
        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:  # 0 - left button pressed
            gameplay = True
            player_x = 150
            enemy_list.clear()
            bullets.clear()
            bullets_remaining = 8

    pygame.display.update()  # constantly refreshes the app screen

    for event in pygame.event.get():  # go through the list of all possible events
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == enemy_timer:  # monitor the execution of the timer
            enemy_list.append(enemy.get_rect(topleft=(enemy_x, enemy_y)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_f and bullets_remaining > 0:
            bullets.append(bullet.get_rect(topleft=(player_x + 30, player_y + 10)))
            bullets_remaining -= 1

    clock.tick(15)  # setting fps
