from General import *
from Mouse import *
from Player import *
from Text import * 

#init keyboard
def initKeys(configFilePath):
	inFile = open(configFilePath, "r")

	fileContent = inFile.read()
	lineToLine = fileContent.split("\n")# Creating a iterable version of the file

	#We set up the key table
	Game.keys = {}

	for line in lineToLine:
		if len(line) == 0:
			continue
        
		keyWord = Utils.getWord(0, line) #The index of the value
		value = Utils.getWord(2, line)

		# We check if the file synthax isn't broken
		if Utils.getWord(1, line) != "=":
			print("syntaxe du fichier abimée, relisez vous didiou!")
			break

		y=0 # The actual level in the value

		# Searching the first modifier
		first = Utils.getWord(y, keyWord, 0, ".")

		if first == "key":
			logic.keys[keyWord] =	Utils.strToEvent(value)

#The class holding the general behaviour of the game:
class Game:
	def __init__(self, players):
		initKeys(logic.expandPath("//conf.mol"))
		#bge.constraints.setDebugMode(bge.constraints.DBG_DRAWWIREFRAME)
		#Constants:
		self.players = players
		self.mouse = Mouse()
		self.prefix = "default"
		
		self.radialSpeedIncrease = 1 #The speed with the radial speed will increase
		self.maxVelocity = 10
		self.maxDotValue = 0.5
		self.maxTimer = 6.0
		self.minTimer = 2.0
		
		self.reticuleXY = overlayer1.objects["reticuleXY"]
		self.reticuleXZ = overlayer1.objects["reticuleXZ"]
		overlayer1.objects["curveXZ"].localScale.y *= self.maxDotValue
		self.flagXY = overlayer1.objects["flagXY"]
		self.flagXZ = overlayer1.objects["flagXZ"]
		
		self.molkky = scene.objects["Mölkky"]
		self.puppet = scene.objects["Mölkky_puppet"]
		self.origin = scene.objects["Origin"]
		self.reference = scene.objects["reference"].worldPosition
		self.pinList = []
		for i in range(0,12):
			self.pinList.append(scene.objects["pin."+str(i+1)].groupMembers["pin"])
		
		#Variables:
		self.test = 0
		self.playerNumber = 0 #The ID of the actual player
		self.player = self.players[self.playerNumber]
		self.molkkyLaunched = 0
		self.leftActivated = 0
		self.rightActivated = 0
		self.oldLeftClick = 0
		self.leftClick = 0
		self.timer = Utils.Timer()
		
		self.oldPinsPos = [Vector((0, 0, 0))] * 12
		self.oldMollkyPos = Vector((0, 0, 0))
		
		#Init oldPinsPos && oldMollkyPos
		for i in range(0,12):
			self.oldPinsPos[i] = self.pinList[i].worldPosition
		self.oldMollkyPos = Vector((self.molkky.worldPosition.x, self.molkky.worldPosition.y, self.molkky.worldPosition.z))
		
	#Set all the variables to their init value, and put the pins to their starting position
	def initGame(self):
		convertHeight = 0.8660254038
		diameter = (5.5 + 3) * .01 #The diameter of a pin +0.5
		y = convertHeight*diameter #The distance betwin a pin and a higher one
		demiDiam = diameter/2
		
		self.posTab = [
			Vector((self.reference.x-demiDiam, self.reference.y)), #1
			Vector((self.reference.x+demiDiam, self.reference.y)), #2
			
			Vector((self.reference.x-diameter, self.reference.y+y)), #3
			Vector((self.reference.x, self.reference.y+y)), #10
			Vector((self.reference.x+diameter, self.reference.y+y)), #4

			Vector((self.reference.x-diameter-demiDiam, self.reference.y+2*y)), #5
			Vector((self.reference.x-demiDiam, self.reference.y+2*y)),  #11
			Vector((self.reference.x+demiDiam, self.reference.y+2*y)), #12
			Vector((self.reference.x+diameter+demiDiam, self.reference.y+2*y)), #6
			
			Vector((self.reference.x-diameter, self.reference.y+3*y)), #7
			Vector((self.reference.x, self.reference.y+3*y)), #8
			Vector((self.reference.x+diameter, self.reference.y+3*y)), #9
		]
			
		for i, pos in enumerate(self.posTab):
			self.pinList[i].worldPosition = Vector((pos.x, pos.y, self.reference.z))
			#print(self.reference.rayCast(Vector((0, -150, 0))))
			#self.pinList[i].worldPosition.z = self.reference.rayCast(Vector((0, -100, 0)))[1][2]
	
	#Count the fallen pins, put them straight again, and change the current player
	def nextTurn(self):
		self.molkkyLaunched = 0
		self.molkky.worldPosition.z = -100000
		#Set all the pins to their base:
		for i in range(0,12):
			pin = self.pinList[i]
			if pin.worldOrientation[2].dot(Vector((0, 0, 1))) < self.maxDotValue:
				self.player.pinFall(i)
				pin.worldOrientation = (0, 0, 0)
				pin.worldLinearVelocity = (0, 0, 0)
				pin.worldAngularVelocity = (0, 0, 0)
				pin.worldPosition.z = self.reference.z
				
		winOrNotToWin = self.player.endTurn() #We check if the player won the game
		self.playerNumber += 1
		if self.playerNumber >= len(self.players):
			self.playerNumber = 0
		self.player = self.players[self.playerNumber]
		#self.molkkyLaunched = 0
		print("Next turn for "+self.player.name + " \n")
		return winOrNotToWin
	
	#Update the game with the actions of the player in the current frame
	def update(self):
		self.mouse.updateMousePos() #Update the mouse
		
		#Doing some test to update the player actions...
		event = logic.mouse.inputs
		if event[bge.events.LEFTMOUSE].values[-1] == 1:
			self.leftClick = 1
		elif event[bge.events.LEFTMOUSE].values[-1] == 0:
			self.leftClick = 0
		
		#Test if we should launch the molkky
		if self.oldLeftClick == 1 and self.leftClick == 0 and self.molkkyLaunched == 0:
			print("Launching the molkky")
			self.puppet.worldPosition = Vector((0, 0, -10000))
			self.molkkyLaunched = 1
			self.molkky.worldLinearVelocity = self.mouse.getVelocityVector()
			self.molkky.worldPosition = self.mouse.getMolkkyPosition(self.origin.worldPosition)
			self.molkky.worldOrientation = Vector((0,0,0))
			self.molkky.worldAngularVelocity = (0, 0, 0)
			logic.mouse.position = (0,0)
			self.timer.set(0)

		if self.molkkyLaunched == 0:
			self.puppet.worldPosition = self.mouse.getMolkkyPosition(self.origin.worldPosition)
			posRep1 = self.mouse.getMolkkyPosition(self.reticuleXY.worldPosition)
			self.flagXY.worldPosition = Vector((posRep1.x, posRep1.y, self.reticuleXY.worldPosition.z))
			posRep2 = self.mouse.getMolkkyPosition(Vector((0,0,0)))
			self.flagXZ.worldPosition = Vector((sqrt(posRep2.y**2+posRep2.x**2)*Utils.getSign(posRep2.y*-1)+self.reticuleXZ.worldPosition.x, posRep2.z+self.reticuleXZ.worldPosition.y, self.reticuleXZ.worldPosition.z))
		elif self.molkkyLaunched == 1:
			#Check if the current player turn has finished:
			nbrMolkkyOK = 0
			for i in range(0,12):
				if self.oldPinsPos[i] == self.pinList[i].worldPosition:
					nbrMolkkyOK += 1
			#If all the pins hadn't moved, this turn is over!
			if nbrMolkkyOK == 12:
				if (self.molkky.worldPosition == self.oldMollkyPos or self.timer.get() > self.maxTimer) and self.timer.get() > self.minTimer:
					#Test if the current player won the game
					if self.nextTurn() == 1:
						winner = self.player
						return self.player.name
		
		#Reset && update:
		#Init oldPinsPos && oldMollkyPos
		for i in range(0,12):
			self.oldPinsPos[i] = self.pinList[i].worldPosition

		self.oldMollkyPos = Vector((self.molkky.worldPosition.x, self.molkky.worldPosition.y, self.molkky.worldPosition.z))
		
		self.leftActivated = 0
		self.rightActivated = 0
		self.oldLeftClick = self.leftClick
			
		return ""
