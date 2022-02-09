from http.client import GATEWAY_TIMEOUT
import pygame
import random
import time
from qiskit import QuantumCircuit, Aer
from qiskit.visualization import plot_bloch_multivector
import os
import matplotlib.pyplot as plt

SCREEN_WIDTH = 1000 # 가로크기
SCREEN_HEIGHT = 800 # 세로크기

CAT_WIDTH = 150
CAT_HEIGHT = 150

GATE_WIDTH = 150
GATE_HEIGHT = 150

STATE_WIDTH = 250
STATE_HEIGHT = 250

FRAMES_PER_SECOND = 60 # update display upto FRAMES_PER_SECOND times per a second

pygame.init()

bgm = pygame.mixer.Sound("resource/music/Horizon.mp3")

background_title = pygame.transform.scale(
    pygame.image.load("resource/background_images/Title_background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
background_in_game = pygame.transform.scale(
    pygame.image.load("resource/background_images/background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
background_die = pygame.transform.scale(
    pygame.image.load("resource/background_images/Died_background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

def create_gate(path):
    return pygame.transform.scale(pygame.image.load(path), (GATE_WIDTH, GATE_HEIGHT))

X = create_gate("resource/gate/xgate.png")
Y = create_gate("resource/gate/ygate.png")
Z = create_gate("resource/gate/zgate.png")
H = create_gate("resource/gate/hgate.png")
S = create_gate("resource/gate/sgate.png")
S_dagger = create_gate("resource/gate/sdgate.png")
T = create_gate("resource/gate/tgate.png")
T_dagger = create_gate("resource/gate/tdgate.png")
M = create_gate("resource/gate/measure.png")

gates = {
    "X": X,
    "Y": Y,
    "Z": Z,
    "H": H,
    "S": S,
    "S+": S_dagger,
    "T": T,
    "T+": T_dagger,
    "M": M
    }

sim = Aer.get_backend("aer_simulator")

class Cat(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.attack_animation = False
        self.key_left = True
        self.sprites = []
        self.sprites.append(pygame.transform.scale(pygame.image.load("resource/cat_layers/cat_walk_left.png"), (CAT_WIDTH, CAT_HEIGHT)))
        self.sprites.append(pygame.transform.scale(pygame.image.load("resource/cat_layers/cat_stand_left.png"), (CAT_WIDTH, CAT_HEIGHT)))
        self.sprites.append(pygame.transform.scale(pygame.image.load("resource/cat_layers/cat_walk_right.png"), (CAT_WIDTH, CAT_HEIGHT)))
        self.sprites.append(pygame.transform.scale(pygame.image.load("resource/cat_layers/cat_stand_right.png"), (CAT_WIDTH, CAT_HEIGHT)))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def attack(self, key_left):
        self.attack_animation = True
        self.key_left = key_left
        if key_left == False:
            self.current_sprite = 2

    def keyup(self):
        self.attack_animation = False

    def update(self,speed):
        if self.attack_animation == True:
            if self.key_left == True:
                self.current_sprite += speed
                if int(self.current_sprite) >= len(self.sprites)/2:
                    self.current_sprite = 0

            if self.key_left == False:
                self.current_sprite += speed
                if int(self.current_sprite) >= len(self.sprites):
                    self.current_sprite = 2

        self.image = self.sprites[int(self.current_sprite)]

moving_sprites = pygame.sprite.Group()
cat = Cat(100,100)
moving_sprites.add(cat)

class Game:

    def __init__(self) -> None:
        pygame.display.set_caption("Shrodinger's Qat")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.is_alive = True
        self.game_font = pygame.font.Font(None,40)
    
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

    def __prepare_game(self):
        self.gate_string = ""
        self.score = 0
        self.start_time = time.time()

        self.catXpos = (SCREEN_WIDTH / 2) - (CAT_WIDTH / 2)
        self.catYpos = SCREEN_HEIGHT - CAT_HEIGHT
        self.catSpeed = 1
        self.catDirection = 0

        self.gateXpos = random.randrange(0, int(SCREEN_WIDTH*(0.7933))-GATE_WIDTH) # 게이트 초기 x값
        self.gateYpos = 100
        self.gate_speed = 7
        self.gate_dspeed = 0.1
        self.gate_speed_limit = 10
        self.__new_gate()

        self.qc = QuantumCircuit(1)
        self.qc.h(0)
        self.__new_state()


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
                        cat.attack(True)
                    if event.key == pygame.K_RIGHT:
                        self.catDirection = +1
                        cat.attack(False)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT: # 왼쪽 화살표 키
                        self.catDirection = 0
                        cat.keyup()
            
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
        catRect = cat.rect # 캐릭터 판정 위치
        catRect.left = self.catXpos
        catRect.top = self.catYpos
        
        gateRect = self.gate.get_rect() # 게이트 판정 위치
        gateRect.left = self.gateXpos
        gateRect.top = self.gateYpos

        if catRect.colliderect(gateRect): # 충돌이 일어났다면
        
            if self.gate_kind == "M":
                # <- measure by current state
                self.is_alive = False
            
            else:                    
                self.gate_string = self.gate_string + " " + self.gate_kind
                self.__new_gate()
                self.__new_state() # update bloch sphere picture

    def __new_gate(self):
        # (다음번 떨어질 게이트 정하기)
        self.gate_kind, self.gate = random.choice(list(gates.items()))
            
        # (새로운 게이트 위치 설정)
        self.gateXpos = random.randrange(0, int(SCREEN_WIDTH*0.7933)-GATE_WIDTH)
        self.gateYpos = 100
        
        # (게이트 점수 업데이트)
        self.score += 1
        if self.gate_speed < self.gate_speed_limit:
            self.gate_speed += self.gate_dspeed
    
    def __new_state(self):

        # <- gate update on self.qc

        if not os.path.exists("./temp"):
            os.mkdir("./temp")

        qc_init = self.qc.copy()
        qc_init.save_statevector()
        statevector = sim.run(qc_init).result().get_statevector()

        try:
            self.state = pygame.transform.scale(pygame.image.load(f"./temp/{statevector}.png"), (STATE_WIDTH, STATE_HEIGHT))
        except:
            plot_bloch_multivector(statevector)
            plt.savefig(f"./temp/{statevector}.png")
            plt.cla()
            self.state = pygame.transform.scale(pygame.image.load(f"./temp/{statevector}.png"), (STATE_WIDTH, STATE_HEIGHT))
            # os.remove(f"./temp/{statevector}.png")

    
    def __graphic_update(self):
        time_text = self.game_font.render(f"time : {str(int(time.time() - self.start_time))} sec", True, (0,0,0)) #타이머 표시
        score_text = self.game_font.render(f"score : {str(self.score)}", True, (0,0,0))
        eat_gate_text = self.game_font.render(f"Gates you got : {str(self.gate_string)}", True, (0,0,0))

        self.screen.fill((0,0,255)) # clear all
        self.screen.blit(background_in_game, (0,0))
        # self.screen.blit(cat, (self.catXpos , self.catYpos))
        moving_sprites.draw(self.screen)
        moving_sprites.update(0.25)
        self.screen.blit(self.gate, (self.gateXpos , self.gateYpos))
        self.screen.blit(time_text, (10,10))
        self.screen.blit(score_text, (10,30))
        self.screen.blit(eat_gate_text, (10, 50))
        self.screen.blit(self.state, (750,0))
        
        pygame.display.update()



    def game_over(self):

        bgm.stop()
        self.screen.blit(background_die, (0,0))

        while self.is_running:
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