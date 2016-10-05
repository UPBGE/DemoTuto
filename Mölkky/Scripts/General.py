import bge.logic as logic
from bge import *
import bge
from mathutils import *
from math import *
import Utils

scene = logic.getCurrentScene()
overlayer1 = logic.getSceneList()[1]

logic.goodScore = 50
logic.logicFPS = 24 #overlayer1.render.fps

logic.texts = []
def actText():
	for i in logic.texts:
		i.write()
		
scene.post_draw = [actText]
