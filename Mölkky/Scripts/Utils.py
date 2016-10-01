#Return the sign of x: 1 or -1
def getSign(x):
	if x >= 0:
		return 1
	return -1

from bge import *
import bge.logic as logic

class Timer:
	def __init__(self, name = "timer"):
		print("Init the timer")
		logic.getCurrentController().owner["timer"]
	def get(self):
		return logic.getCurrentController().owner["timer"]
	def set(self, value):
		logic.getCurrentController().owner["timer"] = value

#get the word_num word in the chaine chain
#Optional: reverse: if == 1, then begin by the end
#		   espace: the character considered as a "space" between the sentence's words
def getWord(word_num, chaine, reverse = 0, espace = " "):
    word = str()
    increment = 1
    raison = 0
    fin = float(len(chaine))
    if reverse > 0:
        increment = -1
        raison = float(len(chaine))-1.
        fin = -1

    compteur = 0
    for c in range(raison, int(fin/increment)):
        if chaine[c*increment] == espace:
            compteur += 1
            continue
        
        if compteur == word_num:
            word += (chaine[c*increment])
        elif compteur > word_num:
            break
    
    if word == "":
        print(" The word you was looking for (n°" +str(word_num)+ ") can't be found in the string you brought to me (" +chaine+ ")")

    if reverse > 0:
        wordFinal = str()
        #Ici j'inverse le sens de la chaine finale pour la remettre à l'enroit
        for c in range(-1, word.size()-1):
            wordFinal += (word[len(word)-1-c])
        return wordFinal
    
    return word


#This script show the conversion into number of the major part of the events:
def strToEvent(str):
    out = 0
    if str == "A":
        out = events.AKEY
    elif str == "B":
        out = events.BKEY
    elif str == "C":
        out = events.CKEY
    elif str == "D":
        out = events.DKEY
    elif str == "E":
        out = events.EKEY
    elif str == "F":
        out = events.FKEY
    elif str == "G":
        out = events.GKEY
    elif str == "H":
        out = events.HKEY
    elif str == "I":
        out = events.IKEY
    elif str == "J":
        out = events.JKEY
    elif str == "K":
        out = events.KKEY
    elif str == "L":
        out = events.LKEY
    elif str == "M":
        out = events.MKEY
    elif str == "N":
        out = events.NKEY
    elif str == "O":
        out = events.OKEY
    elif str == "P":
        out = events.PKEY
    elif str == "Q":
        out = events.QKEY
    elif str == "R":
        out = events.RKEY
    elif str == "S":
        out = events.SKEY
    elif str == "T":
        out = events.TKEY
    elif str == "U":
        out = events.UKEY
    elif str == "V":
        out = events.VKEY
    elif str == "W":
        out = events.WKEY
    elif str == "X":
        out = events.XKEY
    elif str == "Y":
        out = events.YKEY
    elif str == "Z":
        out = events.ZKEY
    elif str == "capslock":
        out = events.CAPSLOCKKEY
    elif str == "lctrl":
        out = events.LEFTCTRLKEY
    elif str == "lalt":
        out = events.LEFTALTKEY
    elif str == "ralt":
        out = events.RIGHTALTKEY
    elif str == "rctrl":
        out = events.RIGHTCTRLKEY
    elif str == "rshift":
        out = events.RIGHTSHIFTKEY
    elif str == "lshift":
        out = events.LEFTSHIFTKEY
    elif str == "left":
        out = events.LEFTARROWKEY
    elif str == "down":
        out = events.DOWNARROWKEY
    elif str == "right":
        out = events.RIGHTARROWKEY
    elif str == "up":
        out = events.UPARROWKEY
    elif str == "space":
        out = events.SPACEKEY
    elif str == "enter":
        out = events.ENTERKEY
        
    return out
"""
left_ctrl
left_alt
right_alt
right_ctrl
right_shift
left_shift
left_arrow
down_arrow
right_arrow
up_arrow
bge.events.LEFTMOUSE
bge.events.MIDDLEMOUSE
bge.events.RIGHTMOUSE
bge.events.WHEELUPMOUSE
bge.events.WHEELDOWNMOUSE
bge.events.MOUSEX
bge.events.MOUSEY

bge.events.ZEROKEY
bge.events.ONEKEY
bge.events.TWOKEY
bge.events.THREEKEY
bge.events.FOURKEY
bge.events.FIVEKEY
bge.events.SIXKEY
bge.events.SEVENKEY
bge.events.EIGHTKEY
bge.events.NINEKEY
Modifiers Keys


Numberpad Keys

bge.events.PAD0
bge.events.PAD1
bge.events.PAD2
bge.events.PAD3
bge.events.PAD4
bge.events.PAD5
bge.events.PAD6
bge.events.PAD7
bge.events.PAD8
bge.events.PAD9
bge.events.PADPERIOD
bge.events.PADSLASHKEY
bge.events.PADASTERKEY
bge.events.PADMINUS¶
bge.events.PADENTER
bge.events.PADPLUSKEY
print(": "+events.EventToString())"""


