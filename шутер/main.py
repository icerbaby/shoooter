from pygame import *
from random import randint

fps = 60
game_finished, game_run, game_paused, game_finished2 = False, True, False, False
clock = time.Clock()


window_width, window_height = 1115, 570

kills, lost,  = 0, 0,

in_menu = True

stop_draw = False

boss_killed = False

window = display.set_mode((window_width, window_height))
display.set_caption("Илья маладес")


font.init()

score_font = font.SysFont("Arial", 32, True)
main_font = font.SysFont("Arial", 72, True)
big_font = font.SysFont("Arial", 35, True)


mixer.init()
music=mixer.Sound("Дляигрывшутеры31KhaosHammer_Battlefield4MainThemeSong_muzmo_su.mp3")
music.play()
fire_sound = mixer.Sound("z_uk-vystrel-s-pistoleta.mp3")
miss_sound = mixer.Sound("damage1.mp3")
kill_sound = mixer.Sound("death2.mp3")
lose_sound = mixer.Sound("game-lost.mp3")
win_sound = mixer.Sound("game-won.mp3")

class Menu:
    def __init__(self):
        window.fill((200,200,200))
        self.font = font.Font(None, 36)
        self.font2 = font.Font(None, 31)
        self.difficulty1_button = Rect(150, window_height /2, 180, 50)
        self.difficulty2_button = Rect(480, window_height /2, 190, 50)
        self.difficulty3_button = Rect(800, window_height /2, 180, 50)
        self.exit_button = Rect(450,480, 259,128)
        self.difficulty3_text = self.font.render("Сложная", True, (255, 255, 255))
        self.difficulty2_text = self.font.render("Средняя", True, (255, 255, 255))
        self.difficulty1_text = self.font.render("Легкая", True, (255, 255, 255))
        self.exit_text = self.font2.render("Выход", True, (119,221,119))
        self.welcome_text = big_font.render("Вас приветствует игра Шутер! Для начала игры выберите сложность", True,(255, 253,208))
    
    def draw_buttons(self):  
        mars_button.reset() 
        uranus_button.reset()
        earth_button.reset() 
        exit_button.reset()
        window.blit(self.exit_text,(self.exit_button.x + 125, self.exit_button.y))
        window.blit(self.difficulty1_text, (self.difficulty1_button.x + 55, self.difficulty1_button.y + 18))  
        window.blit(self.difficulty2_text, (self.difficulty2_button.x + 42, self.difficulty2_button.y + 10))
        window.blit(self.difficulty3_text, (self.difficulty3_button.x + 52, self.difficulty3_button.y + 15))
        window.blit(self.welcome_text,(70, 70) )

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.difficulty1_button.collidepoint(mouse.get_pos()):  
                return "Легкая"  
            elif self.difficulty2_button.collidepoint(mouse.get_pos()):  
                return "Средняя"
            elif self.difficulty3_button.collidepoint(mouse.get_pos()):
                return "Сложная"  
            elif self.exit_button.collidepoint(mouse.get_pos()):
                return "Выход"  
        return None

class WinEndMenu:
    def __init__(self):
        window.fill((200,200,200))
        self.font = font.Font(None, 36)
        self.font2 = font.Font(None, 31)
        self.exit_button = Rect(450,480, 259,128)
        self.exit_text = self.font2.render("Выход", True, (119,221,119))
        self.win_text = main_font.render("Ты выиграл!", True, (255,255,0))
        
    
    def draw_buttons(self):  
        exit_button.reset()
        window.blit(self.exit_text,(self.exit_button.x + 125, self.exit_button.y))
        window.blit(self.win_text,(window_width / 2 - self.win_text.get_width() / 2, window_height / 2 - self.win_text.get_height() / 2))

    def handle_event(self, event):
        if event.type == MOUSEBUTTONDOWN:
            if self.exit_button.collidepoint(mouse.get_pos()):
                return "Exit"
        return None


class LoseEndMenu:
    def __init__(self):
        window.fill((200,200,200))
        self.font = font.Font(None, 36)
        self.font2 = font.Font(None, 31)
        self.exit_button = Rect(450,480, 259,128)
        self.exit_text = self.font2.render("Выход", True, (119,221,119))
        self.lose_text = main_font.render("Вы проиграли!", True, (255,0,0))
        
    
    def draw_buttons(self):   
        exit_button.reset()
        window.blit(self.exit_text,(self.exit_button.x + 125, self.exit_button.y))
        window.blit(self.lose_text,(window_width / 2 - self.lose_text.get_width() / 2, window_height / 2 - self.lose_text.get_height() / 2))

        

    def handle_event(self, event):
            if event.type == MOUSEBUTTONDOWN:
                if self.exit_button.collidepoint(mouse.get_pos()):
                    return "Выход"  
            return None

class GameSprite(sprite.Sprite):
    def __init__(self, img, pos, size, speed,):
        super().__init__()

        
        self.image = transform.smoothscale(
            image.load(img),
            size
        )

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos

        self.speed = speed
        self.width, self.height = size

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    fire_delay = fps * 0.25
    fire_timer = fire_delay
    can_fire = True

    def update(self):

        if not self.can_fire:
            if self.fire_timer > 0:
                self.fire_timer -= 1
            else:
                self.fire_timer = self.fire_delay
                self.can_fire = True
            

        keys = key.get_pressed()
        if keys[K_a]:
            if self.rect.x > 0:
                self.rect.x -= self.speed
        if keys[K_d]:
            if self.rect.x < window_width - self.width:
                self.rect.x += self.speed

        if keys[K_SPACE] and self.can_fire:
            fire_sound.play()
            self.fire()
            self.can_fire = False
    def fire(self):
        new_pylya = Pulya(img="pylya.png", pos=(self.rect.x, self.rect.y), size=(100, 100), speed=15)

        gryppa_pylb.add(new_pylya)
        

class Enemy(GameSprite):
    def __init__(self, img, pos, size, speed, health):
        super().__init__(img, pos, size, speed)
        self.health = health

        


    def update(self):
        global lost
        
        self.health_font = score_font.render(str(self.health), True, (255, 255,255))
        window.blit(self.health_font, self.rect.topright)
        self.rect.y += self.speed
        if self.rect.y >= window_height or sprite.collide_rect(self, player):
            lost += 1
            miss_sound.play()
            self.kill()

class Boss(GameSprite):
    def __init__(self, img, pos, size, speed, health):
        super().__init__(img, pos, size, speed)
        self.health = health

        


    def update(self):
        global lost
        
        self.health_font = score_font.render(str(self.health), True, (255, 255,255))
        window.blit(self.health_font, self.rect.topright)
        self.rect.y += self.speed
        if self.rect.y >= window_height or sprite.collide_rect(self, player):
            screen_text = main_font.render("Ты проиграл(", True, (255,0,0))
            window.blit(screen_text, (window_width / 2 - screen_text.get_width() / 2, window_height / 2 - screen_text.get_height() / 2))
            music.stop()
            fire_sound.stop()
            lose_sound.play()
            self.kill()
            game_finished = True



class Pulya(GameSprite):
    def update(self):
        global kills
        global game_finished2
        global boss_killed
        
        self.rect.y -= self.speed

        enemys_collided_list = sprite.spritecollide(self,enemys_group, False)

        bosses_collided_list = sprite.spritecollide(self,bosses_group, False)

        if len(enemys_collided_list) > 0:
            enemy = enemys_collided_list[0]

            if enemy.health > 1:
                enemy.health -= 1
                self.kill()
            else:
                enemy.kill()
                self.kill()
                kills +=1

        
        
        if len(bosses_collided_list) > 0:
            boss = bosses_collided_list[0]

            if boss.health > 1:
                boss.health -=1
                self.kill
            else:
                boss.kill()
                self.kill()
                boss_killed = True
                
                game_finished2 = True

            
            kill_sound.play()
            self.kill()

        if self.rect.y <= 0:
            self.kill()

lose_endmenu = LoseEndMenu()
win_endmenu = WinEndMenu()
exit_button = GameSprite(img = "ракетакнопкавыход.png", pos= (440, 430), size=(259,128), speed = 0)
earth_button = GameSprite(img="земля_кнопка.png", pos=(150, 225), size=(190,190), speed = 0)
uranus_button = GameSprite(img="уран_кнопка.png", pos=(800, 217), size=(200,200), speed = 0)
mars_button = GameSprite(img="марс_кнопка.png", pos=(480, 215), size=(190,190), speed = 0)
bg2 = GameSprite(img = "bg2.jpg", pos=(0, 0), size=(window_width, window_height), speed = 0)
bg = GameSprite(img = "bg.jpg", pos=(0, 0), size=(window_width, window_height), speed = 0)
player = Player(img = "igrok.png", pos=(5, window_height - 64), size=(96, 64), speed = 5)
menu = Menu()


enemys_group = sprite.Group()

bosses_group = sprite.Group()

gryppa_pylb = sprite.Group()


bosses_spawn_delay = fps 
bosses_spawn_timer = fps * 10000

enemys_spawn_delay = fps
enemys_spawn_timer = enemys_spawn_delay

while in_menu:
    music.stop()
    for ev in event.get():
        if ev.type == QUIT:
            game_run = False
    bg.reset()
    menu.draw_buttons()
    
    display.update()

    for ev in event.get():
        action = menu.handle_event(ev)
        if action == "Легкая" and in_menu:
            in_menu = False
        elif action == "Средняя" and in_menu:
            in_menu = False
        elif action == "Сложная" and in_menu:
            in_menu = False
        elif action == "Выход" and in_menu:
            in_menu = False
            game_run = False


while game_paused:
    for ev in event.get():
        if ev.type == QUIT:
            game_run = False
    for ev in event.get():
        action = win_endmenu.handle_event(ev)
        if action == "Выход":           
            game_run = False
        
    


while game_run:
    
    for ev in event.get():
        if ev.type == QUIT:
            game_run = False
        if ev.type == MOUSEBUTTONDOWN:
            mouse_pos = ev.pos

            # ПУТЬ КОСТЫЛЕЙ
            if win_endmenu.exit_button.collidepoint(mouse_pos) and boss_killed:
                game_run = False

    if not in_menu and action == "Легкая":
        bg.reset()
        if not stop_draw:
            player.reset()
            bosses_group.draw(window)
            gryppa_pylb.draw(window)
    
            kills_text = score_font.render("Убито: " + str(kills), True, (255, 255,255))
            lost_text = score_font.render("Пропущено: "+ str(lost), True, (255,255,255))

            window.blit(kills_text, (5,5))
            window.blit(lost_text, (5,37))

        if kills >= 10:
            game_paused = True
            bosses_spawn_delay -=1
            if bosses_spawn_delay == 0:
                bosses_spawn_delay = bosses_spawn_timer

                easy_boss = Boss(img = "easy_boss.png", pos=(window_width /2, 0), size = (192, 128), speed = 0.5, health = 10)
                bosses_group.add(easy_boss)
            if boss_killed == True:
                stop_draw = True
                win_endmenu.draw_buttons()
                
                music.stop()
                fire_sound.stop()
                win_sound.play()








        
        if lost >= 15:
            lose_endmenu.draw_buttons()
            stop_draw = True
            boss_killed = True
            music.stop()
            fire_sound.stop()
            lose_sound.play()
            game_finished2 = True
            game_finished = True
        if not game_finished2:
            if not game_finished and not game_paused:
                if not stop_draw:
                    r = randint(1,3)
                    if enemys_spawn_timer > 0:
                        enemys_spawn_timer -= 1
                    else:
                        if r == 1:
                            new_enemy = Enemy(img="vrag.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 5), health = 3 )
                            enemys_group.add(new_enemy)
                            enemys_spawn_timer = enemys_spawn_delay
                        if r == 2:
                            new_enemy = Enemy(img="vrag2.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 5), health = 2 )
                            enemys_group.add(new_enemy)
                            enemys_spawn_timer = enemys_spawn_delay
                        if r== 3:
                            new_enemy = Enemy(img="vrag3.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 4), health = 1 )
                            enemys_group.add(new_enemy)
                            enemys_spawn_timer = enemys_spawn_delay
                    enemys_group.draw(window)
                    enemys_group.update()
            bosses_group.update()
            player.update()
            gryppa_pylb.update()   
            
                
    elif not in_menu and action == "Средняя":
        bg.reset()
        if not stop_draw:
            player.reset()
            bosses_group.draw(window)
            gryppa_pylb.draw(window)
        
            kills_text = score_font.render("Убито: " + str(kills), True, (255, 255,255))
            lost_text = score_font.render("Пропущено: "+ str(lost), True, (255,255,255))

            window.blit(kills_text, (5,5))
            window.blit(lost_text, (5,37))

        if kills >= 15:
            game_paused = True
            bosses_spawn_delay -=1
            if bosses_spawn_delay == 0:
                bosses_spawn_delay = bosses_spawn_timer
            
                medium_boss = Boss(img = "medium_boss.png", pos=(window_width /2, 0), size = (192, 128), speed = 0.5, health = 15)
                bosses_group.add(medium_boss)
            if boss_killed == True:
                stop_draw = True
                win_endmenu.draw_buttons()
                
                music.stop()
                fire_sound.stop()
                win_sound.play()
                
                   
                    
            
           


            
        
        if lost >= 10:
            lose_endmenu.draw_buttons()
            stop_draw = True
            music.stop()
            fire_sound.stop()
            lose_sound.play()
            game_finished2 = True
            game_finished = True
        if not game_finished2:
            if not game_finished and not game_paused:
                if not stop_draw:
                    r = randint(1,3)
                    if enemys_spawn_timer > 0:
                        enemys_spawn_timer -= 1
                    else:
                        if r == 1:
                            new_enemy = Enemy(img="vrag.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 4), health = 3 )
                            enemys_group.add(new_enemy)
                            enemys_spawn_timer = enemys_spawn_delay
                        if r == 2:
                            new_enemy = Enemy(img="vrag2.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 4), health = 2 )
                            enemys_group.add(new_enemy)
                            enemys_spawn_timer = enemys_spawn_delay
                        if r== 3:
                            new_enemy = Enemy(img="vrag3.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 4), health = 1 )
                            enemys_group.add(new_enemy)
                            enemys_spawn_timer = enemys_spawn_delay
                    enemys_group.draw(window)
                    enemys_group.update()
            bosses_group.update()
            player.update()
            gryppa_pylb.update()
    elif not in_menu and action == "Сложная":
        bg.reset()
        if not stop_draw:
            player.reset()
            bosses_group.draw(window)
            gryppa_pylb.draw(window)
        
            kills_text = score_font.render("Убито: " + str(kills), True, (255, 255,255))
            lost_text = score_font.render("Пропущено: "+ str(lost), True, (255,255,255))

            window.blit(kills_text, (5,5))
            window.blit(lost_text, (5,37))

        if kills >= 20:
            game_paused = True
            bosses_spawn_delay -=1
            if bosses_spawn_delay == 0:
                bosses_spawn_delay = bosses_spawn_timer
            
                hard_boss = Boss(img = "hard_boss.png", pos=(window_width /2, 0), size = (192, 128), speed = 0.5, health = 20)
                bosses_group.add(hard_boss)
            if boss_killed == True:
                stop_draw = True
                win_endmenu.draw_buttons()
                
                music.stop()
                fire_sound.stop()
                win_sound.play()
                
                   
                    
            
           


            
        
        if lost >= 10:
            lose_endmenu.draw_buttons()
            stop_draw = True
            music.stop()
            fire_sound.stop()
            lose_sound.play()
            game_finished2 = True
            game_finished = True
        if not game_finished2:
            if not game_finished and not game_paused:
                if not stop_draw:
                    r = randint(1,3)
                    if enemys_spawn_timer > 0:
                        enemys_spawn_timer -= 1
                    else:
                        if r == 1:
                            new_enemy = Enemy(img="vrag.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 4), health = 3 )
                            enemys_group.add(new_enemy)
                            enemys_spawn_timer = enemys_spawn_delay
                        if r == 2:
                            new_enemy = Enemy(img="vrag2.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 4), health = 2 )
                            enemys_group.add(new_enemy)
                            enemys_spawn_timer = enemys_spawn_delay
                        if r== 3:
                            new_enemy = Enemy(img="vrag3.png", pos = (randint(100, window_width - 100), -100), size=(96,64), speed = randint(2, 4), health = 1 )
                            enemys_group.add(new_enemy)
                            enemys_spawn_timer = enemys_spawn_delay
                    enemys_group.draw(window)
                    enemys_group.update()
            bosses_group.update()
            player.update()
            gryppa_pylb.update()
    #elif:
        #music.stop()
        #fire_sound.stop()
        #menu.draw_buttons()
    elif in_menu and action == "Выход":
        

        game_run = False
            
    display.update()
    clock.tick(fps)
