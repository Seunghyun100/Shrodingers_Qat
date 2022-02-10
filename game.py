from xmlrpc.client import Boolean
import pygame
import random
import time
from qiskit import QuantumCircuit, Aer
from qiskit.visualization import plot_bloch_multivector
import os
import matplotlib.pyplot as plt
import numpy as np
from scipy import rand

from animation.cat import Cat

SCREEN_WIDTH = 1000 # 가로크기
SCREEN_HEIGHT = 800 # 세로크기

GATE_WIDTH = 50
GATE_HEIGHT = 50

CAT_WIDTH = 120
CAT_HEIGHT = 120

STATE_WIDTH = 190
STATE_HEIGHT = 190

TARGET_STATE_WIDTH = 200
TARGET_STATE_HEIGHT = 220

FRAMES_PER_SECOND = 60 # update display upto FRAMES_PER_SECOND times per a second

pygame.init()

bgm = pygame.mixer.Sound("resource/music/Horizon.mp3")

background_title = pygame.transform.scale(
    pygame.image.load("resource/background_images/Title_background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
background_in_game = pygame.transform.scale(
    pygame.image.load("resource/background_images/background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
background_die = pygame.transform.scale(
    pygame.image.load("resource/background_images/Died_background.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

def load_image_from(path, width, height):
    return pygame.transform.scale(pygame.image.load(path), (width, height))

X = load_image_from("resource/gate/xgate.png", GATE_WIDTH, GATE_HEIGHT)
Y = load_image_from("resource/gate/ygate.png", GATE_WIDTH, GATE_HEIGHT)
Z = load_image_from("resource/gate/zgate.png", GATE_WIDTH, GATE_HEIGHT)
H = load_image_from("resource/gate/hgate.png", GATE_WIDTH, GATE_HEIGHT)
S = load_image_from("resource/gate/sgate.png", GATE_WIDTH, GATE_HEIGHT)
S_dagger = load_image_from("resource/gate/sdgate.png", GATE_WIDTH, GATE_HEIGHT)
T = load_image_from("resource/gate/tgate.png", GATE_WIDTH, GATE_HEIGHT)
T_dagger = load_image_from("resource/gate/tdgate.png", GATE_WIDTH, GATE_HEIGHT)
M = load_image_from("resource/gate/measure.png", GATE_WIDTH, GATE_HEIGHT)

all_gates = {
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

all_target_states = {
    "0": load_image_from("resource/target_state/0.png", TARGET_STATE_WIDTH, TARGET_STATE_HEIGHT),
    "1": load_image_from("resource/target_state/1.png", TARGET_STATE_WIDTH, TARGET_STATE_HEIGHT),
    "x-0": load_image_from("resource/target_state/x-0.png", TARGET_STATE_WIDTH, TARGET_STATE_HEIGHT),
    "x-1": load_image_from("resource/target_state/x-1.png", TARGET_STATE_WIDTH, TARGET_STATE_HEIGHT),
    "x-2": load_image_from("resource/target_state/x-2.png", TARGET_STATE_WIDTH, TARGET_STATE_HEIGHT),
    "x-3": load_image_from("resource/target_state/x-3.png", TARGET_STATE_WIDTH, TARGET_STATE_HEIGHT),
    "x+0": load_image_from("resource/target_state/x+0.png", TARGET_STATE_WIDTH, TARGET_STATE_HEIGHT),
    "x+1": load_image_from("resource/target_state/x+1.png", TARGET_STATE_WIDTH, TARGET_STATE_HEIGHT),
    "x+2": load_image_from("resource/target_state/x+2.png", TARGET_STATE_WIDTH, TARGET_STATE_HEIGHT),
    "x+3": load_image_from("resource/target_state/x+3.png", TARGET_STATE_WIDTH, TARGET_STATE_HEIGHT),
    "x0": load_image_from("resource/target_state/x0.png", TARGET_STATE_WIDTH, TARGET_STATE_HEIGHT),
    "x1": load_image_from("resource/target_state/x1.png", TARGET_STATE_WIDTH, TARGET_STATE_HEIGHT),
    "x2": load_image_from("resource/target_state/x2.png", TARGET_STATE_WIDTH, TARGET_STATE_HEIGHT),
    "x3": load_image_from("resource/target_state/x3.png", TARGET_STATE_WIDTH, TARGET_STATE_HEIGHT),
    "x4": load_image_from("resource/target_state/x4.png", TARGET_STATE_WIDTH, TARGET_STATE_HEIGHT),
    "x5": load_image_from("resource/target_state/x5.png", TARGET_STATE_WIDTH, TARGET_STATE_HEIGHT),
    "x6": load_image_from("resource/target_state/x6.png", TARGET_STATE_WIDTH, TARGET_STATE_HEIGHT),
    "x7": load_image_from("resource/target_state/x7.png", TARGET_STATE_WIDTH, TARGET_STATE_HEIGHT),
}

sim = Aer.get_backend("aer_simulator")

moving_sprites = pygame.sprite.Group()
cat = Cat(CAT_WIDTH, CAT_HEIGHT)
moving_sprites.add(cat)

class Game:

    def __init__(self) -> None:
        pygame.display.set_caption("Shrodinger's Qat")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_running = True
        self.is_gaming = True
        self.game_font = pygame.font.Font(None,40)
        self.key_left = False
    
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

    def __prepare_game(self, dead=True):
        self.gate_string = ""
        if dead:
            self.score = 0
            self.start_time = time.time()

        self.catXpos = (SCREEN_WIDTH / 2) - (CAT_WIDTH / 2)
        self.catYpos = SCREEN_HEIGHT - CAT_HEIGHT
        self.catSpeed = 1
        self.catDirection = 0

        self.gate1Xpos = random.randrange(0, int(SCREEN_WIDTH*(0.7933))-GATE_WIDTH) # 게이트 초기 x값
        self.gate1Ypos = 100
        self.gate2Xpos = random.randrange(0, int(SCREEN_WIDTH*(0.7933))-GATE_WIDTH) # 게이트 초기 x값
        self.gate2Ypos = 100

        self.gate_speed = 7
        self.gate_dspeed = 0.1
        self.gate_speed_limit = 10
        self.__new_gate(1) # self.gate1, self.gate1_kind is determined here
        self.__new_gate(2)

        self.qc = QuantumCircuit(1)
        self.qc.h(0)
        self.__update_state()
        
        self.__new_target_state() # self.target_state is determined here


    def play_game(self):

        self.screen.blit(background_in_game, (0,0))
        bgm.play(-1)
        self.is_gaming = True

        while self.is_gaming:

            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.is_running = False
                    return
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.catDirection = -1
                        self.key_left = True
                        cat.attack(self.key_left)
                        
                    if event.key == pygame.K_RIGHT:
                        self.catDirection = +1
                        self.key_left = False
                        cat.attack(self.key_left)

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT and self.key_left: # 왼쪽 화살표 키
                        self.catDirection = 0
                        cat.keyup()
                    if event.key == pygame.K_RIGHT and not self.key_left:
                        self.catDirection = 0
                        cat.keyup()
            
            # cat's info update
            self.__cat_position_info_update()
            
            # gate's info update
            self.__gate_position_info_update()

            # check collision
            self.__check_collision()
            
            # total graphic update
            self.__graphic_update()
    
    def __cat_position_info_update(self):
        self.catXpos += self.catDirection * self.clock.tick(FRAMES_PER_SECOND) * self.catSpeed
        if self.catXpos < 0: # 캐릭터가 화면 밖으로 빠져나가지 않게 조정
            self.catXpos = 0
        elif self.catXpos > int(SCREEN_WIDTH*(0.7933)) - CAT_WIDTH:
            self.catXpos = int(SCREEN_WIDTH*(0.7933)) - CAT_WIDTH  

    def __gate_position_info_update(self):
        self.gate1Ypos += self.gate_speed
        self.gate2Ypos += self.gate_speed
        if self.gate1Ypos > SCREEN_HEIGHT - GATE_HEIGHT: # 게이트가 화면 밖으로 빠져나가지 않게 조정
            self.__new_gate(1)
        if self.gate2Ypos > SCREEN_HEIGHT - GATE_HEIGHT: # 게이트가 화면 밖으로 빠져나가지 않게 조정
            self.__new_gate(2)
    
    def __check_collision(self):
        catRect = cat.rect # 캐릭터 판정 위치
        catRect.left = self.catXpos
        catRect.top = self.catYpos
        
        gateRect1 = self.gate1.get_rect() # 게이트 판정 위치
        gateRect1.left = self.gate1Xpos
        gateRect1.top = self.gate1Ypos

        gateRect2 = self.gate2.get_rect() # 게이트 판정 위치
        gateRect2.left = self.gate2Xpos
        gateRect2.top = self.gate2Ypos

        if catRect.colliderect(gateRect1): # 충돌이 일어났다면
        
            if self.gate1_kind == "M":
                self.is_gaming = False
                self.__new_gate(1)
            
            else:                    
                self.gate_string = self.gate_string + " " + self.gate1_kind
                self.__update_state(1) # update bloch sphere picture
                self.__new_gate(1)
                
                # <- if self.state_kind == self.target_state_kind
                # score up
                # make new_target_state

        if catRect.colliderect(gateRect2): # 충돌이 일어났다면
        
            if self.gate2_kind == "M":
                self.is_gaming = False
                self.__new_gate(2)
            
            else:                    
                self.gate_string = self.gate_string + " " + self.gate2_kind
                self.__update_state(2) # update bloch sphere picture
                self.__new_gate(2)


    def __new_gate(self, gate_num):
        
        if gate_num == 1:
            self.gate1_kind, self.gate1 = random.choice(list(all_gates.items())) # (다음번 떨어질 게이트 정하기)
            self.gate1Xpos = random.randrange(0, int(SCREEN_WIDTH*0.7933)-GATE_WIDTH) # (새로운 게이트 위치 설정)
            self.gate1Ypos = 100

        if gate_num == 2:
            self.gate2_kind, self.gate2 = random.choice(list(all_gates.items()))
            self.gate2Xpos = random.randrange(0, int(SCREEN_WIDTH*0.7933)-GATE_WIDTH)
            self.gate2Ypos = 100
        
        # (게이트 점수 업데이트)
        self.score += 1
        if self.gate_speed < self.gate_speed_limit:
            self.gate_speed += self.gate_dspeed
    
    def __update_state(self, gate_num=None):

        if gate_num == 1:
            if self.gate1_kind == "X":
                self.qc.x(0)
            if self.gate1_kind == "Y":
                self.qc.y(0)
            if self.gate1_kind == "Z":
                self.qc.z(0)
            if self.gate1_kind == "H":
                self.qc.h(0)
            if self.gate1_kind == "S":
                self.qc.s(0)
            if self.gate1_kind == "T":
                self.qc.t(0)
            if self.gate1_kind == "S+":
                self.qc.sdg(0)
            if self.gate1_kind == "T+":
                self.qc.tdg(0)
        
        if gate_num == 2:
            if self.gate2_kind == "X":
                self.qc.x(0)
            if self.gate2_kind == "Y":
                self.qc.y(0)
            if self.gate2_kind == "Z":
                self.qc.z(0)
            if self.gate2_kind == "H":
                self.qc.h(0)
            if self.gate2_kind == "S":
                self.qc.s(0)
            if self.gate2_kind == "T":
                self.qc.t(0)
            if self.gate2_kind == "S+":
                self.qc.sdg(0)
            if self.gate2_kind == "T+":
                self.qc.tdg(0)

        # print(self.gate_string)
        # print(self.qc)
        # print(self.gate1_kind, self.gate2_kind)
        qc_init = self.qc.copy()
        qc_init.save_statevector()
        statevector = sim.run(qc_init).result().get_statevector()

        self.live_prob = np.absolute(statevector[0])**2

        if not os.path.exists("./temp"):
            os.mkdir("./temp")

        plot_bloch_multivector(statevector)
        plt.savefig("./temp/statevector.png")
        plt.cla()
        self.state = pygame.transform.scale(pygame.image.load("./temp/statevector.png"), (STATE_WIDTH, STATE_HEIGHT))

    def __new_target_state(self):
        self.target_state_kind, self.target_state = random.choice(list(all_target_states.items()))
    
    def __graphic_update(self):
        time_text = self.game_font.render(f"time : {str(int(time.time() - self.start_time))} sec", True, (0,0,0)) #타이머 표시
        score_text = self.game_font.render(f"score : {str(self.score)}", True, (0,0,0))
        eat_gate_text = self.game_font.render(f"Gates you got : {str(self.gate_string)}", True, (0,0,0))

        self.screen.fill((0,0,255)) # clear all
        self.screen.blit(background_in_game, (0,0))
        moving_sprites.draw(self.screen)
        moving_sprites.update(0.25)
        self.screen.blit(self.gate1, (self.gate1Xpos , self.gate1Ypos))
        self.screen.blit(self.gate2, (self.gate2Xpos , self.gate2Ypos))
        self.screen.blit(time_text, (10,10))
        self.screen.blit(score_text, (10,30))
        self.screen.blit(eat_gate_text, (10, 50))
        self.screen.blit(self.state, (800,0))
        self.screen.blit(self.target_state, (800,300))
        
        pygame.display.update()

    def measure(self):

        bgm.stop()
        self.screen.blit(background_die, (0,0))

        measure_pic = []

        measure_pic.append(pygame.transform.scale(pygame.image.load("resource/cat_measure/measure_live.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)))
        measure_pic.append(pygame.transform.scale(pygame.image.load("resource/cat_measure/measure_die.png"), (SCREEN_WIDTH, SCREEN_HEIGHT)))
        alive = pygame.transform.scale(pygame.image.load("resource/cat_measure/alive.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
        dead = pygame.transform.scale(pygame.image.load("resource/cat_measure/dead.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))

        is_while_break = False
        while self.is_running:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    self.is_running = False
                    return

                if event.type == pygame.KEYDOWN:
                    is_while_break = True
            
            if is_while_break:
                break

            self.screen.blit(measure_pic[random.randint(0,1)], (0,0))
            pygame.display.update()
            self.clock.tick(FRAMES_PER_SECOND)
        
        judge = random.random()
        if self.live_prob >= judge:
            self.screen.blit(alive, (0,0))
            pygame.display.update()
            time.sleep(1)
            self.__prepare_game(dead=False)
        else:
            self.screen.blit(dead, (0,0))
            pygame.display.update()
            time.sleep(1)
            self.__prepare_game(dead=True)
        
    


        
        


def main():
    g = Game()
    g.show_title()
    while g.is_running:
        g.play_game()
        g.measure()
    pygame.quit()


if __name__ == "__main__":
    main()