#Import Modules
import pygame
import pygame.mixer
import random
#Setup the window

pygame.init()
window = pygame.display.set_mode((512, 736))
pygame.display.set_caption('Doing Knightly Things In A Timely Manner')
#Tilemap Object
class Tilemap:
	def __init__(self, path, tiles):
		#put txt file of level into nested list
		with open(path, 'r') as text_file:
			lines = text_file.read().split('\n')
		row = []
		self.level = []
		for line in lines:
			for character in line:
				row.append(int(character))
			self.level.append(row)
			row = []

		self.tiles = tiles
	
	def draw(self, window):
		for y, row in enumerate(self.level):
			for x, tile in enumerate(row):
				if tile > 0:
					window.blit(self.tiles[tile-1], (x*32, y*32))
				
#Enemy Object
class EnemySpawning:
	def __init__(self, level, anim):
		self.level = level
		self.fires = []
		self.timer = 0
		self.wait_time = 1
		self.anim = anim
		self.enemies = []
		for y, row in enumerate(self.level.level):
			for x, tile in enumerate(row):
				if tile == 3:
					self.fires.append((x,y))
		
	def update(self):
		self.timer += 1
		if self.timer % self.wait_time == 0 and len(self.enemies) < 4:
			ex, ey = random.choice(self.fires)
			self.enemies.append(Enemy(ex*32, ey*32, 1, True, self.level, self.anim))
			self.wait_time = random.randint(3,6)*100
		for e in self.enemies:
			e.update()

	def draw(self, window):
		for e in self.enemies:
			e.draw(window)
class BatSpawning:
	def __init__(self, level, anim):
		self.timer = 0
		self.bats = []
		self.level = level
		self.fires = []
		self.anim = anim
		for y, row in enumerate(self.level.level):
			for x, tile in enumerate(row):
				if tile == 3:
					self.fires.append((x*32,y*32))

	def update(self):
		self.timer += 1
		if len(self.bats) < 3 and self.timer % 300 == 0:
			x,y = random.choice(self.fires)
			self.bats.append(Bat(x,y-32,1,self.anim))
			self.timer = 0
		
		for i in self.bats:
			i.update(self.level)

	def draw(self, window):
		for i in self.bats:
			i.draw(window)

class Bat:
	def __init__(self, x, y, health, anim):
		self.x = x
		self.y = y
		self.timer = 0
		self.move = {'Up': False, 'Down':False, 'Left': False, 'Right':False}
		self.still = True
		self.vspd = 4
		self.health = health
		self.anim = anim
		self.frame = 0
		if self.x < 256:
			self.move['Right'] = True
		else:
			self.move['Left'] = True
		if self.y < 352:
			self.move['Up'] = True
		else:
			self.move['Down'] = True

	def update(self, level):
		self.timer += 1
		if self.timer % 10 == 0:
			self.frame += 1
			if self.frame >= 3:
				self.frame = 0
		if self.move['Right'] == True:
			self.x += 1
			if self.x+16 == 512:
				self.move['Right'] = False
				self.move['Left'] = True
			elif level.level[int((self.y)/32)][int((self.x+16)/32)] == 1 or level.level[int((self.y+15)/32)][int((self.x+16)/32)] == 1 or self.x+16 == 512:
				self.move['Right'] = False
				self.move['Left'] = True
		elif self.move['Left'] == True:
			self.x -= 1
			if self.x-1 == 0:
				self.move['Right'] = True
				self.move['Left'] = False
			elif level.level[int((self.y)/32)][int((self.x-1)/32)] == 1 or level.level[int((self.y+15)/32)][int((self.x-1)/32)] == 1 or self.x == 0:
				self.move['Right'] = True
				self.move['Left'] = False
		
		if self.move['Up'] == True:
			self.y -= 1
			if self.y-1 == 0:
				self.move['Up'] = False
				self.move['Down'] = True
			elif level.level[int((self.y-1)/32)][int((self.x)/32)] == 1 or level.level[int((self.y-1)/32)][int((self.x+15)/32)] == 1 or self.y-1 == 0:
				self.move['Up'] = False
				self.move['Down'] = True
		elif self.move['Down'] == True:
			self.y += 1
			if level.level[int((self.y+16)/32)][int((self.x)/32)] == 1 or level.level[int((self.y+16)/32)][int((self.x+15)/32)] == 1 or self.y+16 == 704:
				self.move['Up'] = True
				self.move['Down'] = False


		
		
		
			
	def draw(self, window):
		if self.move['Right'] == True:
			window.blit(self.anim[self.frame], (self.x, self.y))
		else:
			window.blit(pygame.transform.flip(self.anim[self.frame], True, False), (self.x, self.y))

			
class Enemy:
	def __init__(self, x, y, health, rand_move, level, anim):
		self.x = x
		self.y = y
		self.fires = ()
		self.health = health
		self.rand_move = rand_move
		self.move_start = False
		self.move_timer = 0
		self.move = {'Right': False, 'Down': False, 'Up': False, 'Left': False, 'Still':True}
		self.level = level
		self.last = 'Nada'
		self.anim = anim
		self.anim_timer = 0
		self.f = 0
		self.frame = self.anim[0]
		

	def update(self):
		#print('X: ' + str(self.x) + '\nY: ' + str(self.y))
		if self.rand_move == True:
			if self.move_start == True:
				self.move_start = False
				if self.x == 0:
					self.move['Right'] = True
				elif self.x == 480:
					self.move['Left'] = True
				else:
					moves = []
					if self.level.level[int((self.y+32)/32)][int((self.x)/32)] != 0:
						if self.level.level[int((self.y+32)/32)][int((self.x+32)/32)] != 0:
							moves.append('Right')
						if self.level.level[int((self.y+32)/32)][int((self.x-1)/32)] != 0:
							moves.append('Left')
						if self.level.level[int((self.y+32)/32)][int((self.x)/32)] == 2:
							moves.append('Down')
						if self.level.level[int((self.y)/32)][int((self.x)/32)] == 2:
							moves.append('Up')

					if self.last == 'Down':
						moves.remove('Up')
					elif self.last == 'Up':
						moves.remove('Down')
					a = random.choice(moves)
					self.last = a
					self.move[a] = True
					
			else:
				if self.move['Right'] == True or self.move['Left'] == True or self.move['Still'] == True:
					self.move_timer += 1
					self.anim_timer += 1
					if self.anim_timer >= 0 and self.anim_timer < 5:
						self.f = 0
					elif self.anim_timer >= 5 and self.anim_timer < 10:
						self.f = 1
					elif self.anim_timer >= 10 and self.anim_timer < 15:
						self.f = 0
					elif self.anim_timer >= 15 and self.anim_timer < 20:
						self.f = 2
					else:
						self.anim_timer = 0
						self.f = 0
				
						
					if self.move_timer > 32:
						self.move_timer = 0
						if self.move['Still'] == True:
							self.move['Still'] = False
							self.move_start = True
						elif self.move['Still'] == False:
							self.move['Right'] = False
							self.move['Left'] = False
							self.move['Still'] = True
							self.f = 0
					if self.move['Right'] == True and self.level.level[int((self.y)/32)][int((self.x+32)/32)] != 1:
						self.x += 1
						self.frame = self.anim[self.f]
					if self.move['Left'] == True and self.level.level[int((self.y)/32)][int((self.x-1)/32)] != 1:
						self.x -= 1
						self.frame = pygame.transform.flip(self.anim[self.f], True, False)
				elif self.move['Down'] == True:
					self.anim_timer += 1
					if self.anim_timer >= 0 and self.anim_timer < 5:
						self.f = 3
					elif self.anim_timer >= 5 and self.anim_timer < 10:
						self.f = 4
					elif self.anim_timer >= 10 and self.anim_timer < 15:
						self.f = 3
					elif self.anim_timer >= 15 and self.anim_timer < 20:
						self.f = 5
					else:
						self.anim_timer = 0
						self.f = 3
					self.y += 1
					self.frame = self.anim[self.f]
					if self.level.level[int((self.y+32)/32)][int((self.x)/32)] == 1:
						self.move['Down'] = False
						self.move['Still'] = True
				elif self.move['Up'] == True:
					self.anim_timer += 1
					if self.anim_timer >= 0 and self.anim_timer < 5:
						self.f = 3
					elif self.anim_timer >= 5 and self.anim_timer < 10:
						self.f = 4
					elif self.anim_timer >= 10 and self.anim_timer < 15:
						self.f = 3
					elif self.anim_timer >= 15 and self.anim_timer < 20:
						self.f = 5
					else:
						self.anim_timer = 0
						self.f = 3
					self.y -= 1
					self.frame = self.anim[self.f]
					if self.level.level[int((self.y+31)/32)][int((self.x)/32)] == 0:
						self.move['Up'] = False
						self.move['Still'] = True
				else:
						if self.anim_timer >= 0 and self.anim_timer < 5:
							self.f = 3
						elif self.anim_timer >= 5 and self.anim_timer < 10:
							self.f = 4
						elif self.anim_timer >= 10 and self.anim_timer < 15:
							self.f = 3
						elif self.anim_timer >= 15 and self.anim_timer < 20:
							self.f = 5
						else:
							self.anim_timer = 0
							self.f = 3
				


	def draw(self, window):
		window.blit(self.frame, (self.x, self.y))
		
#Arrow Object
class Arrow:
	def __init__(self, facing, x, y):
		self.img_left = pygame.image.load('Assets/Other/Arrow.png').convert_alpha()
		self.img_right = pygame.transform.rotate(self.img_left, 180)
		self.img_up = pygame.transform.rotate(self.img_left, 270)
		self.facing = facing
		if self.facing == 'Left':
			self.x = x-16
			self.y = y+15
		elif self.facing == 'Right':
			self.x = x+31
			self.y = y+15
		elif self.facing == 'Up':
			self.x = x+15
			self.y = y-16
	
	def update(self):
		if self.facing == 'Left':
			self.x -= 4
		elif self.facing == 'Right':
			self.x += 4
		elif self.facing == 'Up':
			self.y -= 4

	def draw(self, window):
		if self.facing == 'Left':
			window.blit(self.img_left, (self.x, self.y))
		elif self.facing == 'Right':
			window.blit(self.img_right, (self.x, self.y))
		if self.facing == 'Up':
			window.blit(self.img_up, (self.x, self.y))
	


#Player Object
class Player:
	def __init__(self, x, y, level, spawning, anim, bats, gui, updates, font):
		#Player Variables
		self.x = x
		self.y = y
		self.onLadder = False
		self.gravity = 2
		self.move = {'Up': False, 'Down': False, 'Left': False, 'Right': False}
		self.facing = 'Left'
		self.old_face = 'Left'
		self.level = level
		self.arrows = []
		self.en_spawning = spawning
		self.anim = anim
		self.img = anim[0]
		self.anim_timer = 0
		self.shoot = False
		self.shoot_timer = 0
		self.bats = bats
		self.gui = gui
		self.inv_timer = 0
		self.updates = updates
		self.score = 0
		self.score_timer = 0
		self.score_coords = [-100,-100]
		self.multiplier = 1
		self.font = font
		self.hurt = pygame.mixer.Sound('sounds/hurt.wav')
		self.shoot_s = pygame.mixer.Sound('sounds/shoot.wav')


	
	def update(self):
		#Player movements
		if self.move['Right'] == True and self.x+33 < 512:
			if self.level.level[int((self.y)/32)][int((self.x+32)/32)] != 1 and self.level.level[int((self.y+31)/32)][int((self.x+32)/32)] != 1 and self.onLadder == False: 
				self.x += 1
			elif self.onLadder == True and self.level.level[int((self.y+31)/32)][int((self.x)/32)] == 0:
				self.onLadder = False
				self.x += 1
			elif self.onLadder == True and self.level.level[int((self.y+31)/32)][int((self.x)/32)] == 2 and self.level.level[int((self.y+32)/32)][int((self.x)/32)] == 1:
				self.onLadder = False
				self.x += 1

		elif self.move['Left'] == True and self.x > 0:
			if self.level.level[int((self.y)/32)][int((self.x-1)/32)] != 1 and self.level.level[int((self.y+31)/32)][int((self.x-1)/32)] != 1 and self.onLadder == False:  
				self.x -= 1
			elif self.onLadder == True and self.level.level[int((self.y+31)/32)][int((self.x)/32)] == 0:
				self.onLadder = False
				self.x -= 1
			elif self.onLadder == True and self.level.level[int((self.y+31)/32)][int((self.x)/32)] == 2 and self.level.level[int((self.y+32)/32)][int((self.x)/32)] == 1:
				self.onLadder = False
				self.x -= 1

		elif self.move['Up'] == True:
			if self.level.level[int((self.y+31)/32)][int((self.x+31)/32)] == 2:
				self.x = int((self.x+31)/32)*32
				self.onLadder = True
				self.y -= 1
			elif self.level.level[int((self.y+31)/32)][int((self.x-1)/32)] == 2:
				self.x = int((self.x-1)/32)*32
				self.onLadder = True
				self.y -= 1
		elif self.move['Down'] == True:
			if self.level.level[int((self.y+32)/32)][int((self.x+31)/32)] == 2:
				self.x = int((self.x+31)/32)*32
				self.onLadder = True
				self.y += 1
			elif self.level.level[int((self.y+32)/32)][int((self.x-1)/32)] == 2:
				self.x = int((self.x-1)/32)*32
				self.onLadder = True
				self.y += 1

		#Gravity {Checks if grass is under player on both sides, then checks if player is on ladder, then checks to see if player is on top of a ladder on both sides}
		if self.level.level[int((self.y+33)/32)][int(self.x/32)] == 1 or self.level.level[int((self.y+33)/32)][int((self.x+31)/32)] == 1 or self.onLadder == True or self.level.level[int((self.y+33)/32)][int(self.x/32)] == 2 and self.level.level[int((self.y+31)/32)][int(self.x/32)] == 0 or self.level.level[int((self.y+33)/32)][int((self.x+31)/32)] == 2 and self.level.level[int((self.y+31)/32)][int((self.x+31)/32)] == 0:
			self.gravity = 0
		else:
			self.gravity = 2

		self.y += self.gravity

		#PLayer Arrows
		for a in self.arrows:
			a.update()
			if a.x+15 <= 0 or a.x >= 512 or a.y+3 <= 0 or a.y >= 704:
				self.arrows.remove(a)
			elif self.level.level[int(a.y/32)][int(a.x/32)] == 1:
				self.arrows.remove(a)
			else:
				for e in self.en_spawning.enemies:
					if a.x >= e.x and a.x <= e.x+31 and a.y >= e.y and a.y <= e.y+31:
						self.arrows.remove(a)
						self.en_spawning.enemies.remove(e)
						if self.score_timer > 0:
							self.multiplier += 1
						self.score_timer = 180
						self.score = 100 * self.multiplier
						self.gui.score += self.score
						self.score_coords = [e.x, e.y]
						break
				for b in self.bats.bats:
					if a.x >= b.x and a.x <= b.x+15 and a.y >= b.y and a.y <= b.y+15:
						self.arrows.remove(a)
						self.bats.bats.remove(b)
						if self.score_timer > 0:
							self.multiplier += 1
						self.score_timer = 180
						self.score = 250 * self.multiplier
						self.gui.score += self.score
						self.score_coords = [b.x, b.y]

		#score
		if self.score_timer > 0:
			self.score_timer -= 1
			if self.score_timer % 5 == 0:
				self.score_coords[1] -= 1
		else:
			self.score_coords = [-100, -100]
			self.multiplier = 1
		#enemy collision
		if self.inv_timer > 0:
			self.inv_timer -= 1
		elif self.inv_timer == 0:
			for i in self.en_spawning.enemies:
				if i.x >= self.x and i.x <= self.x+31 and i.y >= self.y and i.y <= self.y+31:
					self.gui.health -= 1
					self.inv_timer = 270
					pygame.mixer.Sound.play(self.hurt)
				elif i.x+31 >= self.x and i.x+31 <= self.x+31 and i.y >= self.y and i.y <= self.y+31:
					self.gui.health -= 1
					self.inv_timer = 270
					pygame.mixer.Sound.play(self.hurt)

				elif i.x+31 >= self.x and i.x+31 <= self.x+31 and i.y+31 >= self.y and i.y+31 <= self.y+31:
					self.gui.health -= 1
					self.inv_timer = 270
					pygame.mixer.Sound.play(self.hurt)

				elif i.x >= self.x and i.x <= self.x+31 and i.y+31 >= self.y and i.y+31 <= self.y+31:
					self.gui.health -= 1
					self.inv_timer = 270
					pygame.mixer.Sound.play(self.hurt)

			for i in self.bats.bats:
				if i.x >= self.x and i.x <= self.x+31 and i.y >= self.y and i.y <= self.y+31:
					self.gui.health -= 1
					self.inv_timer = 270
					pygame.mixer.Sound.play(self.hurt)

				elif i.x+15 >= self.x and i.x+15 <= self.x+31 and i.y >= self.y and i.y <= self.y+31:
					self.gui.health -= 1
					self.inv_timer = 270
					pygame.mixer.Sound.play(self.hurt)

				elif i.x+15 >= self.x and i.x+15 <= self.x+31 and i.y+15 >= self.y and i.y+15 <= self.y+31:
					self.gui.health -= 1
					self.inv_timer = 270
					pygame.mixer.Sound.play(self.hurt)

				elif i.x >= self.x and i.x <= self.x+31 and i.y+15 >= self.y and i.y+15 <= self.y+31:
					self.gui.health -= 1
					self.inv_timer = 270
					pygame.mixer.Sound.play(self.hurt)

		if self.gui.health <= 0:
			self.updates.run = False

		
		#Updating animation
		if self.onLadder == True:
			if self.move['Up'] == True or self.move['Down']:
				self.anim_timer += 1
			if self.anim_timer >= 0 and self.anim_timer < 6:
				self.img = self.anim[6]
			elif self.anim_timer >= 6 and self.anim_timer < 12:
				self.img = self.anim[7]
			elif self.anim_timer >= 12:
				self.anim_timer = 0
				self.img = self.anim[6]
		elif self.move['Right'] == True:
			self.anim_timer += 1
			if self.anim_timer >= 0 and self.anim_timer < 4:
				self.img = self.anim[0]
			elif self.anim_timer >= 4 and self.anim_timer < 8:
				self.img = self.anim[1]
			elif self.anim_timer >= 8 and self.anim_timer < 12:
				self.img = self.anim[0]
			elif self.anim_timer >= 12 and self.anim_timer < 16:
				self.img = self.anim[2]
			elif self.anim_timer >= 16:
				self.anim_timer = 0
				self.img = self.anim[0]
		elif self.move['Right'] == False and self.facing == 'Right':
			self.old = 'Right'
			self.anim_timer = 0
			if self.shoot == False:
				self.img = self.anim[0]
			else:
				self.img = self.anim[4]
		elif self.move['Left'] == True:
			self.anim_timer += 1
			if self.anim_timer >= 0 and self.anim_timer < 4:
				self.img = pygame.transform.flip(self.anim[0], True, False)
			elif self.anim_timer >= 4 and self.anim_timer < 8:
				self.img = pygame.transform.flip(self.anim[1], True, False)
			elif self.anim_timer >= 8 and self.anim_timer < 12:
				self.img = pygame.transform.flip(self.anim[0], True, False)
			elif self.anim_timer >= 12 and self.anim_timer < 16:
				self.img = pygame.transform.flip(self.anim[2], True, False)
			elif self.anim_timer >= 16:
				self.anim_timer = 0
				self.img = pygame.transform.flip(self.anim[0], True, False)
		elif self.move['Left'] == False and self.facing == 'Left':
			self.old = 'Left'
			self.anim_timer = 0
			if self.shoot == False:
				self.img = pygame.transform.flip(self.anim[0], True, False)
			else:
				self.img = pygame.transform.flip(self.anim[4], True, False) 
		elif self.facing == 'Up' and self.onLadder == False:
			if self.shoot == False:
				if self.old == 'Right':
					self.img = self.anim[3]
				else:
					self.img = pygame.transform.flip(self.anim[3], True, False)
			else:
				if self.old == 'Right':
					self.img = self.anim[5]
				else:
					self.img = pygame.transform.flip(self.anim[5], True, False)
		
		
		if self.shoot == True:
			self.shoot_timer += 1
			if self.shoot_timer >= 30:
				self.shoot = False
				self.shoot_timer = 0
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT: #If user closes window
				self.updates.run = False

			if event.type == pygame.KEYDOWN: #If a key is held down
				if event.key == pygame.K_a: #if key is a
					self.move['Left'] = True
					self.facing = 'Left'
				elif event.key == pygame.K_d:#if key is d
					self.move['Right'] = True
					self.facing = 'Right'
				elif event.key == pygame.K_w:#if key is w
					self.move['Up'] = True
					self.facing = 'Up'
				elif event.key == pygame.K_s:#if key is s
					self.move['Down'] = True
				if event.key == pygame.K_SPACE and len(self.arrows) < 3 and self.move['Up'] == False and self.move['Down'] == False and self.move['Left'] == False and self.move['Right'] == False:
					self.arrows.append(Arrow(self.facing, self.x, self.y))
					self.shoot = True
					pygame.mixer.Sound.play(self.shoot_s)

				if event.key == pygame.K_ESCAPE:
					self.updates.run = False

			elif event.type == pygame.KEYUP:#If a key is released
				if event.key == pygame.K_a:#if key is a
					self.move['Left'] = False
				elif event.key == pygame.K_d:#if key is d
					self.move['Right'] = False
				elif event.key == pygame.K_w:#if key is w
					self.move['Up'] = False
				elif event.key == pygame.K_s:#if key is s
					self.move['Down'] = False
			


	def draw(self, window):
		#Score
		if self.score_timer > 0:
			score_text = self.font.render(str(self.score), False, (0,0,0))
			window.blit(score_text, (self.score_coords[0]-3, self.score_coords[1]+3))
			score_text = self.font.render(str(self.score), False, (255,255,255))
			window.blit(score_text, (self.score_coords))

		#PLayer Animations
		window.blit(self.img, (self.x, self.y))
		if self.inv_timer > 0 and self.inv_timer < 30 or self.inv_timer > 45 and self.inv_timer < 75 or self.inv_timer > 90 and self.inv_timer < 120 or self.inv_timer > 135 and self.inv_timer < 195 or self.inv_timer >210:
			window.blit(self.anim[8], (self.x, self.y))

		#Player Arrows
		for a in self.arrows:
			a.draw(window)

#Object for pygame events
class Updates:
	def __init__(self):
		#Updates variables
		self.run = True
		self.timer = 3600
	def update(self):
		self.timer -= 1
		
class PlayerGui:
	def __init__(self, health, score, level, font, highscore, img, update):
		self.health = health
		self.score = score
		self.level = level
		self.font = font
		self.highscore = highscore.scores[0]
		self.img = img
		self.update = update

	def draw(self, window):
		level_texta = self.font.render('LEVEL', True, (255, 255, 255))
		level_textb = self.font.render(str(self.level), True, (255, 255, 255))
		level_rect = level_textb.get_rect(center = (47, 710))

		score_texta = self.font.render('SCORE', True, (255, 255, 255))
		score_textb = self.font.render(str(self.score), True, (255, 255, 255))
		score_rect = level_textb.get_rect(center = (150, 710))

		hs_texta = self.font.render('HIGHSCORE', True, (255, 255, 255))
		hs_textb = self.font.render(str(self.highscore), True, (255, 255, 255))
		hs_rect = level_textb.get_rect(center = (275, 710))

		life_text = self.font.render('LIFE', True, (255, 255, 255))

		timer_text = self.font.render(str(int(self.update.timer/60)) + ' sec', True, (255,255,255))
		timer_rect = timer_text.get_rect(center=(256,16))
		
		pygame.draw.rect(window, (0,0,0), (200, 0, 112, 24))

		window.blit(timer_text, timer_rect)

		pygame.draw.rect(window, (0,0,0), (0,672,512,64))

		window.blit(level_texta, (8, 680))
		window.blit(level_textb, level_rect)

		window.blit(score_texta, (108,680))
		window.blit(score_textb, score_rect)

		window.blit(hs_texta, (208,680))
		window.blit(hs_textb, hs_rect)

		window.blit(life_text, (400,680))
		for i in range(0,5):
			if i < self.health:
				window.blit(self.img[0], ((i*18)+386, 700))
			else:
				window.blit(self.img[1], ((i*18)+386, 700))
class Highscores:
	def __init__(self):
		self.path = 'scores.txt'
		self.initials = []
		with open(self.path, 'r') as file:
			self.scores = file.read().split('\n')
			self.scores = self.scores[:5]
		for i, e in enumerate(self.scores):
			if i < 5:
				self.scores[i] = int(e[3:])
				self.initials.append(e[:3])

	def updateScores(self, new_score, initials):
		
		self.scores.append(new_score)
		self.scores = sorted(self.scores, key=int, reverse=True)
		self.initials.insert(self.scores.index(new_score), initials)
		self.scores = self.scores[:-1]
		self.initials = self.initials[:-1]
		

		with open(self.path, 'w') as file:
			for i, e in enumerate(self.scores):
				file.write(self.initials[i] + str(e)+'\n')


#Tile Images
grassImg = pygame.image.load('Assets/Tiles/Grass.png').convert_alpha()
grassImg = pygame.transform.scale(grassImg, (32, 32))
ladderImg = pygame.image.load('Assets/Tiles/Ladder.png').convert_alpha()
ladderImg = pygame.transform.scale(ladderImg, (32, 32))
fireImg = pygame.image.load('Assets/Tiles/Fire.png').convert_alpha()
fireImg = pygame.transform.scale(fireImg, (32, 32))
brickImg = pygame.image.load('Assets/Tiles/brick.png').convert_alpha()
brickImg = pygame.transform.scale(brickImg, (32, 32))
chainImg = pygame.image.load('Assets/Tiles/chain.png').convert_alpha()
chainImg = pygame.transform.scale(chainImg, (32, 32))
sandImg = pygame.image.load('Assets/Tiles/sand.png').convert_alpha()
sandImg = pygame.transform.scale(sandImg, (32, 32))
leafImg = pygame.image.load('Assets/Tiles/leaf.png').convert_alpha()
leafImg = pygame.transform.scale(leafImg, (32, 32))
vineImg = pygame.image.load('Assets/Tiles/vine.png').convert_alpha()
vineImg = pygame.transform.scale(vineImg, (32, 32))

tiles = [grassImg, ladderImg, fireImg]
tiles_dungeon = [brickImg, chainImg, fireImg]
tiles_jung = [leafImg, vineImg, fireImg]
tile_sand = [sandImg, ladderImg, fireImg]

#Player Images
player_1_f1 = pygame.image.load('Assets/Player/player_1_anim_1.png').convert_alpha()
player_1_f1 = pygame.transform.scale(player_1_f1, (32, 32))
player_1_f2 = pygame.image.load('Assets/Player/player_1_anim_2.png').convert_alpha()
player_1_f2 = pygame.transform.scale(player_1_f2, (32, 32))
player_1_f3 = pygame.image.load('Assets/Player/player_1_anim_3.png').convert_alpha()
player_1_f3 = pygame.transform.scale(player_1_f3, (32, 32))
player_1_up = pygame.image.load('Assets/Player/player1_up_1.png').convert_alpha()
player_1_up = pygame.transform.scale(player_1_up, (32, 32))
player_1_bow_norm = pygame.image.load('Assets/Player/player1_bow_1.png').convert_alpha()
player_1_bow_norm = pygame.transform.scale(player_1_bow_norm, (32, 32))
player_1_bow_up = pygame.image.load('Assets/Player/player1_bow_2.png').convert_alpha()
player_1_bow_up = pygame.transform.scale(player_1_bow_up, (32, 32))
player_1_ladder_1 = pygame.image.load('Assets/Player/player1_ladder_anim_2.png').convert_alpha()
player_1_ladder_1 = pygame.transform.scale(player_1_ladder_1, (32, 32))
player_1_ladder_2 = pygame.image.load('Assets/Player/player1_ladder_anim_3.png').convert_alpha()
player_1_ladder_2 = pygame.transform.scale(player_1_ladder_2, (32, 32))
shield = pygame.image.load('Assets/Player/sheild_1.png').convert_alpha()
shield = pygame.transform.scale(shield, (32,32))
player_anim_1 = [player_1_f1, player_1_f2, player_1_f3, player_1_up, player_1_bow_norm, player_1_bow_up, player_1_ladder_1, player_1_ladder_2, shield]
#Enemy Images
enemy_walk_1 = pygame.image.load('Assets/Enemies/enemy_purple_1.png').convert_alpha()
enemy_walk_1 = pygame.transform.scale(enemy_walk_1, (32,32))
enemy_walk_2 = pygame.image.load('Assets/Enemies/enemy_purple_2.png').convert_alpha()
enemy_walk_2 = pygame.transform.scale(enemy_walk_2, (32,32))
enemy_walk_3 = pygame.image.load('Assets/Enemies/enemy_purple_3.png').convert_alpha()
enemy_walk_3 = pygame.transform.scale(enemy_walk_3, (32,32))
enemy_ladder_1 = pygame.image.load('Assets/Enemies/enemy_purple_4.png').convert_alpha()
enemy_ladder_1 = pygame.transform.scale(enemy_ladder_1, (32,32))
enemy_ladder_2 = pygame.image.load('Assets/Enemies/enemy_purple_5.png').convert_alpha()
enemy_ladder_2 = pygame.transform.scale(enemy_ladder_2, (32,32))
enemy_ladder_3 = pygame.image.load('Assets/Enemies/enemy_purple_6.png').convert_alpha()
enemy_ladder_3 = pygame.transform.scale(enemy_ladder_3, (32,32))

enemy_anim = [enemy_walk_1, enemy_walk_2, enemy_walk_3, enemy_ladder_1, enemy_ladder_2, enemy_ladder_3]
#bat Images
bat_1 = pygame.image.load('Assets/Enemies/bat_1.png').convert_alpha()
bat_1 = pygame.transform.scale(bat_1, (16,16))
bat_2 = pygame.image.load('Assets/Enemies/bat_2.png').convert_alpha()
bat_2 = pygame.transform.scale(bat_2, (16,16))
bat_3 = pygame.image.load('Assets/Enemies/bat_3.png').convert_alpha()
bat_3 = pygame.transform.scale(bat_3, (16,16))

bat_anim = [bat_1, bat_2, bat_3]

#Other Images
hp_full = pygame.image.load('Assets/Other/hp_1.png').convert_alpha()
hp_full = pygame.transform.scale(hp_full, (16, 16))
hp_none = pygame.image.load('Assets/Other/hp_2.png').convert_alpha()
hp_none = pygame.transform.scale(hp_none, (16, 16))

hp_img = [hp_full, hp_none]
#Fonts
small_font = pygame.font.Font('Assets/Fonts/PressStart2P.ttf', 12)
main_font = pygame.font.Font('Assets/Fonts/PressStart2P.ttf', 16)
big_font = pygame.font.Font('Assets/Fonts/PressStart2P.ttf', 24)

class Level:
	def __init__(self, highscores, tilemap, updates, clock, enemy, bat, gui, player):
		self.highscores = highscores
		self.tilemap = tilemap
		self.updates = updates
		self.clock = clock
		self.enemy = enemy
		self.bat = bat
		self.gui = gui
		self.player = player

	def update(self):
		self.enemy.update()
		self.bat.update()
		self.player.update()
		self.updates.update()


	def draw(self, window):
		self.tilemap.draw(window)
		self.enemy.draw(window)
		self.bat.draw(window)
		self.player.draw(window)
		self.gui.draw(window)


class Main:
	def __init__(self, level, levels, window, font, big_font, small_font, en_anim, bat_anim, player_anim, hp_anim, plains, dungeon, jungle, sand):
		self.level = level
		self.levels = levels
		self.window = window
		self.font = font
		self.big_font = big_font
		self.small_font = small_font
		self.current = 0
		self.run = True
		self.start = False
		self.title = True
		self.options = ['Play', 'Controls', 'Exit']
		self.current = 0
		self.en_anim = en_anim
		self.bat_anim = bat_anim
		self.player_anim = player_anim
		self.hp_anim = hp_anim
		self.current_level = 0
		self.level_screen = 0
		self.string = "Let's Get Started!"
		self.name = ['-', '-', '-']
		self.place = 0
		self.death = False
		self.high_screen = False
		self.plains = plains
		self.dungeon = dungeon
		self.jungle = jungle
		self.sand = sand
		self.controls = False
		self.credits = False
		pygame.mixer.music.load("sounds/title.wav")
		pygame.mixer.music.play(-1)
	def drawTitle(self):
		

		window.fill((0,0,0))

		title_texta = self.big_font.render('Doing Knightly Things', True, (255, 255, 255))
		title_recta = title_texta.get_rect(center=(256, 32))
		title_textb = self.big_font.render('In a Timely Manner!', True, (255, 255, 255))
		title_rectb = title_textb.get_rect(center=(256, 64))
		ver_text = self.small_font.render('Ver: 1.0 Alpha', True, (255, 255, 255))
		credits_text = self.small_font.render('By: Peyton Moon & Richard Holt', True, (225, 255, 255))

		window.blit(title_texta, title_recta)
		window.blit(title_textb, title_rectb)
		window.blit(credits_text, (0, 724))
		window.blit(ver_text, (0, 710))
		if self.title == True:
			for y, text in enumerate(self.options):
				if y == self.current:
					option = self.font.render(text, True, (255, 255, 0))
				else:
					option = self.font.render(text, True, (255, 255, 255))
				option_rect = option.get_rect(center=(256,(y*32)+256))
				window.blit(option, option_rect)
		elif self.controls == True:
			texta = self.font.render('Use WASD to move!', True, (255, 255, 255))
			textb = self.font.render('Press SPACE to shoot!', True, (255, 255, 255))
			textc = self.font.render('Get a high score!', True, (255, 255, 255))
			texta_rect = texta.get_rect(center=(256, 200))
			textb_rect = textb.get_rect(center=(256, 300))
			textc_rect = textc.get_rect(center=(256, 400))

			window.blit(texta, texta_rect)
			window.blit(textb, textb_rect)
			window.blit(textc, textc_rect)



				

	def updateTitle(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.run = False
				elif event.key == pygame.K_w:
					self.current -= 1
					if self.current < 0:
						self.current = len(self.options)-1
				elif event.key == pygame.K_s:
					self.current += 1
					if self.current > len(self.options)-1:
						self.current = 0
				elif event.key == pygame.K_SPACE:
					if self.controls == True:
						self.controls = False
						self.title = True
					else:
						if self.current == 0:
							self.start = True
							self.level_screen = 300
						elif self.current == 1:
							self.controls = True
							self.title = False
						elif self.current == 2:
							self.run = False

	def deathScreen(self):
		if self.high_screen == False:
			con_texta = self.big_font.render('Congratuations!', True, (255, 255, 255))
			con_textb = self.big_font.render('You Got...', True, (255, 255, 255))
			con_textc = self.big_font.render(str(self.level.gui.score), True, (255, 255, 0))
			con_textd = self.big_font.render('Points', True, (255, 255, 255))
			name_text = self.big_font.render('Name?', True, (255, 255, 255))
			name_str = ''.join(self.name)
			name_textb = self.big_font.render(str(name_str), True, (255, 255, 255))
			enter_text = self.font.render('Press [ENTER] to confirm!', True, (255, 255, 255))
			texta_rect = con_texta.get_rect(center=(256,25))
			textb_rect = con_textb.get_rect(center=(256,75))
			textc_rect = con_textc.get_rect(center=(256,125))
			textd_rect = con_textd.get_rect(center=(256,175))
			namea_rect = name_text.get_rect(center=(256,225))
			nameb_rect = name_textb.get_rect(center=(256,275))
			enter_rect = enter_text.get_rect(center=(256,325))
			window.blit(con_texta, texta_rect)
			window.blit(con_textb, textb_rect)
			window.blit(con_textc, textc_rect)
			window.blit(con_textd, textd_rect)
			window.blit(name_text, namea_rect)
			window.blit(name_textb, nameb_rect)
			window.blit(enter_text, enter_rect)

		else:
			scores = self.big_font.render('HIGHSCORES', True, (255, 255, 255))
			score_rect = scores.get_rect(center=(256, 25))
			window.blit(scores, score_rect)
			for i in range(0, 5):
				string = self.level.highscores.initials[i] + ' ' + str(self.level.highscores.scores[i])
				text = self.font.render(string, True, (255, 255, 255))
				text_rect = text.get_rect(center=(256, (i*25)+75))
				window.blit(text, text_rect)
			enter_text = self.font.render('Press [ENTER] to continue!', True, (255, 255, 255))
			enter_rect = enter_text.get_rect(center=(256,325))
			window.blit(enter_text, enter_rect)
			

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.run = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.run = False
				if self.high_screen == True:
					if event.key == pygame.K_RETURN:
						self.death = False
						self.high_screen = False
						self.start = False
						self.current_level = 0
						self.level.tilemap = Tilemap(self.levels[self.current_level], self.level.tilemap.tiles)
						self.level.enemy = EnemySpawning(self.level.tilemap, self.en_anim)
						self.level.bat = BatSpawning(self.level.tilemap, self.bat_anim)
						self.level.updates.timer = 3600
						self.level.gui.update.run = True
						self.level.gui = PlayerGui(5, 0, 1, self.font, self.level.highscores, self.level.gui.img, self.level.gui.update)
						self.current_level = 0
						self.level.player = Player(240, 608, self.level.tilemap, self.level.enemy, self.level.player.anim, self.level.bat, self.level.gui, self.level.updates, self.level.player.font)
						self.level.tilemap.tiles = self.plains
				elif self.high_screen == False:
					if self.place > 0:
						if event.key == pygame.K_BACKSPACE:
							self.place -= 1
							self.name[self.place] = '-'
					if event.key == pygame.K_RETURN:
						name_str = ''.join(self.name)
						self.level.highscores.updateScores(self.level.gui.score, name_str)
						self.high_screen = True
					elif self.place < 3:
						if event.key == pygame.K_a:
							self.name[self.place] = 'A'
							self.place += 1
						if event.key == pygame.K_b:
							self.name[self.place] = 'B'
							self.place += 1
						if event.key == pygame.K_c:
							self.name[self.place] = 'C'
							self.place += 1
						if event.key == pygame.K_d:
							self.name[self.place] = 'D'
							self.place += 1
						if event.key == pygame.K_e:
							self.name[self.place] = 'E'
							self.place += 1
						if event.key == pygame.K_f:
							self.name[self.place] = 'F'
							self.place += 1
						if event.key == pygame.K_g:
							self.name[self.place] = 'G'
							self.place += 1
						if event.key == pygame.K_h:
							self.name[self.place] = 'H'
							self.place += 1
						if event.key == pygame.K_i:
							self.name[self.place] = 'I'
							self.place += 1
						if event.key == pygame.K_j:
							self.name[self.place] = 'J'
							self.place += 1
						if event.key == pygame.K_k:
							self.name[self.place] = 'K'
							self.place += 1
						if event.key == pygame.K_l:
							self.name[self.place] = 'L'
							self.place += 1
						if event.key == pygame.K_m:
							self.name[self.place] = 'M'
							self.place += 1
						if event.key == pygame.K_n:
							self.name[self.place] = 'N'
							self.place += 1
						if event.key == pygame.K_o:
							self.name[self.place] = 'O'
							self.place += 1
						if event.key == pygame.K_p:
							self.name[self.place] = 'P'
							self.place += 1
						if event.key == pygame.K_q:
							self.name[self.place] = 'Q'
							self.place += 1
						if event.key == pygame.K_r:
							self.name[self.place] = 'R'
							self.place += 1
						if event.key == pygame.K_s:
							self.name[self.place] = 'S'
							self.place += 1
						if event.key == pygame.K_t:
							self.name[self.place] = 'T'
							self.place += 1
						if event.key == pygame.K_u:
							self.name[self.place] = 'U'
							self.place += 1
						if event.key == pygame.K_v:
							self.name[self.place] = 'V'
							self.place += 1
						if event.key == pygame.K_w:
							self.name[self.place] = 'W'
							self.place += 1
						if event.key == pygame.K_x:
							self.name[self.place] = 'X'
							self.place += 1
						if event.key == pygame.K_y:
							self.name[self.place] = 'Y'
							self.place += 1
						if event.key == pygame.K_z:
							self.name[self.place] = 'Z'
							self.place += 1

	def levelScreen(self, window):
		level_texta = self.big_font.render('LEVEL', True, (255, 255, 255))
		level_textb = self.big_font.render(str(self.level.gui.level), True, (255, 255, 255))
		inspirational_text = self.font.render(self.string, True, (255, 255, 255))
		recta = level_texta.get_rect(center=(256, 256))
		rectb = level_textb.get_rect(center=(256, 300))
		rectc = inspirational_text.get_rect(center=(256, 512))

		window.blit(level_texta, recta)
		window.blit(level_textb, rectb)
		window.blit(inspirational_text, rectc)


	def draw(self, window):
		self.level.draw(window)

	def update(self):
		self.level.update()
		if self.level.updates.run == False:
			if self.level.gui.health > 0:
				self.run = False
			elif self.level.gui.health <= 0:
				self.death = True
		if self.level.updates.timer == 0:
			self.level.updates.timer = 3600
			self.current_level += 1
			if self.current_level > 3:
				self.current_level = 0
			self.level.tilemap = Tilemap(self.levels[self.current_level], self.level.tilemap.tiles)
			self.level.enemy = EnemySpawning(self.level.tilemap, self.en_anim)
			self.level.bat = BatSpawning(self.level.tilemap, self.bat_anim)
			self.level.player.level = self.level.tilemap
			self.level.player.gui.level += 1
			self.level_screen = 300
			self.string = random.choice(['Well Done!', 'Keep Going!', "Don't Give Up!", 'Push Onward!', 'On To Victory!', 'Forward To Glory!', 'Add To Your Legend Brave Knight!', 'Crush Thine Enemies!', 'Be A Hero!', 'Fight To Save The Land!'])

			if self.current_level == 0:
				self.level.player = Player(240, 608, self.level.tilemap, self.level.enemy, self.level.player.anim, self.level.bat, self.level.player.gui, self.level.updates, self.level.player.font)
				self.level.tilemap.tiles = self.plains
			elif self.current_level == 1:
				self.level.player = Player(240, 128, self.level.tilemap, self.level.enemy, self.level.player.anim, self.level.bat, self.level.player.gui, self.level.updates, self.level.player.font)
				self.level.tilemap.tiles = self.sand
			elif self.current_level == 2:
				self.level.player = Player(32, 608, self.level.tilemap, self.level.enemy, self.level.player.anim, self.level.bat, self.level.player.gui, self.level.updates, self.level.player.font)
				self.level.tilemap.tiles = self.jungle
			elif self.current_level == 3:
				self.level.player = Player(240, 128, self.level.tilemap, self.level.enemy, self.level.player.anim, self.level.bat, self.level.player.gui, self.level.updates, self.level.player.font)
				self.level.tilemap.tiles = self.dungeon


#objects
#AUDIO NEEDS 16Bit, 22050 Hz and Mono
highscores = Highscores()
level_one_tm = Tilemap('Levels/plains_level.txt', tiles)
updates = Updates()
clock = pygame.time.Clock()
enemySpawn = EnemySpawning(level_one_tm, enemy_anim)
batSpawn = BatSpawning(level_one_tm, bat_anim)
playergui = PlayerGui(5,0,1, main_font,highscores, hp_img, updates)
player = Player(240, 608, level_one_tm, enemySpawn, player_anim_1, batSpawn, playergui, updates, main_font)

level = Level(highscores, level_one_tm, updates, clock, enemySpawn, batSpawn, playergui, player)

main = Main(level, ['Levels/plains_level.txt', 'Levels/desert_level.txt', 'Levels/jungle_level.txt', 'Levels/dungeon_level.txt'], window, main_font, big_font, small_font, enemy_anim, bat_anim, player_anim_1, hp_img, tiles, tiles_dungeon, tiles_jung, tile_sand)
while main.run:

	if main.level_screen > 0:
		main.level_screen -= 1
		window.fill((0,0,0))
		main.levelScreen(window)
		pygame.display.update()
		if main.level_screen == 1:
			if main.current_level == 0:
				pygame.mixer.music.load("sounds/plains.wav")
				pygame.mixer.music.play(-1)
			elif main.current_level == 1:
				pygame.mixer.music.load("sounds/desert.wav")
				pygame.mixer.music.play(-1)
			elif main.current_level == 2:
				pygame.mixer.music.load("sounds/jungle.wav")
				pygame.mixer.music.play(-1)
			elif main.current_level == 3:
				pygame.mixer.music.load("sounds/dungeon.wav")
				pygame.mixer.music.play(-1)
			
	elif main.start == False:
		window.fill((0,0,0))
		main.drawTitle()
		pygame.display.update()
		main.updateTitle()
	elif main.death == True:
		window.fill((0,0,0))
		main.deathScreen()
		pygame.display.update()
	else:
		if main.current_level != 3:
			window.fill((0,200,200))
		else:
			window.fill((50,50,50))
		main.draw(window)
		pygame.display.update()
		main.update()
	clock.tick(240)

pygame.quit()