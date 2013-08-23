# -*- coding: utf-8 -*-

from models import Piece
from models import Player

class Match:
	'''
	A match represents a 2-players competition
	'''

	MAX_BOARD_COLS = 4
	MAX_BOARD_ROWS = 4

	PIECE_PROPERTIES = [
		["blue", "short", "square", "hollow"],
		["blue", "short", "square", "solid"],
		["blue", "short", "round", "hollow"],
		["blue", "short", "round", "solid"],
		["blue", "tall", "square", "hollow"],
		["blue", "tall", "square", "solid"],
		["blue", "tall", "round", "hollow"],
		["blue", "tall", "round", "solid"],
		["red", "short", "square", "hollow"],
		["red", "short", "square", "solid"],
		["red", "short", "round", "hollow"],
		["red", "short", "round", "solid"],
		["red", "tall", "square", "hollow"],
		["red", "tall", "square", "solid"],
		["red", "tall", "round", "hollow"],
		["red", "tall", "round", "solid"]
	]

	def initBoard(self):
		cols = self.MAX_BOARD_COLS
		rows = self.MAX_BOARD_ROWS
		self.board = [[None for j in range(cols)] for i in range(rows)]

	def initPieces(self):
		self.pieces = []
		for prop in self.PIECE_PROPERTIES:
			piece = Piece({
				"color": prop[0],
				"height": prop[1],
				"shape": prop[2],
				"consistency": prop[3]
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
