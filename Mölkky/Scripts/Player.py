from General import *
from bge.types import KX_GameObject
from Text import *

#A class holding things about succeed, struggle, fail and tears:
class Player:
	def __init__(self, number, name=str("Dude")):
		#Constants
		self.score = 0
		self.name = str("          ")
		self.name = name[0:9]
		
		#Variables
		self.pinFallen = []
		self.emptyTurns = 0 #Count the number of turns without points
		
		self.textName = Text()
		self.textScore = Text()
		self.textName.consRel(self.name, "Russian.ttf", overlayer1.objects["playerNameText"].worldPosition-Vector((0, number*0.1*6, 0)), overlayer1.objects["Camera"].worldPosition, 6, Vector((0.1, 0.05)))
		self.textScore.consRel(str(self.score), "Russian.ttf", overlayer1.objects["playerScoreText"].worldPosition-Vector((0, number*0.1*6, 0)), overlayer1.objects["Camera"].worldPosition, 6, Vector((0.1, 0.05)))
		
		print("  Player "+name+" has been successfully created")
		
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
		
		if self.score == logic.goodScore: #Change this line to == wen the game will be finished
			returned = 1
		elif self.score > logic.goodScore:
			self.score = 25
			
		print(self.name+" ended his turn with "+str(len(self.pinFallen))+" fallen pins and a score of "+str(self.score))
		self.textScore.text = str(self.score)
		#Reset:
		self.pinFallen = []
		
		return returned

"""		
class Mollki(types.KX_GameObject):
	def __init__(self, obj, position):
		self.pos = position

mollki = Mollki(scene.objects["möllki"])
print(mollki.pos)
print(mollki.name)
"""
