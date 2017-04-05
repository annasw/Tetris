import os, sys
import random
import pygame
from pygame.locals import *

# LEFT TO DO:
# - rotate blocks
# - gravity
# - deleting rows

class Tetris:
	colors = {'RED':pygame.Color(255,0,0),
	          'PURPLE':pygame.Color(128,0,128),
			  'GREEN':pygame.Color(0,128,0),
			  'AQUA':pygame.Color(0,255,255),
			  'BLUE':pygame.Color(0,0,255),
			  'ORANGE':pygame.Color(128,0,0),
			  'YELLOW':pygame.Color(255,255,0),
			  'GRAY':pygame.Color(200,200,200),
			  'BLACK':pygame.Color(0,0,0)}
	
	genres = ['LONG','RHOOK','LHOOK','SQUARE','SBLOCK',
			  'TBLOCK','ZBLOCK']
	
	FPS = 30
	fpsClock = pygame.time.Clock()
	
	def __init__(self, width=464, height=576):
		pygame.init()
		self.width = width # with sidebars
		self.barWidth = 40 # sidebars
		self.gameWidth = self.width - self.barWidth*2 # width w/out sidebars
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.gameOver = False
		
		self.blockSize = 24
		self.walls = [pygame.Rect(0,0,self.barWidth,self.height),pygame.Rect(self.width-self.barWidth,0,self.barWidth,self.height)]
		
		# array of placed blocks:
		# it has gameWidth/blockSize columns and height/blockSize rows
		self.placedBlocks = [[None for x in range(self.gameWidth/self.blockSize)] for y in range(self.height/self.blockSize)]
		#self.placedBlocks = 
		
		self.startCoordinates = (self.barWidth + self.blockSize*2,0)
		pygame.display.set_caption('Tetris!')
		
	def newBlock(self):
		genre = random.choice(self.genres)
		self.tetro = Tetromino(genre,self.blockSize,
						  self.startCoordinates[0],self.startCoordinates[1])
		
		
	# turn these into walls
	def drawScreen(self):
		self.screen.fill(self.colors['BLACK'])
		for w in self.walls:
			pygame.draw.rect(self.screen,self.colors['GRAY'],w)
		
		for row in self.placedBlocks:
			for b in row:
				if b != None:
					# deal with color later tbh
					#pygame.draw.rect(self.screen,self.colors[b.blockColor],b)
					pygame.draw.rect(self.screen,self.colors["RED"],b)
		
		#if self.tetro:
		for b in self.tetro.rectGroup:
			pygame.draw.rect(self.screen,self.colors[self.tetro.blockColor],b)
	
	# deal with the death of a block
	def blockDeath(self):
		# deleting rows,
		
		# adds block to placedBlocks
		for b in self.tetro.rectGroup:
			xIdx = (b.x-self.barWidth)/self.blockSize
			yIdx = b.y/self.blockSize
			self.placedBlocks[yIdx][xIdx] = b
		
		
		'''for row in range(len(self.placedBlocks)-1,-1,-1):
			for u in range(len(self.placedBlocks[0])):
				if'''

	
	def checkGameOver(self):
		for e in self.tetro.rectGroup:
			for y in self.placedBlocks:
				for x in y:
					if x != None and e.colliderect(x):
						return True
		return False
		
	
	# need to deal with newBlocks becoming just blocks - self.tetro
	# (or sentient)
	def MainLoop(self):
		self.newBlock()
		while True:
			self.fpsClock.tick(self.FPS)
			
			for e in pygame.event.get():
				if e.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
					pygame.quit()
					sys.exit()
			if not self.gameOver:
				key = pygame.key.get_pressed()
				if key[pygame.K_LEFT]:
					self.tetro.move(-self.blockSize,0,self.walls, self.placedBlocks, self.height)
				if key[pygame.K_RIGHT]:
					self.tetro.move(self.blockSize,0,self.walls,self.placedBlocks, self.height)
				# tetrominos cant move up lol
				# maybe set up to be rotate (if&when that becomes a thing)?
				#if key[pygame.K_UP]:
				#	self.tetro.move(0,-self.blockSize,self.walls, self.height)
				if key[pygame.K_DOWN]:
					self.tetro.move(0,self.blockSize,self.walls,self.placedBlocks, self.height)
				
				if not self.tetro.alive:
					# also need to handle adding it to collisions detection,
					# deleting rows,
					# ending game, etc.
					
					self.blockDeath()
					
					self.newBlock()
					
					# consider coloring screen red and putting GAME OVER text on it
					if self.checkGameOver():
						self.gameOver = True
						self.tetro.alive = False

			self.drawScreen()
			pygame.display.flip()
		
		
	
	'''def MainLoop(self): # draw, update, check input?
		while True:
			#self.screen.blit(self.grp, (50,50))
			for event in pygame.event.get():
				if event.type == QUIT:
					pygame.quit()
					sys.exit()
			pygame.display.update()
			#self.fpsClock.tick(FPS)'''

class Tetromino:
	blockColors = {'LONG':'AQUA','RHOOK':'BLUE','LHOOK':'ORANGE',
			  'SQUARE':'YELLOW','SBLOCK':'GREEN',
			  'TBLOCK':'PURPLE','ZBLOCK':'RED'}
	
	def __init__(self, genre, blockSize, x_coord, y_coord):
		#pygame.sprite.Sprite.__init__(self)
		self.genre = genre
		self.blockSize = blockSize
		self.x_coord = x_coord
		self.y_coord = y_coord
		self.blockColor = self.blockColors[genre]
		self.alive = True
		
		#self.rectGroup = pygame.sprite.Group()
		self.rectGroup = []
		
		if self.genre=='LONG':
			self.rectGroup.append(Rect(self.x_coord, self.y_coord,
			                   self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord, self.y_coord+blockSize,
							   self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord, self.y_coord+blockSize*2,
							   self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord, self.y_coord+blockSize*3,
							   self.blockSize, self.blockSize))
		elif self.genre=='RHOOK':
			self.rectGroup.append(Rect(self.x_coord,self.y_coord,
								  self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord+blockSize,self.y_coord,
								  self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord, self.y_coord+blockSize,
								  self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord, self.y_coord+blockSize*2,
								  self.blockSize, self.blockSize))
		elif self.genre=='LHOOK':
			self.rectGroup.append(Rect(self.x_coord,self.y_coord,
								  self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord+blockSize,self.y_coord,
								  self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord+blockSize, self.y_coord+blockSize,
								  self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord+blockSize, self.y_coord+blockSize*2,
								  self.blockSize, self.blockSize))
		elif self.genre=='SQUARE':
			self.rectGroup.append(Rect(self.x_coord,self.y_coord,
								  self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord+blockSize,self.y_coord,
								  self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord, self.y_coord+blockSize,
								  self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord+blockSize, self.y_coord+blockSize,
								  self.blockSize, self.blockSize))
		elif self.genre=='SBLOCK':
			self.rectGroup.append(Rect(self.x_coord+blockSize,self.y_coord,
								  self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord+blockSize*2,self.y_coord,
								  self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord, self.y_coord+blockSize,
								  self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord+blockSize, self.y_coord+blockSize,
								  self.blockSize, self.blockSize))
		elif self.genre=='ZBLOCK':
			self.rectGroup.append(Rect(self.x_coord,self.y_coord,
								  self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord+blockSize,self.y_coord,
								  self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord+blockSize, self.y_coord+blockSize,
								  self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord+blockSize*2, self.y_coord+blockSize,
								  self.blockSize, self.blockSize))
		elif self.genre=='TBLOCK':
			self.rectGroup.append(Rect(self.x_coord+blockSize,self.y_coord,
								  self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord,self.y_coord+blockSize,
								  self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord+blockSize, self.y_coord+blockSize,
								  self.blockSize, self.blockSize))
			self.rectGroup.append(Rect(self.x_coord+blockSize*2, self.y_coord+blockSize,
								  self.blockSize, self.blockSize))
	

	
	def move(self, dx, dy, wallArray, placedBlocks, height):
		if dx!=0:
			self.move_single_axis(dx,0,wallArray, placedBlocks, height)
		if dy!=0:
			self.move_single_axis(0,dy,wallArray, placedBlocks, height)
			
	# move ALL rects in the piece, check each for collision;
	# if there's ANY collision, move them ALL back
	# 
	# New theory: we don't actually need to account for collision;
	# if there's a wall, just don't move; we move discretely
	# probably need to deal with already-landed tetr.s separately
	def move_single_axis(self, dx, dy, walls, placedBlocks, ht):
		correction = False # undo move for ALL rects?
		
		for e in self.rectGroup:
			e.x += dx
			e.y += dy
			
			# maybe also check the fallen blocks?
			for wall in walls: # need to get this in somehow
				if e.colliderect(wall):
					correction = True
			for row in placedBlocks:
				for block in row:
					if block != None:
						if e.colliderect(block):
							correction = True
			
			# check that we don't go off the top or bottom
			# MAYBE CHECKING WALL HEIGHT ISN'T A GOOD IDEA
			if e.y < 0 or e.bottom > ht:
				correction = True
			
		# AFTER all movement, undo if necessary
		if correction:
			for e in self.rectGroup:
				e.x -= dx
				e.y -= dy
			if dy!=0: # block is dead
				self.alive = False

		

def main():
	t = Tetris()
	t.MainLoop()

if __name__=='__main__':
	main()
