import pygame
import random
import os

FPS = 60
WIDTH = 500
HEIGHT = 600

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
#遊戲初始化 & 創建視窗
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("星際大戰")
clock = pygame.time.Clock()

#載入圖片
bg_img = pygame.image.load(os.path.join("img", "銀河.jfif")).convert()
player_img = pygame.image.load(os.path.join("img", "飛機.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (40, 30))
player_mini_img.set_colorkey(BLACK)
rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert()
pygame.display.set_icon(rock_img)
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
expl_anim = {}
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
for i in range(8):
    expl_img = pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()
    expl_img.set_colorkey(BLACK)
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (100, 100)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    player_expl_img = pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()
    player_expl_img.set_colorkey(BLACK)
    expl_anim['player'].append(pygame.transform.scale(player_expl_img, (300, 300)))
power_imgs = {}
power_imgs['shield'] = pygame.image.load(os.path.join("img", "shield.png")).convert()
power_imgs['gun'] = pygame.image.load(os.path.join("img", "gun.png")).convert()
power_imgs['armer'] = pygame.image.load(os.path.join("img", "armer.png")).convert()
power_imgs['luck'] = pygame.image.load(os.path.join("img", "luck.png")).convert()

#載入音樂、音效

shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))
shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))
expl_sounds = [
    pygame.mixer.Sound(os.path.join("sound", "expl0.wav")), 
    pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))
]
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))


#下載字體
font_name = os.path.join("font.ttf")
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def new_rock():
    r= Rock()
    all_sprites.add(r)
    rocks.add(r)

def draw_health(surf, hp, max, x, y):
    if hp < 0:
        hp = 0
    BAR_LENTH = max
    BAR_HEIGHT = 10
    fill = (hp/max)*BAR_LENTH
    outline_rect = pygame.Rect(x, y, BAR_LENTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 40*i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_progress(surf, p_score, t_score, x, y):
    fill_rect = pygame.Rect(x, y, WIDTH * p_score / t_score, 7)
    pygame.draw.rect(surf, YELLOW, fill_rect)

def draw_init():
    screen.blit(bg_img, (0, 0))
    draw_text(screen, '太空生存戰!', 64, WIDTH/2, HEIGHT/4)
    draw_text(screen, '← → 移動飛船 空白鍵發射子彈', 22, WIDTH/2, HEIGHT/2)
    draw_text(screen, '按P暫停遊戲', 18, WIDTH/2, HEIGHT*5/8-40)
    draw_text(screen, '按空白鍵開始遊戲!', 18, WIDTH/2, HEIGHT*3/4)
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    waiting = False
                    return False
      
def draw_shop(goal, p_times, coin):
    shop_list = ['', 'luck', 'gun', 'armer']
    shop_nm = ['', '幸運', '子彈', '血量']
    shop_lim = ['', 9, 14, 4]
    waiting = True
    while waiting:
        clock.tick(FPS)
        screen.blit(bg_img, (0, 0))
        draw_text(screen, '太空商店', 64, WIDTH/2, HEIGHT/7)
        draw_text(screen, '下一次商店在' + str("{:.0f}".format(goal)) + '分時出現', 25, WIDTH/2, HEIGHT/5+64)
        draw_text(screen, '$'+str("{:.0f}".format(coin)), 18, WIDTH-60, HEIGHT-100)
        shop_price = ['', 100*(p_times[0]+1), 100*(p_times[1]+1), 100*(p_times[2]+1)]
        image_rect = {}
        for i in range(1,4):  
            sp_img = power_imgs[shop_list[i]]
            image_rect[f"rect_{i}"] = sp_img.get_rect(topleft = (WIDTH/4*i-25, HEIGHT/2-30 ))
            screen.blit(sp_img, (image_rect[f"rect_{i}"].topleft)) 
            if p_times[i-1] > shop_lim[i]:
                draw_text(screen, "完售", 22, WIDTH/4*i, HEIGHT/3+30)
            else:
                draw_text(screen, str(shop_price[i]), 22, WIDTH/4*i, HEIGHT/3+30)
            draw_text(screen, shop_nm[i], 22, WIDTH/4*i, HEIGHT/2+20)
        draw_text(screen, '*按E繼續遊戲*', 18, WIDTH/2, HEIGHT*4/5)
        pygame.display.update()
        #取得輸入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return [True]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if image_rect["rect_1"].collidepoint(event.pos) and coin >= shop_price[1]:
                    p_times[0] +=1
                    if p_times[0] > shop_lim[1]+1:
                        p_times[0] = shop_lim[1]+1
                    else:
                        coin -= shop_price[1]
                    
                elif image_rect["rect_2"].collidepoint(event.pos) and coin >= shop_price[2]:
                    p_times[1] += 1
                    if p_times[1] > shop_lim[2]+1:
                        p_times[1] = shop_lim[2]+1
                    else:
                        coin -= shop_price[2]

                elif image_rect["rect_3"].collidepoint(event.pos) and coin >= shop_price[3]:
                    p_times[2] += 1
                    if p_times[2] > shop_lim[3]+1:
                        p_times[2] = shop_lim[3]+1
                    else:
                        coin -= shop_price[3]
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_e:
                    waiting = False
                    return [False, p_times, coin]

#Sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (52, 46))
        self.image.set_colorkey(BLACK) 
        #定位
        self.rect = self.image.get_rect()
        self.radius = 23
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 8
        self.health = 100
        self.maxhp = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gunpow = 1
        self.gun_time = 0
        self.shoot_time = 0
        self.luckp = 0
        self.luck_time = 0

    def update (self):
        now = pygame.time.get_ticks()
        if self.gunpow > 1 and now - self.gun_time > 4250:
            self.gun -= 1
            self.gun_time = now

        if self.luckp == 1 and now - self.luck_time > 3000:
            self.luckp = 0
            self.luck_time = now 
 
        if self.hidden and now - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        now = pygame.time.get_ticks()
        if not(self.hidden):
            if now - self.shoot_time > 250:
                self.shoot_time = now
                if self.gun > 20:
                    self.gun = 20
                if self.gun == 1:
                    bullet = Bullet(self.rect.centerx, self.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    #shoot_sound.play()
                elif self.gun >= 2 :
                    for i in range(self.gun): 
                        bullet = Bullet(self.rect.left - self.gun*10 + (self.rect.width + self.gun*20)/(self.gun - 1) * i, self.rect.centery)
                        all_sprites.add(bullet)
                        bullets.add(bullet)
                shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH/2, HEIGHT+500)

    def gunup(self):
        self.gun += 1
        self.gunpow += 1
        self.gun_time = pygame.time.get_ticks()

    def luck(self, luck):
        self.luckp = 1
        luck -= 0.1
        if luck < 0.3:
            luck = 0.3
        self.luck_time = pygame.time.get_ticks()
        return luck

class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        size = random.randrange(15, 150)
        self.image_ori = pygame.transform.scale(rock_img, (size, size))
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.image = pygame.transform.scale(rock_img, (size, size))
        
        #定位
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * 0.9 / 2 )
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(-50, WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-6, 6)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)

    #定義隕石旋轉的函數
    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center

    def update (self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        #超出視窗後重製速度、位置
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bullet_img, (20, 40))
        self.image.set_colorkey(BLACK)
        #定位
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update (self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = expl_anim[self.size][0]
        #定位
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update (self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]):
                self.kill()
            else:
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun', 'armer', 'luck'])
        self.image = power_imgs[self.type]
        self.image.set_colorkey(BLACK)
        #定位
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update (self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()



pygame.mixer.music.play(-1) #重複播放背景音樂
pygame.mixer.music.set_volume(0.7) #聲音大小

#遊戲迴圈
show_init = True
running = True

while running:
    if show_init:
        close = draw_init()
        if close:
            break #debug用
        show_init = False
        show_shop = False
        show_pause = False
        goal = 1000
        g_rate = 1
        ori_luck = 0.924
        luck = 0.924
        p_times = [0, 0, 0]
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            new_rock()
        score = 0
        score_p = 0
        goal_p = 1000 
        coin = 0

    if show_shop:
        goal += 1000 * g_rate
        goal_p = 1000 * g_rate
        g_rate += 1
        if g_rate > 10: 
            g_rate -= 0.1
        close = draw_shop(goal, p_times, coin)
        if close[0]:
            break
        show_shop = False
        p_times = close[1]
        coin = close[2]
        luck = ori_luck - 0.05*p_times[0]
        all_sprites = pygame.sprite.Group()
        rocks = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powers = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        player.gun += 1*(p_times[1])
        player.maxhp += 10*(p_times[2])
        player.health = player.maxhp
        score_p = 0
        for i in range(8):
            new_rock()
        
    if show_pause:
        waiting = True
        #draw_text(screen, "PAUSE", 30, WIDTH/2, HEIGHT/2)
        pygame.display.update()
        while waiting:
            clock.tick(FPS)
            #取得輸入
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        show_pause = False
                        waiting = False

    clock.tick(FPS)
    #取得輸入
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                show_pause = True
        
    #更新遊戲
    all_sprites.update()

    key_p = pygame.key.get_pressed()  
    if (key_p[pygame.K_SPACE]):
        player.shoot()
        
    #判斷石頭 子彈相撞
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)   
    for hit in hits:
        random.choice(expl_sounds).play()
        score += hit.radius
        score_p += hit.radius
        coin += hit.radius/2//10*10

        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > luck:
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)
        new_rock()

    #判斷石頭 飛船相撞
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)
    for hit in hits:
        new_rock()
        #隕石傷害
        player.health -= hit.radius
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        random.choice(expl_sounds).play()
        if player.health <= 0:
            death_expl = Explosion(player.rect.center, 'player')
            all_sprites.add(death_expl)
            die_sound.play()
            player.lives -= 1
            player.health = player.maxhp
            player.hide()

    #判斷寶物 飛船相撞
    hits = pygame.sprite.spritecollide(player, powers, True)
    for hit in hits:
        if hit.type == 'shield':
            player.health += 20
            if player.health > player.maxhp:
                player.health = player.maxhp
            shield_sound.play()

        if hit.type == 'gun':
            player.gunup()
            gun_sound.play()

        if hit.type == 'armer':
            player.maxhp += 20
            if player.maxhp > 200:
                player.maxhp = 200
                player.health += 10
                if player.health > 200:
                    player.health = 200
            else:
                player.health += 20

        if hit.type == 'luck':
            luck = player.luck(luck)

    if player.lives == 0 and not(death_expl.alive()):
        show_init = True        
    if score > goal:
        show_shop = True

    #畫面顯示
    screen.fill(BLACK)
    screen.blit(bg_img, (0, 0))
    all_sprites.draw(screen)
    draw_text(screen, str("{:.0f}".format(score)), 18, WIDTH/2, 10)
    draw_text(screen, '$'+str("{:.0f}".format(coin)), 18, WIDTH-60, HEIGHT-100)
    draw_health(screen, player.health, player.maxhp, 5, 15)
    draw_lives(screen, player.lives, player_mini_img, WIDTH-125, 15)
    draw_progress(screen, score_p, goal_p, 0, HEIGHT-7)
    pygame.display.update()

pygame.quit