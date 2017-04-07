import os, sys
import random
import math
import pygame
from pygame.locals import *

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
	
	# returns True if there is currently a collision, False otherwise.
	def checkCollision(self, walls, placedBlocks):
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
		return correction
	
	# direction to rotate. "CW" is clockwise, "CCW" is counterclockwise
	def rotate(self, walls, placedBlocks, direction):
		'''
		Rotate the block,
		Check for collision,
		If so rotate back to original (i.e. undo rotation)
		'''
		
		self.placedBlocks = placedBlocks
		
		# figure out number of rotations given genre and direction
		numRotations = 0
		if direction == "CW":
			numRotations = 1
		else: # direction == "CCW"
			numRotations = self.maxOrientation[self.genre]
		
		for r in range(numRotations):
			self.rotateBlock()
		
		correction = self.checkCollision(walls, self.placedBlocks)
		if correction:
			if direction == "CW":
				numRotations = self.maxOrientation[self.genre]
			else:
				numRotations = 1
			for r in range(numRotations):
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