import pygame
from os.path import join
import random
from math import sqrt 
from pygame import time



ressources_folder = 'ressources'
screen__width = 700
screen__length = 700

screen = pygame.display.set_mode((screen__width, screen__length))
#images :
player_icon = pygame.image.load(join(ressources_folder, 'player.png')).convert_alpha()
enemie_icon = pygame.image.load(join(ressources_folder , 'enemy.png')).convert_alpha()
bullet_icon = pygame.image.load(join(ressources_folder , 'bullet.png')).convert_alpha()
bullet_icon_rotated = pygame.transform.rotate(bullet_icon , 180)
background = pygame.image.load(join(ressources_folder, "background.jpg")).convert_alpha()
background = pygame.transform.scale(background, (screen__width, screen__length)).convert_alpha()
big_enemie_icon = pygame.image.load(join(ressources_folder , 'big_enemy.png')).convert_alpha()
big_enemie_icon = pygame.transform.scale(big_enemie_icon , (200 , 200))



class Player(object) :

    def __init__(self ,icon ,x ,y ):
        self.icon = pygame.image.load(join(ressources_folder , icon))
        self.x = x 
        self.y = y
        self.change_x = 0
        self.change_y = 0
        self.hitbox = ()
        self.health = 100

    def display_health_bar(self):
        health_bar_red = (self.x , self.y + self.hitbox[3] , self.hitbox[2] ,10)
        health_bar_green = (self.x , self.y + self.hitbox[3] ,(self.hitbox[2]*self.health) / 100 ,10)
        pygame.draw.rect( screen, (255 , 0 , 0) , (health_bar_red) )
        pygame.draw.rect( screen, (0 , 255 , 0) , health_bar_green )



    def check_bordinates(self ):
        return (self.x < screen__width - 60 ) and (self.y < screen__length - 60) and (self.x > 0 and self.y > 0)


    def isCollision(self , other_player):

        def rectCollision(rect1 , rect2):
            P11 = (rect1[0] ,rect1[1])
            P12 = (rect1[0] + rect1[2], rect1[1] )
            P13 = (rect1[0] , rect1[1] + rect1[3])
            P14 = (rect1[0] + rect1[2] ,rect1[1] + rect1[3] )
            if inBox(P11, rect2) or inBox(P12, rect2) or inBox(P13, rect2) or inBox(P14, rect2) :
                return True

        def inBox(point , rect ) :
            if point[0] <= rect[0] + rect[2] and point[0] >= rect[0] and point[1] <= rect[1] + rect[3] and point[1] >= rect[1]:
                return True
            else : return False
        return rectCollision(self.hitbox, other_player.hitbox)

        
                    

  

class Ship(Player):

    change_x = 0
    change_y = 0

    def __init__(self, x, y) :
        self.icon = player_icon
        self.x = x
        self.y = y
        self.hitbox = (self.x , self.y , 65 , 60)
        self.health = 100

       
    def beenhit(self):
        self.health -= 10

    def display_ship(self):
        screen.blit(self.icon , (self.x , self.y))
        self.hitbox = (self.x , self.y , 65 , 60)

    def move(self , event):
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT :
                self.change_x = -5
                self.change_y = 0
            if event.key == pygame.K_RIGHT :
                self.change_x = 5
                self.change_y = 0
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_LEFT :
                self.change_x = 0
                self.change_y = 0
            if event.key == pygame.K_RIGHT :
                self.change_x = 0
                self.change_y = 0

    def change_coordinates(self):
        if self.check_bordinates() :
            self.x += self.change_x
            self.y += self.change_y
        else : 
            self.change_x = 0
            self.change_y = 0
            if self.x <= 0 :
                self.x = 5
            elif self.x >= screen__width - 60:
                self.x = screen__width - 61

    def display_health_bar(self):
        health_bar_red = (20 , 650 , 200 , 15)
        health_bar_green = (20 , 650 , self.health * 2 , 15)
        pygame.draw.rect( screen, (255 , 0 , 0) , (health_bar_red) )
        pygame.draw.rect( screen, (0 , 255 , 0) , health_bar_green )




class Enemy(Player):

    def __init__(self  , icon = None ) :
        if not icon == None :
            self.icon = icon
        else :
            self.icon = enemie_icon
        self.x = random.randint(0 ,650)
        self.y = random.randint( 0, 50)
        self.hitbox = (self.x , self.y , 65 , 60)
        if random.randint(0, 1) == 0 :
            self.right = False
        else : 
            self.right = True

    def display_enemy(self ):
        screen.blit(self.icon , (self.x , self.y))
        self.hitbox = (self.x , self.y , self.hitbox[2] , self.hitbox[3])

    def change_coordinates(self ):
        if self.right == True :
            self.x += 2
            if self.x >= screen__width - 60:
                self.right = False
                self.x += -2
                self.y += 40
        if self.right == False :
            self.x += -2
            if self.x <= 5:
                self.right = True
                self.x += 2
                self.y += 40


class BigEnemy(Enemy):

    def __init__(self , icon = None):
        if icon == None :
            super().__init__(self)
            self.icon = big_enemie_icon
            self.hitbox = (self.x , self.y , 200 , 200)
            self.health = 100
        else : 
            super().__init__(self , icon = icon)
            self.icon = icon
        self.dic = {}

    def change_coordinates(self):

        if self.right == True :
            self.x += 2
            if self.x >= screen__width - 60:
                self.right = False
                self.x += -2
        if self.right == False :
            self.x += -2
            if self.x <= 5:
                self.right = True
                self.x += 2

    def shoot_bullet(self):
        self.dic[self.x] = Bullet(self.x + self.hitbox[2]/2 , self.y + self.hitbox[3] , icon= bullet_icon_rotated)
        counter = 0
        for bullet_index in self.dic :
            counter +=1
            if counter == 30 :
                self.dic[bullet_index].shoot_bullet(down = True)
                counter = 0





class Bullet(Player) :

    def __init__(self ,x ,y , icon = None):
        if icon == None :
            self.icon = bullet_icon
        else :
            self.icon = icon
        self.x = x 
        self.y = y
        self.hitbox = (self.x + 10 , self.y , 10 , 30)

    def shoot_bullet(self , down = False):
        screen.blit(self.icon ,(round(self.x) , round(self.y)))
        if down == False :
            self.y -= 5
        else : 
            self.y += 5
        self.hitbox = (self.x + 10 , self.y , 10 , 30)





def main():
    #initialiase the pygame module : 
    pygame.init()

    #setting the screen ready :
    screen = pygame.display.set_mode((screen__width, screen__length))

    #Sounds stuff :
    pygame.mixer.init()
    pygame.mixer.music.load(join(ressources_folder , 'background.wav'))
    pygame.mixer.music.play(-1)
    explosion_sound = pygame.mixer.Sound(join(ressources_folder,'explosion.wav'))
    laser_sound = pygame.mixer.Sound(join(ressources_folder , 'laser.wav'))
    
    #the list of the enemiess :
    numbEnemies = 10 
    enemies = [Enemy() for _ in range(numbEnemies)]
    
    #the player : which is a ship :D
    player = Ship(300, 575)
    
    # this is for eleminating the enemies from enemies list , just because we can't delete an enemie in a list while iterating over that list that gives an error 
    dic_buullets_player = {}
    #The score variable :
    score = 0

    big_enemie_time = False

    #font stuff :
    font = pygame.font.Font('freesansbold.ttf', 32)

    start_ticks = pygame.time.get_ticks()

    clock = pygame.time.Clock()
    #the game loop :
    big_enemie = BigEnemy()    
    running = True
    while running :
        #screen stuff :
        screen.fill((97, 159, 182))
        screen.blit(background , (0 , 0))

        #calculate the seconds before begining to play :
        secondes = (pygame.time.get_ticks() - start_ticks )/1000

        #displaying the player's ship :
        player.display_ship()
        player.display_health_bar()

        #displaying enemies
        [enemi.display_enemy() for enemi in enemies]

        #moving enemies around :
        [enemi.change_coordinates() for enemi in enemies]

        #capture events :
        for event in pygame.event.get():
            player.move(event)

            if event.type == pygame.QUIT :
                running = False
            if event.type == pygame.KEYDOWN :
                if event.key == pygame.K_SPACE :
                    dic_buullets_player[player.x] = Bullet(player.x , player.y)
                    laser_sound.play()
        

        [dic_buullets_player[bullet_index].shoot_bullet() for bullet_index in dic_buullets_player]        

        player.change_coordinates()

        dict_bullets2 = {}

        dict_bullet_bigenemi = {}

        
        for enemi in enemies :
            for bullet_index in dic_buullets_player :
                if enemi.isCollision(dic_buullets_player[bullet_index]):
                    explosion_sound.play()
                    dict_bullets2[bullet_index] = dic_buullets_player[bullet_index]
                    try :
                        enemies.remove(enemi)
                    except ValueError as e :
                        print(e)
                    score += 1
                    if not big_enemie_time :
                        enemies.append(Enemy())
            if player.isCollision(enemi):
                print('Game Over')
                #add a function to go to the game over menu :

        for bullet_index in dic_buullets_player :
            if not dic_buullets_player[bullet_index].check_bordinates() :
                dict_bullets2[bullet_index] = dic_buullets_player[bullet_index] 
        
        for bullet in dict_bullets2 :
            dic_buullets_player.pop(bullet)


        if secondes >= 10 and score >= 10 :
            big_enemie_time = True
            big_enemie.display_enemy()
            big_enemie.display_health_bar()
            big_enemie.change_coordinates()
            big_enemie.shoot_bullet()

        #displaying the score : 
        text = font.render(f"Score  :  {score} ", True, (255, 255, 255))
        screen.blit(text , ( 5 , 5 ) )

        #FPS 60 :
        clock.tick(60)
        pygame.display.update()




if __name__ == '__main__':
    main()
