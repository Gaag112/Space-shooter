#Создай собственный Шутер!

from pygame import *
from random import randint
from time import sleep

ufo = 0
kill = 0
count_tick = 0
count_fire = 0
count_bullet = 0
health = 100
Reload = False
Pause = False

class GameSprite(sprite.Sprite):
    def __init__(self, image_name, recx, recy, sprite_speed, x, y):
        super().__init__()
        self.recx = recx
        self.recy = recy
        self.sprite_speed = sprite_speed
        self.x = x
        self.y = y
        self.image = transform.scale(
            image.load(image_name), (self.recx, self.recy)
        )
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def show(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def __init__(self, image_name, recx, recy, sprite_speed, x, y):
        super().__init__(image_name, recx, recy, sprite_speed, x, y)
    def update(self):
        key_pressed = key.get_pressed()
        if self.rect.x > 30 and key_pressed[K_LEFT]:
            self.rect.x -= self.sprite_speed
        elif self.rect.x < 630 and key_pressed[K_RIGHT]:
            self.rect.x += self.sprite_speed
    def fire(self):
        pass
class Enemy(GameSprite):
    def __init__(self, image_name, recx, recy, sprite_speed, x, y, x_start, y_start):
        super().__init__(image_name, recx, recy, sprite_speed, x, y)
        self.x_start = x_start
        self.y_start = y_start
    def update(self):
        global ufo
        if self.rect.y < 450:
            self.rect.y += self.sprite_speed
        else:
            self.rect.x = self.x_start
            self.rect.y = self.y_start
            self.x_start = randint(50, 650)
            self.y_start = randint(50, 70)
            ufo += 1
class Bullet(GameSprite):
    def __init__(self, image_name, recx, recy, sprite_speed, x, y):
        super().__init__(image_name, recx, recy, sprite_speed, x, y)
    def update(self):
        if self.rect.y > 0:
            self.rect.y -= self.sprite_speed
        else:
            self.kill()

class Asteroid(GameSprite):
    def __init__(self, image_name, recx, recy, sprite_speed, x, y):
        super().__init__(image_name, recx, recy, sprite_speed, x, y)
    def update(self):
        global asteroid_count
        if self.rect.y < 500:
            self.rect.y+=self.sprite_speed
        else:
            self.rect.x = randint(50, 650)
            self.rect.y = randint(50, 70)

window = display.set_mode((700, 500))
display.set_caption("Шутер")
mixer.init()
mixer.music.load("space.ogg")

font.init()
mixer.music.play()
fire = mixer.Sound("fire.ogg")

clock = time.Clock()
count = font.SysFont('Arial', 20)
font_ufo = count.render("Пропущенных монстров: "+str(ufo), True, (215, 215, 0))
font_kill = count.render("Убитых монсров: "+str(kill), True, (215, 215, 0))
font_health = count.render("Здоровье: "+str(health), True, (0, 215, 0))
finish_table = font.SysFont('Arial', 70)
font_win = finish_table.render("YOU WIN!", True, (215, 0, 215))
font_lose = finish_table.render("YOU LOSE!", True, (0, 215, 0))
font_pause = finish_table.render("PAUSE!", True, (0, 0, 0))

reload_table = font.SysFont('Arial', 50)
font_reload = reload_table.render("WAIT RELOAD!", True, (215, 0, 0))
background = transform.scale(
    image.load("galaxy.jpg"), (700, 500)
)

player = Player("rocket.png", 70, 70, 5, 350, 400)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(5):
    monster = Enemy("ufo.png", 80, 60, 1, randint(50, 650), randint(50, 70), randint(50, 650), randint(50, 70))
    monsters.add(monster)

for i in range(2):
    asteroid = Asteroid("asteroid.png", 120, 100, 0.5, randint(50, 650), randint(50, 70))
    asteroids.add(asteroid)

game = True
finish = False
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
    if not finish:
        window.blit(background, (0, 0))
        font_ufo = count.render("Пропущенных монстров: "+str(ufo), True, (215, 215, 0))
        font_kill = count.render("Убитых монсров: "+str(kill), True, (215, 215, 0))
        font_health = count.render("Здоровье: "+str(health), True, (0, 215, 0))
      
        window.blit(font_kill, (20, 50))
        window.blit(font_ufo, (20, 30))
        window.blit(font_health, (20, 70))
    
        monsters.draw(window)
        key_press = key.get_pressed()
        if key_press[K_p]:
            sleep(0.5)
            finish = True
            Pause = True
        if key_press[K_SPACE]:
            if not Reload:
                sleep(0.03)
                bullet = Bullet("bullet.png", 10, 10, 10, player.rect.x+30, player.rect.y)
                bullets.add(bullet)
                fire.play()
                count_bullet += 1
            if count_bullet == 5:
                Reload = True
                count_tick = 0
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        player.show()
        player.update()
        monsters.update()

        if Reload:
            window.blit(font_reload, (220, 450))

        if sprite.groupcollide(monsters, bullets, True, True):
            kill += 1
            monster = Enemy("ufo.png", 80, 60, 1, randint(50, 650), randint(50, 70), randint(50, 650), randint(50, 70))
            monsters.add(monster)
        if sprite.spritecollide(player, asteroids, True):
            health-=50
            asteroid = Asteroid("asteroid.png", 120, 100, 0.5, randint(50, 650), randint(50, 70))
            asteroids.add(asteroid)
        if sprite.spritecollide(player, monsters, True):
            health -= 25
        if ufo > 5 or health <= 0:
            window.blit(font_lose, (250, 200))
            finish = False
        if kill >= 10:
            window.blit(font_win, (250, 200))
            finish = False

        clock.tick(60)
        count_tick+=1
        count_fire+=1
        if Reload:
            if count_tick == 180:
                Reload = False
                count_bullet = 0
        display.update()
    elif Pause:
        window.blit(font_pause, (300, 250))
        key_press = key.get_pressed()
        if key_press[K_p]:
            sleep(0.5)
            Pause = False
            finish = False
        clock.tick(60)
        display.update()
