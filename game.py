from http.client import GATEWAY_TIMEOUT
import pygame
import random
import time

SCREEN_WIDTH = 1000 # 가로크기
SCREEN_HEIGHT = 800 # 세로크기

CAT_WIDTH = 150
CAT_HEIGHT = 150

GATE_WIDTH = 150
GATE_HEIGHT = 150

FRAMES_PER_SECOND = 60 # update display upto FRAMES_PER_SECOND times per a second

pygame.init()

bgm = pygame.mixer.Sound("resource/music/Horizon.mp3")

background_title = pygame.transform.scale(
    pygame.image.load("resource/background_images/Title_background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
background_in_game = pygame.transform.scale(
    pygame.image.load("resource/background_images/background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
background_die = pygame.transform.scale(
    pygame.image.load("resource/background_images/Died_background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

cat = pygame.transform.scale(
    pygame.image.load("resource/cat_layers/cat_stand.png"), (CAT_WIDTH, CAT_HEIGHT))




H = pygame.transform.scale(
    pygame.image.load("resource/gate/hgate.png"), (GATE_WIDTH, GATE_HEIGHT))
X = pygame.transform.scale(
    pygame.image.load("resource/gate/xgate.png"), (GATE_WIDTH, GATE_HEIGHT))
M = pygame.transform.scale(
    pygame.image.load("resource/gate/measure.png"), (GATE_WIDTH, GATE_HEIGHT))

gates = {
    "H" : H, "X": X, "M": M
    }




class Game:

    def __init__(self) -> None:
        pygame.display.set_caption("Shrodinger's Qat")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.is_alive = True
        self.game_font = pygame.font.Font(None,40)
    
    def __prepare_game(self):
        self.gate_string = ""
        self.score = 0
        self.start_time = time.time()

        self.catXpos = (SCREEN_WIDTH / 2) - (CAT_WIDTH / 2)
        self.catYpos = SCREEN_HEIGHT - CAT_HEIGHT
        self.catSpeed = 1
        self.catDirection = 0

        self.gateXpos = random.randrange(0, int(SCREEN_WIDTH*(0.7933))-GATE_WIDTH) # 게이트 초기 x값
        self.gateYpos = 0  
        self.gate_speed = 7
        self.gate_dspeed = 0.1
        self.gate_speed_limit = 10
        self.__new_gate()
    
    def show_title(self):
        self.screen.blit(background_title, (0,0))

        while True:
            
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.is_running = False
                    return

                if event.type == pygame.KEYDOWN:
                    self.__prepare_game()
                    return
            
            pygame.display.update()
            self.clock.tick(FRAMES_PER_SECOND)

        
    
    def play_game(self):

        self.screen.blit(background_in_game, (0,0))
        bgm.play(-1)
        self.start_time = time.time()
        self.is_alive = True

        while self.is_alive:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.is_running = False
                    return
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.catDirection = -1
                    if event.key == pygame.K_RIGHT:
                        self.catDirection = +1

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: # 왼쪽 화살표 키
                        self.catDirection = 0
            
            # cat's info update
            self.__cat_info_update()
            
            # gate's info update
            self.__gate_info_update()

            # check collision
            self.__check_collision()
            
            # total graphic update
            self.__graphic_update()
    
    def __cat_info_update(self):
        self.catXpos += self.catDirection * self.clock.tick(FRAMES_PER_SECOND) * self.catSpeed
        if self.catXpos < 0: # 캐릭터가 화면 밖으로 빠져나가지 않게 조정
            self.catXpos = 0
        elif self.catXpos > int(SCREEN_WIDTH*(0.7933)) - CAT_WIDTH:
            self.catXpos = int(SCREEN_WIDTH*(0.7933)) - CAT_WIDTH  

    def __gate_info_update(self):
        self.gateYpos += self.gate_speed
        if self.gateYpos > SCREEN_HEIGHT - GATE_HEIGHT: # 게이트가 화면 밖으로 빠져나가지 않게 조정
            self.__new_gate()
    
    def __check_collision(self):
        catRect = cat.get_rect() # 캐릭터 판정 위치
        catRect.left = self.catXpos
        catRect.top = self.catYpos
        
        gateRect = self.gate.get_rect() # 게이트 판정 위치
        gateRect.left = self.gateXpos
        gateRect.top = self.gateYpos

        if catRect.colliderect(gateRect): # 충돌이 일어났다면
        
            if self.gate_kind == "M":     
                self.is_alive = False
            
            else:                    
                self.gate_string = self.gate_string + " " + self.gate_kind
                self.__new_gate()

    def __new_gate(self):
        # (다음번 떨어질 게이트 정하기)
        self.gate_kind, self.gate = random.choice(list(gates.items()))
            
        # (새로운 게이트 위치 설정)
        self.gateXpos = random.randrange(0, int(SCREEN_WIDTH*0.7933)-GATE_WIDTH)
        self.gateYpos = 0
        
        # (게이트 점수 업데이트)
        self.score += 1
        if self.gate_speed < self.gate_speed_limit:
            self.gate_speed += self.gate_dspeed
    
    def __graphic_update(self):
        time_text = self.game_font.render(f"time : {str(int(time.time() - self.start_time))} sec", True, (0,0,0)) #타이머 표시
        score_text = self.game_font.render(f"score : {str(self.score)}", True, (0,0,0))
        eat_gate_text = self.game_font.render(f"Gates you got : {str(self.gate_string)}", True, (0,0,0))

        self.screen.fill((0,0,255)) # clear all
        self.screen.blit(background_in_game, (0,0))
        self.screen.blit(cat, (self.catXpos , self.catYpos))
        self.screen.blit(self.gate, (self.gateXpos , self.gateYpos))
        self.screen.blit(time_text, (10,10))
        self.screen.blit(score_text, (10,30))
        self.screen.blit(eat_gate_text, (10, 50))
        
        pygame.display.update()


    def game_over(self):
        bgm.stop()
        self.screen.blit(background_die, (0,0))

        while True:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.is_running = False
                    return

                if event.type == pygame.KEYDOWN:
                    self.__prepare_game()
                    return
            
            pygame.display.update()
            self.clock.tick(FRAMES_PER_SECOND)



def main():
    g = Game()
    g.show_title()
    while g.is_running:
        g.play_game()
        g.game_over()
    pygame.quit()


if __name__ == "__main__":
    main()