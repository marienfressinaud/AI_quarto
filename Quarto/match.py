# -*- coding: utf-8 -*-

from models import Piece
from models import Player
from util import getBoardValues

class Match:
	'''
	A match represents a 2-players competition
	'''

	MAX_BOARD_ROWS = 4
	MAX_BOARD_COLS = 4

	STATES = {
		"WAIT_SELECTION": 1,
		"WAIT_POSITIONING": 2,
		"CHECK_END_MATCH": 3,
		"END_GAME": 4,
		"J1_WIN": 5,
		"J2_WIN": 6,
		"DRAW": 7
	}

	def initBoard(self):
		cols = self.MAX_BOARD_COLS
		rows = self.MAX_BOARD_ROWS
		self.board = [[None for j in range(cols)] for i in range(rows)]

	def initPieces(self):
		self.pieces = []

		for i in range(16):
			color = Piece.PROPERTIES[0][i / 8 % 2]
			height = Piece.PROPERTIES[1][i / 4 % 2]
			shape = Piece.PROPERTIES[2][i / 2 % 2]
			consistency = Piece.PROPERTIES[3][i % 2]

			piece = Piece({
				"color": color,
				"height": height,
				"shape": shape,
				"consistency": consistency
			})

			self.pieces.append(piece)

	def __init__(self, configuration):
		self.initBoard()
		self.initPieces()

		name = configuration["name_player1"]
		intelligence = configuration["intelligence_player1"]
		player1 = Player(self, name, intelligence)

		name = configuration["name_player2"]
		intelligence = configuration["intelligence_player2"]
		player2 = Player(self, name, intelligence)

		self.players = []
		self.players.append(player1)
		self.players.append(player2)

		self.active_player = player1

		self.state = self.STATES["WAIT_SELECTION"]

	def run(self):
		while self.state != self.STATES["END_GAME"]:
			self.processState()

		self.endGame()

	def printBoard(self):
		print "  ",
		for j in range(self.MAX_BOARD_COLS):
			print "%3d   " % (j + 1),
		print
		print "-" * 30,
		print

		for i in range(self.MAX_BOARD_ROWS):
			print str(i + 1) + "|",
			for j in range(self.MAX_BOARD_COLS):
				piece = self.board[i][j]
				if piece is None:
					print "%(pad)5s|" \
					    % { "pad": "" },
				else:
					print "%(piece)4s |" \
					    % { "piece": str(piece) },
			print ""

	def processState(self):
		if self.state == self.STATES["WAIT_SELECTION"]:
			self.selectPiece()
			self.nextPlayer()
			self.state = self.STATES["WAIT_POSITIONING"]
		elif self.state == self.STATES["WAIT_POSITIONING"]:
			self.putOnBoard()
			self.state = self.STATES["CHECK_END_MATCH"]
		elif self.state == self.STATES["CHECK_END_MATCH"]:
			res = self.checkWinning()

			if res == "win" or res == "draw":
				self.state = self.STATES["END_GAME"]
			else:
				self.state = self.STATES["WAIT_SELECTION"]
		else:
			# TODO raise exception
			pass

	def getUnusedPieces(self):
		list = []

		for piece in self.pieces:
			if piece.position is None:
				list.append(piece)

		return list

	def getUnusedPositions(self):
		list = []

		for i in range(self.MAX_BOARD_ROWS):
			for j in range(self.MAX_BOARD_COLS):
				if self.board[i][j] is None:
					list.append({
						"x": i,
						"y": j
					})

		return list

	def getWiningProperties(self):
		props = set()

		for board_values in getBoardValues(self.board):
			if board_values["color"] == -3:
				props.add("red")
			elif board_values["color"] == 3:
				props.add("blue")

			if board_values["height"] == -3:
				props.add("short")
			elif board_values["height"] == 3:
				props.add("tall")

			if board_values["shape"] == -3:
				props.add("round")
			elif board_values["shape"] == 3:
				props.add("square")

			if board_values["consistency"] == -3:
				props.add("solid")
			elif board_values["consistency"] == 3:
				props.add("hollow")

		return props

	def getOtherPlayer(self, player):
		j1 = self.players[0]
		j2 = self.players[1]

		if j1 == player:
			return j2
		else:
			return j1

	def movePiece(self, piece, pos):
		if self.board[pos["x"]][pos["y"]] is None:
			self.board[pos["x"]][pos["y"]] = piece
			piece.position = pos
			return True
		return False

	def boardIsFull(self):
		unusedPos = self.getUnusedPositions()
		return len(unusedPos) == 0

	def selectPiece(self):
		unused =  self.getUnusedPieces()
		msg = "\nChoose a piece: "
		for p in unused:
			msg += str(p) + " "
		print msg

		piece = self.active_player.selectPiece()
		self.getOtherPlayer(self.active_player).selectedPiece = piece

	def nextPlayer(self):
		self.active_player = self.getOtherPlayer(self.active_player)

	def putOnBoard(self):
		print "\nChoose a position (horizontal vertical)"
		self.printBoard()

		while self.active_player.hasSelectedPiece():
			self.active_player.putOnBoard()

	def checkWinning(self):
		for board_values in getBoardValues(self.board):
			color = board_values["color"] ** 2
			height = board_values["height"] ** 2
			shape = board_values["shape"] ** 2
			consistency = board_values["consistency"] ** 2

			if color == 16 or height == 16 \
			or shape == 16 or consistency == 16:
				return "win"

		if self.boardIsFull():
			return "draw"

		return "no_win"

	def endGame(self):
		res = self.checkWinning()

		print
		if res == "win":
			print self.active_player.name, "is the winner!"
		elif res == "draw":
			print "No solution, no winner..."

		self.printBoard()
