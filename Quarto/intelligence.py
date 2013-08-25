# -*- coding: utf-8 -*-

from models import Piece
from match import Match
from util import maximizeProperty, evalBoard
import ui

import random

class Intelligence:
	"""
	Intelligence should be an abstract class.
	It designates, in fact, an artificial intelligence.
	The are different types of AI like Random, Novice or Minimax-D which
	heritated all of Intelligence
	"""

	def selectPiece(self, match):
		pass

	def putOnBoard(self, match, piece):
		pass

class Human(Intelligence):

	def selectPiece(self, match):
		return ui.askSelectPiece(match.board.unusedPieces())

	def putOnBoard(self, match, piece):
		return ui.askPosition(match.board.unusedPositions())

class Random(Intelligence):
	"""
	A random intelligence chooses randomly both of location of its current
	piece and the piece to give to its opponent
	"""

	def selectPiece(self, match):
		available_pieces = match.board.unusedPieces()
		i = random.randint(0, len(available_pieces) - 1)

		ui.showSelectedPiece(available_pieces[i])

		return available_pieces[i]

	def putOnBoard(self, match, piece):
		available_pos = match.board.unusedPositions()
		i = random.randint(0, len(available_pos) - 1)

		ui.showSelectedPosition(available_pos[i])

		return available_pos[i]

class Novice(Intelligence):
	"""
	A novice intelligence plays as follows:
	* It always places its piece in a winning formation, if possible.
	  Otherwise, it chooses randomly among the existing open cells.
	* If given a choice among pieces to give the opponent, it always chooses
	  one that cannot be used to immediately win the game,
	  if such a piece is available.
	"""

	def getNonWiningPieces(self, match, pieces):
		winning_props = match.getWiningProperties()
		list = []
		for p in pieces:
			if not p.color in winning_props \
			and not p.height in winning_props \
			and not p.shape in winning_props \
			and not p.state in winning_props:
				list.append(p)
		return list

	def selectPiece(self, match):
		unused_pieces = match.board.unusedPieces()
		available_pieces = self.getNonWiningPieces(match, unused_pieces)
		if len(available_pieces) < 1:
			available_pieces = unused_pieces

		i = random.randint(0, len(available_pieces) - 1)

		ui.showSelectedPiece(available_pieces[i])

		return available_pieces[i]

	def putOnBoard(self, match, piece):
		better_color = maximizeProperty(
			match.board.board,
			{ "propriety": "color", "value": piece.color }
		)
		better_height = maximizeProperty(
			match.board.board,
			{ "propriety": "height", "value": piece.height }
		)
		better_shape = maximizeProperty(
			match.board.board,
			{ "propriety": "shape", "value": piece.shape }
		)
		better_state = maximizeProperty(
			match.board.board,
			{ "propriety": "state", "value": piece.state }
		)

		val_max = max((
			better_color["value"],
			better_height["value"],
			better_shape["value"],
			better_state["value"]
		))

		final_pos = None
		for best in (better_color, better_height, \
		             better_shape, better_state):
			if best["value"] == val_max:
				final_pos = best["position"]

		if final_pos is None:
			available_pos = match.board.unusedPositions()
			i = random.randint(0, len(available_pos) - 1)
			final_pos = available_pos[i]

		ui.showSelectedPosition(final_pos)

		return final_pos

class Minimax(Intelligence):
	"""
	A Minimax intelligence implements Minimax algorithm
	with alpha-beta pruning. It must be the better player!
	"""

	STILL_NOVICE_UNTIL = 12

	MAX_VAL_DEPTH = 5

	STATE_MAX = 1
	STATE_MIN = 2

	EVAL_WIN = 100
	EVAL_DRAW = 90

	def __init__(self, depth):
		if depth < 1:
			depth = 1
		elif depth > self.MAX_VAL_DEPTH:
			depth = self.MAX_VAL_DEPTH

		self.max_depth = depth

	def evaluation(self, board, played_pos):
		eval = 0

		if board.isWon():
			eval = self.EVAL_WIN
		elif board.isFull():
			eval = self.EVAL_DRAW
		else:
			eval = evalBoard("row", board.board, played_pos)
			eval += evalBoard("col", board.board, played_pos)

			if played_pos["x"] == played_pos["y"]:
				eval += evalBoard(
					"diag-down", board.board, played_pos
				)
			elif played_pos["x"] == 3 - played_pos["y"]:
				eval += evalBoard(
					"diag-up", board.board, played_pos
				)

		return eval

	def alphaBeta(self, board, played_piece, played_pos,
	                    state, alpha, beta, depth):
		board.putPiece(played_piece, played_pos)

		available_pieces = board.unusedPieces()
		available_pos = board.unusedPositions()
		eval = 0

		if depth == 0 and board.isWon():
			eval = self.EVAL_WIN
		elif board.isFull() or depth == self.max_depth:
			eval = self.evaluation(board, played_pos)
		elif state == self.STATE_MAX:
			for piece in available_pieces:
				for pos in available_pos:
					eval = self.alphaBeta(
						board, piece, pos,
						self.STATE_MIN,
						alpha, beta, depth + 1
					)

					alpha = max(eval, alpha)
			eval = alpha
		elif state == self.STATE_MIN:
			for piece in available_pieces:
				for pos in available_pos:
					eval = self.alphaBeta(
						board, piece, pos,
						self.STATE_MAX,
						alpha, beta, depth + 1
					)

					beta = min(eval, beta)
					if alpha >= beta:
						board.takeOff(played_piece)
						return beta
			eval = beta

		board.takeOff(played_piece)
		return eval

	def selectPiece(self, match):
		available_pieces = match.board.unusedPieces()
		available_pos = match.board.unusedPositions()
		chosen_piece = None
		alpha, beta = 0, self.EVAL_WIN

		if len(available_pieces) >= self.STILL_NOVICE_UNTIL:
			return Novice().selectPiece(match)

		for piece in available_pieces:
			alpha = 0

			for pos in available_pos:
				eval = self.alphaBeta(
					match.board, piece, pos,
					self.STATE_MIN, alpha, beta, 0
				)
				alpha = max(alpha, eval)

			if alpha <= beta:
				beta = alpha
				chosen_piece = piece

		ui.showSelectedPiece(chosen_piece)

		return chosen_piece

	def putOnBoard(self, match, piece):
		better_pos = None
		alpha, beta = 0, self.EVAL_WIN
		available_pos = match.board.unusedPositions()

		if len(available_pos) >= self.STILL_NOVICE_UNTIL:
			return Novice().putOnBoard(match, piece)

		for pos in available_pos:
			eval = self.alphaBeta(
				match.board, piece, pos,
				self.STATE_MAX, alpha, beta, 0
			)

			if eval > alpha:
				alpha = eval
				better_pos = pos

		ui.showSelectedPosition(better_pos)

		return better_pos