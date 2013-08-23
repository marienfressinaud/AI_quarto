# -*- coding: utf-8 -*-

from models import Piece
from models import Player

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
		print " ",
		for j in range(self.MAX_BOARD_COLS):
			print "%3d   " % (j + 1),
		print

		for i in range(self.MAX_BOARD_ROWS):
			print (i + 1),
			for j in range(self.MAX_BOARD_COLS):
				piece = self.board[i][j]
				if piece is None:
					print "%(pad)5s|" \
					    % { "pad": "" },
				else:
					print "%(piece)5s|" \
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
		print ">",

		piece = self.active_player.selectPiece()
		self.otherPlayer(self.active_player).selectedPiece = piece

	def otherPlayer(self, player):
		j1 = self.players[0]
		j2 = self.players[1]

		if j1 == player:
			return j2
		else:
			return j1

	def nextPlayer(self):
		self.active_player = self.otherPlayer(self.active_player)

	def putOnBoard(self):
		print "\nChoose a position (horizontal vertical)"
		self.printBoard()
		print ">",

		while self.active_player.hasSelectedPiece():
			self.active_player.putOnBoard()


	def processChecking(self, mode):
		for i in range(self.MAX_BOARD_ROWS):
			val_color = 0
			val_height = 0
			val_shape = 0
			val_consistency = 0

			piece = None

			if mode == "diag-down" or mode == "diag-up":
				if mode == "diag-down":
					piece = self.board[i][i]
				elif mode == "diag-up":
					piece = self.board[3 - i][i]

				if not(piece is None):
					val_color += piece.color_int()
					val_height += piece.height_int()
					val_shape += piece.shape_int()
					val_consistency += piece.consistency_int()
			else:
				for j in range(self.MAX_BOARD_COLS):
					if mode == "vertical":
						piece = self.board[i][j]
					elif mode == "horizontal":
						piece = self.board[j][i]

					if not(piece is None):
						val_color += piece.color_int()
						val_height += piece.height_int()
						val_shape += piece.shape_int()
						val_consistency += piece.consistency_int()

			val_color *= val_color
			val_height *= val_height
			val_shape *= val_shape
			val_consistency *= val_consistency

			if val_color == 16 or val_height == 16 \
			or val_shape == 16 or val_consistency == 16:
			# if val_color == 16:
				return True

		return False


	def checkWinning(self):
		if self.processChecking("vertical") \
		or self.processChecking("horizontal") \
		or self.processChecking("diag-down") \
		or self.processChecking("diag-up"):
			return "win"

		if self.boardIsFull():
			return "draw"

		return "no_win"

	def endGame(self):
		res = self.checkWinning()

		if res == "win":
			print self.active_player.name, "is the winner!"
		elif res == "draw":
			print "No solution, no winner..."
