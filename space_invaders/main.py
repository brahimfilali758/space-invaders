import pygame
from os.path import join
import random
from pygame import time


pygame.init()

ressources_folder = 'ressources'
screen__width = 700
screen__length = 700

# setting up the screen :
screen = pygame.display.set_mode((screen__width, screen__length))


# Colors :
green = (16, 101, 17)
red = (243, 0, 22)

# images :
player_icon = pygame.image.load(
    join(ressources_folder, 'player.png')).convert_alpha()
enemy_icon = pygame.image.load(
    join(ressources_folder, 'enemy.png')).convert_alpha()
bullet_icon = pygame.image.load(
    join(ressources_folder, 'bullet.png')).convert_alpha()
bullet_icon_rotated = pygame.transform.rotate(bullet_icon, 180)
background_part_2 = pygame.image.load(
    join(ressources_folder, "background_part_2.png")).convert_alpha()
background_part_2 = pygame.transform.scale(
    background_part_2, (screen__width, screen__length)).convert_alpha()
background_part_1 = pygame.image.load(
    join(ressources_folder, "background_part_1.png")).convert_alpha()
background_part_1 = pygame.transform.scale(
    background_part_1, (screen__width, screen__length)).convert_alpha()
big_enemie_icon = pygame.image.load(
    join(ressources_folder, 'big_enemy.png')).convert_alpha()
big_enemie_icon = pygame.transform.scale(big_enemie_icon, (200, 200))
explosion_icon = pygame.image.load(
    join(ressources_folder, 'explosion.png')).convert_alpha()
explosion_icon = pygame.transform.scale(explosion_icon, (50, 50))
enemy_big_ship_icon = pygame.image.load(
    join(ressources_folder, 'enemy_big_ship.png')).convert_alpha()
enemy_big_ship_icon = pygame.transform.scale(enemy_big_ship_icon, (100, 100))
start_button = pygame.image.load(
    join(ressources_folder, 'start_button.png')).convert_alpha()
start_button = pygame.transform.scale(start_button, (150, 150))
game_over_icon = pygame.image.load(
    join(ressources_folder, 'game_over.png')).convert_alpha()
game_over_icon = pygame.transform.scale(
    game_over_icon, (200, 200)).convert_alpha()

# Sounds:
pygame.mixer.init()
# pygame.mixer.music.load(join(ressources_folder , 'background.wav'))
# pygame.mixer.music.play(-1)
explosion_sound = pygame.mixer.Sound(join(ressources_folder, 'explosion.wav'))
laser_sound = pygame.mixer.Sound(join(ressources_folder, 'laser.wav'))

# font stuff :
font = pygame.font.Font('freesansbold.ttf', 32)


class Animation :

    def __init__(self ,character ,bullet ,icon = None ):
        self.icon = icon if not icon == None else explosion_icon
        self.duration = 2000
        self.timer = Timer()
        self.pos = ((character.x + bullet.x)/2 , (character.y + bullet.y)/2)
        # self.character = character
        # self.bullet = bullet

    def play_animation(self) :
        if not self.timer.get() >= 200 :
            screen.blit(self.icon , self.pos)



class Timer:
    def __init__(self):
        self.accumulated_time = 0
        self.start_time = pygame.time.get_ticks()
        self.running = True

    def pause(self):
        if not self.running:
            raise Exception('Timer is already paused')
        self.running = False
        self.accumulated_time += pygame.time.get_ticks() - self.start_time

    def resume(self):
        if self.running:
            raise Exception('Timer is already running')
        self.running = True
        self.start_time = pygame.time.get_ticks()

    def get(self):
        if self.running:
            return (self.accumulated_time +
                    (pygame.time.get_ticks() - self.start_time))
        else:
            return self.accumulated_time


class Backgound:
    def __init__(self, speed = 1 ):
        self.x1 = 0
        self.y1 = screen__length * -1
        self.x2 = 0
        self.y2 = 0
        self.speed = speed
        self.first_icon = background_part_1
        self.second_icon = background_part_2

    def update(self):
        self.y1 += self.speed
        self.y2 += self.speed
        if self.y1 == screen__length:
            self.y1 = screen__length * -1
        if self.y2 == screen__length:
            self.y2 = screen__length * -1

    def draw(self):
        screen.blit(self.first_icon, (self.x1, self.y1))
        screen.blit(self.second_icon, (self.x2, self.y2))


class Character(object):

    def __init__(self, icon, x, y):
        self.icon = icon
        self.x = x
        self.y = y
        self.hitbox = (self.x, self.y, icon.get_rect(
        ).size[0], icon.get_rect().size[1])
        self.health = 100
        self.bullets = []   

    def display(self):
        screen.blit(self.icon, (self.x, self.y))
        self.hitbox = (self.x, self.y, self.hitbox[2], self.hitbox[3])
        pygame.draw.rect(screen , red , self.hitbox , 1)

    def display_health_bar(self):
        health_bar_red = (self.x, self.y + self.hitbox[3], self.hitbox[2], 10)
        health_bar_green = (
            self.x, self.y + self.hitbox[3], (self.hitbox[2]*self.health) / 100, 10)
        pygame.draw.rect(screen, red, (health_bar_red))
        pygame.draw.rect(screen, green, health_bar_green)

    def in_fielled(self):
        return (self.x < screen__width - 60) and (self.y < screen__length - 60) and (self.x > 0 and self.y > 0)

    def check_collision(self, other_player):

        def rectCollision(rect1, rect2):
            P11 = (rect1[0], rect1[1])
            P12 = (rect1[0] + rect1[2], rect1[1])
            P13 = (rect1[0], rect1[1] + rect1[3])
            P14 = (rect1[0] + rect1[2], rect1[1] + rect1[3])
            if inBox(P11, rect2) or inBox(P12, rect2) or inBox(P13, rect2) or inBox(P14, rect2):
                return True

        def inBox(point, rect):
            if point[0] <= rect[0] + rect[2] and point[0] >= rect[0] and point[1] <= rect[1] + rect[3] and point[1] >= rect[1]:
                return True
            else:
                return False
        return rectCollision(self.hitbox, other_player.hitbox)

    def been_hit(self, health_lost):
        self.health -= health_lost


    def explose(self):
        self.icon = explosion_icon


class Player(Character):

    def __init__(self, x, y):
        super().__init__(player_icon, x, y)
        self.change_x = 0
        self.change_y = 0

    def update_position(self):
        self.right = self.change_x > 0
        if self.in_fielled():
            self.x += self.change_x
            self.y += self.change_y
        else:
            self.change_x = 0
            self.change_y = 0
            if self.x <= 0:
                self.x = 5
            elif self.x >= screen__width - 60 :
                self.x = screen__width - 61

    def shoot_bullets(self):
        self.bullets.append(Bullet(self.x, self.y, True))
        for bullet in self.bullets:
            if not bullet.in_fielled():
                self.bullets.remove(bullet)

    def display_health_bar(self):
        health_bar_red = (40, 650, 200, 10)
        health_bar_green = (40, 650, (200*self.health) / 100, 10)
        pygame.draw.rect(screen, red, (health_bar_red))
        pygame.draw.rect(screen, green, health_bar_green)


class Enemy(Character):

    def __init__(self, icon=None):
        if icon == None:
            super().__init__(enemy_icon, random.randint(0, 650), random.randint(0, 50))
        else:
            super().__init__(icon, random.randint(0, 650), random.randint(0, 50))

        # you can write that in a more elegant way
        self.right = False if random.randint(0, 1) == 0 else True
        self.timer = Timer()

    def update_position(self):
        if self.right:
            self.x += 2
            self.y += 1
            if self.x >= screen__width - 60:
                self.right = False
                self.x += -2
        if not self.right:
            self.x += -2
            self.y += 1
            if self.x <= 5:
                self.right = True
                self.x += 2

    def shoot_bullets(self):
        self.bullets.append(Bullet(self.x, self.y, False , icon = bullet_icon_rotated))
        for bullet in self.bullets:
            if not bullet.in_fielled():
                self.bullets.remove(bullet)



class BigEnemy(Enemy):

    def __init__(self, icon):
        super(BigEnemy, self).__init__(icon=icon)

    def update_position(self, player_to_chase):

        if self.right:
            self.x += 2
            self.y += .1
            if self.x >= screen__width - 60:
                self.right = random.randint(0, 2)
                self.x += -2
        if not self.right:
            self.x += -2
            self.y += .1
            if self.x <= 5:
                self.right = random.randint(0, 2)
                self.x += 2


class Bullet:

    def __init__(self, x, y, up, icon = None):
        self.x = x
        self.y = y
        self.up = up
        self.hitbox = (self.x , self.y, 30, 30)
        self.icon = bullet_icon if icon == None else icon

    def update_position(self):
        screen.blit(self.icon, (self.x, self.y))
        pygame.draw.rect(screen , green , self.hitbox , 1)

        if self.up:
            self.y -= 5
            self.hitbox = (self.x , self.y, 30, 30)
        else:
            self.y += 5
            self.hitbox = (self.x , self.y, 30, 30)

    def in_fielled(self):
        return Character.in_fielled(self)

    def check_collision(self , other_player) :
        return Character.check_collision(self , other_player)


def game_loop():

    start_ticks = pygame.time.get_ticks()
    clock = pygame.time.Clock()
    time_elapsed_since_last_action = 0
    

    score = 0

    numbEnemies = 10
    enemies = [Enemy() for _ in range(numbEnemies)]

    player = Player(300, 575)

    big_enemy = BigEnemy(icon=enemy_big_ship_icon)
    big_enemy_time = False
    backgound = Backgound(1)



    animations = []

    running = True
    while running :

        # screen stuff :
        backgound.update()
        backgound.draw()

        # calculate the seconds before begining to play :
        secondes = (pygame.time.get_ticks() - start_ticks)/1000

        # displaying the player's ship :
        player.display()
        player.display_health_bar()

        # displaying enemies
        [enemy.display() for enemy in enemies]

        # moving enemies around :
        [enemy.update_position() for enemy in enemies]

        # capture events :
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot_bullets()
                    laser_sound.play()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.change_x = -5
                    player.change_y = 0
                if event.key == pygame.K_RIGHT:
                    player.change_x = 5
                    player.change_y = 0
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.change_x = 0
                    player.change_y = 0
                if event.key == pygame.K_RIGHT:
                    player.change_x = 0
                    player.change_y = 0

        player.update_position()
        # player.remove_bullets_outside_fielld()
        [bullet.update_position() for bullet in player.bullets]

        for enemy in enemies:
            for bullet in player.bullets:
                if enemy.check_collision(bullet):
                    explosion_sound.play()
                    animations.append(Animation(character = enemy , bullet = bullet))
                    enemy.explose()
                    try:
                        player.bullets.remove(bullet)
                        enemies.remove(enemy)
                    except ValueError as e:
                        print(e)
                    score += 1
                    if not big_enemy_time:
                        enemies.append(Enemy())
            if player.check_collision(enemy):
                if not player.health <= 0 :
                    player.health -= 1
                else : 
                    game_over()
        [animation.play_animation() for animation in animations]

        if secondes >= 10 and score >= 10 :
            big_enemy_time = True
        if big_enemy_time :
            big_enemy.display()
            big_enemy.display_health_bar()
            if int(secondes) % 3 == 0 :
                big_enemy.update_position(player)
            if time_elapsed_since_last_action >= 1000 :
                big_enemy.shoot_bullets()
                time_elapsed_since_last_action = 0
            [bullet.update_position() for bullet in big_enemy.bullets]
            for bullet in big_enemy.bullets :
                if bullet.check_collision(player) :
                    player.health -= 1 
                    big_enemy.bullets.remove(bullet)
            for bullet in player.bullets :
                if bullet.check_collision(big_enemy) :
                    big_enemy.health -= 1
                    player.bullets.remove(bullet)
            if big_enemy.health <= 0 :
                big_enemy_time = False
                start_ticks = pygame.time.get_ticks()


        # displaying the score :
        text = font.render(f"Score  :  {score} ", True, (255, 255, 255))
        screen.blit(text, (5, 5))

        
        # FPS 60 :
        dt = clock.tick(60)
        time_elapsed_since_last_action += dt
        pygame.display.update()


def intro_loop():
    start_ticks = pygame.time.get_ticks()
    clock = pygame.time.Clock()

    backgound = Backgound(2)

    running_itro = True
    while running_itro:

        # screen stuff :
        backgound.update()
        backgound.draw()

        screen.blit(start_button, (300, 100))

        secondes = (pygame.time.get_ticks() - start_ticks)/1000

        # capture events :
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running_itro = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[0] >= 300 and pos[0] <= 450 and pos[1] >= 100 and pos[1] <= 250 :
                    game_loop()

        # FPS 60 :
        clock.tick(60)
        pygame.display.update()


def game_over() :

    clock = pygame.time.Clock()

    backgound = Backgound(2)

    running_game_over = True 
    while running_game_over :
        backgound.update()
        backgound.draw()
        screen.blit(game_over_icon , (260 , 200))

        for event in pygame.event.get() :
            if event.type == pygame.QUIT :
                running_game_over = False
                pygame.quit()
                quit()

        clock.tick(60)
        pygame.display.update()




def main():
    intro_loop()


if __name__ == '__main__':
    main()
