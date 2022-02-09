import pygame, sys

class Player(pygame.sprite.Sprite):
	def __init__(self, pos_x, pos_y):
		super().__init__()
		self.die_animation = False
		self.sprites = []
		self.sprites.append(pygame.image.load('resource/cat_layers/cat_stand_right.png'))
		self.sprites.append(pygame.image.load('resource/cat_layers/cat_die.png'))
		self.sprites.append(pygame.image.load('resource/cat_layers/cat_live.png'))
		self.current_sprite = 0
		self.image = self.sprites[self.current_sprite]

		self.rect = self.image.get_rect()
		self.rect.topleft = [pos_x,pos_y]


	def if_die(self):
		self.die_animation = True

	def get_result(self,die):
		self.die_animation = False
		if die == True:
			self.current_sprite = 1
		if die == False:
			self.current_sprite = 2

	def update(self,speed):
		if self.die_animation == True:
			self.current_sprite += speed
			if int(self.current_sprite) >= 2:
				self.current_sprite = 0

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
		#TODO : 이벤트 적절하게 수정
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				player.if_die()

			# 살 때
			if event.key == pygame.K_UP:
				player.get_result(True)

			#죽을때
			if event.key == pygame.K_RIGHT:
				player.get_result(False)

	# Drawing
	screen.fill((0,0,0))
	moving_sprites.draw(screen)
	moving_sprites.update(1)
	pygame.display.flip()
	clock.tick(60)