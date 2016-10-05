from General import *
from Mouse import *
from Player import *

import bgl
import blf

#The Text holding class
class Text:
	def __init__(self):
		self.text = ""
		
	def consAbs(self, text, fontPath, position, size, normPos = -1, normSize = -1):
		self.text = text
		self.position = position
		self.size = size
		self.fontPath = fontPath

		#Test if we are using relative or absolute position
		self.normPos = normPos
		if normPos < 0:
			if position.x <= 1 and position.y <= 1:
				self.normPos = 1
			else:
				self.normPos = 0
		if normSize < 0:
			if size.x <= 1 and size.y <= 1:
				self.normSize = 1
			else:
				self.normSize = 0

		self.renderSize = Vector((render.getWindowWidth(), render.getWindowHeight()))
		logic.texts.append(self)
		self.updateFont()
	
	#This function take an object to help positionning the Text.
	def consRel(self, text, fontPath, objPos, camPos, camScale, size = Vector((40, 40))):
		relativeDist = objPos - camPos
		ratio = Vector((relativeDist.x / camScale, relativeDist.y / camScale*render.getWindowWidth()/render.getWindowHeight())) + Vector((0.5, 0.5))
		ratio.y = 1 - ratio.y
		self.consAbs(text, fontPath, ratio, size)
		
	def updateFont(self):
		# create a new font object, use external ttf file
		if self.fontPath[0] != '/' or self.fontPath[0] != '\\':
			self.fontPath = logic.expandPath('//'+self.fontPath)
		# store the font indice - to use later
		self.fontID = blf.load(self.fontPath)
	
	def write(self):
		# OpenGL setup
		bgl.glMatrixMode(bgl.GL_PROJECTION)
		bgl.glLoadIdentity()
		bgl.gluOrtho2D(0, self.renderSize.x, 0, self.renderSize.y)
		bgl.glMatrixMode(bgl.GL_MODELVIEW)
		bgl.glLoadIdentity()

		# BLF drawing routine
		if self.normPos == 1:
			blf.position(self.fontID, (self.renderSize.x * self.position.x), self.renderSize.y - (self.renderSize.y * self.position.y), 0)
		else:
			blf.position(self.fontID, self.position.x, self.renderSize.y - self.position.y, 0)
			
		if self.normSize == 1:
			blf.size(self.fontID, int(self.renderSize.x * self.size.x), int(self.renderSize.y * self.size.y))
		else:
			blf.size(self.fontID, int(self.size.x), int(self.size.y))
		blf.draw(self.fontID, self.text)
