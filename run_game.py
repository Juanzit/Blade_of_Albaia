import time
import pgzrun
import math
import random

WIDTH = 800
HEIGHT = 580

menu = Actor('albaiaquestmenu', (405, 200))
gameoverr = Actor('gameoover-1', (405, 200))
map10 = Actor('map1frame1')
map11 = Actor('map1frame2')
map12 = Actor('map1frame3')

wall1 = Actor('wall1', (165, 520))
wall2 = Actor('wall2', (665, 520))
floor1 = Actor('floor1', (400, 560))
floor2 = Actor('floor2', (127, 520))
floor3 = Actor('floor3', (700, 520))
floor4 = Actor('floor4', (770, 465))
floor5 = Actor('floor5', (43, 473))
floor6 = Actor('floor6', (423, 468))
floor7 = Actor('floor7', (530,350))
floor8 = Actor('floor7', (350, 280))
floor10 = Actor('floor7', (650, 220))

floor9 = Actor('floor4', (30, 400))  
floor11 = Actor('floor4', (350, 400))  

floor912_x = 100
floor913_x = 280
floor12 = Actor('floor4', (floor912_x, 400))
floor13 = Actor('floor4', (floor913_x, 400))
floor912_left = True
floor913_left = False

plataforms = [floor1, floor2, floor3, floor4, floor5, floor6, floor7, floor8, floor9, floor10, floor11, floor12, floor13, wall1, wall2]

fragment_x = [415,34,555,519,300,694,336]
fragment_y = [536,439,458,334,260,200,394]
f_xy = random.randint(0, 6)
fragment = Actor('fragment', (fragment_x[f_xy], fragment_y[f_xy]))
score = 0

time_counter = 0
music_on = 0
screens = 1

game_over = False
dexters = []

class Dexter(Actor):
    def __init__(self, x, y, speed=2, start_x=0, end_x=800):
        super().__init__('dexter1', (x, y))
        self.speed = speed
        self.direction = 1
        self.start_x = start_x
        self.end_x = end_x
        self.scale = 0.5
        self.flip_x = False  

    def move(self):
        self.x += self.speed * self.direction
        if self.x >= self.end_x or self.x <= self.start_x:
            self.direction *= -1
            self.flip_x = not self.flip_x

def create_dexters():
    global dexters
    dexters.clear()  
    
    dexters.append(Dexter(
        x=400, 
        y=floor1.y - 20, 
        speed=2, 
        start_x=floor1.x - 60,  
        end_x=floor1.x + 60   
    ))
    
    dexters.append(Dexter(
        x=423,
        y=floor6.y - 20,
        speed=1.8,
        start_x=423 - 50,
        end_x=423 + 50
    ))
    
    dexters.append(Dexter(
        x=530,
        y=floor7.y - 20,
        speed=2.2,
        start_x=530 - 50,
        end_x=530 + 50
    ))
    
    dexters.append(Dexter(
        x=350,
        y=floor8.y - 20,
        speed=1.5,
        start_x=350 - 50,
        end_x=350 + 50
    ))
   
    dexters.append(Dexter(
        x=650,
        y=floor10.y - 20,
        speed=2,
        start_x=650 - 50,
        end_x=650 + 50
    ))

class Kaya(Actor):
    def __init__(self, x, y):
        super().__init__('kaya1front-1', (x, y))
        self.image = 'kaya1front-1'
        self.scale = 0.5
        self.speed = 3
        self.jumping = False  
        self.y_velocity = 0
        self.gravity = 0.8
        self.jump_strength = -12
        self.direction = 1
        self.height = 49  

    def update(self):
        if keyboard.left:
            self.x -= self.speed
            self.direction = -1
        if keyboard.right:
            self.x += self.speed
            self.direction = 1

        self.y_velocity += self.gravity
        prev_y = self.y
        self.y += self.y_velocity

        self.jumping = True
        for plataforma in plataforms:
            if self.colliderect(plataforma):
                if self.y_velocity >= 0 and prev_y <= plataforma.y:
                    plataforma_top = plataforma.y - (plataforma.height / 2)
                    self.y = plataforma_top - (self.height / 2)
                    self.y_velocity = 0
                    self.jumping = False 

        if keyboard.up and not self.jumping:
            self.y_velocity = self.jump_strength
            self.jumping = True
            self.image = 'kaya1jump'
        else:
            self.image = 'kaya1front-1'

        self.x = max(0, min(WIDTH, self.x))

        if self.colliderect(fragment):
            f_xy = random.randint(0, 6)
            fragment.y = fragment_y[f_xy]
            fragment.x = fragment_x[f_xy]
            global score
            score += 10
        
kaya = Kaya(10, 540)

buttons = [
    {"rect": Rect((230, 350), (360, 50)), "text": "Iniciar Jogo", "action": "start"},
    {"rect": Rect((230, 410), (360, 50)), "text": "Desligar Música", "action": "music"},
    {"rect": Rect((230, 470), (360, 50)), "text": "Sair", "action": "exit"}
]

buttons2 = [{"rect": Rect((230, 470), (360, 50)), "text": "Avançar", "action": "skip"}]

buttons3 = [
    {"rect": Rect((230, 350), (360, 50)), "text": "Jogar Novamente", "action": "menu"},
    {"rect": Rect((230, 410), (360, 50)), "text": "Sair", "action": "exit"}
]

background_frames = [map10, map11, map12]
current_frame = 0
animation_speed = 0.6 
last_update = 0

def plataform_mover():
    global floor913_x, floor912_x, floor912_left, floor913_left

    if floor912_left:
        floor912_x += 1
        if floor912_x >= 180:
            floor912_left = False
    else:
        floor912_x -= 1
        if floor912_x <= 100:
            floor912_left = True

    if floor913_left:
        floor913_x += 1
        if floor913_x >= 280:
            floor913_left = False
    else:
        floor913_x -= 1
        if floor913_x <= 200:
            floor913_left = True

def collidecheck():
    for plataforma in plataforms:
        if kaya.colliderect(plataforma):
            if kaya.y <= plataforma.y:
                return True
    return False

def update():
    global time_counter, current_frame, last_update, screens, game_over, music_on, score

    if screens == 3:

        if not dexters: 
            create_dexters()
            
        if not game_over:
 
            kaya.update()  

            for dexter in dexters:
                dexter.move()
                if kaya.colliderect(dexter):
                    game_over = True
                    screens = 4
                    score = 0
                    music.stop()
                    if music_on % 2 == 1:
                        music.stop()
                        music_on += 1
                    else:
                        music.play("gameover")
                        music_on += 1
                    
    
    time_counter += 0.07 
    menu.y = 200 + 10 * math.sin(time_counter)
    drawgame()

    if time_counter - last_update > animation_speed:
        current_frame = (current_frame + 1) % len(background_frames)
        last_update = time_counter
    plataform_mover()

def draw():
    screen.clear()
    if score >= 200:
        endoflevel1()
    else:
        drawgame()

def drawgame():
    global screens

    if screens == 1:
        screen.fill((0, 0, 24))
        menu.draw()
        screen.draw.text(
                "Blade of Albaia",
                center=(WIDTH//2, 50),
                fontsize=50,
                gcolor="#371756", owidth=1.5, ocolor=(0,0,0), 
                fontname="pressstart2pregular", 
                color=(159, 2, 255)
            )
        for btn in buttons:
            screen.draw.filled_rect(btn["rect"], (0, 2, 26))
            screen.draw.text(
                btn["text"],
                center=btn["rect"].center,
                owidth=1.5, ocolor=(0,0,0),
                fontname="pressstart2pregular", 
                color=(159, 2, 255)
            )
        
    elif screens == 2:
        screen.fill((0, 0, 24))
        screen.draw.text(
            "Introdução",
            center=(WIDTH // 2, 50),
            fontsize=20,
            gcolor="#371756", owidth=1.5, ocolor=(0,0,0), 
            fontname="pressstart2pregular", 
            color=(159, 2, 255)
        )
        screen.draw.text(
            "Bem-vindo(a) ao mundo de Albaia! \n Você é Kaya, uma heroína destinada a \n salvar Albaia do reino de trevas de Dexter.\n\n",
            center=(WIDTH // 2, 150),
            fontsize=12,
            owidth=1.5, ocolor=(0,0,0),
            fontname="pressstart2pregular", 
            color=(159, 2, 255)
        )
        screen.draw.text(
            "Para cumprir seu destino, você deve coletar os \n Fragmentos da Lâmina Sagrada, pedaços da lendária \n 'Lâmina de Albaia' que foi quebrada e espalhada pelo map. \n Ao coletá-los, Kaya recupera seu poder e poderá derrotar \n Dexter para restaurar a luz no reino!",
            center=(WIDTH // 2, 200),
            fontsize=12,
            owidth=1.5, ocolor=(0,0,0),
            fontname="pressstart2pregular", 
            color=(159, 2, 255)
        )
        screen.draw.text(
            "Controles:",
            center=(WIDTH // 2, 280),
            fontsize=18,
            owidth=1.5, ocolor=(0,0,0),
            fontname="pressstart2pregular", 
            color=(159, 2, 255)
        )
        screen.draw.text(
            "setas do teclado para mover e pular",
            center=(WIDTH // 2, 300),
            fontsize=15,
            owidth=1.5, ocolor=(0,0,0),
            fontname="pressstart2pregular", 
            color=(159, 2, 255)
        )
        for btn in buttons2:
            screen.draw.filled_rect(btn["rect"], (0, 2, 26))
            screen.draw.text(
                btn["text"],
                center=btn["rect"].center,
                owidth=1.5, ocolor=(0,0,0),
                fontname="pressstart2pregular", 
                color=(159, 2, 255)
            )
    elif screens == 3:
        background_frames[current_frame].draw()
        
        screen.draw.text(
            "Pontuação: " + str(score),
            center=(WIDTH // 2, 50),
            fontsize=20,
            owidth=1.5, ocolor=(0,0,0),
            fontname="pressstart2pregular", 
            color=(159, 2, 255)
        )
        fragment.draw()
        floor12.x = floor912_x
        floor13.x = floor913_x

        for plataforma in plataforms:
            plataforma.draw()

        kaya.draw()  
        for dexter in dexters:
            dexter.draw()
    elif screens == 4:  
        screen.fill((17, 7, 12))
        gameoverr.draw()
        screen.draw.text(
            "Game Over",
            center=(WIDTH//2, 200),
            fontsize=50,
            color=(255, 0, 0)
        )
        for btn in buttons3:
            screen.draw.filled_rect(btn["rect"], (0, 2, 26))
            screen.draw.text(
                btn["text"],
                center=btn["rect"].center,
                owidth=1.5, ocolor=(0,0,0),
                fontname="pressstart2pregular", 
                color=(159, 2, 255)
            )      
        

def on_mouse_down(pos):
    global music_on, screens, game_over, dexters
    
    if screens == 4: 
        for btn in buttons3:
            if btn["rect"].collidepoint(pos):
                if btn["action"] == "menu":
                    screens = 1
                    game_over = False
                    dexters = []  
                    kaya.x = 0
                    kaya.y = 540
                    
                    score = 0
                elif btn["action"] == "exit":
                    quit()
    if screens == 1:
        for btn in buttons:
            if btn["rect"].collidepoint(pos):
                if btn["action"] == "start":
                    music.stop()
                    screens = 2
                elif btn["action"] == "music":
                    if music_on % 2 == 1:
                        music.play("musicamenu")
                        music_on += 1
                    else:
                        music.stop()
                        music_on += 1
                elif btn["action"] == "exit":
                    quit()
    elif screens == 2:
        for btn in buttons2:
            if btn["rect"].collidepoint(pos):
                if btn["action"] == "skip":
                    screens = 3 
                    if music_on % 2 == 0:
                        music.play("musicajogo")
                    else:
                        music.stop()

music.play("musicamenu")
pgzrun.go()