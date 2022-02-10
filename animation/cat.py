import pygame

class Cat(pygame.sprite.Sprite):
    def __init__(self, CAT_WIDTH, CAT_HEIGHT):
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
        # self.rect.topleft = [pos_x, pos_y]

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
