# -*- coding: utf-8 -*-

from models import Piece, Board, Player
from util import getBoardValues

import ui

class Match:
	'''
	A match represents a 2-players competition
	'''

	STATES = {
		"WAIT_SELECTION": 1,
		"WAIT_POSITIONING": 2,
		"CHECK_END_MATCH": 3,
		"END_GAME": 4,
		"J1_WIN": 5,
		"J2_WIN": 6,
		"DRAW": 7
	}

	def __init__(self, configuration):
		self.board = Board()

		player1 = Player(
			self,
			configuration["name_player1"],
			configuration["intelligence_player1"]
		)

		player2 = Player(
			self,
			configuration["name_player2"],
			configuration["intelligence_player2"]
		)

		self.players = (player1, player2)
		self.active_player = player1

		self.state = self.STATES["WAIT_SELECTION"]

	def run(self):
		while self.state != self.STATES["END_GAME"]:
			self.processState()

		self.endGame()

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
			# Impossible state, but don't take risks
			self.state = self.STATES["END_GAME"]

	def getWiningProperties(self):
		props = set()

		for board_values in getBoardValues(self.board.board):
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

	def selectPiece(self):
		ui.showChoosePiece(self.board.unusedPieces())

		piece = self.active_player.selectPiece()
		self.getOtherPlayer(self.active_player).selectedPiece = piece

	def nextPlayer(self):
		self.active_player = self.getOtherPlayer(self.active_player)

	def putOnBoard(self):
		ui.showChoosePosition()
		ui.showBoard(self.board)

		while self.active_player.hasSelectedPiece():
			self.active_player.putOnBoard()

	def checkWinning(self):
		for board_values in getBoardValues(self.board.board):
			color = board_values["color"] ** 2
			height = board_values["height"] ** 2
			shape = board_values["shape"] ** 2
			consistency = board_values["consistency"] ** 2

			if color == 16 or height == 16 \
			or shape == 16 or consistency == 16:
				return "win"

		if self.board.isFull():
			return "draw"

		return "no_win"

	def endGame(self):
		res = self.checkWinning()

		if res == "win":
			ui.showEndGame(self.active_player)
		elif res == "draw":
			ui.showEndGame(None)

		ui.showBoard(self.board)
