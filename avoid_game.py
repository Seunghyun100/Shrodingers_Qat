# Shrodinger's Qat game

import pygame
import random

# Initialization
pygame.init()
score = 0

#FPS
clock = pygame.time.Clock()

#화면 크기 설정
screenWidth = 1000 # 가로크기
screenHeight = 700 # 세로크기
screen = pygame.display.set_mode((screenWidth,screenHeight))  #가로, 세로


# 배경 이미지
background = pygame.image.load("./resource/background.jpeg")
background = pygame.transform.scale(background, (screenWidth, screenHeight))

# 캐릭터
character = pygame.image.load("./resource/cat.png")
character = pygame.transform.scale(character, (50, 50))
characterWidth, characterHeight = character.get_rect().size  # img 크기 불러옴

# 캐릭터 위치
characterXpos = (screenWidth / 2) - (characterWidth / 2)
characterYpos = screenHeight - characterHeight

# 이동할 좌표
toX, toY = 0,0

# 이동속도
characterSpeed = 0.6

# 난수 생성: 똥 생성용
randomNumber = 30
poSpeed = 10

# 적
enemy = pygame.image.load("./resource/pika.png")
enemySize = enemy.get_rect().size
enemyWidth = enemySize[0]
enemyHeight = enemySize[1]
enemyXpos = 200
enemyYpos = 100

# 타이틀
pygame.display.set_caption("Shrodinger's Qat")

# 폰트 정의
game_font = pygame.font.Font(None,40) #폰트, 크기

# 전체 플레이 시간
totalTime = 0
startTicks = pygame.time.get_ticks()

# Event
running = True
while running:  #실행창
    dt = clock.tick(20)
    #print("fps: " + str(clock.get_fps()))
    screen.fill((0,0,0))
    
    #캐릭터가 1초 100만큼 이동:
    #10FPs : 1초동안 10번 작동 -> 10만큼~~~ 100
    #20FPs : 1초동안 20번 작동 -> 5만큼~~~ 100
    
    # 어떤 이벤트가 발생했는지에 따라 좌표의 변경 정도 결정
    for event in pygame.event.get():

        # 창을 닫으면
        if event.type == pygame.QUIT:
            running = False
        
        # 키를 누른 순간에
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: # 왼쪽 화살표 키
                toX -= characterSpeed
            if event.key == pygame.K_RIGHT: # 오른쪽 화살표 키
                toX += characterSpeed
        
        # 키를 떼는 순간에
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: # 왼쪽 화살표 키
                toX = 0
            elif event.key == pygame.K_UP or event.key == pygame.K_DOWN: # 오른쪽 화살표 키
                toY = 0
    
    # 캐릭터 좌표를 업데이트
    characterXpos += toX * dt
    characterYpos += toY * dt
    
    # 캐릭터가 화면 밖으로 빠져나가지 않게 조정
    if characterXpos < 0:
        characterXpos = 0
    elif characterXpos > screenWidth - characterWidth:
        characterXpos = screenWidth - characterWidth

    if characterYpos < 0:
        characterYpos = 0
    elif characterYpos > screenHeight - characterHeight:
        characterYpos = screenHeight - characterHeight
    
    randomNumberx = random.randrange(0, screenWidth-enemyWidth)
    
    # 적의 세로 위치 조정
    if enemyYpos > screenHeight - enemyHeight:
        enemyYpos = 0
        enemyXpos = randomNumberx
        score += 1
        poSpeed += 2
    enemyYpos += poSpeed

    # 충돌 판정
    characterRect = character.get_rect() # 캐릭터 판정 위치
    characterRect.left = characterXpos
    characterRect.top = characterYpos
    
    enemyRect = enemy.get_rect() # 적 판정 위치
    enemyRect.left = enemyXpos
    enemyRect.top = enemyYpos
    
    if characterRect.colliderect(enemyRect):
        print("Collision")
        running = False
            
    #타이머
    elapsedTime = (pygame.time.get_ticks()) / 1000 # 경과시간이 ms 이므로 초단위로 표시
    # if totalTime - elapsedTime < 0:
    #     print("시간초과")
    #     running = False
    timer = game_font.render("timer : %s"%str(int(totalTime + elapsedTime)), True, (255,255,255))
    
    # 출력할 글자, 색상
    score_s = game_font.render("score : %s"%str(score), True, (255,255,255))
    
    # 전체 그래픽 출력
    screen.fill((0,0,255))
    screen.blit(background, (0,0)) 
    screen.blit(character, (characterXpos , characterYpos))
    screen.blit(enemy, (enemyXpos , enemyYpos))
    screen.blit(timer, (10,10))
    screen.blit(score_s, (10,30))
    
    pygame.display.update() #화면 새로고침

pygame.quit() #pygame 종료