import pgzrun
import math

WIDTH = 800
HEIGHT = 580

menu = Actor('albaiaquestmenu', (405, 200))
time = 0
music_on = 0
telas = 1
score = 0

buttons = [
    {"rect": Rect((230, 350), (360, 50)), "text": "Iniciar Jogo", "action": "start"},
    {"rect": Rect((230, 410), (360, 50)), "text": "Desligar Música", "action": "music"},
    {"rect": Rect((230, 470), (360, 50)), "text": "Sair", "action": "exit"}
]
buttons2 = [{"rect": Rect((230, 470), (360, 50)), "text": "Avançar", "action": "skip"}]
def update():
    global time
    time += 0.07 
    menu.y = 200 + 10 * math.sin(time)
    drawgame()

def draw():
    screen.clear()
    if score >= 200:
        endoflevel1()
    else:
        drawgame()
    """
    screen.draw.text(
        "Best: {}".format(storage['highscore']),
        color=(200, 170, 0),
        midbottom=(WIDTH // 2, HEIGHT - 10),
        fontsize=30,
        fontname="pressstart2pregular",
        shadow=(1, 1)
    ) """
def drawgame():
    global telas

    if telas == 1:
        screen.fill((0, 0, 24))
        menu.draw()
        screen.draw.text(
                "Blade of Albaia",
                center= (WIDTH// 2, 50),
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
    elif telas == 2:
        screen.fill((0, 0, 24))
        screen.draw.text(
                #"No reino flutuante de Albaia, onde ilhas suspensas são conectadas por pontes\n de cristal e ruínas ancestrais escondem segredos de deuses adormecidos,\n"  +
                #" Kaya nasceu sob o signo da Flecha Celeste, uma profecia que a marcou como protetora do equilíbrio. Sua espada de ponta flechada, Alvorada de Ébano, foi forjada com fragmentos de um meteorito que caiu sobre Albaia, capaz de cortar até mesmo as sombras.\n Suas adagas gêmeas, Lâmina do Crepúsculo e Espinho da Aurora, são heranças de uma ordem de guerreiras extinta, e sua capa vermelha é tingida com o pigmento de flores que só crescem nos picos mais altos do reino.",
                "Introdução",
                center= (WIDTH// 2, HEIGHT//2),
                fontsize=10, 
                fontname="pressstart2pregular", 
                color=(159, 2, 255)
            )
        for btn in buttons:
        if btn["rect"].collidepoint(pos):
            if btn["action"] == "start":
                music.stop()
                telas = 2
                
            elif btn["action"] == "music":
                
                if music_on % 2 == 1:
                    music.play("musicamenu")
                    music_on += 1
                else:
                    music.stop()
                    music_on += 1
                
            elif btn["action"] == "exit":
                quit()
    
def on_mouse_down(pos):
    global music_on,telas
    
    for btn in buttons:
        if btn["rect"].collidepoint(pos):
            if btn["action"] == "start":
                music.stop()
                telas = 2
                
            elif btn["action"] == "music":
                
                if music_on % 2 == 1:
                    music.play("musicamenu")
                    music_on += 1
                else:
                    music.stop()
                    music_on += 1
                
            elif btn["action"] == "exit":
                quit()

music.play("musicamenu")

pgzrun.go()