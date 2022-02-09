import pygame, sys

class Player(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y):
		super().__init__()
		self.attack_animation = False
		self.key_left = True
		self.sprites = []
		self.sprites.append(pygame.image.load('resource/cat_layers/cat_walk_left.png'))
		self.sprites.append(pygame.image.load('resource/cat_layers/cat_stand_left.png'))
		self.sprites.append(pygame.image.load('resource/cat_layers/cat_walk_right.png'))
		self.sprites.append(pygame.image.load('resource/cat_layers/cat_stand_right.png'))
		self.current_sprite = 0
		self.image = self.sprites[self.current_sprite]

		self.rect = self.image.get_rect()
		self.rect.topleft = [pos_x,pos_y]

	def attack(self,key_left):
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

# General setup
pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Sprite Animation")

# Creating the sprites and groups
moving_sprites = pygame.sprite.Group()
player = Player(100,100)
moving_sprites.add(player)

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				player.attack(True)
			if event.key == pygame.K_RIGHT:
				player.attack(False)

		if event.type == pygame.KEYUP:
			player.keyup()

	# Drawing
	screen.fill((0,0,0))
	moving_sprites.draw(screen)
	moving_sprites.update(0.25)
	pygame.display.flip()
	clock.tick(60)