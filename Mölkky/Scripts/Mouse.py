from General import *

#Handle everything about mouse, including velocity computing for the möllky
class Mouse:
	def __init__(self):
		bge.logic.mouse.visible = 1
		
		#Constants:
		self.sensitivity = Vector((.5, 1))
		self.widthDivHeight = (bge.render.getWindowWidth()/bge.render.getWindowHeight())
		self.minMouse = .1
		self.vectorTempo = 3 #The number of mouse events between the two points of the vector

		#Variables:
		logic.mouse.position = (0.5, 0.5)
		self.relPos = Vector(((logic.mouse.position[0]-0.5)*self.widthDivHeight*2, (-logic.mouse.position[1]+0.5)*2))
		self.oldRelPos = [self.relPos] * self.vectorTempo #the mouse position history
		print(self.relPos)
	
	#Get the last mouse position
	def updateMousePos(self):
		self.relPos.x = (logic.mouse.position[0]-0.5)*(bge.render.getWindowWidth()/bge.render.getWindowHeight())*2
		self.relPos.y = (-logic.mouse.position[1]+0.5)*2
		
		#Verify the mouse cursor is into his authorized zone, else displace it to his old position:
		if sqrt(self.relPos.x**2 + self.relPos.y**2) > 1 or self.relPos.x > self.relPos.y*Utils.getSign(self.relPos.y) or self.relPos.x < -self.relPos.y*Utils.getSign(self.relPos.y):
			if self.relPos.x > self.minMouse or self.relPos.x < -self.minMouse or self.relPos.y > self.minMouse or self.relPos.y < -self.minMouse:
				self.relPos = self.oldRelPos[-1]
				
		logic.mouse.position = (self.relPos.x/2/(bge.render.getWindowWidth()/bge.render.getWindowHeight())+0.5, -self.relPos.y/2 +0.5 )  
		tmpMouse = list(self.oldRelPos)
		tmpMouse.append(self.relPos)

		for i in range(1, len(tmpMouse)):
			self.oldRelPos[i-1] = Vector(tmpMouse[i])
	
	#Check were is the mouse, update his position and return the actual vector of the molkky velocity
	def getVelocityVector(self):
		print("Computing the velocity vector")
		speed2D = Vector((0,0))
		#Compute the current actual 2D speed of the mouse (m/s)
		speed2D.x = (self.relPos.x-self.oldRelPos[0].x) * self.sensitivity.x * logic.logicFPS / self.vectorTempo
		speed2D.y = (self.relPos.y-self.oldRelPos[0].y) * self.sensitivity.y * logic.logicFPS / self.vectorTempo
		print(speed2D)
		X = sqrt((self.relPos.x)**2 + (self.relPos.y)**2)*pi
		#Compute the 2D velocity curve tangent vector with cos interpolation
		velocityCurve = Vector((1, -sin(X), cos(X)))
		
		returned = Vector((speed2D.x*velocityCurve.x, -speed2D.y*velocityCurve.y, sqrt(speed2D.x**2+speed2D.y**2)*velocityCurve.z))
		print(returned)
		#Multiply vectors:
		return returned
	
	#Depending of the origin we give to it, return the current coordinates of the molkky
	def getMolkkyPosition(self, origin):
		return Vector((self.relPos.x, self.relPos.y, sin(-sqrt(((self.relPos.x)**2 + (self.relPos.y**2))/2+0.5)*pi)+1)) + origin
