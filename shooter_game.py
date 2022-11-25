#Создай собственный Шутер!

from pygame import *
from random import randint
mixer.init()
win_width = 700
win_height = 500 
window = display.set_mode((win_width, win_height))  
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
game = True
finish = False
clock=time.Clock()
FPS = 60
score = 0
goal = 10
lost = 0
max_lost = 3
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load('rocket.png'), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
        
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < win_height - 80:
            self.rect.y += self.speed
    def Fire(self):
        bullet = Bullet("bullet.png", self.rect.centrex, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

ship = Player("rocket.png",7,win_height - 80, 5)
cyborg = Enemy("ufo.png",win_width - 80, 280, 7)
cyborg = Enemy("ufo.png",win_width - 60, 280, 7)
cyborg = Enemy("ufo.png",win_width - 70, 280, 7)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, win_width - 80), -40,  randint(1,5))
    monsters.add(monster)
finish = False
run = True
font.init()
font = font.Font(None, 35)
win = font.render('GAME WIN!', True,(0, 255, 255))
lose = font.render('GAME END!', True,(255, 0, 75))
win = font.render('YOU WIN!', True,(0, 255, 0))
lose = font.render('YOU LOSE!', True,(255, 0, 0))
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.type == K_SPACE:
                player.Fire()
    if not finish:
        window.blit(background, (0, 0))
        text = font.render("Счёт: "+ str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font.render("Пропущено:" + str(lost), 1, 3 )
        collides = sprite.groupcollide(cyborg, bullets, True, True)
        for collide in collides:
            score = score + 1
            cyborg = Enemy('ufo.png',  randint(80, win_width - 80)-40, 80, 50, randint(1, 5))
            cyborgs.add(cyborg)
        
        if sprite.spritecollide(ship, cyborg, False) or lost >= max_lost:
            finish =True
            window.blit(lose, (200, 200))
        if score >= goal:
            finish = True
            window.blit(win, 200, 200)

    clock.tick(FPS) 
    display.update()
