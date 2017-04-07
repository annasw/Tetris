import os, sys
import random
import math
import pygame
from pygame.locals import *

'''
FUNCTIONALITY YET TO ADD:
- Next block preview
- Better turning mechanics (near walls, etc. - should be able to move r or l one square if that fits)
- Restart mechanic (on pause or endgame)
- Block storage (one at a time/no more than one switch in a row)
- Two-way rotation
'''

class Tetris:
	colors = {'RED':pygame.Color(255,0,0),
	          'PURPLE':pygame.Color(128,0,128),
			  'GREEN':pygame.Color(0,128,0),
			  'AQUA':pygame.Color(0,255,255),
			  'BLUE':pygame.Color(0,0,255),
			  'ORANGE':pygame.Color(128,0,0),
			  'YELLOW':pygame.Color(255,255,0),
			  'PINK':pygame.Color(255,51,153),
			  'SEA':pygame.Color(0,102,102),
			  'GRAY':pygame.Color(100,100,100),
			  'BLACK':pygame.Color(0,0,0),
			  'WHITE':pygame.Color(255,255,255)}
	
	genres = ['LONG','RHOOK','LHOOK','SQUARE','SBLOCK',
			  'TBLOCK','ZBLOCK']
	
	FPS = 120
	fpsClock = pygame.time.Clock()
	blockSize = 40
	barWidth = int(blockSize*2.5) # sidebars
	widthInBlocks = 12
	heightInBlocks = 20
	
	def __init__(self, width=blockSize*widthInBlocks+barWidth*2, height=blockSize*heightInBlocks):
		pygame.init()
		self.width = width # with sidebars
		self.gameWidth = self.width - self.barWidth*2 # width w/out sidebars
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.score = 0
		self.nextBlock = None
		
		self.walls = [pygame.Rect(0,0,self.barWidth,self.height),pygame.Rect(self.width-self.barWidth,0,self.barWidth,self.height)]
		
		# array of placed blocks:
		# it has gameWidth/blockSize columns and height/blockSize rows
		self.placedBlocks = [[None for x in range(self.gameWidth/self.blockSize)] for y in range(self.height/self.blockSize)]
		
		self.startCoordinates = (self.barWidth + self.blockSize*2,0)
		pygame.display.set_caption('Tetris!')
		
	def newBlock(self):
		genre = random.choice(self.genres)
		if self.nextBlock == None:
			self.tetro = Tetromino(genre,self.blockSize,
						  self.startCoordinates[0],self.startCoordinates[1], self.height, self.placedBlocks)
		else:
			self.tetro = Tetromino(self.nextBlock.genre,self.blockSize,
								   self.startCoordinates[0],self.startCoordinates[1], self.height, self.placedBlocks)

		self.nextBlock = Tetromino(genre,self.barWidth/5,self.width-(4*self.barWidth/5),self.height/4, self.height, self.placedBlocks)
		
		
		
	# turn these into walls
	def drawScreen(self):
		self.screen.fill(self.colors['BLACK'])
		for w in self.walls:
			pygame.draw.rect(self.screen,self.colors['GRAY'],w)
		
		# display score
		myFont = pygame.font.SysFont("monospace", 15)
		label = myFont.render(str(self.score), 1, self.colors['WHITE'])
		labelDimensions = myFont.size(str(self.score)) # duple (width, height)
		self.screen.blit(label, (self.width-labelDimensions[0],0))
		
		for row in self.placedBlocks:
			for b in row:
				if b != None:
					# deal with color later tbh
					#pygame.draw.rect(self.screen,self.colors[b.blockColor],b)
					pygame.draw.rect(self.screen,self.colors["RED"],b)
		
		#if self.tetro:
		for b in self.tetro.rectGroup:
			pygame.draw.rect(self.screen,self.colors[self.tetro.blockColor],b)
		
		if self.tetro.alive:
			for b in self.tetro.ghostBlocks:
				pygame.draw.rect(self.screen,self.colors['WHITE'],b)
			for b in self.nextBlock.rectGroup:
				pygame.draw.rect(self.screen,self.colors[self.nextBlock.blockColor],b)
		
		# draw gridlines
		for y in range(self.blockSize,self.height,self.blockSize):
			pygame.draw.line(self.screen,self.colors['WHITE'],(self.barWidth,y),(self.width-self.barWidth,y))
		for x in range(self.barWidth+self.blockSize,self.width-self.barWidth,self.blockSize):
			pygame.draw.line(self.screen,self.colors['WHITE'],(x,0),(x,self.height))
				
	# IT'S WORKING
	# IT'S WORKIIIIIING
	def clearRows(self):
		emptyRows = [] # list of indices of empty rows
		for rowIdx in range(len(self.placedBlocks)):
			if None not in self.placedBlocks[rowIdx]:
				emptyRows.append(rowIdx)
				# empty the row
				self.placedBlocks[rowIdx] = [None for x in range(self.gameWidth/self.blockSize)]
		# for each empty row,
		# change the y-val of everything above it to move each block down one row
		# then we're gonna remake the 2D array
		for row in emptyRows:
			for rowIdx in range(row):
				for i in self.placedBlocks[rowIdx]:
					if i != None:
						i.y+=self.blockSize
		
		newArray = [[None for x in range(self.gameWidth/self.blockSize)] for y in range(self.height/self.blockSize)]
		
		for row in self.placedBlocks:
			for elt in row:
				if elt != None:
					xIdx = (elt.x-self.barWidth)/self.blockSize
					yIdx = elt.y/self.blockSize
					newArray[yIdx][xIdx] = elt
		self.placedBlocks = newArray
		
		clearedRows = len(emptyRows)
		if clearedRows==1:
			self.score += 100
		elif clearedRows==2: # bonus: 1.25x
			self.score += 250
		elif clearedRows==3: # bonus: 1.5x
			self.score += 450
		elif clearedRows==4: # big bonus: 2x
			self.score += 800
	
	# deal with the death of a block
	def blockDeath(self):		
		# adds block to placedBlocks
		for b in self.tetro.rectGroup:
			xIdx = (b.x-self.barWidth)/self.blockSize
			yIdx = b.y/self.blockSize
			self.placedBlocks[yIdx][xIdx] = b
		
		self.clearRows()
	
	
	
	# pause method. also handles exiting the game
	def pause(self):
		# display a screen with PAUSE and
		# Q TO QUIT and ESC TO UNPAUSE
		
		pauseScreen = pygame.Surface((self.width, self.height))
		
		pauseScreen.fill(self.colors['BLUE'])
		pauseScreen.set_alpha(128)
		self.screen.blit(pauseScreen, (0,0))
		
		# pausescreen text
		pauseText = "PAUSED"
		instructionText = "Q TO QUIT, ESC TO UNPAUSE"
		
		myFont = pygame.font.SysFont("monospace", 30, 1)
		pauseWord = myFont.render(pauseText, 1, self.colors['RED'])
		instructions = myFont.render(instructionText,1,self.colors['RED'])
		
		pauseWordDimensions = myFont.size(pauseText) # duple (width, height)
		instructionsDimensions = myFont.size(instructionText)
		
		self.screen.blit(pauseWord, ((self.width-pauseWordDimensions[0])/2,self.height/4))
		self.screen.blit(instructions, ((self.width-instructionsDimensions[0])/2,self.height/2))
		
		
		#pauseScreen.blit(pauseWord, ((self.width-pauseWordDimensions[0])/2,self.height/.25))
		#pauseScreen.blit(instructions, ((self.width-instructionsDimensions[0])/2,self.height/.5))		
		
		pygame.display.flip()
		
		
		pauseStart = pygame.time.get_ticks()
		while True:
			self.fpsClock.tick(self.FPS)
			
			done = False
			
			for e in pygame.event.get():
				if e.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if e.type == pygame.KEYDOWN:
					# press q to quit
					if e.key == pygame.K_q:
						pygame.quit()
						sys.exit()
				# resume the game
					if e.key == pygame.K_ESCAPE and pygame.time.get_ticks()-pauseStart>200:
						done = True
			if done: break
	
	def checkGameOver(self):
		for e in self.tetro.rectGroup:
			for y in self.placedBlocks:
				for x in y:
					if x != None and e.colliderect(x):
						return True
		return False
	
	def endGame(self):
		# display gameOver text and wait for input
		
		'''make new outside method/class that calls instances of this class to restart game'''
		
		self.drawScreen()
		
		gameOverScreen = pygame.Surface((self.width, self.height))
		
		gameOverScreen.fill(self.colors['RED'])
		gameOverScreen.set_alpha(128)
		self.screen.blit(gameOverScreen, (0,0))
		
		# gameOverScreen text
		text1 = "GAME OVER"
		text2 = "FINAL SCORE: " + str(self.score)
		#text3 = "Q TO QUIT, R TO RESTART"
		text3 = "Q TO QUIT"
		
		myFont = pygame.font.SysFont("monospace", 30, 1)
		doneText1 = myFont.render(text1,1,self.colors['BLUE'])
		doneText2 = myFont.render(text2,1,self.colors['BLUE'])
		doneText3 = myFont.render(text3,1,self.colors['BLUE'])

		text1Dimensions = myFont.size(text1) # duple (width, height)
		text2Dimensions = myFont.size(text2)
		text3Dimensions = myFont.size(text3)
		
		self.screen.blit(doneText1, ((self.width-text1Dimensions[0])/2,self.height/4))
		self.screen.blit(doneText2, ((self.width-text2Dimensions[0])/2,self.height/2))
		self.screen.blit(doneText3, ((self.width-text3Dimensions[0])/2,3*self.height/4))
				
		pygame.display.flip()
		
		pauseStart = pygame.time.get_ticks()
		while True:
			self.fpsClock.tick(self.FPS)
			
			for e in pygame.event.get():
				if e.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if e.type == pygame.KEYDOWN:
					# press q to quit
					if e.key == pygame.K_q:
						pygame.quit()
						sys.exit()
					# press r to restart
					'''doesn't work yet'''
					if e.key == pygame.K_r:
						pygame.quit()
						sys.exit()
	
	def MainLoop(self):
		self.newBlock()
		lastRotation = pygame.time.get_ticks()
		timeAtLastDrop = pygame.time.get_ticks()
		lastHardDrop = pygame.time.get_ticks()
		timeBetweenRotations = 100
		timeBetweenHardDrops = 250
		timeBetweenMoves = 75
		
		lastLeft = pygame.time.get_ticks()
		lastRight = pygame.time.get_ticks()
		lastDown = pygame.time.get_ticks()
		
		while True:
			self.fpsClock.tick(self.FPS)
			
			for e in pygame.event.get():
				if e.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
					self.pause()

			# gravity
			timeNow = pygame.time.get_ticks()
			# initially drop once per second, increasing in speed with higher score
			if timeNow - timeAtLastDrop > 1000*(math.e**(-1.*self.score/10000)):
				timeAtLastDrop = timeNow
				self.tetro.move(0,self.blockSize,self.walls,self.placedBlocks)
						
			key = pygame.key.get_pressed()
			# LEFT, RIGHT, or DOWN to move the tetromino
			if key[pygame.K_LEFT] and self.tetro.alive:
				tmp = pygame.time.get_ticks()
				if tmp - lastLeft > timeBetweenMoves:
					lastLeft = tmp
					self.tetro.move(-self.blockSize,0,self.walls, self.placedBlocks)
			if key[pygame.K_RIGHT] and self.tetro.alive:
				tmp = pygame.time.get_ticks()
				if tmp - lastRight > timeBetweenMoves:
					lastRight = tmp
					self.tetro.move(self.blockSize,0,self.walls,self.placedBlocks)
			if key[pygame.K_DOWN] and self.tetro.alive:
				tmp = pygame.time.get_ticks()
				if tmp - lastDown > timeBetweenMoves:
					lastDown = tmp
					self.tetro.move(0,self.blockSize,self.walls,self.placedBlocks)
			
			# UP to rotate
			if key[pygame.K_UP]:
				tempTime = pygame.time.get_ticks()
				if tempTime - lastRotation > timeBetweenRotations:
					lastRotation = tempTime
					self.tetro.rotate(self.walls, self.placedBlocks)
			
			# or F to rotate right and D to rotate left
			if key[pygame.K_f]:
				tempTime = pygame.time.get_ticks()
				if tempTime - lastRotation > timeBetweenRotations:
					lastRotation = tempTime
					self.tetro.rotate(self.walls, self.placedBlocks)
			if key[pygame.K_d]:
				tempTime = pygame.time.get_ticks()
				if tempTime - lastRotation > timeBetweenRotations:
					lastRotation = tempTime
					self.tetro.rotate(self.walls, self.placedBlocks)
			
			# SPACE to harddrop
			if key[pygame.K_SPACE]:
				tempTime = pygame.time.get_ticks()
				if tempTime - lastHardDrop > timeBetweenHardDrops:
					lastHardDrop = tempTime
					while self.tetro.alive:
						self.tetro.move(0,self.blockSize,self.walls,self.placedBlocks)
			
			if not self.tetro.alive:				
				self.blockDeath()
				self.newBlock()
				
				if self.checkGameOver():
					self.endGame()

			self.drawScreen()
			pygame.display.flip()
		


class Tetromino:
	blockColors = {'LONG':'AQUA','RHOOK':'BLUE','LHOOK':'ORANGE',
			  'SQUARE':'YELLOW','SBLOCK':'GREEN',
			  'TBLOCK':'PURPLE','ZBLOCK':'PINK'}
	
	maxOrientation = {'LONG':1,'RHOOK':3,'LHOOK':3,'SQUARE':0,
					  'SBLOCK':1,'TBLOCK':3,'ZBLOCK':1}
	
	# Genre is the shape of block
	def __init__(self, genre, blockSize, x_coord, y_coord, height, placedBlocks):
		self.genre = genre
		self.blockSize = blockSize
		self.x_coord = x_coord
		self.y_coord = y_coord
		self.blockColor = self.blockColors[genre]
		self.alive = True
		self.placedBlocks = placedBlocks
		self.height = height
		
		# Attribute to track orientation
		# Initially 0; this is the max for SQUARE
		# LONG, SBLOCK, and ZBLOCKs also have a 1
		# LHOOK, RHOOK, and TBLOCK also have 2 and 3, based on clockwise rotation from initial orientation
		self.orientation = 0
		
		# Array of the rects in the tetromino
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
		
		# Create a "ghost" piece at the bottom to show where tetromino would land with a harddrop
		self.dropGhosts()
	
	def rotate(self, walls, placedBlocks):
		'''
		Rotate the block,
		Check for collision,
		If so rotate back to original (i.e. undo rotation)
		'''
		self.placedBlocks = placedBlocks
		self.rotateBlock()
		
		correction = False
		for e in self.rectGroup:
			for wall in walls:
				if e.colliderect(wall):
					correction = True
			for row in self.placedBlocks:
				for block in row:
					if block != None:
						if e.colliderect(block):
							correction = True
			
			if e.y < 0 or e.bottom > self.height:
				correction = True
			
		if correction:
			if self.orientation == 0:
				desiredOrientation = self.maxOrientation[self.genre]
			else: desiredOrientation = self.orientation -1
			while self.orientation != desiredOrientation:
				self.rotateBlock()
		
		self.dropGhosts()
	
	def rotateBlock(self):
		if self.genre=='LONG':
			if self.orientation == 0: # vertical -> horizontal
				self.rectGroup[1].y -= self.blockSize
				self.rectGroup[1].x += self.blockSize
				self.rectGroup[2].y -= self.blockSize*2
				self.rectGroup[2].x += self.blockSize*2
				self.rectGroup[3].y -= self.blockSize*3
				self.rectGroup[3].x += self.blockSize*3
				self.orientation = 1
			elif self.orientation == 1: # horizontal -> vertical (undo previous if)
				self.rectGroup[1].y += self.blockSize
				self.rectGroup[1].x -= self.blockSize
				self.rectGroup[2].y += self.blockSize*2
				self.rectGroup[2].x -= self.blockSize*2
				self.rectGroup[3].y += self.blockSize*3
				self.rectGroup[3].x -= self.blockSize*3
				self.orientation = 0
		elif self.genre=='SQUARE':
			pass # squares can't rotate
		elif self.genre=='SBLOCK':
			if self.orientation == 0: #z to vertical-orientation
				self.rectGroup[0].x += self.blockSize
				self.rectGroup[1].y += self.blockSize
				self.rectGroup[2].y -= self.blockSize
				self.rectGroup[2].x += self.blockSize
				self.rectGroup[3].y -= self.blockSize*2
				self.orientation = 1
			elif self.orientation == 1:
				self.rectGroup[0].x -= self.blockSize
				self.rectGroup[1].y -= self.blockSize
				self.rectGroup[2].y += self.blockSize
				self.rectGroup[2].x -= self.blockSize
				self.rectGroup[3].y += self.blockSize*2
				self.orientation = 0
		elif self.genre=='ZBLOCK':
			if self.orientation == 0:
				self.rectGroup[0].x += self.blockSize*2
				self.rectGroup[1].y += self.blockSize*2
				self.orientation = 1
			elif self.orientation == 1:
				self.rectGroup[0].x -= self.blockSize*2
				self.rectGroup[1].y -= self.blockSize*2
				self.orientation = 0
		elif self.genre=='LHOOK':
			if self.orientation == 0:
				self.rectGroup[0].x += self.blockSize*2
				self.rectGroup[1].x += self.blockSize
				self.rectGroup[1].y += self.blockSize
				self.rectGroup[3].y -= self.blockSize
				self.rectGroup[3].x -= self.blockSize
				self.orientation = 1
			elif self.orientation == 1:
				self.rectGroup[0].y += self.blockSize*2
				self.rectGroup[1].y += self.blockSize
				self.rectGroup[1].x -= self.blockSize
				self.rectGroup[3].x += self.blockSize
				self.rectGroup[3].y -= self.blockSize
				self.orientation = 2
			elif self.orientation == 2:
				self.rectGroup[0].x -= self.blockSize*2
				self.rectGroup[1].x -= self.blockSize
				self.rectGroup[1].y -= self.blockSize
				self.rectGroup[3].x += self.blockSize
				self.rectGroup[3].y += self.blockSize
				self.orientation = 3
			elif self.orientation == 3:
				self.rectGroup[0].y -= self.blockSize*2
				self.rectGroup[1].y -= self.blockSize
				self.rectGroup[1].x += self.blockSize
				self.rectGroup[3].y += self.blockSize
				self.rectGroup[3].x -= self.blockSize
				self.orientation = 0
		elif self.genre=='RHOOK':
			if self.orientation == 0:
				self.rectGroup[0].x += self.blockSize
				self.rectGroup[0].y += self.blockSize
				self.rectGroup[1].y += self.blockSize*2
				self.rectGroup[3].x -= self.blockSize
				self.rectGroup[3].y -= self.blockSize
				self.orientation = 1
			elif self.orientation == 1:
				self.rectGroup[0].x -= self.blockSize
				self.rectGroup[0].y += self.blockSize
				self.rectGroup[1].x -= self.blockSize*2
				self.rectGroup[3].x += self.blockSize
				self.rectGroup[3].y -= self.blockSize
				self.orientation = 2
			elif self.orientation == 2:
				self.rectGroup[0].x -= self.blockSize
				self.rectGroup[0].y -= self.blockSize
				self.rectGroup[1].y -= self.blockSize*2
				self.rectGroup[3].x += self.blockSize
				self.rectGroup[3].y += self.blockSize
				self.orientation = 3
			elif self.orientation == 3:
				self.rectGroup[0].x += self.blockSize
				self.rectGroup[0].y -= self.blockSize
				self.rectGroup[1].x += self.blockSize*2
				self.rectGroup[3].x -= self.blockSize
				self.rectGroup[3].y += self.blockSize
				self.orientation = 0
		elif self.genre=='TBLOCK':
			if self.orientation == 0:
				self.rectGroup[1].x += self.blockSize
				self.rectGroup[1].y += self.blockSize
				self.orientation = 1
			elif self.orientation == 1:
				self.rectGroup[0].y += self.blockSize*2
				self.rectGroup[1].x -= self.blockSize
				self.rectGroup[1].y -= self.blockSize
				self.orientation = 2
			elif self.orientation == 2:
				self.rectGroup[0].y -= self.blockSize*2
				self.rectGroup[3].y += self.blockSize
				self.rectGroup[3].x -= self.blockSize
				self.orientation = 3
			elif self.orientation == 3:
				self.rectGroup[3].x += self.blockSize
				self.rectGroup[3].y -= self.blockSize
				self.orientation = 0
				
	def dropGhosts(self):
		self.ghostBlocks = []
		for a in self.rectGroup:
			self.ghostBlocks.append(Rect(a.x,a.y,self.blockSize,self.blockSize))
		
		# drop ghostblocks to the bottom
		correction = False
		while not correction:			
			for e in self.ghostBlocks:
				e.y += self.blockSize
				
				for row in self.placedBlocks:
					for block in row:
						if block != None:
							if e.colliderect(block):
								correction = True
				
				if e.y < 0 or e.bottom > self.height:
					correction = True
				
			if correction:
				for e in self.ghostBlocks:
					e.y -= self.blockSize
		
	
	def move(self, dx, dy, wallArray, placedBlocks):
		self.placedBlocks = placedBlocks
		if dx!=0:
			self.move_single_axis(dx,0,wallArray)
		if dy!=0:
			self.move_single_axis(0,dy,wallArray)
		
		if self.alive:
			self.dropGhosts()
			
			
	# move ALL rects in the piece, check each for collision;
	# if there's ANY collision, move them ALL back
	def move_single_axis(self, dx, dy, walls):
		correction = False
		
		for e in self.rectGroup:
			e.x += dx
			e.y += dy
			
			# maybe also check the fallen blocks?
			for wall in walls: # need to get this in somehow
				if e.colliderect(wall):
					correction = True
			for row in self.placedBlocks:
				for block in row:
					if block != None:
						if e.colliderect(block):
							correction = True
			
			# check that we don't go off the top or bottom
			# MAYBE CHECKING WALL HEIGHT ISN'T A GOOD IDEA
			if e.y < 0 or e.bottom > self.height:
				correction = True
			
		# AFTER all movement, undo if necessary
		if correction:
			for e in self.rectGroup:
				e.x -= dx
				e.y -= dy
			if dy!=0: # block is dead
				self.alive = False

'''class ghostPiece(Tetromino):
	def __init__(self, genre, blockSize, x_coord, y_coord):
		#super().__init__(genre, blockSize, x_coord, y_coord)
		self.ghostBlocks = rectGroup
		
	def __init__(self, blocks):
		self.ghostBlocks = blocks'''
		
		
		

def main():
	t = Tetris()
	t.MainLoop()

if __name__=='__main__':
	main()
