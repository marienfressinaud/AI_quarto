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
