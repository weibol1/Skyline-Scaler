import pygame
import random

# Resolution and Startup
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption("Skyline Scaler")

# image load & resize
playerimg = pygame.image.load("img/player.png").convert_alpha()
playerimg = pygame.transform.scale(playerimg, (80, 80))

platimg = pygame.image.load("img/platform1.png").convert_alpha()
platimg = pygame.transform.scale(platimg, (160, 24))

cloudimg = pygame.image.load("img/cloud.png").convert_alpha()
cloudimg = pygame.transform.scale(cloudimg, (58, 32))
ufoimg = pygame.image.load("img/ufo.png").convert_alpha()
ufoimg = pygame.transform.scale(ufoimg, (58, 32))

pygame.mixer.music.load("img/menu.wav")
pygame.mixer.music.play(-1)

# classes
class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def draw(self):
        action = False

        # mouse position
        pos = pygame.mouse.get_pos()

        # mouse over button and click
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


class playerclass(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = playerimg
        self.hitbox = pygame.Rect(x, y, 32, 5)

    def move(self):
        global movement
        self.hitbox.x = self.x + 26
        self.hitbox.y = self.y + 80

        if movement:
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.x -= 4
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.x += 4

    def draw(self):
        screen.blit(self.image, (self.x, self.y))
        # pygame.draw.rect(screen, (255, 0, 0), self.hitbox, 2)


class platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = platimg
        self.hitbox = pygame.Rect(x, y, 160, 12)

    def move(self):
        self.hitbox.x = self.x
        self.hitbox.y = self.y

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        global game_state
        self.x = x
        self.y = y
        self.image = cloudimg
        self.hitbox = pygame.Rect(x, y, 58, 32)

    def move(self):
        self.hitbox.x = self.x
        self.hitbox.y = self.y

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


# functions
def skylevels():
    global jumpcount, falling, is_jumping, volume
    global cloud1side, cloud1leftside, cloud1rightside, cloud2side, cloud2leftside, cloud2rightside
    screen.fill((157, 215, 239))

    # sound load
    jumpsound1 = pygame.mixer.Sound('img/jump.mp3')
    cloudsound1 = pygame.mixer.Sound('img/cloudsound.mp3')
    pygame.mixer.Sound.set_volume(jumpsound1, volume / 100)
    pygame.mixer.Sound.set_volume(cloudsound1, volume / 100)

    # image load & resize
    skyscraperimg1 = pygame.image.load("img/skyscraper1.png").convert_alpha()
    skyscraperimg1 = pygame.transform.scale(skyscraperimg1, (384, 384))

    backg = pygame.image.load("img/sky background.png").convert()
    backg = pygame.transform.scale(backg, (1280, 1280))

    grass = pygame.image.load("img/grass.png").convert()
    grass = pygame.transform.scale(grass, (1280, 15))

    spacelevels = ['level6', 'level7', 'level8']

    if game_state.state in spacelevels:
        # code for blitting the skyscrapers
        spaceimg1 = pygame.image.load("img/space1.png").convert()
        spaceimg1 = pygame.transform.scale(spaceimg1, (512, 512))
        cloud1.image = ufoimg
        cloud2.image = ufoimg

        for x in range(0, 1280, 512):
            screen.blit(spaceimg1, (x, 0))
            screen.blit(spaceimg1, (x, 512))

    if game_state.state == 'level1' or game_state.state == 'endlesslevel':
        screen.blit(backg, (0, -560))
    if game_state.state == 'level2':
        screen.blit(backg, (0, -460))
    if game_state.state == 'level3':
        screen.blit(backg, (0, -360))
    if game_state.state == 'level4':
        screen.blit(backg, (0, -260))
    if game_state.state == 'level5':
        screen.blit(backg, (0, -160))

    # clouds moving
    if cloud1side == 1:
        cloud1leftside = True
        cloud1rightside = False
    if cloud2side == 1:
        cloud2leftside = True
        cloud2rightside = False
    if cloud1side == 2:
        cloud1leftside = False
        cloud1rightside = True
    if cloud2side == 2:
        cloud2leftside = False
        cloud2rightside = True

    cloudlist = [cloud1, cloud2]  # cloud collisions with the player

    for cloud in cloudlist:
        cloud.draw()
        cloud.move()

    if cloud1leftside:
        cloud1.x += 1
    if cloud1rightside:
        cloud1.x -= 1

    if cloud2leftside:
        cloud2.x += 1.5
    if cloud2rightside:
        cloud2.x -= 1.5

    if cloud1.x >= 1500:
        cloud1side = 2

    if cloud1.x <= -200:
        cloud1side = 1

    if cloud2.x >= 1500:
        cloud2side = 2

    if cloud2.x <= -200:
        cloud2side = 1

    # draw classes to screen
    platlist = [plat1, plat2, plat3, plat4, plat5]

    for plat in platlist:
        plat.draw()
        plat.move()

    player.draw()
    player.move()

    if player.x <= 380:
        player.x = 380

    if player.x >= 825:
        player.x = 825

    for plat in platlist:
        if player.hitbox.colliderect(plat.hitbox):
            player.y = plat.y - 90

    if player.hitbox.colliderect(cloud1.hitbox) or player.hitbox.colliderect(cloud2.hitbox):
        cloudsound1.play()
        is_jumping = True
        falling = False
        jumpcount = 30

    # jumping for the player
    if not gameover:
        if not is_jumping:
            if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
                jumpsound1.play()
                falling = False
                is_jumping = True
        else:
            if jumpcount >= -30:
                neg = 1
                if jumpcount < 0:
                    neg = -1
                player.y -= (jumpcount ** 2) * 0.020 * neg
                jumpcount -= 1

            else:
                is_jumping = False
                falling = True
                jumpcount = 30

    if falling:
        player.y += 9

    # player borders
    if game_state.state == 'level1':
        if player.y >= 625:
            player.y = 625

    # code for blitting the skyscrapers
    for y in range(0, 720, 384):
        screen.blit(skyscraperimg1, (0, y))
        screen.blit(skyscraperimg1, (896, y))

    if game_state.state == 'level1' or game_state.state == 'endlesslevel' and levels == 0:
        screen.blit(grass, (0, 705))

def randomy():
    plat5y = random.randint(85, 115)  # top right
    plat4y = random.randint(235, 305)  # middle
    plat3y = random.randint(345, 415)  # middle
    plat2y = random.randint(465, 535)  # middle
    plat2.y = plat2y
    plat3.y = plat3y
    plat4.y = plat4y
    plat5.y = plat5y

class Gamestate:
    def __init__(self):
        self.state = 'mainmenu'

    def mainmenu(self):
        global running, movement
        screen.fill((25, 25, 25))

        pygame.mixer.music.set_volume(volume / 100)

        spaceimg1 = pygame.image.load("img/space1.png").convert()
        spaceimg1 = pygame.transform.scale(spaceimg1, (512, 512))

        for x in range(0, 1280, 512):
            screen.blit(spaceimg1, (x, 0))
            screen.blit(spaceimg1, (x, 512))

        # image load
        title = pygame.image.load('img/title.png').convert_alpha()
        startimg = pygame.image.load('img/start.png').convert_alpha()
        endlessimg = pygame.image.load('img/endless.png').convert_alpha()
        creditsimg = pygame.image.load('img/credits.png').convert_alpha()
        optionsimg = pygame.image.load('img/options.png').convert_alpha()
        exitimg = pygame.image.load('img/exit.png').convert_alpha()

        # image resize
        title = pygame.transform.scale(title, (732, 124))
        startimg = pygame.transform.scale(startimg, (228, 68))
        endlessimg = pygame.transform.scale(endlessimg, (300, 66))
        creditsimg = pygame.transform.scale(creditsimg, (292, 68))
        optionsimg = pygame.transform.scale(optionsimg, (296, 64))
        exitimg = pygame.transform.scale(exitimg, (164, 68))

        # buttons
        start_but = Button(50, 200, startimg, 1)
        endless_but = Button(50, 300, endlessimg, 1)
        credits_but = Button(50, 400, creditsimg, 1)
        options_but = Button(50, 500, optionsimg, 1)
        exit_but = Button(50, 600, exitimg, 1)

        # main code
        screen.blit(title, (300, 20))

        if start_but.draw():
            self.state = 'level1'
            player.x = 620
            player.y = 640
            movement = True

        if endless_but.draw():
            self.state = 'endlesslevel'

        if credits_but.draw():
            self.state = 'creditsmenu'

        if options_but.draw():
            self.state = 'optionsmenu'

        if exit_but.draw():
            running = False

    def creditsmenu(self):
        screen.fill((25, 25, 25))

        credits_font = pygame.font.Font('img/FieldGuide.ttf', 45)
        credit1_text = credits_font.render("Skyline Scaler", True, (255, 255, 255))
        credit2_text = credits_font.render('Ghastly Games Team Members:', True, (255, 255, 255))
        credit3_text = credits_font.render('Lead Programmer and Art Designer: Corey Stuckey', True, (255, 255, 255))
        credit4_text = credits_font.render('Sound Design and Media Coordinator: Jakeb Ranew', True, (255, 255, 255))
        credit5_text = credits_font.render('Senior music Designer: Crusty Trayson', True, (255, 255, 255))
        credit6_text = credits_font.render('www.ghastlygames.net', False, (255, 255, 255))
        screen.blit(credit1_text, (100, 75))
        screen.blit(credit2_text, (100, 150))
        screen.blit(credit3_text, (100, 225))
        screen.blit(credit4_text, (100, 300))
        screen.blit(credit5_text, (100, 375))
        screen.blit(credit6_text, (100, 450))

        esc_font = pygame.font.Font('img/FieldGuide.ttf', 72)
        credit7_text = esc_font.render('Press [ESC] to Exit', True, (255, 255, 255))

        screen.blit(credit7_text, (350, 630))

        if keys[pygame.K_ESCAPE]:
            self.state = 'mainmenu'

    def optionsmenu(self):
        global windowedshown, fullscreenshown, screen, volume, b_timer
        screen.fill((25, 25, 25))

        pygame.mixer.music.set_volume(volume / 100)

        b_timer += 1

        larrow = pygame.image.load("img/left arrow.png").convert_alpha()
        rarrow = pygame.image.load("img/right arrow.png").convert_alpha()
        larrow = pygame.transform.scale(larrow, (80, 130))
        rarrow = pygame.transform.scale(rarrow, (80, 130))

        apply = pygame.image.load("img/apply button.png").convert_alpha()
        apply = pygame.transform.scale(apply, (216, 80))

        # Code for exiting the options menu
        esc_font = pygame.font.Font('img/FieldGuide.ttf', 72)
        credit7_text = esc_font.render('Press [ESC] to Exit', True, (255, 255, 255))

        volume_font = pygame.font.Font('img/FieldGuide.ttf', 72)
        volume_text = volume_font.render(f'Volume: {volume}', True, (255, 255, 255))

        windowed_text = esc_font.render('Windowed', True, (255, 255, 255))
        fullscreen_text = esc_font.render('Fullscreen', True, (255, 255, 255))

        # Main code for the options menu
        left_button2 = Button(100, 400, larrow, 1)
        right_button2 = Button(500, 400, rarrow, 1)
        left_button3 = Button(700, 400, larrow, 1)
        right_button3 = Button(1150, 400, rarrow, 1)
        applybut = Button(230, 530, apply, 1)

        screen.blit(volume_text, (800, 415))

        controls_font = pygame.font.Font('img/FieldGuide.ttf', 48)
        controls1_font = pygame.font.Font('img/FieldGuide.ttf', 96)
        # controls for keyboard
        controls1key = controls_font.render('[ESC] : Exit or Pause', True, (255, 255, 255))
        controls2key = controls_font.render('[A] & [D] or [LEFT-ARROW] & [RIGHT-ARROW] keys To Move', True, (255, 255, 255))
        controls4key = controls_font.render('[SPACE], [W] or [UP-ARROW] : To Jump', True, (255, 255, 255))
        controls5key = controls1_font.render('Controls:', True, (255, 255, 255))

        # controls blitting
        screen.blit(controls1key, (10, 120))
        screen.blit(controls2key, (10, 280))
        screen.blit(controls4key, (10, 200))
        screen.blit(controls5key, (10, 10))

        # code for the buttons for volume and fullscreen
        if left_button2.draw():
            fullscreenshown = False
            windowedshown = True

        if right_button2.draw():
            windowedshown = False
            fullscreenshown = True

        if volume >= 100:
            volume = 100
        if volume <= 0:
            volume = 0

        if left_button3.draw() and b_timer >= 8 and volume >= 1:
            b_timer = 0
            volume -= 1

        if right_button3.draw() and b_timer >= 8 and volume <= 99:
            b_timer = 0
            volume += 1

        if windowedshown:
            screen.blit(windowed_text, (210, 410))
        if fullscreenshown:
            screen.blit(fullscreen_text, (195, 410))

        if applybut.draw() and b_timer >= 60:
            b_timer = 0
            if fullscreenshown:
                screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.FULLSCREEN)
            if windowedshown:
                screen = pygame.display.set_mode((1280, 720), pygame.HWSURFACE | pygame.DOUBLEBUF)

        screen.blit(credit7_text, (350, 630))

        if keys[pygame.K_ESCAPE]:
            b_timer = 0
            self.state = 'mainmenu'

    def level1(self):
        global level_timer

        skylevels()
        level_timer += 1
        if player.y <= 0 and level_timer >= 50:
            level_timer = 0
            randomy()
            self.state = 'level2'
            player.y = player.y + 700

    def level2(self):
        global level_timer
        skylevels()
        level_timer += 1
        if player.y <= 0 and level_timer >= 50:
            level_timer = 0
            randomy()
            self.state = 'level3'
            player.y = player.y + 700
        if player.y >= 720 and level_timer >= 50:
            level_timer = 0
            player.y = 0
            self.state = 'level1'

    def level3(self):
        global level_timer
        skylevels()
        level_timer += 1
        if player.y <= 0 and level_timer >= 50:
            level_timer = 0
            randomy()
            self.state = 'level4'
            player.y = player.y + 700
        if player.y >= 720 and level_timer >= 50:
            level_timer = 0
            player.y = 0
            self.state = 'level2'

    def level4(self):
        global level_timer
        skylevels()
        level_timer += 1
        if player.y <= 0 and level_timer >= 50:
            level_timer = 0
            randomy()
            self.state = 'level5'
            player.y = player.y + 700
        if player.y >= 720 and level_timer >= 50:
            level_timer = 0
            player.y = 0
            self.state = 'level3'

    def level5(self):
        global level_timer
        skylevels()
        level_timer += 1
        if player.y <= 0 and level_timer >= 50:
            level_timer = 0
            randomy()
            self.state = 'level6'
            player.y = player.y + 700
        if player.y >= 720 and level_timer >= 50:
            level_timer = 0
            player.y = 0
            self.state = 'level4'

    def level6(self):
        global level_timer
        skylevels()
        level_timer += 1
        if player.y <= 0 and level_timer >= 50:
            level_timer = 0
            randomy()
            self.state = 'level7'
            player.y = player.y + 700
        if player.y >= 720 and level_timer >= 50:
            level_timer = 0
            player.y = 0
            self.state = 'level5'

    def level7(self):
        global level_timer
        skylevels()
        level_timer += 1
        if player.y <= 0 and level_timer >= 50:
            level_timer = 0
            randomy()
            self.state = 'level8'
            player.y = player.y + 700
        if player.y >= 720 and level_timer >= 50:
            level_timer = 0
            player.y = 0
            self.state = 'level6'

    def level8(self):
        global level_timer
        skylevels()
        level_timer += 1
        if player.y <= 0 and level_timer >= 50:
            level_timer = 0
            randomy()
            self.state = 'winlevel'
            player.y = player.y + 700
        if player.y >= 720 and level_timer >= 50:
            level_timer = 0
            player.y = 0
            self.state = 'level7'

    def winlevel(self):
        global jumpcount, falling, is_jumping
        screen.fill((157, 215, 239))

        player.draw()
        player.move()

        # jumping for the player
        if not is_jumping:
            if keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]:
                falling = False
                is_jumping = True
        else:
            if jumpcount >= -30:
                neg = 1
                if jumpcount < 0:
                    neg = -1
                player.y -= (jumpcount ** 2) * 0.020 * neg
                jumpcount -= 1

            else:
                is_jumping = False
                falling = True
                jumpcount = 30

        if falling:
            player.y += 9

        if player.y >= 640:
            player.y = 640
        if player.x >= 1210:
            player.x = 1210
        if player.x <= -10:
            player.x = -10

        if keys[pygame.K_ESCAPE]:
            self.state = 'mainmenu'

        win_font = pygame.font.Font('img/FieldGuide.ttf', 48)
        win1_font = pygame.font.Font('img/FieldGuide.ttf', 72)
        credit1_text = win_font.render("Congratulations! You Win!", True, (0, 0, 0))
        credit2_text = win_font.render('Thank You for playing our 2024 GMTK Game Jam game!', True, (0, 0, 0))
        credit3_text = win_font.render('Skyline Scaler', True, (0, 0, 0))
        credit4_text = win_font.render('Ghastly Games Team Members:', True, (0, 0, 0))
        credit5_text = win_font.render('Lead Programmer and Art Designer: Corey Stuckey', True, (0, 0, 0))
        credit6_text = win_font.render('Senior music Designer: Crusty Trayson', True, (0, 0, 0))
        credit7_text = win_font.render('Sound Design and Media Coordinator: Jakeb Ranew', True, (0, 0, 0))
        credit8_text = win_font.render('www.ghastlygames.net', True, (0, 0, 0))
        credit9_text = win1_font.render('Press [ESC] to Exit', True, (0, 0, 0))
        screen.blit(credit1_text, (20, 25))
        screen.blit(credit2_text, (20, 100))
        screen.blit(credit3_text, (20, 175))
        screen.blit(credit4_text, (20, 250))
        screen.blit(credit5_text, (20, 325))
        screen.blit(credit6_text, (20, 400))
        screen.blit(credit7_text, (20, 475))
        screen.blit(credit8_text, (20, 550))
        screen.blit(credit9_text, (700, 600))

    def endlesslevel(self):
        global level_timer, able_fail, is_jumping, gameover, levels, movement, gameovertimer
        skylevels()

        cloud1.image = cloudimg
        cloud2.image = cloudimg

        if player.y <= 0:
            levels += 1
            randomy()
            player.x = 800
            player.y = 480
            able_fail = True

        if not able_fail or levels == 0:
            if player.y >= 625:
                player.y = 625

        if able_fail and player.y >= 670:
            gameover = True

        lose_font = pygame.font.Font('img/FieldGuide.ttf', 72)
        lose1text = lose_font.render("Sorry You Lost!", True, (0, 0, 0))
        lose2text = lose_font.render("Levels Highscore:", True, (0, 0, 0))
        lose3text = lose_font.render(str(levels), True, (0, 0, 0))

        if gameover:
            gameovertimer += 1
            movement = False
            is_jumping = False
            screen.blit(lose1text, (410, 50))
            screen.blit(lose2text, (390, 120))
            screen.blit(lose3text, (620, 200))
        if gameovertimer >= 300 and gameover:
            levels = 0
            movement = True
            self.state = 'mainmenu'
            gameovertimer = 0
            gameover = False
            player.x = 600
            player.y = 580
            able_fail = False

    def state_manager(self):
        state_methods = {
            'mainmenu': self.mainmenu,
            'creditsmenu': self.creditsmenu,
            'optionsmenu': self.optionsmenu,
            'level1': self.level1,
            'level2': self.level2,
            'level3': self.level3,
            'level4': self.level4,
            'level5': self.level5,
            'level6': self.level6,
            'level7': self.level7,
            'level8': self.level8,
            'winlevel': self.winlevel,
            'endlesslevel': self.endlesslevel,
        }

        method = state_methods.get(self.state)
        if method:
            method()


# classes
player = playerclass(620, 640)

plat5 = platform(737, 100)
plat4 = platform(384, 270)
plat3 = platform(737, 380)
plat2 = platform(384, 500)
plat1 = platform(737, 600)

cloud1 = cloud(0, 200)
cloud2 = cloud(0, 550)

# references
FPS = 60
game_state = Gamestate()
clock = pygame.time.Clock()
level_timer = 0
volume = 50
able_fail = False
gameover = False
movement = True
levels = 0
gameovertimer = 0

# jumping references
jumpcount = 30
is_jumping = False
falling = False

# optionsmenu references
windowedshown = True
fullscreenshown = False
b_timer = 0

# minecart stuff
cloud1side = random.randint(1, 2)
cloud1leftside = cloud1rightside = False
cloud2side = random.randint(1, 2)
cloud2leftside = cloud2rightside = False

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    clock.tick(FPS)
    game_state.state_manager()

    pygame.display.flip()
pygame.quit()
