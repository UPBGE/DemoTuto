from General import *
from bge.types import KX_GameObject

#A class holding things about succeed, struggle, fail and tears:
class Player:
	def __init__(self, name="Dude"):
		#Constants
		self.score = 0
		self.name = name
		
		#Variables
		self.pinFallen = []
		self.emptyTurns = 0 #Count the number of turns without points
		
		print("  Player "+name+" has been succefully created")
		
	def pinFall(self, pin):
		self.pinFallen.append(pin)#We queue this pin as fallen
		
	#Called by Game when switching player
	def endTurn(self):
		#The default value returned
		returned = 0
	
		if len(self.pinFallen) > 1:
			self.emptyTurns=0#We have at last took down one pin
			self.score += len(self.pinFallen)
		elif len(self.pinFallen) == 1:
			self.emptyTurns=0
			self.score += self.pinFallen[0]
		else:
			self.emptyTurns+=1
		
		if self.emptyTurns >= 3:
			returned = -1
		
		if self.score >= logic.goodScore: #Change this line to == wen the game will be finished
			returned = 1
		elif self.score > logic.goodScore:
			self.score = 25
			
		#Reset:
		self.pinFallen = []
		self.score = 0
		
		return returned

"""		
class Mollki(types.KX_GameObject):
	def __init__(self, obj, position):
		self.pos = position

mollki = Mollki(scene.objects["möllki"])
print(mollki.pos)
print(mollki.name)
"""
