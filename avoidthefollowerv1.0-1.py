from typing import Tuple
import pygame, os, pygame.freetype, math, threading
from random import randint as ri
pygame.init()


WIN_SIZE = (1500, 700)
WIN = pygame.display.set_mode(WIN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption('Avoid the Follower')
pygame.display.set_icon(pygame.image.load(os.path.join('assets','icon.png')))
FPS = 60

SLOWER_CUBE_DURATION = 5 # in seconds
STOP_MOUSE_DURATION = 1
CSIZE = 50
FOLLOW_SPEED = 5
MYSTERY_BOX_CHANCE = 500



CUBEIMAGE = pygame.image.load(os.path.join('assets', 'cube.png'))
CUBEIMAGE = pygame.transform.scale(CUBEIMAGE, (CSIZE,CSIZE))




start_time = 0
passed_time = 0
TIME_STARTED = False
MYSTERY_BOXES = []
ise_start = 0
ise_end = 0
ise_STARTED = False

STOP_MOUSE = False
MYSTERYIMAGE = pygame.image.load(os.path.join('assets','mystery_box.png'))
MYSTERYIMAGE = pygame.transform.scale(MYSTERYIMAGE, (70,25))
def follow_cursor(cube_position: pygame.Rect):
    try:
        mousex, mousey = pygame.mouse.get_pos()
        ocdx = mousex - cube_position.x + (CSIZE // 2 * -1)
        ocdy = mousey - cube_position.y + (CSIZE // 2 * -1)
        distance = math.sqrt(ocdx*ocdx + ocdy*ocdy)
        ocdx /= distance
        ocdy /= distance
        ocdx *= FOLLOW_SPEED
        ocdy *= FOLLOW_SPEED
        cube_position.x += ocdx
        cube_position.y += ocdy
    except ZeroDivisionError:
        pass
def wall_collision(pos: pygame.Rect):
    if pos.x+CSIZE > WIN.get_width():
        pos.x = WIN.get_width()
    if pos.x < 0:
        pos.x=0
    if pos.y < 0:
        pos.y=0
    if pos.y+CSIZE > WIN.get_height():
        pos.y = WIN.get_height()
FONT = pygame.freetype.SysFont('Comic Sans MS', 30)
def generate_mystery_box():
    mysteryBoxRect = MYSTERYIMAGE.get_rect(center=(
        ri(50, WIN.get_width()),
        ri(50, WIN.get_height())
    ))
    MYSTERY_BOXES.append(mysteryBoxRect)
def reset_speed_event():
    global FOLLOW_SPEED
    FOLLOW_SPEED = 5




def unstop_mouse_event():
    global STOP_MOUSE, GOT_CURRENT_MOUSE_POS
    STOP_MOUSE = False
    pygame.event.set_allowed(pygame.MOUSEMOTION)
    pygame.event.set_grab(False)
    GOT_CURRENT_MOUSE_POS = False
    #print('allowing mouse')
def mystery_box_award():
    global FOLLOW_SPEED, STOP_MOUSE
    num = ri(1,2)
    if num == 1:
        # Slower cube
        FOLLOW_SPEED = 2
        threading.Timer(SLOWER_CUBE_DURATION, reset_speed_event).start()
    elif num == 2:
        # Stop mouse
        #print('stoping mouse')
        STOP_MOUSE = True
        threading.Timer(STOP_MOUSE_DURATION, unstop_mouse_event).start()

def handle_box():
    for boxrect in MYSTERY_BOXES:
        if boxrect.collidepoint(pygame.mouse.get_pos()):
            MYSTERY_BOXES.remove(boxrect)
            mystery_box_award()
def draw(cubefollow: pygame.Rect, time):
    global TIME_STARTED, start_time
    WIN.fill((230,230,230))
    WIN.blit(CUBEIMAGE, cubefollow)

    for boxrect in MYSTERY_BOXES:
        WIN.blit(MYSTERYIMAGE, boxrect)

    timefonthaha,_ = FONT.render(str(time/1000)+' second(s)')
    WIN.blit( timefonthaha, timefonthaha.get_rect(center=(WIN.get_width() //2,30)))
    if not TIME_STARTED:
        TIME_STARTED = True
        start_time = pygame.time.get_ticks()
    pygame.display.update()
clock = pygame.time.Clock()
GOT_CURRENT_MOUSE_POS = False
currentmousepos = ()
def main():
    global passed_time, TIME_STARTED, STOP_MOUSE, currentmousepos, GOT_CURRENT_MOUSE_POS
    cubefollow = CUBEIMAGE.get_rect(center=(WIN.get_width() //2,WIN.get_height() //2))
    run = True
    while run:
        clock.tick(FPS)
        if STOP_MOUSE:
            if not GOT_CURRENT_MOUSE_POS:
                currentmousepos = pygame.mouse.get_pos()
                GOT_CURRENT_MOUSE_POS = True
            pygame.event.set_blocked(pygame.MOUSEMOTION)
            pygame.mouse.set_pos(currentmousepos)
            pygame.event.set_grab(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Emergency Exit :)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        if TIME_STARTED:
            passed_time = pygame.time.get_ticks() - start_time
        draw(cubefollow, passed_time)

        if ri(1,MYSTERY_BOX_CHANCE) == MYSTERY_BOX_CHANCE:
            #print('spawned')
            generate_mystery_box()
        
        handle_box()
        wall_collision(cubefollow)
        follow_cursor(cubefollow)
        if cubefollow.collidepoint(pygame.mouse.get_pos()):
            if TIME_STARTED:
                TIME_STARTED = False
                run = False
                dead(passed_time/1000)  
    pygame.quit()
def dead(time_finish):
    unstop_mouse_event()
    dietext,_ = FONT.render(f'You died in {str(time_finish)} seconds')
    spacebartext,_ = FONT.render('Press spacebar to restart')
    run = True
    try:
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
                # Emergency Exit :)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
            keyspressed = pygame.key.get_pressed()
            if keyspressed[pygame.K_SPACE]:
                run = False
                main()
            WIN.fill((230,230,230))
            WIN.blit(dietext, dietext.get_rect(center=(WIN.get_width()//2, WIN.get_height()//2)))
            WIN.blit(spacebartext, spacebartext.get_rect(center=( WIN.get_width()//2, WIN.get_height()//2 + 40 )))
            pygame.display.update()
    except pygame.error:
        pass
    pygame.quit()
if __name__ == '__main__':
    main()