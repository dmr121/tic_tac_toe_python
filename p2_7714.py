#David Rozmajzl dmr121@zips.uakron.edu

'''
The variable called 'board' is the main structure in this program used to keep track of the state
of the board. It is a 1 demensional list of 11 elements. The first 9 elements represent tiles 1-9
on the tic-tac-toe board. This is what the board looks like if the indices are in the tiles
they represent:

 0 |  1 |  2
_____________
 3 |  4 |  5
_____________
 6 |  7 |  8

board[9] is a char which is set to either 'u' or 'c'. 'u' stands for user. This means that 2 users
are playing against each other in this game. 'c' is for computer, meaning that one user is playing
against the computer.

board[10] changes depending on what board[9] is. If board[9] is 'u', then board[10] is either 'X' or
'O' to show whose turn it is to go next in a match against users. User1 is 'X' and User2 is 'O'.

If board[9] is 'c', then board[10] is either 'b' or 'e'. 'b' is for beginner and means that the
computer will play at a beginner level. In other words, the computer places 'O' in a random tile 
whenever it is computer's turn. 'e' is for expert. The computer will play at an expert level using 
special functions that I developed so the computer plays its best game.

The computer uses the function getBestMove() to get the best move based on the current state of the board.
I don't want to get into the specifics of how the computer chooses its exact move, but I will give
a brief outline.

If the computer gets to make the first move, it choses a corner tile. Based on what I've read online, 
starting with a corner tile is the best strategy for maximizing your game. If the user goes first, then
the computer has to go second. If the user played a corner tile for their first move, computer plays the
center tile every time. I also read online that this is the best move if your opponent plays a corner tile
to start. But if the user's first move is not a corner tile, then I have my computer select a random tile
to place its first O.

Whenever getBestMove() is called after this, it first tries to see if it can get 3 in a row. If it does,
it connects its third O and wins. If not, the computer checks to see if its opponent can get 3 in a row. If 
it detects this, the computer places an O in the user's path in order to block the win.

If there is no move that will guarantee a win, then my connectTwoMoves() function checks all possible
places where it can place an O. It checks empty spots in a random order so the computer is not so predictable
every round. If it finds a path for a possible win (using sets) then it places its O there.

After the end of every match, the user is asked if they would like to keep playing. This defaults to no.
If the user types 'y' then the game starts over again and lets the user setup the game from the beginning.

FEATURES REQUIRED FROM THE RUBRIC:
Computer vs user: yes
User vs user: yes
Quit: yes (user is offered this option at the end of every match)
'''

import math
import random

threeByThreeSolutions = [{0, 1, 2}, {3, 4, 5}, {6, 7, 8},
						 {0, 3, 6}, {1, 4, 7}, {2, 5, 8},
						 {0, 4, 8}, {2, 4, 6}]

corners = [0, 2, 6, 8]
edges = [1, 3, 5, 7]
center = 4
OPPONENT = 9
STRATEGY = 10
SHAPE = 10

def makeBoard() -> list:
	return [None] * 9 # 3x3 board

def printBoard(board):
	for index in range(9):
		if board[index] is None:
			print("  ", end='')
		else:
			print(board[index] + " ", end='')
		if (index + 1)%3 == 0:
			if index != 8:
				print('')
				print("_____________")
		else:
			print(" | ", end='')
	print('')

def gameIsDraw(board) -> bool:
	if boardIsFull(board) and gameIsWon(board) == False:
		return True
	else:
		return False

def boardIsFull(board) -> bool:
	for tile in board:
		if tile is None:
			return False
	return True

def placeOnBoard(board, index, shape='X') -> list:
	board[index] = shape
	return board

def acceptValidMove(board):
	move = input("Your move (enter a number between 1 and 9): ")
	try:
		move = int(move)
	except:
		print("Not a number")
		return acceptValidMove(board)

	if move < 1 or move > 9:
		print("Invalid Input")
	elif spotIsOccupied(board, move - 1):
		print("Invalid Input. That spot is already taken")
	else:
		return move

	return acceptValidMove(board)

def spotIsOccupied(board, move):
	return board[move] is not None

def gameIsWon(board) -> bool:
	XBoard = findXTiles(board)
	OBoard = findOTiles(board)

	for solution in threeByThreeSolutions:
		if solution.issubset(XBoard) or solution.issubset(OBoard):
			return True

	return False

def findXTiles(board) -> set:
	XBoard = set()
	for index in range(9):
		if board[index] == 'X':
			XBoard.add(index)
	return XBoard

def findOTiles(board) -> set:
	OBoard = set()
	for index in range(9):
		if board[index] == 'O':
			OBoard.add(index)
	return OBoard

def playerMove(board):
	shape = board[SHAPE]
	if shape == 'X':
		print("Player 1 move")
	elif shape == 'O':
		print("Player 2 move")

	move = acceptValidMove(board)
	if board[OPPONENT] == 'c':
		board = placeOnBoard(board, move-1)
	else:
		board = placeOnBoard(board, move-1, shape)

	printBoard(board)
	print('')

	if gameIsWon(board):
		printWinner(board)
		return
	elif gameIsDraw(board):
		print("Draw")
		return
	
	if board[OPPONENT] == 'c':
		computerMove(board)
	elif shape == 'X':
		board[SHAPE] = 'O'
		playerMove(board)
	elif shape == 'O':
		board[SHAPE] = 'X'
		playerMove(board)

def printWinner(board):
	if board[OPPONENT] == 'c':
		print("You won!")
	elif board[SHAPE] == 'X':
		print("User 1 won!")
	elif board[SHAPE] == 'O':
		print("User 2 won!")

def boardIsEmpty(board) -> bool:
	for element in range(9):
		if board[element] is not None:
			return False
	return True

def getBestMove(board) -> int:
	if boardIsEmpty(board):
		return random.choice(corners)

	finalMove = connectThree(board, 'O')
	if finalMove is not None:
		return finalMove

	blockOpponentMove = connectThree(board, 'X')
	if blockOpponentMove is not None:
		return blockOpponentMove

	connectTwoMove = connectTwoMoves(board)
	if connectTwoMove is not None:
		return connectTwoMove

	if board.count(None) == 1:
		return board.index(None)

	secondMoveOfTheGame = bestSecondMove(board)
	return secondMoveOfTheGame

def bestSecondMove(board):
	opponentTile = 0
	for tile in range(9):
		if board[tile] == 'X':
			opponentTile = tile
	cornerSet = set(corners)
	if {opponentTile}.issubset(cornerSet):
		return 4 # This is the center piece

	randomTile = opponentTile
	while(randomTile == opponentTile):
		randomTile = random.randint(0, 8)

	return randomTile

def connectTwoMoves(board):
	computerBoard = findOTiles(board)
	playerBoard = findXTiles(board)
	numElements = len(computerBoard)
	for element in range(numElements):
		randomElement = random.choice(tuple(computerBoard))
		computerBoard.remove(randomElement)
		potentialSet = {randomElement}
		for tile in range(9):
			if board[tile] is None:
				potentialSet.add(tile)
				for solution in threeByThreeSolutions:
					if potentialSet.issubset(solution):
						if tuple(solution.difference(potentialSet))[0] in playerBoard:
							pass
						else:
							return tile
				potentialSet.remove(tile)
	return None

def connectThree(board, player: str):
	testBoard = set()
	if player == 'X':
		testBoard = findXTiles(board)
	else:
		testBoard = findOTiles(board)

	for tile in range(9):
		if board[tile] is None:
			testBoard.add(tile)
			for solution in threeByThreeSolutions:
				if solution.issubset(testBoard):
					return tile
			testBoard.remove(tile)
	return None

def computerMove(board):
	move = 0
	if board[STRATEGY] == 'b': #beginner strategy
		move = randomMove(board)
	else: #expert strategy
		move = getBestMove(board)
	
	board = placeOnBoard(board, move, 'O')
	print("Computer Move: ", move+1)
	printBoard(board)
	print('')

	if gameIsWon(board):
		print("Computer Won :(")
	elif gameIsDraw(board):
		print("Draw")
	else:
		playerMove(board)

def randomMove(board) -> int:
	potentialMoves = []
	for tile in range(9):
		if board[tile] is None:
			potentialMoves.append(tile)
	return random.choice(potentialMoves)

def startGame():
	board = makeBoard()
	# defaults to computer
	opponent = input('Play against computer or another user (c/u)? ')
	if opponent == 'u':
		print("User")
	else:
		opponent = 'c'
		print("Computer")
	board.append(opponent)

	if opponent == 'c':
		# defaults to random
		strategy = input('Choose a computer strategy. Beginner or expert (b/e)? ')
		if strategy == 'e':
			print("Expert")
		else:
			strategy = 'b'
			print("Beginner")
		board.append(strategy)

		# defaults to computer making the first move
		choice = input('Would you like to make the first move (y/n)? [n] ')
		if choice == 'y':
			playerMove(board)
		else:
			print('')
			computerMove(board)

	if opponent == 'u':
		# defaults to user1 making the first move
		choice = input('Would you like to make the first move? User 1 or user 2 (1/2)? [1] ')
		if choice == '2':
			board.append('O')
			playerMove(board)
		else:
			board.append('X')
			playerMove(board)

###### MAIN LOOP
print("WELCOME TO TIC-TAC-TOE")
print("Created by David Rozmajzl")
print("--------------------------------------")
keepPlaying = True
while keepPlaying:
	startGame()
	# Here is my option to quit
	choice = input('Would you like to keep playing (y/n)? [n] ')
	if choice == 'y':
		pass
	else:
		keepPlaying = False