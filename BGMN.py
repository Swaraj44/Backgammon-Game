from tkinter import *
import tkinter.font as TkFont
import random
import copy
import os
import time
from time import gmtime
from time import strftime
import threading
import sys

class Cone():

	def __init__(self, number):

		self.number = number
		self.checkers = 0
		self.enemy = False
		self.selected = False

	def select(self):

		for cone in coneList:
			cone.deselect()

		self.selected = True

	def deselect(self):

		self.selected = False

	def removePiece(self):

		self.checkers-=1

	def addPiece(self):

		self.checkers+=1

class Window(Frame):


	def __init__(self, parent):

		Frame.__init__(self, parent)
		self.parent = parent
		self.parent.title("Backgammon")
		self.pack(fill=BOTH, expand=1)

	def canvas(self):

		global canvas
		global enemyTurnGraphics
		
		canvas = Canvas( self, bg="black", highlightthickness=0)
		canvas.pack(fill=BOTH, expand=1)


		#draw back squares

		canvas.create_rectangle(0,0,238,300, fill="#222222")
		canvas.create_rectangle(646,0,884,300, fill="#222222")



		#dice

		global diceButton; diceButton = Button(self, text="Roll", command= lambda: pressButton())
		diceButton.place(x=100, y=5)

		#draw cones
		for x in range(1,25):
      
			x_start = 0 + 32 * x + x * 2;   # Calculate x coordinates for the small sticks
			x_end = x_start + 32; # Width of the stick, adjust as needed

			xpnts = [0 + 32 * x + x * 2, 16 + 32 * x + x * 2, 32 + 32 * x + x * 2]
			stickPoints = [x_start, 300, x_end, 300, x_start, 150, x_end, 150]

			conePoints = [xpnts[0], 300, xpnts[1], 80, xpnts[2], 300]

			#normal colors
			if x % 2 == 0:
				color = "#00AA00"
			else:
				color = "#55524F"				

			#Canvas draw cone
			canvas.create_polygon(conePoints, fill=color)

			#canvas.create_rectangle(x_start, 70, x_end, 300 ,fill=color)

			# canvas.create_polygon(stickPoints, fill=color)


		global coneList2
		coneList2=coneList

		self.updateCanvas()


	
	
	def updateCanvas(self):
		global enemyTurnGraphics
		global diceButton

		for i in deleteInUpdate:
			canvas.delete(i)

		#change button text
		if(turnPhase == 0):
			diceButton["text"] = "Roll dice"
		elif(turnPhase >= 5 ):
			diceButton["text"] = "Enemy turn!"
		else:
			diceButton["text"] = "Move your checkers"
			
		#guide text

		deleteInUpdate.append(canvas.create_text(350, 16, anchor=W, fill="white", text=enemyChat, font=("FixedSys", 15)))

		#Draw checkers
			
		for x in range(0,26):
			try:
				if enemyTurnGraphics == False:
					#normal screen
					xpnts = [0 + 32 * x + x * 2, 32 + 32 * x + x * 2]
				else:
					xpnts = [884 - 32 * x - x * 2 - 2, 852 - 32 * x - x * 2 - 2]

				checkers = coneList[x].checkers

				#color according to player
				if enemyTurnGraphics == False:
					#normal colors
					if coneList[x].enemy == False:
						playerColor = "#FFFFFF"				
					else:
						playerColor = "#FF0000"	
					#selection change color
					if coneList[x].selected == True:
						playerColor = "#999999"
						
				else:
					if coneList[x].enemy == False:
						playerColor = "#FF0000"
					else:
						playerColor = "#FFFFFF"
					#selection change color
					if coneList[x].selected == True:
						playerColor = "#990000"
				
				
				counter = 0

				while counter < checkers:
					ypnts = [270 - counter * 30, 300 - counter * 30]		
					
					#Canvas draw checkers
					deleteInUpdate.append(canvas.create_oval(xpnts[0], ypnts[0], xpnts[1], ypnts[1], fill=playerColor, width = 0))
					counter+=1
			except IndexError:
				pass

		#Do dice values


		color1 = "#FFFFFF"
		color2 = "#FFFFFF"
		
		for x in range (0, len(impossibleMoves), 2):
			if impossibleMoves[x] == 0:
				if impossibleMoves[x + 1] == 0:
					color1 = "#FF0000"
				elif impossibleMoves[x + 1] == 1:
					color1 = "#FFFF00"
				elif impossibleMoves[x + 1] == 2:
					color1 = "#00FF00"

			if impossibleMoves[x] == 1:
				if impossibleMoves[x + 1] == 0:
					color2 = "#FF0000"
				elif impossibleMoves[x + 1] == 1:
					color2 = "#FFFF00"
				elif impossibleMoves[x + 1] == 2:
					color2 = "#00FF00"


		canvas.create_rectangle(280,5, 305, 30, outline=color1)
		canvas.create_rectangle(310,5, 335, 30, outline=color2)

		diceDotPoints = self.fetchDiceDotPoints(diceValue[0])
		dice2DotPoints = self.fetchDiceDotPoints(diceValue[1])

		for xdot, ydot in zip( diceDotPoints[0::2], diceDotPoints[1::2] ):

			deleteInUpdate.append(canvas.create_oval(xdot + 279, ydot + 4, xdot + 282, ydot + 7, fill=color1))

		for xdot, ydot in zip( dice2DotPoints[0::2], dice2DotPoints[1::2]):

			deleteInUpdate.append(canvas.create_oval(xdot + 309, ydot + 4, xdot + 312, ydot + 7, fill=color2))

		


	def mousePress(self, event):
		global enemyChat
		global turnPhase

		#bugfix
		if turnPhase == 0 or turnPhase == 5:
			diceButton.place(x=100, y=5)

		#if clicked at cones
		if event.y > 130:
			if turnPhase > 0 and turnPhase < 5:
				click = int(event.x / 34)
				cl=int(click)
				coneClicked = coneList[cl]

				if coneClicked.enemy == False:
					coneClicked.select()
					if enemyChat == "Hyper Backgammon":
						enemyChat = "Hyper Backgammon"
				else:
					enemyChat = "Hyper Backgammon"
			elif turnPhase == 0:
				enemyChat = "Hyper Backgammon"

			else:
				enemyChat = "Hyper Backgammon"
				
		self.updateCanvas()

	def mouseRelease(self, event):

		if event.y > 130:
			try:
				release = int(event.x / 34)
				rl=int(release)
				coneReleased = coneList[rl]
				print("turnPhase---->"+str(turnPhase))
				print("enemyPhase---->"+str(enemyPhase))

				if turnPhase < 5:
					for cone in coneList:

						if cone.selected == True:

							moveChecker(cone, coneReleased)
							cone.deselect()
			except IndexError:
				pass


		else:
			if turnPhase < 5:
				for cone in coneList:
					cone.deselect()

		self.updateCanvas()


	def fetchDiceDotPoints(self, amount):
		#Fetches the coordinates for all the points in the dice
		if amount == 0:
			#at the start
			dicePoints = [0,-100]
		elif amount == 1:
			dicePoints = [12,12]
		elif amount == 2:
			dicePoints = [6,18,18,6]
		elif amount == 3:
			dicePoints = [6,18,18,6,12,12]
		elif amount == 4:
			dicePoints = [6,6,6,18,18,6,18,18]
		elif amount == 5:
			dicePoints = [6,6,6,18,18,6,18,18,12,12]
		else:
			dicePoints = [6,6,6,18,18,6,18,18,6,12,18,12]

		return dicePoints



def Checkers_positions1():
		
		for x in range(0,26):
      
			checkers = coneList2[x].checkers
   
   
			if checkers < 1 :
				continue
   
   
			if coneList2[x].enemy == False:
				print('player-->'+"at -->"+ str(x)+"--with-->"+str(checkers))
									
			else:
				print('Enemy -->'+"at -->"+ str(x)+"--with-->"+str(checkers))
    
			#print('dice Amount t--> '+str(amount))
		print("Dice--->" + str(diceValue))
  
  
  
  
  
  
  
  
  
def risk_at_current_p(player_list,p):
     
		risk=0;
		r1=p+6
		r2=p+12
		diceValue
  
		checkers = coneList2[p].checkers
		if(p==0):
			risk=150
			return risk
  
		if(checkers>1):
			return 0;
  
		for x in range(p,r1+1):
			#print("x-->"+str(x))
      
			if(x==25):
					return risk;
 
			if(player_list[x]=='e'):
					risk+=10;
     
     
		for x in range(r1+1,r2):
			#print("y-->"+str(x))
			if(x==25):
					return risk;
 
			if(player_list[x]=='e'):
					risk+=5;
     
		return risk

  
  
  
  
  
  

def risk_at_p(player_list,p):

     
		risk=100;
		r1=p+6
		r2=p+12
		diceValue
  
		checkers = coneList2[p].checkers
  
		if(player_list[p]=="e"):
			#print("-------------------------------------------*All-----------------------------")
			if(checkers==1):
					risk-=50;
     
			else:
					risk+=999
					return risk;
  
  
		if(checkers>=1):
			return risk;



		for x in range(p,r1+1):
			#print("x-->"+str(x))
      
			if(x==25):
					return risk;
 
			if(player_list[x]=='e'):
					risk+=10;
     
     
		for x in range(r1+1,r2):
			#print("y-->"+str(x))
			if(x==25):
					return risk;
 
			if(player_list[x]=='e'):
					risk+=5;



		return risk
				
		
  
  
  
  
  
  
  
def risk(player_list,p,move_list):
		dd=diceValue[0]
  
  
		#move_list=[]
  
		#shifted_list = self.shift_left(diceValue)
		#diceValue = shifted_list;
    
		xx=risk_at_current_p(player_list,p)
		rr=0
  
		if(p+dd)<26:
			yy=risk_at_p(player_list,p+dd)
			rr=yy-xx
   
		else:
			rr=999
  
		

		move_list.append((0,p,rr))
  
		# print("Risk---1-->"+str(rr))

  
  
  
		dd=diceValue[1]
    
		xx=risk_at_current_p(player_list,p)
		rr=0
  
		if(p+dd)<26:
			yy=risk_at_p(player_list,p+dd)
			rr=yy-xx
   
		else:
			rr=999
  
		move_list.append((1,p,rr))
  
  
		# print("Risk---2-->"+str(rr))
  
  
  
		dd=diceValue[2]
  
		if dd==0:
			return move_list;
  
		xx=risk_at_current_p(player_list,p)
		rr=0
  
		if(p+dd)<26:
			yy=risk_at_p(player_list,p+dd)
			rr=yy-xx
   
		else:
			rr=999
  
  
		move_list.append((2,p,rr))
		# print("Risk---3-->"+str(rr))
  
  
  
		dd=diceValue[3]
  
		xx=risk_at_current_p(player_list,p)
		rr=0
  
		if(p+dd)<26:
			yy=risk_at_p(player_list,p+dd)
			rr=yy-xx
   
		else:
			rr=999
  
  
  
		move_list.append((3,p,rr))
		# print("Risk---4-->"+str(rr))
  
		return move_list;
  
		  

        #coneList[4].checkers=3;
		#coneList[3].checkers=2;
		#coneList[4].enemy == False
		#coneList[3].enemy == True

  

def analyze_risk():
		print("");
		
  



def move_valid(move_list):
     
		dice_list_temp=[0,1]

		if diceValue[2]>0:
			dice_list_temp.append(2)
			dice_list_temp.append(3)
      		
    
		for xx in dice_list_temp:
				valid_touples = [t for t in move_list if ((t[0] == xx) and (t[2] < 300))]
				print(str(xx)+"-->"+str(valid_touples))
    		
		return True;







  
def deside_move(iii):
     
    
		#reverseGame2()
  
		coneList2=coneList
        ##########################################################################################
    
		player_list=[]
		for x in range(0,26):
      
			checkers = coneList2[x].checkers
   
			#coneList2[x]=coneList[25-x]
   
   
			if checkers > 0 :
				
				if coneList2[x].enemy == False:
					player_list.append("p")
									
				else:
					player_list.append("e")
				
			else:
				player_list.append("o")
    
		print("-----------------Player list------------------------------------");
		print(player_list);
  
  
		################################################################################
  
  
  
  
  
  
		i=0
  
		diceValue
  
  
		move_list=[]
  
		for x in player_list:
				if x=="p":
        
					pos=i;
     
					# pos_a=pos+diceValue[0]
					# pos_b=pos+diceValue[1]

					print("--------------------------------------------------------------------------------------------------------------")
     
					# print("Player Red----->"+str(pos)+"-->"+player_list[pos]+"  "+str(pos_a)+"-->"+player_list[pos_a] +"  "+str(pos_b)+"-->"+player_list[pos_b])
     
     
					##########################################################################################################################################
					move_list1=risk(player_list,pos,move_list);
					move_list=move_list1;
        
        
        
				i=i+1

		move_list = sorted(move_list, key=lambda x: x[2])
		print("Move List-->",move_list);
  
  
  
		print ("Dicevalue---->"+str(diceValue))
  
  
  
  
		move_valid(move_list)
  
		#################################################################
  
  
		print("####################--> i ",iii)
  

		#if(iii>-9):
  		# Remove all elements where the first value is xx
			#move_list = [t for t in move_list if t[0] != iii]
			#print("Removed--> i ",iii)


		if(diceValue[0]==0):
  		# Remove all elements where the first value is xx
			move_list = [t for t in move_list if t[0] != 0]
			print("Removed--> i ")
   
		if(diceValue[1]==0):
  		# Remove all elements where the first value is xx
			move_list = [t for t in move_list if t[0] != 1]
			print("Removed--> i ")







		xx,yy,zz = move_list[0]

		print(move_list[0])

		s=yy
		e=s+diceValue[xx]

		print("###################    -->dice value "+str(xx)+" --------->"+str(diceValue[xx]))
  
		move_valid(move_list)
  
		global start
		start=coneList[s]

		global end
		end=coneList[e]

  
		


		
		# moveChecker(start, end)
		print("SStart---->"+str(s))
		print("SEnd------>"+str(e))

		
		

		return xx

  
		
  
		move_validd=move_valid(move_list)
  

		## move

        
	
    


        # Remove all elements where the first value is yy  
		
					
							



def FuzzyAI():
	global coneList

	print("turn phase------"+str(turnPhase))
	print("enemy phase------"+str(enemyPhase))
	global val
	print("hhhhhhhhhhhhh-------------->>"+str(coneList[0].checkers))
	def delayed_move1():
		global val
		val=deside_move(-9)
		moveChecker(start, end)
	canvas.after(1000,delayed_move1)

	#print("executed-------------------------------ejejejje")
	def delayed_move2():
		#time.sleep(4)

		y=1-val
		deside_move(y)
		moveChecker(start, end)
	
	canvas.after(1000,delayed_move2)


	#print("executed2222222222222-------------------------------ejejejje")






	

def pressButton():
	global enemyTurnGraphics
	global totalTurns
	
	checkWinCondition()

	if(turnPhase == 0):
		reverseGame()
		enemyTurnGraphics = False
		rollDice(True)
		totalTurns+=1
		print("start____________________________----------------------------______________________")
		
	elif(turnPhase < 5):
		print("===============================turnphase="+str(turnPhase))
		executeRandomTurn()
		
	elif(turnPhase == 5):
		reverseGame()
		rollDice(False)
		global fuzzy

		enemyTurnGraphics = True

		if fuzzy == False:
			MINI_MAX_AI()
		else:
			FuzzyAI()
		totalTurns+=1
		
	else:
		executeEnemyTurn()
		
def rollDice(playerTurn):                   
	global turnPhase
	global enemyPhase
	
	if (turnPhase == 0 and playerTurn == True) or (turnPhase == 5 and playerTurn == False):
		
		diceValue[0] = random.randint(1,6)
		diceValue[1] = random.randint(1,6)
		
		
			
		del impossibleMoves[:]
		del possibleMoves[:]

		
		if playerTurn == True:
			turnPhase = 3
		else:
			turnPhase = 6
			enemyPhase = 4
				
		checkLegalMoves(2)		

def checkLegalMoves(amount):		
	global turnPhase
	global enemyPhase
	
	imgCones = copy.deepcopy(coneList)
	
	if amount == 2:
	
		#x = dice1
		#y = dice2
		
		x = False
		y = False
		xy = False
		yx = False
	
		#go through moves starting with dice1
		dice1moves = []
		#if there are captured checkers
		if coneList[0].checkers > 0:
			for endingCone in coneList:
				if diceValue[0] == endingCone.number:
					if checkEnemy(endingCone) == True:
						dice1moves = [coneList[0], endingCone]
		else:
			dice1moves = diceLegalMoves(imgCones, 0)
		
		#then go all moves for the 2nd dice after dice 1		
		a = 0
		while a < len(dice1moves):
			x = True
			imgCones[dice1moves[a].number].removePiece()
			imgCones[dice1moves[a + 1].number].addPiece()
			imgCones[dice1moves[a + 1].number].enemy = False
			
			dice2moves = []
			#if there is still checkers captured
			if imgCones[0].checkers > 0:
				for endingCone in imgCones:
					if diceValue[1] == endingCone.number:
						if checkEnemy(endingCone) == True:
							dice2moves = [imgCones[0], endingCone]
			else:
				dice2moves = diceLegalMoves(imgCones, 1)
				
			
			b = 0
			while b < len(dice2moves):
				xy = True
				possibleMoves.extend((0, 0, 0, 0, dice1moves[a], dice1moves[a + 1], dice2moves[b], dice2moves[b + 1]))
				
				b += 2
				
			
			imgCones = copy.deepcopy(coneList)
			a += 2
			
		imgCones = copy.deepcopy(coneList)
		
		#go through moves starting with dice2
		dice2moves = []
		#if there are captured checkers
		if coneList[0].checkers > 0:
			for endingCone in coneList:
				if diceValue[1] == endingCone.number:
					if checkEnemy(endingCone) == True:
						dice2moves = [coneList[0], endingCone]
		else:
			dice2moves = diceLegalMoves(imgCones, 1)
			
		#then go all moves for the 2nd dice after dice 1		
		a = 0
		while a < len(dice2moves):
			y = True
			imgCones[dice2moves[a].number].removePiece()
			imgCones[dice2moves[a + 1].number].addPiece()
			imgCones[dice2moves[a + 1].number].enemy = False
			
			dice1moves = []
			#if there is still checkers captured
			if imgCones[0].checkers > 0:
				for endingCone in imgCones:
					if diceValue[0] == endingCone.number:
						if checkEnemy(endingCone) == True:
							dice1moves = [imgCones[0], endingCone]
			else:
				dice1moves = diceLegalMoves(imgCones, 0)
			
			b = 0
			while b < len(dice1moves):
				yx = True
				possibleMoves.extend((0, 0, 0, 0, dice2moves[a], dice2moves[a + 1], dice1moves[b], dice1moves[b + 1]))
				
				b += 2
				
			
			imgCones = copy.deepcopy(coneList)
			a += 2
			
		#exceptions
		
		if x == False and yx == False:
			#dice 1, 0 moves
			impossibleMoves.extend((0,0))
			turnPhase+=1
			enemyPhase+=2
			
		if x == False and yx == True:
			#dice1, possible moves after y
			impossibleMoves.extend((0,1))
		
		if y == False and xy == False:
			#dice 2, 0 moves
			impossibleMoves.extend((1,0))
			turnPhase+=1
			enemyPhase+=2
			
		if y == False and xy == True:
			#dice2, possible moves after x
			impossibleMoves.extend((1,1))
			
		if x == True and y == False and xy == False:
		
			a = 0
			
			while a < len(dice1moves):
				possibleMoves.extend((0,0,0,0,0,0,dice1moves[a], dice1moves[a + 1]))
				a += 2
	
	
		if y == True and x == False and yx == False:
		
			a = 0
			
			while a < len(dice2moves):
				possibleMoves.extend((0,0,0,0,0,0, dice2moves[a], dice2moves[a + 1]))
				a += 2
			
		if x == True and y == True and xy == False and yx == False:
			
			turnPhase+=1
			enemyPhase+=2
			a = 0
			
			if diceValue[0] > diceValue[1]:
				#dice 2, 0 moves
				impossibleMoves.extend((1,0))
				
				while a < len(dice1moves):
					possibleMoves.extend((0,0,0,0,0,0, dice1moves[a], dice1moves[a + 1]))
					
					a+=2
					
			else:
				#dice 1, 0 moves
				impossibleMoves.extend((0,0))
				while a < len(dice2moves):
					possibleMoves.extend((0,0,0,0,0,0, dice2moves[a], dice2moves[a + 1]))
					
					a+=2
		
		if x == True and xy == True and y == True and yx == False:
			
			#dice 2, can be ruined
			impossibleMoves.extend((1,2))	
		
		if x == True and xy == False and y == True and yx == True:
			
			#dice 2, can be ruined
			impossibleMoves.extend((1,2))
			
	
			

	
def diceLegalMoves(imgCones, diceNo):
	#find legal moves
	startingCones = []
	diceMoves = []
	
	for cone in imgCones:

		if cone.enemy == False:
			if cone.checkers > 0:
				startingCones.append(cone)

					
	for cone1 in startingCones:
		for cone2 in imgCones:
		
			if cone1.number + diceValue[diceNo] == cone2.number:
			
				if checkEnemy(cone2) == True:
				
					diceMoves.extend((cone1, cone2))
	
	return diceMoves;

#Move checkers around
def moveChecker(startingCone, endingCone):
	global turnPhase
	global enemyChat
	global enemyTurnGraphics
			
	print("startingCone.number------"+str(startingCone.number))
	print("endingCone.number------"+str(endingCone.number))
	if checkObvious(startingCone, endingCone) == True or turnPhase >= 5:
		
		#Enemy move
		if turnPhase >= 5:
			print("turnphase--------->"+str(turnPhase))
			print("enemyphase--------->"+str(enemyPhase))




			lineSaid = False
			startingCone.removePiece()

			
			if endingCone.number != 25:
				#Enemy eats
				if endingCone.enemy == True and endingCone.checkers == 1:
					eatEnemy(endingCone)
					line = 1
					if line == 1:
						enemyChat = "Hyper Backgammon"
					lineSaid = True
				
				
				endingCone.addPiece()
				endingCone.enemy = False
				
			turnPhase += 1
			print("turnphase   1--------->"+str(turnPhase))
			print("enemyphase  1--------->"+str(enemyPhase))
			
			if turnPhase == 10:
				turnPhase = 0
				
			#check which dice to reset
			
			if endingCone.number - startingCone.number == diceValue[1]:
				diceValue[1] = 0

			elif endingCone.number - startingCone.number == diceValue[0]:
				diceValue[0] = 0
				
			if lineSaid == False:
				line = random.randint(1,5)
				if line == 1:
					enemyChat = "Hyper Backgammon"

				
		
		#Player move
		else:
			a = 0
			print("turnphase--------->"+str(turnPhase))
			print("enemyphase--------->"+str(enemyPhase))
			while a < len(possibleMoves):
				try:
					if (
						startingCone.number == possibleMoves[a + (turnPhase - 1) * 2].number and 
						endingCone.number == possibleMoves[a + (turnPhase - 1) * 2 + 1].number
						):
						#Move is legal
						lineSaid = False
						startingCone.removePiece()
						
						if endingCone.number != 25:	
							if endingCone.enemy == True and endingCone.checkers == 1:
				
								#Player eats
								eatEnemy(endingCone)
								line = 1
								if line == 1:
									enemyChat = "Hyper Backgammon"
								
								lineSaid = True
					

							endingCone.addPiece()
							endingCone.enemy = False
						
						turnPhase+=1;				
						print("turnphase   2--------->"+str(turnPhase))
						print("enemyphase  2--------->"+str(enemyPhase))
						#check which dice to reset
						
							
						if endingCone.number - startingCone.number == diceValue[1]:
							diceValue[1] = 0

						elif endingCone.number - startingCone.number == diceValue[0]:
							diceValue[0] = 0
																	
						if lineSaid == False:
							line = 1
							if line == 1:
								enemyChat = "Hyper Backgammon"
							
								
						break
				except AttributeError:
					pass
				except IndexError:
					pass
				a+=8
	#move random move button out of screen so it can't be pressed
	global diceButton; 
	
	if testModeOn == False:
		if turnPhase < 5 and turnPhase != 0:
			diceButton.place(x=100, y=-100)
		else:
			diceButton.place(x=100, y=5)
		

def checkObvious(startingCone,endingCone):
	global enemyChat

	b = endingCone.number
	a = startingCone.number
	
	if b == a:
		enemyChat = "Hyper Backgammon"
		return False
	elif b < a:
		enemyChat = "Hyper Backgammon"
		return False
	elif b - a != diceValue[0] and b - a != diceValue[1]:
		enemyChat = "Hyper Backgammon"
		return False

	elif checkEnemy(endingCone) == False:
		enemyChat = "Hyper Backgammon"
		return False
		
	elif coneList[0].checkers > 0 and startingCone.number != 0:
		enemyChat = "Hyper Backgammon"
		return False	

	else:
		return True

def checkWinCondition():
	global enemyChat
	global turnPhase
	
	playerEmpty = True
	enemyEmpty = True
	
	for cone in coneList:
		if cone.enemy == False:
			if cone.checkers > 0:
				playerEmpty = False
		else:
			if cone.checkers > 0:
				enemyEmpty = False
				
	if playerEmpty == True or enemyEmpty == True:
		#quit the gui
		global gameEnded
		global testModeOn
		
		if testModeOn == True:
			global enemyWins
			global playerWins
		
		
		if testModeOn == False:
			global root
			root.destroy()
		
		gameEnded = True
		
		
		if turnPhase < 6 and turnPhase != 0:
			
			if testModeOn == False:
				print ("\n\n AI: Well well, congratulations... You won\n ")
				
			else:
				playerWins += 1
				print ("\r games simulated: %s" % (playerWins + enemyWins))
				sys.stdout.flush(),
				
		else:
			if testModeOn == False:
				print ("\n\n AI: Easy game, I win\n ")
			else:
				enemyWins += 1
				print ("\r games simulated: %s" % (playerWins + enemyWins))
				sys.stdout.flush()

		#write statistics

		line = ""
		
		#add day and time
		
		line += strftime("%d.%m.%y %H:%M -- ", gmtime())
		
		#add winner name
		
		if turnPhase < 6 and turnPhase != 0:
			line += "Player"
		else:
			line += "AI"
		
		#add game length
		
		global totalTurns
		global startTime
		gameLengthTime = time.time() - startTime
		gameLengthMinutes = int(gameLengthTime / 60)
		gameLengthSeconds = gameLengthTime % 60
		
		#Formating
		seconds = "%.0f" % (gameLengthSeconds)
		if gameLengthSeconds < 10:
			seconds = "0" + str(seconds)
		
		
		line += " -- length: time %s:%s, turns %s. " % (gameLengthMinutes, seconds, totalTurns)
	
		#and \n
		
		line += "\n"
		
			
		#start opening file
		pyfilepath = os.path.dirname(__file__)
		txtfilepath = "statistics.txt"
		completepath = os.path.join(pyfilepath, txtfilepath)
		

		
		#creates file if it doesn't exist and starts appending
		with open(completepath, 'a') as statistics:
			statistics.write(line)
		#opens it and reads it
		
		if testModeOn == False:
			mainMenu()
			
def checkEnemy(cone):
	#Returns True if valid move
	if cone.enemy == True:
		#check if you can home checkers
		if cone.number == 25:
			for cone in coneList[0:19]:
				if cone.enemy == False and cone.checkers > 0:
					return False
					
			return True
			
		
		if cone.checkers == 0:
			return True

		if cone.checkers == 1:
			return True

		if cone.checkers > 1:
			return False
	else:
		return True

def eatEnemy(cone):
	cone.enemy = False
	cone.checkers-=1
	coneList[25].checkers+=1



def reverseGame():
	
	#save cone owners
	coneOwners = []
	for cone in coneList:
		if cone.enemy == True:
			coneOwners.append(False)
		else:
			coneOwners.append(True)
			
	#save checkers amounts
	checkerAmounts = []
	
	
	for cone in coneList:
		checkerAmounts.append(cone.checkers)
	
	#deposit checker amounts and cone owners
	for i in range(0, len(coneList)):
		coneList[i].checkers = checkerAmounts[len(checkerAmounts) - 1 - i]
		coneList[i].enemy = coneOwners[len(coneOwners) - 1 - i]
  
  
  
  

  
  
  
  
  
  
  
		
def executeEnemyTurn():
	global turnPhase
	global enemyPhase
	global bestRoute
		
	try:
		#select cone
		if enemyPhase % 2 == 0:
			for cone in coneList:
				if cone.number == bestRoute[enemyPhase].number:
					cone.select()
					
		else:
			for cone1 in coneList:
				for cone2 in coneList:
					if cone1.number == bestRoute[enemyPhase - 1].number and cone2.number == bestRoute[enemyPhase].number:
						moveChecker(cone1, cone2)
			for cone in coneList:
				cone.deselect()
		
		enemyPhase += 1
	except (TypeError, IndexError) as e:
		turnPhase = 0


########



def executeRandomTurn():
	global turnPhase

	if len(possibleMoves) > 0:
		randomNumber = random.randint(0, len(possibleMoves) - 1) // 8
		randomRoute = possibleMoves[(randomNumber * 8):(randomNumber * 8 +8)]
		
		for i in range(0, len(randomRoute), 2):
			if randomRoute[i] != 0:
				
				for cone1 in coneList:
					for cone2 in coneList:
						
						if cone1.number == randomRoute[i] and cone2.number == randomRoute[i + 1]:
							
							moveChecker(cone1, cone2)

	turnPhase=5



def MINI_MAX_AI():
    global bestRoute
    global turnPhase
	
    print("minimax----------------------------------")
    
    # Generate all possible routes
    routes = []
    for i in range(0, len(possibleMoves), 8):
        routes.append(possibleMoves[i:i+8])
    
    # Calculate the best route using minimax
    bestScore, bestRoute = minimax(routes, depth=4, maximizingPlayer=True)
    
    if bestRoute is None:
        turnPhase = 0

def minimax(routes, depth, maximizingPlayer):
    if depth == 0 or not routes:
        return evaluateRoutes(routes), None
    
    if maximizingPlayer:
        maxEval = float('-inf')
        bestRoute = None
        for route in routes:
            score = evaluateRoute(route)
            if score > maxEval:
                maxEval = score
                bestRoute = route
        return maxEval, bestRoute
    else:
        minEval = float('inf')
        bestRoute = None
		
        for route in routes:
            score = evaluateRoute(route)
            if score < minEval:
                minEval = score
                bestRoute = route
        return minEval, bestRoute

def evaluateRoutes(routes):
    scores = []
    for route in routes:
        scores.append(evaluateRoute(route))
    return max(scores) if scores else 0

def evaluateRoute(route):
    imgCones = copy.deepcopy(coneList)
    score = calculateScoreRecursion(route, imgCones, 0, 0)
    return score

# Modify calculateScoreRecursion to fit within the minimax framework
def calculateScoreRecursion(route, imgCones, recursionAmount, score):
    if recursionAmount == 8:
        return score
    else:
        if route[recursionAmount] == 0:
            pass
        else:
            for cone in imgCones:
                if route[recursionAmount + 1].number == cone.number:
                    if cone.enemy == True and cone.checkers == 1:
                        score += 20
                        scoreBonus = (25 - cone.number) * 6
                        score += scoreBonus
                    if cone.number == 25:
                        score += 1000
                    elif cone.enemy == False and cone.checkers > 0:
                        score += 20
                        if cone.checkers == 1:
                            score += 20
                    else:
                        for cone1 in coneList:
                            if cone1.enemy == True and cone.checkers > 0:
                                if abs(cone.number - cone1.number) < 6:
                                    score -= 3
                                elif abs(cone.number - cone1.number) < 12:
                                    score -= 1
                if route[recursionAmount].number == cone.number:
                    if cone.checkers == 2:
                        for cone1 in coneList:
                            if cone1.enemy == True and cone.checkers > 0:
                                if abs(cone.number - cone1.number) < 6:
                                    score -= 10
                                elif abs(cone.number - cone1.number) < 12:
                                    score -= 3
                        score -= 30
                    if cone.number > 19 and cone.checkers > 1:
                        score -= 50
            for cone in imgCones:
                if cone.number == route[recursionAmount].number:
                    cone.removePiece()
                elif cone.number == route[recursionAmount + 1].number:
                    cone.addPiece()
                    cone.enemy = False
        return calculateScoreRecursion(route, imgCones, recursionAmount + 2, score)





def initializeGame():	

	#Globals
	global coneList
	coneList = []
	global coneList2
	coneList2 = []
	global diceValue
	diceValue = [0,0,0,0]
	global deleteInUpdate
	deleteInUpdate = []

	#player 1: 0 -> roll dice -> 
	# ( 1 -> move -> 2 -> move ->) 3 -> move -> 4 -> move -> 5
	# 5-10 for enemy
	global turnPhase
	turnPhase = 0
	global enemyPhase
	enemyPhase = 0
	global bestRoute
	bestRoute = []
	global possibleMoves
	possibleMoves = []
	global enemyTurnGraphics
	enemyTurnGraphics = False

	#for gamelog
	global totalTurns
	totalTurns = 0
	global startTime
	startTime = time.time()

	#array: dice no, reason: 0 no possible moves (red), 1 only possible if moved certainly (yellow), 2 only possible if not moved (green), 3 always possible (white)
	global impossibleMoves
	impossibleMoves = []


	for x in range (0, 26):

		cone = Cone(x)

		#starting setup

		if x == 0:
			cone.enemy = False	
		elif x == 1:
			cone.checkers+=2
			cone.enemy = False
		elif x == 6:
			cone.checkers+=5
			cone.enemy = True
		elif x == 8:
			cone.checkers+=3
			cone.enemy = True		
		elif x == 12:
			cone.checkers+=5
			cone.enemy = False
		elif x == 13:
			cone.checkers+=5
			cone.enemy = True
		elif x == 17:
			cone.checkers+=3
			cone.enemy = False
		elif x == 19:
			cone.checkers+=5
			cone.enemy = False
		elif x == 24:
			cone.checkers+=2
			cone.enemy = True
		elif x == 25:
			cone.enemy = True
		

		coneList.append(cone)
		
	global enemyChat; enemyChat = "Hyper Backgammon"
	global gameEnded; gameEnded = False
		
	reverseGame()


def mainMenu(mode):
	#Menu
	
	global testModeOn

	while True:
	

		playerInput ="p"
		
		if playerInput.upper() == "Q" or playerInput.upper() == "QUIT":
			sys.exit()
			break
		
		if playerInput.upper()  == "P" or playerInput.upper() == "PLAY":
			
			testModeOn = False
			global fuzzy 
			fuzzy = True
			#print("N - Normal mode\n")
			#print("H - Hard mode\n")
			#playerInput = input(" ")
			playerInput=mode
   
   
			if playerInput.upper() == "H" or playerInput.upper() == "HARD":
				fuzzy = False
			else:
				fuzzy=True
			initializeGame()
			startTkinter()
			sys.exit()
			break

		if playerInput.upper() == "T" or playerInput.upper() == "TEST AI":
			global gameEnded
			
			while True:
			
				numberInput = input("\n Give amount of games to simulate: ")
				
				try:
					numberInput = int(numberInput)
					break
				except ValueError:
					pass
			
			a = 0
			
			global playerWins
			playerWins = 0
			global enemyWins
			enemyWins = 0
			
			while a < numberInput:
			
				testModeOn = True
				initializeGame()
							
				while gameEnded == False:
					pressButton()
			
				a+=1
				
			print ("\n Player won: %s (%.2f%%)" % (playerWins, float(playerWins) / (playerWins + enemyWins) * 100))
			print (" AI won: %s (%.2f%%)" % (enemyWins, float(enemyWins) / (playerWins + enemyWins) * 100))
	
			
		if playerInput.upper()  == "S" or playerInput.upper() == "STATISTICS":
			#open statistics

			pyfilepath = os.path.dirname(__file__)
			txtfilepath = "statistics.txt"
			completepath = os.path.join(pyfilepath, txtfilepath)
			
			
			#creates file if it doesn't exist
			open(completepath, "a")
			
			
			#opens it and reads it
			with open(completepath, 'r') as statistics:
				data = statistics.read()
			
			print ("\n\n")
			if len(data) == 0:
				print (" - no data - ")
			print (data)
			
			print ("\n\n Do you wish to reset the game log?")
			playerInput = raw_input(' write "RESET" to reset the database, anything else to not\n ')
			
			while True:
				if playerInput.upper() == "RESET" or playerInput.upper() == '"RESET"':
					open(completepath, "w")
					print (" reset succesfull")
					mainMenu()
				else:
					mainMenu()
def startTkinter():

	global root
	root = Tk()
	root.geometry("900x300")
	root.resizable(width=FALSE, height=FALSE)

	#Create object Window(Frame)
	gui = Window(root)
	#onClickListener and Canvas on our Frame
	root.bind("<Button-1>", gui.mousePress)
	root.bind("<ButtonRelease-1>", gui.mouseRelease)
	gui.canvas()
	root.mainloop()

#mainMenu()
