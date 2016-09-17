from General import *
from Mouse import *
from Player import *

"""
#init keyboard
def initKeys(configFilePath):
	inFile = open(configFilePath, "r")

    fileContent = inFile.read()
    b = fileContent.split("\n")# Creating a iterable version of the file
    DKeys.initDefKeys()
    #We set up the key table
    Game.keys = {}

	for i in b:
        if len(i) == 0:
            continue
        
        keyWord = Utils.getWord(0, i) # The index of the value
        value = Utils.getWord(2, i)
        
        # We check if the file synthax isn't broken
        if Utils.getWord(1, i) != "=":
            print("syntaxe du fichier abimée, relisez vous didiou!")
            break
        
        y=0 # The actual level in the value
        
        # Looking if the key is reafering to a player
        if Utils.getWord(0, keyWord, 0, ".")[0] == "p":
            s = "player "+Utils.getWord(0, keyWord, 0, ".")[1] # Searching for the layer number.
            y += 1
            
        # Searching the first modifier
        first = Utils.getWord(y, keyWord, 0, ".")
        
        if first == "key":
            logic.keys[keyWord] = Utils.strToEvent(value)
            """
            
#The class holding the general behaviour of the game:
class Game:
	def __init__(self, players):
		#initKeys("/home/creeps/Documents/Projets/UPBGE/conf.mol")
		
		#Constants:
		self.players = players
		self.mouse = Mouse()
		self.radialSpeedIncrease = 1 #The speed with the radial speed will increase
		self.maxVelocity = 10
		self.reticuleXY = overlayer1.objects["reticuleXY"]
		self.curveXZ = overlayer1.objects["curveXZ"]
		self.flagXY = overlayer1.objects["flagXY"]
		self.flagXZ = overlayer1.objects["flagXZ"]
		
		self.molkky = scene.objects["Mölkky"]
		self.origin = scene.objects["Origin"].worldPosition
		reference = self.reference = scene.objects["reference"].worldPosition
		self.prefix = "default"
		self.maxDotValue = 0.5
		self.pinList = [scene.objects["pin"]]
		pinGroup = scene.objects["pin"]
		for i in range(0,11):
			self.pinList.append(scene.objects["pin."+str(i+1)].groupMembers["pin"])
		
		#Variables:
		self.playerNumber = len(players)
		self.player = self.players[self.playerNumber-1]
		self.molkkyLaunched = 0
		self.leftActivated = 0
		self.rightActivated = 0
		self.oldLeftClick = 0
		self.leftClick = 0
		
		self.oldPinsPos = [Vector((0, 0, 0))] * 12
		self.oldMollkyPos = Vector((0, 0, 0))
		
		#Init oldPinsPos && oldMollkyPos
		for i in range(0,12):
			self.oldPinsPos[i-1] = self.pinList[i].worldPosition
		self.oldMollkyPos = self.molkky.worldPosition
		
	#Set all the variables to their init value, and put the pins to their starting position
	def initGame(self):
		convertHeight = 0.8660254038
		diameter = (5.5 + 0.5) * .01 #The diameter of a pin +0.5
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
	
	#Count the fallen pins, put them straight again, and change the current player
	def nextTurn(self):
		#Set all the pins to their base:
		for i in range(0,12):
			pin = self.pinList[i]
			if pin.worldOrientation[2].dot(Vector((0, 0, 1))) < self.maxDotValue:
				self.player.pinFall(i)
				pin.worldOrientation = (0, 0, 0)
				pin.worldPosition.z = self.reference.z
				
		
		winOrNotToWin = self.player.endTurn() #We check if the player won the game
		self.playerNumber += 1
		if self.playerNumber >= len(self.players):
			self.playerNumber = 0
		self.player = self.players[self.playerNumber]
		return winOrNotToWin
	
	#Update the game with the actions of the player in the current frame
	def update(self):
		#Doing some test to update the player actions...
		
		event = logic.mouse.inputs
		if event[bge.events.LEFTMOUSE].values[-1] == 1:
			self.leftClick = 1
		elif event[bge.events.LEFTMOUSE].values[-1] == 0:
			self.leftClick = 0
		
		if self.leftClick == 1:
			#!!!!!!!!!!!!!! Changer méthode aquisition des touches !!!!!!!!!!!!!
			#Test radial speed change :
			"""
			if logic.KX_INPUT_JUST_ACTIVATED == keyboard.events[logic.keys[self.prefix+".key.up"]]:
				self.radialVelocity.z += self.radialSpeedIncrease
				self.upActivated = 1
			if logic.KX_INPUT_JUST_ACTIVATED == keyboard.events[logic.keys[self.prefix+".key.down"]]:
				self.radialVelocity.z -= self.radialSpeedIncrease
				self.downActivated = 1
			if logic.KX_INPUT_JUST_ACTIVATED == keyboard.events[logic.keys[self.prefix+".key.left"]]:
				self.leftActivated = 1
				
			if logic.KX_INPUT_JUST_ACTIVATED == keyboard.events[logic.keys[self.prefix+".key.right"]]:
				self.rightActivated = 1
			#Actually not used, but maybe implement another key later:
			if logic.KX_INPUT_JUST_ACTIVATED == keyboard.events[logic.keys[self.prefix+".key.lshift"]]:
				self.leftShiftActivated = 1
		
			
			#If no keys has been triggered, then lower their value
			if (self.upActivated | self.downActivated | self.leftActivated | self.rightActivated) == 0:
				if abs(self.radialVelocity.x) >= self.radialSpeedDecrease:
					self.radialVelocity.x -= self.radialSpeedDecrease*getSign(self.radialVelocity.x)
				else
					self.radialVelocity.x = 0
				if abs(self.radialVelocity.x) >= self.radialSpeedDecrease:
					self.radialVelocity.x -= self.radialSpeedDecrease*getSign(self.radialVelocity.x)
				else
					self.radialVelocity.y = 0
				if abs(self.radialVelocity.x) >= self.radialSpeedDecrease:
					self.radialVelocity.x -= self.radialSpeedDecrease*getSign(self.radialVelocity.x)
				else
					self.radialVelocity.z = 0
					
			if abs(self.radialVelocity.x) > self.maxVelocity:
				self.radialVelocity.x = self.maxVelocity*getSign(self.radialVelocity.x)
			if abs(self.radialVelocity.y) > self.maxVelocity:
				self.radialVelocity.y = self.maxVelocity*getSign(self.radialVelocity.y)
			if abs(self.radialVelocity.z) > self.maxVelocity:
				self.radialVelocity.z = self.maxVelocity*getSign(self.radialVelocity.z)
			"""
		
		#Test if we should launch the molkky
		if self.oldLeftClick == 1 and self.leftClick == 0:
			print("Launching the molkky")
			self.molkkyLaunched = 1
			self.molkky.worldLinearVelocity = self.mouse.getVelocityVector()
			self.molkky.worldPosition = self.mouse.getMolkkyPosition(self.origin)
		if self.molkkyLaunched == 0:
			self.molkky.worldPosition = self.mouse.getMolkkyPosition(self.origin)
			posRep1 = self.mouse.getMolkkyPosition(self.reticuleXY.worldPosition)
			self.flagXY.worldPosition = Vector((posRep1.x, posRep1.y, self.reticuleXY.worldPosition.z))
			posRep2 = self.mouse.getMolkkyPosition(Vector((0,0,0)))
			self.flagXZ.worldPosition = Vector((sqrt(posRep2.y**2+posRep2.x**2)*Utils.getSign(posRep2.y*-1)+self.curveXZ.worldPosition.x, posRep2.z+self.curveXZ.worldPosition.y, self.curveXZ.worldPosition.z))
		
		if self.molkkyLaunched == 1:
			#Check if the current player turn has finished:
			nbrMolkkyOK = 0
			for i in range(0,12):
				if self.oldPinsPos[i] == self.pinList[i].worldPosition:
					nbrMolkkyOK += 1
			#If all the pins hadn't moved, this turn is over!
			if nbrMolkkyOK == 12 and self.molkky.worldPosition == self.oldMollkyPos:
				#Test if the current player won the game
				if self.nextTurn() == 1:
					winner = self.player
					return self.player.name
		
		#Reset && update:
		#Init oldPinsPos && oldMollkyPos
		for i in range(0,12):
			self.oldPinsPos[i] = self.pinList[i].worldPosition
			
		self.oldMollkyPos = self.molkky.worldPosition
		
		self.leftActivated = 0
		self.rightActivated = 0
		self.oldLeftClick = self.leftClick
			
		return ""
