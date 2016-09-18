from General import *

#Handle everything about mouse, including velocity computing for the möllky
class Mouse:
	def __init__(self):
		#Constants:
		self.angleFactor = 1
		self.rayMouse = 300
		self.minMouse = 20
		
		#Variables:
		self.mousePos = Vector((logic.mouse.inputs[bge.events.MOUSEX].values[-1], logic.mouse.inputs[bge.events.MOUSEY].values[-1]))
		self.oldMousePos = self.mousePos
		
		self.oldValueMousePos = Vector((self.mousePos.x, self.mousePos.y))
		self.centerMouse = Vector((bge.logic.mouse.inputs[bge.events.MOUSEX].values[0], bge.logic.mouse.inputs[bge.events.MOUSEY].values[0]))
	
	#Get the last mouse position
	def updateMousePos(self):
		self.mousePos = Vector((bge.logic.mouse.inputs[bge.events.MOUSEX].values[-1], -bge.logic.mouse.inputs[bge.events.MOUSEY].values[-1]))
		
		self.locPos = self.mousePos - self.centerMouse
		
		#Verify the mouse cursor is into his authorized zone, else displace it to his old position:		
		if sqrt(self.locPos.x**2 + self.locPos.y**2) > self.rayMouse or self.locPos.y*Utils.getSign(self.locPos.y) < self.locPos.x or self.locPos.y*Utils.getSign(self.locPos.y) < -self.locPos.x:
			if self.locPos.x > self.minMouse or self.locPos.x < -self.minMouse or self.locPos.y > self.minMouse or self.locPos.y < -self.minMouse:
				self.addToLocalMousePos((self.oldValueMousePos.x-self.mousePos.x), (self.oldValueMousePos.y - self.mousePos.y))
		
		self.oldValueMousePos = Vector((self.mousePos.x, self.mousePos.y))
	
	#Get the position in local coordinates, return a value between 0 and 1
	def getLocalPos(self):
		self.updateMousePos()
		self.locPos = self.mousePos - self.centerMouse
		return self.locPos
		
	#Add a relative position to the local mouse position
	def addToLocalMousePos(self, x, y):
		self.centerMouse.x -= x
		self.centerMouse.y -= y
		
	#Change the actual mouse position in the local coordinates
	"""def changeLocalPos(self, x, y):
		addToLocalPos(-(mousePos.x - x), -(mousePos.y - y))"""
	
	#Check were is the mouse, update his position and return the actual vector of the molkky velocity
	def getVelocityVector(self):
		self.updateMousePos()
		print("!!! Computing the velocity vector !!!")
		print(bge.logic.mouse.inputs[bge.events.MOUSEX].values)
		#Compute the current actual 2D speed of the mouse (m/s)
		speed2D = Vector(((self.mousePos.x - bge.logic.mouse.inputs[bge.events.MOUSEX].values[0])/self.rayMouse, (bge.logic.mouse.inputs[bge.events.MOUSEY].values[-1] - bge.logic.mouse.inputs[bge.events.MOUSEY].values[0])/self.rayMouse*-1)) * logic.logicFPS
		
		print(self.mousePos.y)
		print(bge.logic.mouse.inputs[bge.events.MOUSEY].values[0])
		print(bge.logic.mouse.inputs[bge.events.MOUSEY].values[0] + self.mousePos.y)
		print(speed2D)
		
		X = sqrt((self.getLocalPos().x/self.rayMouse)**2 + (self.getLocalPos().y/self.rayMouse)**2)*pi
		#print(X)
		
		#Compute the 2D velocity curve tangent vector with cos interpolation
		velocityCurveVector = Vector((-sin(X), 1, cos(X)))
		returned = Vector((sqrt(speed2D.x**2+speed2D.y**2)*velocityCurveVector.x*-Utils.getSign(speed2D.x), speed2D.y*velocityCurveVector.y, sqrt(speed2D.x**2+speed2D.y**2)*velocityCurveVector.z*-1))
		#print(velocityCurveVector)
		#print(returned)
		
		#Multiply vectors:
		return returned
	
	#Depending of the origin we give to it, return the current coordinates of the molkky
	def getMolkkyPosition(self, origin):
		return Vector((self.getLocalPos().x/self.rayMouse, (self.getLocalPos().y)/self.rayMouse, 1-sin((1-sqrt((self.getLocalPos().x/self.rayMouse)**2 + (self.getLocalPos().y/self.rayMouse)**2))*(pi/2)))) + origin
	
