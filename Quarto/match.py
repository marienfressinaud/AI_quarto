# -*- coding: utf-8 -*-

from models import Piece
from models import Player

class Match:
	'''
	A match represents a 2-players competition
	'''

	MAX_BOARD_COLS = 4
	MAX_BOARD_ROWS = 4

	def initBoard(self):
		cols = self.MAX_BOARD_COLS
		rows = self.MAX_BOARD_ROWS
		self.board = [[None for j in range(cols)] for i in range(rows)]

	def initPieces(self):
		self.pieces = []
		for color in Piece.COLORS:
			for height in Piece.HEIGHTS:
				for shape in Piece.SHAPES:
					for cons in Piece.CONSISTENCIES:
						piece = Piece({
							"color": color,
							"height": height,
							"shape": shape,
							"consistency": cons
						})
						self.pieces.append(piece)

	def __init__(self, configuration):
		self.initBoard()
		self.initPieces()

		name = configuration["name_player1"]
		intelligence = configuration["intelligence_player1"]
		player1 = Player(name, intelligence)

		name = configuration["name_player2"]
		intelligence = configuration["intelligence_player2"]
		player2 = Player(name, intelligence)

		self.players = []
		self.players.append(player1)
		self.players.append(player2)
		self.active_player = player1

	def run(self):
		for piece in self.pieces:
			print piece,
		print ""

		for player in self.players:
			if player.isAI:
				print player.name, "has an artificial intelligence"
			else:
				print player.name, "is a human"

		print "Not implemented"

	def selectPiece(self, piece):
		print "Not implemented"

	def nextPlayer(self):
		print "Not implemented"

	def putOnBoard(self, piece, destination):
		print "Not implemented"

	def endGame(self):
		print "Not implemented"
