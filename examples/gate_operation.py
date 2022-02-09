import numpy as np
import pygame
import matplotlib.pyplot as plt
from qiskit.visualization import plot_bloch_vector

from examples.blochsphere_plot import *

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
BACKGROUND_COLOR = (255, 255, 255)
FRAMES_PER_SECOND = 60 # update display upto FRAMES_PER_SECOND times per a second

def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("pygame window title")
    clock = pygame.time.Clock()
    # font = pygame.font.SysFont("Arial", 20)

    playing = True
    gate_str = ""

    print("press x, y, z, h, s, t to make gate operation")

    while playing:

        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                playing = False
            
            if event.type == pygame.KEYUP:

                if event.key == pygame.K_x:
                    gate_str += 'X'
                    print("x pressed", gate_str)
                if event.key == pygame.K_y:
                    gate_str += 'Y'
                    print("y pressed", gate_str)
                if event.key == pygame.K_z:
                    gate_str += 'Z'
                    print("z pressed", gate_str)
                if event.key == pygame.K_h:
                    gate_str += 'H'
                    print("h pressed", gate_str)
                if event.key == pygame.K_s:
                    gate_str += 'S'
                    print("s pressed", gate_str)
                if event.key == pygame.K_t:
                    gate_str += 'T'
                    print("t pressed", gate_str)

            # keys_pressed = pygame.key.get_pressed()
            # if keys_pressed[pygame.K_LEFT]:
            #     print("L Pressed")
            # if keys_pressed[pygame.K_RIGHT]:
            #     print("R Pressed")
            
            screen.fill(BACKGROUND_COLOR)

            bloch_sphere = load_bloch_sphere(list(gate_str))
            bloch_sphere = pygame.transform.scale(bloch_sphere, (200,200))
            screen.blit(bloch_sphere, (0,0))
        
        pygame.display.update()
        clock.tick(FRAMES_PER_SECOND)

    pygame.quit()

if __name__ == "__main__":
    main()