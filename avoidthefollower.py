import pygame, os, math, pygame.freetype
pygame.init()
WIN_SIZE = (1500, 700)
WIN = pygame.display.set_mode(WIN_SIZE, pygame.RESIZABLE)
pygame.display.set_caption('Avoid the Follower')
pygame.display.set_icon(pygame.image.load(os.path.join('assets','icon.png')))
FPS = 60
CSIZE = 50
CUBEIMAGE = pygame.image.load(os.path.join('assets', 'cube.png'))
CUBEIMAGE = pygame.transform.scale(CUBEIMAGE, (CSIZE,CSIZE))
FOLLOW_SPEED = 5
start_time = 0
passed_time = 0
TIME_STARTED = False
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
def draw(cubefollow: pygame.Rect, time):
    global TIME_STARTED, start_time
    WIN.fill((230,230,230))
    WIN.blit(CUBEIMAGE, cubefollow)
    timefonthaha,_ = FONT.render(str(time/1000)+' second(s)')
    WIN.blit( timefonthaha, timefonthaha.get_rect(center=(WIN.get_width() //2,30)))
    if not TIME_STARTED:
        TIME_STARTED = True
        start_time = pygame.time.get_ticks()
    pygame.display.update()
clock = pygame.time.Clock()
def main():
    global passed_time, TIME_STARTED
    cubefollow = CUBEIMAGE.get_rect(center=(WIN.get_width() //2,WIN.get_height() //2))
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        if TIME_STARTED:
            passed_time = pygame.time.get_ticks() - start_time
        draw(cubefollow, passed_time)
        wall_collision(cubefollow)
        follow_cursor(cubefollow)
        if cubefollow.collidepoint(pygame.mouse.get_pos()):
            if TIME_STARTED:
                TIME_STARTED = False
                run = False
                dead(passed_time/1000)  
    pygame.quit()
def dead(time_finish):
    dietext,_ = FONT.render(f'You died in {str(time_finish)} seconds')
    spacebartext,_ = FONT.render('Press spacebar to restart')
    run = True
    try:
        while run:
            clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
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