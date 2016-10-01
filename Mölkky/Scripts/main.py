import bge.logic as logic

def initBegin():
	logic.begin = 0

def main():
	import sys
	sys.path.append(logic.expandPath("//Scripts"))
	import Game
	import Player
	logic.game = Game.Game([Player.Player("Roosendal"), Player.Player("Toon")])
	logic.begin = 1
	logic.game.initGame()
			  
def main_loop():
	if logic.begin == 1:
		import Game
		out = logic.game.update()#Update the game
		#If we have a winner, game is done!
		if out != "":
			print(" WINNER : "+out)
			logic.exit()
