# -*- coding: utf-8 -*-

from models import Piece
from match import Match
from util import maximizeProperty, eval_position, getWiningProperties
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
		ui.showPlayer(match.active_player)
		return ui.askSelectPiece(match.board.unusedPieces())

	def putOnBoard(self, match, piece):
		ui.showPlayer(match.active_player)
		return ui.askPosition(match.board.unusedPositions())

class Random(Intelligence):
	"""
	A random intelligence chooses randomly both of location of its current
	piece and the piece to give to its opponent
	"""

	def selectPiece(self, match):
		available_pieces = match.board.unusedPieces()
		i = random.randint(0, len(available_pieces) - 1)

		ui.showPlayer(match.active_player)
		ui.showSelectedPiece(available_pieces[i])

		return available_pieces[i]

	def putOnBoard(self, match, piece):
		available_pos = match.board.unusedPositions()
		i = random.randint(0, len(available_pos) - 1)

		ui.showPlayer(match.active_player)
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
		winning_props = getWiningProperties(match.board.board)
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

		if len(available_pieces) >= 15:
			return Random().selectPiece(match)

		i = random.randint(0, len(available_pieces) - 1)

		ui.showPlayer(match.active_player)
		ui.showSelectedPiece(available_pieces[i])

		return available_pieces[i]

	def putOnBoard(self, match, piece):
		available_pos = match.board.unusedPositions()

		if len(available_pos) >= 15:
			return Random().putOnBoard(match, piece)

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
			i = random.randint(0, len(available_pos) - 1)
			final_pos = available_pos[i]

		ui.showPlayer(match.active_player)
		ui.showSelectedPosition(final_pos)

		return final_pos

class Minimax(Intelligence):
	"""
	A Minimax intelligence implements Minimax algorithm
	with alpha-beta pruning. It must be the better player!
	"""

	STILL_NOVICE_UNTIL = 13

	MAX_VAL_DEPTH = 5

	STATE_MAX = 1
	STATE_MIN = 2

	EVAL_WIN = 200
	EVAL_DRAW = 199

	def __init__(self, depth):
		if depth < 1:
			depth = 1
		elif depth > Minimax.MAX_VAL_DEPTH:
			depth = Minimax.MAX_VAL_DEPTH

		self.max_depth = depth

	def evaluation(self, board, played_pos):
		eval_pos = eval_position("row", board.board, played_pos)
		eval_pos += eval_position("col", board.board, played_pos)

		if played_pos["x"] == played_pos["y"]:
			eval_pos += eval_position(
				"diag-down", board.board, played_pos
			)
		elif played_pos["x"] == 3 - played_pos["y"]:
			eval_pos += eval_position(
				"diag-up", board.board, played_pos
			)

		return min(Minimax.EVAL_WIN, 50 + eval_pos * 0.5)

	def alphaBeta(self, board, played_piece, played_pos,
	              state, alpha, beta, depth):
		board.putPiece(played_piece, played_pos)

		available_pieces = board.unusedPieces()
		available_pos = board.unusedPositions()
		eval = 0

		if board.isWon():
			eval = Minimax.EVAL_WIN
		elif board.isFull():
			eval = Minimax.EVAL_DRAW
		elif depth >= self.max_depth:
			eval = self.evaluation(board, played_pos)
		elif state == Minimax.STATE_MAX:
			eval = 0
			for piece in available_pieces:
				for pos in available_pos:
					eval = max(eval,
						self.alphaBeta(
							board, piece, pos,
							Minimax.STATE_MIN, alpha, beta, depth + 1
						)
					)

					if eval >= beta:
						board.takeOff(played_piece)
						return eval

					alpha = max(alpha, eval)
			eval = alpha
		elif state == Minimax.STATE_MIN:
			eval = Minimax.EVAL_WIN
			for piece in available_pieces:
				for pos in available_pos:
					eval = min(eval,
						self.alphaBeta(
							board, piece, pos,
							Minimax.STATE_MAX, alpha, beta, depth + 1
						)
					)

					if alpha >= eval:
						board.takeOff(played_piece)
						return eval

					beta = min(beta, eval)
			eval = beta

		board.takeOff(played_piece)

		if state == Minimax.STATE_MAX:
			eval = Minimax.EVAL_WIN - eval

		return eval

	def selectPiece(self, match):
		available_pieces = match.board.unusedPieces()
		available_pos = match.board.unusedPositions()
		fallback_i = random.randint(0, len(available_pieces) - 1)
		chosen_piece = available_pieces[fallback_i]
		alpha, beta = 0, Minimax.EVAL_WIN

		if len(available_pieces) >= Minimax.STILL_NOVICE_UNTIL:
			return Novice().selectPiece(match)

		solution = False
		for piece in available_pieces:
			alpha = 0

			for pos in available_pos:
				eval = self.alphaBeta(
					match.board, piece, pos,
					Minimax.STATE_MIN, alpha, beta, 1
				)

				alpha = max(alpha, eval)

			if alpha < beta:
				beta = alpha
				chosen_piece = piece
				solution = True

		ui.showPlayer(match.active_player)
		ui.showSelectedPiece(chosen_piece)

		return chosen_piece

	def putOnBoard(self, match, piece):
		available_pos = match.board.unusedPositions()
		fallback_i = random.randint(0, len(available_pos) - 1)
		better_pos = available_pos[fallback_i]
		alpha, beta = 0, Minimax.EVAL_WIN

		if len(available_pos) >= Minimax.STILL_NOVICE_UNTIL:
			return Novice().putOnBoard(match, piece)

		for pos in available_pos:
			eval = self.alphaBeta(
				match.board, piece, pos,
				Minimax.STATE_MIN, alpha, beta, 1
			)

			if eval > alpha:
				alpha = eval
				better_pos = pos

		ui.showPlayer(match.active_player)
		ui.showSelectedPosition(better_pos)

		return better_pos